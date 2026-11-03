"""Configuración reproducible del TFG: semillas y versiones fijadas de los modelos.

Uso típico al inicio de cada script o notebook::

    from config import ReproConfig

    cfg = ReproConfig()
    cfg.validate()                    # juez y oráculo: otra familia y separados
    cfg.set_global_seed(cfg.seeds[0]) # fija random, numpy y (si está) torch
    modelo = cfg.models["gpt-4o"].litellm_name

Todas las ejecuciones deben registrar ``cfg.snapshot()`` en su log JSONL para
que cada resultado quede ligado a las semillas y versiones exactas.
"""

from __future__ import annotations

import hashlib
import json
import os
import random
from dataclasses import asdict, dataclass, field
from typing import Optional


@dataclass(frozen=True)
class ModelSpec:
    """Un modelo con su versión fijada.

    ``model_id`` debe ser siempre un identificador inmutable: un snapshot con
    fecha en las APIs comerciales (nunca un alias como ``gpt-4o``) o un repo de
    Hugging Face más ``revision`` (hash de commit) en los modelos abiertos.
    """

    model_id: str
    provider: str  # prefijo de LiteLLM: "openai", "hosted_vllm", ...
    family: str  # familia del modelo, para evitar circularidad juez/entrevistador
    open_weights: bool
    license: str
    revision: Optional[str] = None  # hash de commit en Hugging Face (modelos abiertos)
    notes: str = ""

    @property
    def litellm_name(self) -> str:
        """Nombre que se pasa a ``litellm.completion(model=...)``."""
        return f"{self.provider}/{self.model_id}"


# --- Registro de modelos ------------------------------------------------------
# Revisa las fechas de retirada antes del piloto del WP2 y fija los hashes de
# commit de los modelos abiertos al descargarlos (``revision``).
MODELS: dict[str, ModelSpec] = {
    # Entrevistadores evaluados (diseño principal: 3 modelos)
    "gpt-4o": ModelSpec(
        model_id="gpt-4o-2024-08-06",
        provider="openai",
        family="openai",
        open_weights=False,
        license="OpenAI Terms of Use",
        notes="Comercial. Fuentes secundarias anuncian su retirada el 14-01-2027: "
        "verificar en la página de deprecations de OpenAI.",
    ),
    "llama-3": ModelSpec(
        model_id="meta-llama/Llama-3.1-8B-Instruct",
        provider="hosted_vllm",
        family="meta",
        open_weights=True,
        license="Llama 3.1 Community License (repo con acceso restringido en HF)",
        revision=None,  # TODO: fijar hash de commit al descargar
    ),
    "salamandra-7b": ModelSpec(
        model_id="BSC-LT/salamandra-7b-instruct",
        provider="hosted_vllm",
        family="bsc",
        open_weights=True,
        license="Apache-2.0",
        revision=None,  # TODO: fijar hash de commit al descargar
        notes="Abierto con buen español; cota inferior según el plan del TFG.",
    ),
    # Opcional si hay GPU o endpoint alojado suficiente
    "alia-40b": ModelSpec(
        model_id="BSC-LT/ALIA-40b",
        provider="hosted_vllm",
        family="bsc",
        open_weights=True,
        license="Apache-2.0",
        revision=None,
        notes="Opcional. ~80 GB en bf16: requiere varias GPU o endpoint alojado. "
        "Comprobar si existe variante instruct antes de usarlo.",
    ),
    # Juez y oráculo: modelos distintos entre sí (evita el acoplamiento del
    # artículo original) y de familia distinta a la de todos los entrevistadores.
    # Pesos abiertos: no se retiran y permiten reproducir el entorno. Sustituibles
    # por modelos comerciales de otra familia si el κ del WP5 lo exige.
    "judge": ModelSpec(
        model_id="Qwen/Qwen2.5-72B-Instruct",
        provider="hosted_vllm",
        family="qwen",
        open_weights=True,
        license="Qwen License",
        revision=None,  # TODO: fijar hash de commit al descargar
    ),
    "oracle": ModelSpec(
        model_id="google/gemma-3-27b-it",
        provider="hosted_vllm",
        family="gemma",
        open_weights=True,
        license="Gemma Terms of Use",
        revision=None,  # TODO: fijar hash de commit al descargar
    ),
}


@dataclass
class ReproConfig:
    """Semillas, versiones de modelos y parámetros fijos de los experimentos."""

    # Al menos 3 semillas cuando la temperatura sea > 0 (plan del TFG)
    seeds: tuple[int, ...] = (13, 42, 2026)

    models: dict[str, ModelSpec] = field(default_factory=lambda: dict(MODELS))
    interviewers: tuple[str, ...] = ("gpt-4o", "llama-3", "salamandra-7b")
    judge: str = "judge"
    oracle: str = "oracle"

    # Parámetros de generación
    interviewer_temperature: float = 0.7
    judge_temperature: float = 0.0  # juez determinista
    oracle_temperature: float = 0.0
    max_tokens: int = 512

    # Entorno (ReqElicitGym)
    max_turns: int = 20

    # Registro
    log_dir: str = "logs"
    cache_dir: str = ".cache/llm"

    # --- Semillas -------------------------------------------------------------
    @staticmethod
    def set_global_seed(seed: int) -> None:
        """Fija la aleatoriedad de Python, NumPy y, si están instalados, PyTorch."""
        os.environ["PYTHONHASHSEED"] = str(seed)
        random.seed(seed)
        try:
            import numpy as np

            np.random.seed(seed)
        except ImportError:
            pass
        try:
            import torch

            torch.manual_seed(seed)
            if torch.cuda.is_available():
                torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        except ImportError:
            pass

    @staticmethod
    def derive_seed(base_seed: int, *parts: object) -> int:
        """Semilla estable por (semilla base, escenario, estrategia, ...).

        Sirve para la API (parámetro ``seed`` de OpenAI) y para que cada diálogo
        sea reproducible por separado, con independencia del orden de ejecución.
        """
        key = ":".join([str(base_seed), *map(str, parts)]).encode()
        return int.from_bytes(hashlib.sha256(key).digest()[:4], "big")

    # --- Validación y trazabilidad --------------------------------------------
    def validate(self) -> None:
        """Comprueba la configuración antes de lanzar experimentos."""
        for name in (*self.interviewers, self.judge, self.oracle):
            if name not in self.models:
                raise KeyError(f"Modelo '{name}' no está en el registro")
        evaluated = {self.models[m].family for m in self.interviewers}
        for role, name in (("juez", self.judge), ("oráculo", self.oracle)):
            family = self.models[name].family
            if family in evaluated:
                raise ValueError(
                    f"El {role} ({name}) es de la familia '{family}', igual que un "
                    "entrevistador evaluado: riesgo de circularidad."
                )
        if self.models[self.judge].family == self.models[self.oracle].family:
            raise ValueError(
                "Juez y oráculo son de la misma familia: se pierde la separación "
                "que el TFG introduce frente a ReqElicitGym."
            )
        if len(self.seeds) < 3 and self.interviewer_temperature > 0:
            raise ValueError("Se necesitan al menos 3 semillas con temperatura > 0")

    def snapshot(self) -> dict:
        """Diccionario serializable para guardar en cada log JSONL."""
        data = asdict(self)
        data["models"] = {k: asdict(v) for k, v in self.models.items()}
        return data

    def fingerprint(self) -> str:
        """Hash corto de la configuración, útil para nombrar ejecuciones y cachés."""
        raw = json.dumps(self.snapshot(), sort_keys=True).encode()
        return hashlib.sha256(raw).hexdigest()[:12]


if __name__ == "__main__":
    cfg = ReproConfig()
    cfg.validate()
    print(json.dumps(cfg.snapshot(), indent=2, ensure_ascii=False))
    print("fingerprint:", cfg.fingerprint())
