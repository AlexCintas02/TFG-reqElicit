# Presupuesto de API — diseño principal (3.600 diálogos)

**Resumen.** El diseño principal del TFG (3 modelos × 4 estrategias × ~100 escenarios × 3 semillas ≈ 3.600 diálogos) cuesta entre **≈ 130 $ y ≈ 850 $**, con un escenario base de **≈ 400 $**, margen del 20 % incluido. Lo que más pesa no son los entrevistadores sino **el juez y el oráculo**, que intervienen en todos los diálogos: elegir su modelo es la decisión de coste principal.

> Estimación previa al piloto del WP2. Los precios son tarifas públicas de referencia en USD por millón de tokens y deben comprobarse antes de gastar; el piloto (10 escenarios) sustituirá los tokens supuestos por los medidos.

## 1. Supuestos

| Parámetro | Valor | Fuente |
|---|---|---|
| Diálogos | 3.600 (1.200 por modelo entrevistador) | Plan del TFG, diseño principal |
| Turnos medios por diálogo | 10 (máximo 20) | Plan del TFG / ReqElicitGym |
| Llamadas por turno | 3 (entrevistador, oráculo, juez) | Plan del TFG: ~30 llamadas por diálogo |
| Tokens que añade cada turno al historial | ~150 (pregunta ~50 + respuesta ~100) | Supuesto |

Contexto fijo por llamada (prompt de sistema, escenario, rúbrica) y salida por llamada:

| Rol | Contexto fijo | Salida | Entrada por diálogo (10 turnos) | Salida por diálogo |
|---|---|---|---|---|
| Entrevistador | ~825 | ~150 | 15.000 | 1.500 |
| Oráculo (cliente simulado; ve el escenario y los implícitos ocultos) | ~1.575 | ~120 | 22.500 | 1.200 |
| Juez (clasifica el turno y comprueba los implícitos pendientes) | ~1.825 | ~100 | 25.000 | 1.000 |
| **Total** | | | **62.500** | **3.700** |

La entrada de cada llamada es el contexto fijo más el historial acumulado, por lo que crece de forma cuadrática con el número de turnos.

## 2. Volumen total

| Rol | Tokens de entrada | Tokens de salida |
|---|---|---|
| Entrevistadores (por modelo, 1.200 diálogos) | 18,0 M | 1,8 M |
| Oráculo + juez (los 3.600 diálogos) | 171,0 M | 7,9 M |
| **Total** | **225,0 M** | **13,3 M** |

## 3. Coste de los entrevistadores

| Modelo (ver `src/config.py`) | Despliegue | Precio ref. (entrada / salida por 1M) | Coste |
|---|---|---|---|
| GPT-4o (`gpt-4o-2024-08-06`) | API OpenAI | 2,50 $ / 10,00 $ | **63 $** |
| Llama-3.1-8B-Instruct | Endpoint alojado | ~0,20 $ / 0,20 $ | **4 $** |
| Salamandra-7B-instruct | GPU propia o alquilada de 24 GB con vLLM | ~1 $/h × ~10 h | **≤ 10 $** (0 $ con GPU de la universidad) |
| **Subtotal** | | | **≈ 77 $** |

## 4. Coste del juez y el oráculo, y total

El juez y el oráculo deben ser de una familia distinta a la de los entrevistadores (para evitar circularidad) y distintos entre sí. Tres gamas de precio:

| Escenario | Precio juez + oráculo (entrada / salida por 1M) | Juez + oráculo | + Entrevistadores | **Total con 20 % de margen** | Coste por diálogo |
|---|---|---|---|---|---|
| Económico | 0,15 $ / 0,60 $ | 30 $ | 107 $ | **≈ 129 $** | 0,036 $ |
| **Base** | 1,25 $ / 5,00 $ | 253 $ | 330 $ | **≈ 396 $** | 0,110 $ |
| Alto | 3,00 $ / 15,00 $ | 632 $ | 709 $ | **≈ 851 $** | 0,236 $ |

El margen del 20 % cubre el piloto del WP2, los reintentos por errores y límites de tasa y las repeticiones por fallos.

La configuración actual (`src/config.py`) usa para juez y oráculo modelos de pesos abiertos (Qwen2.5-72B-Instruct y Gemma-3-27B-it). En endpoints alojados suelen caer entre la gama económica y la base; con GPU propia el coste pasa a horas de GPU.

## 5. Sensibilidad

| Si cambia… | Efecto en el coste |
|---|---|
| Turnos medios 10 → 15 | ×1,8 |
| Turnos medios 10 → 20 (máximo) | ×2,7 |
| Razonamiento en cadena (B1) con ~4× salida del entrevistador | ≈ +15 $ (sobre todo GPT-4o) |
| Caché de prompts del proveedor sobre el contexto fijo (~70 % de la entrada de juez y oráculo; descuentos del 50-90 %) | −35 % a −65 % de la entrada de juez y oráculo |
| Caché local de respuestas (`diskcache`) al relanzar ejecuciones | Las repeticiones idénticas no se pagan |

## 6. Volumen total del TFG (referencia)

El plan prevé unos 5.000 diálogos en total (principal + 800 de perfiles + comparación de idioma). Con el coste por diálogo del escenario base serían **≈ 550 $** (≈ 180 $ económico, ≈ 1.180 $ alto).

## 7. Recomendaciones

1. **Medir antes de comprometer.** El piloto del WP2 (10 escenarios, un modelo abierto y uno comercial) debe registrar tokens reales por rol; recalcula esta tabla con ellos.
2. **Validar el juez barato primero.** Si el juez económico alcanza κ ≥ 0,70 frente a humanos en el WP5, el escenario económico es suficiente.
3. **Fijar un tope de gasto** en el panel de cada proveedor (p. ej. 150 % del escenario elegido).
4. **Riesgo de retirada.** Fuentes secundarias indican que `gpt-4o-2024-08-06` se retira el 14-01-2027, antes del fin de los experimentos (H4, semana 14). Compruébalo en la página de deprecations de OpenAI y, si se confirma, ejecuta primero todo lo que dependa de GPT-4o o elige otro snapshot.
