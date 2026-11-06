# WP1 · Notas de extracción estructurada (paso 1 de 2)

Documento intermedio de la tarea **H1-02 (WP1 – Revisión del estado del arte)**. Recoge, paper a paper, lo que necesitan los paquetes WP3 (dataset), WP5 (simulador y juez), WP6 (entrevistador) y WP7 (sintetizador). El paso 2 (capítulo y matriz comparativa) se escribirá a partir de aquí.

**Convenciones**
- Las cifras van tal como aparecen en el artículo, con su página (`p. N`, numeración del PDF).
- Las citas literales de prompts se dejan en inglés, como en el original.
- ⚠️ marca inconsistencias o puntos dudosos; 🔧 marca lo que hay que comprobar en el código (WP2).
- *Nota propia* marca interpretaciones mías, no afirmaciones del artículo.

---

## 0. Inventario de `docs/papers/` y plan de lotes

| Archivo | Trabajo | Lote |
|---|---|---|
| `2602.18306v1.pdf` | ReqElicitGym (Jin et al., 2026) | 1 |
| `2505.03733v2.pdf` | WebGen-Bench (Lu et al., 2025) | 1 |
| `2509.22644v1.pdf` | WebGen-Agent (Lu et al., 2025) | 1 |
| `2507.02564v1.pdf` | LLMREI (Korn et al., 2025) | 2 |
| `2507.02858v1.pdf` | Requirements Elicitation Follow-Up Question Generation (Shen et al., 2025) | 2 |
| `2406.11439v1.pdf` | GPT-Powered Elicitation Interview Script Generator (Görer y Aydemir, 2024) | 2 |
| `2404.16045v1.pdf` | Elicitron (Ataei et al., 2024) | 3 |
| `2509.01048v1.pdf` | Generative Goal Modeling (Sharfuddin y Breaux, 2025) | 3 |
| `2411.19552v2.pdf` | RECOVER (Voria et al., 2025) | 3 |
| `2606.25867v1.pdf` | LENS: requisitos latentes en conversaciones (Sivakumar et al., 2026) | 3 |
| `2509.11446v1.pdf` | LLMs for RE: revisión sistemática (Zadenoori et al., 2025) | 4 |
| `2004.01099v2.pdf` | NLP4RE: estudio de mapeo (Zhao et al.) | 4 |
| `2507.13081v1.pdf` | iReDev: A Knowledge-Driven Multi-Agent Framework (Jin et al., 2025) | 4 |
| `AcceptedREjSpecialIssueFinalVersion.pdf` | Teaching RE Interviews: Learning from Mistakes (Bano et al., 2019) | 4 |
| `wer202511.pdf` | From Elicitation Interviews to Software Requirements (Almeida et al., 2025) | 4 |

| Lote | Tema | Paquetes que alimenta | Estado |
|---|---|---|---|
| 1 | Entorno, métricas y datos fuente | WP2, WP3, WP5 | ✅ Hecho y validado |
| 2 | Entrevistador y baselines B2/B3 | WP6 | ✅ Hecho y validado |
| 3 | Simulación de stakeholders y síntesis | WP5 (perfiles), WP7 | ✅ Hecho y validado |
| 4 | Revisiones sistemáticas, taxonomía de errores y generación multi-agente | Capítulo, taxonomías, RQ, WP6, WP7 | ✅ Hecho (este documento) |

> ✅ Con la extracción del Lote 4 queda completado el **Paso 1 de WP1** sobre la totalidad de los **15 trabajos** de `docs/papers/`.

---

## Lote 1

### 1.1 ReqElicitGym

**Referencia y año**
- Dongming Jin, Zhi Jin, Zheng Fang, Linyu Li, Xiaotian Yang, Yuanpeng He, Xiaohong Chen. *ReqElicitGym: An Evaluation Environment for Interview Competence in Conversational Requirements Elicitation.* arXiv:2602.18306v1, 20-02-2026.
- Venue: preprint con plantilla de ACM TOSEM. ⚠️ Los metadatos son de plantilla ("Vol. 1, No. 1", "February 2025", "Received 20 February 2007"), así que no consta que esté aceptado: citarlo como preprint de arXiv.
- Código y datos: https://github.com/jdm4pku/ReqElicitBench.

**Problema y fase de RE**
- **Elicitación interactiva**: evalúa la competencia de entrevista de un LLM en diálogo de varios turnos, con **simulación de stakeholder** (oráculo) y **juez** automático.
- De las cuatro fases de entrevista de Christel y Kang (preparación, entrevista, registro, integración, p. 4) cubre solo la entrevista. **No evalúa los requisitos redactados al final** (hueco que cubre nuestro WP7).

**Metodología / arquitectura agéntica**

Tres módulos: dataset, oráculo y juez ("task evaluator"). El oráculo abre con el requisito inicial; el entrevistador elige estrategia y pregunta hasta que termina (máx. **20 turnos**, p. 13).

| Rol | Modelo | Configuración | Prompt |
|---|---|---|---|
| Entrevistador (evaluado) | 7 LLM (ver abajo) | Mismo prompt para todos; **una sola pregunta por turno** o señal de fin; Non-CoT y CoT; temperatura 0; máx. 2.048 tokens (Non-CoT) y 8.196 (CoT) (p. 16) | **No está en el artículo** ("provided in our replication package") 🔧 |
| Oráculo | GPT-5.2 (p. 13) ⚠️ GPT-5.1 en p. 3 | Temperatura 0,7; máx. 1.024 tokens; timeout 30 s | Fig. 5 (abajo) |
| Juez | GPT-5.2 | Temperatura 0,0; máx. 1.024 tokens; timeout 30 s | Fig. 6 (abajo) |

- **Separación de roles**: los tres están separados por prompt, pero **oráculo y juez usan el mismo modelo**, y GPT-5.2 es además uno de los entrevistadores evaluados (circularidad en sus propios experimentos).
- **Principios del oráculo** (p. 10): (1) *Groundedness*: solo revela lo anotado como implícito; (2) *Passive response*: no aporta nada que no se le pregunte; (3) *Context awareness*: condiciona en todo el historial.
- **Estado interno**: el entorno mantiene el conjunto de implícitos **pendientes** (el juez solo ve los que quedan). El entrevistador no tiene estado estructurado: es prompting libre.
- **Acoplamiento juez → oráculo** (*nota propia*, deducido de las variables de la Fig. 5): el oráculo **no ve la lista de implícitos**; solo recibe el tipo de acción, la marca de relevancia y el implícito que el juez ha detectado. Por tanto el oráculo solo puede revelar lo que el juez marca: un error del juez se propaga a la respuesta del cliente. La validación del oráculo usó la relevancia anotada por humanos (p. 10), así que ese efecto en cadena no está medido.

Prompt del oráculo (Fig. 5, p. 11, literal):
```
System Role. You are a user being interviewed about your software requirements. Respond naturally to the
interviewer's questions or statements.
Response Guidelines.
• Answer based on your implicit requirements if the question is relevant.
• If the question is not relevant, politely indicate that you do not care about it.
• Keep responses brief and concise (1–3 sentences).
• Maintain a natural and conversational tone.
• Adjust your response according to the full dialogue context.
Output Format. Return a JSON object: {"response": "<answer>"}
Input Variables.
Conversation History: {conversation_history}
Interviewer's Latest Utterance: {latest_utterance}
Context Metadata:
  Action type: {action_type}
  Relevance flag: {is_relevant}
  Relevant implicit requirement: {relevant_requirement} (null if not relevant)
```

Prompt del juez (Fig. 6, p. 12, literal; titulado "Validation Judge Prompt Design"):
```
System Role. You are an expert evaluator assessing the interviewer's action in a conversational requirements
elicitation process. Classify the interviewer's latest action and determine whether it targets remaining implicit
requirements.
Action Definitions.
• clarify: Ask for clarification of previously mentioned information.
• probe: Explore new or more detailed requirement information.
• finish: Conclude the conversation after sufficient information is collected.
Evaluation Guidelines.
• Analyze the latest utterance based on full context.
• Determine the action type (clarify, probe, finish).
• If probe, assess whether it targets remaining implicit requirements.
• Provide a brief justification.
Output Format. Return a JSON object:
{"action_type": "<type>",
 "is_relevant_to_implicit_requirements": <true/false>,
 "relevant_implicit_requirement_id": "<id or null>",
 "reasoning": "<explanation>"}
Input Variables.
Initial Requirements: {initial_requirements}
Conversation History: {conversation_history}
Interviewer's Latest Utterance: {latest_utterance}
Remaining Implicit Requirements: {remaining_requirements}
```

**Modelos evaluados** (p. 14-15): GPT-5.2, Claude Opus 4.5, Gemini 3 Flash, DeepSeek V3.2, Kimi K2.5, GLM-4.7 y Qwen3 235B A22B 2507.

**Datos, idioma y dominio**
- **101 escenarios** de desarrollo web en **10 tipos de aplicación**, en **inglés**. Fuente: las 101 instrucciones de test de **WebGen-Bench** (sintéticas, licencia MIT). El ejemplo de la Fig. 3 (informes de bolsa) es la instrucción de test n.º 1 de WebGen-Bench.
- Cada escenario tiene: *Initial Req* (descripción incompleta), *Implicit Req* (detalles que faltan, cada uno de tipo **Interaction**, **Content** o **Style**) y *Final Req* (historias de usuario).
- Totales (p. 9): **101 Initial Req, 632 Implicit Req y 1.000 Final Req**. Por escenario: requisito inicial de 7 a 39 palabras (media 21,86); implícitos de 2 a 12 (media 6,26); historias finales de 4 a 24 (media 9,90).
- Distribución por tipo (Tabla 1, p. 9):

| Tipo | #Esc. | Long. inicial (mín/media/máx) | #Implícitos (mín/media/máx) | #Finales (mín/media/máx) |
|---|---|---|---|---|
| Showcase Websites | 22 | 9 / 29,88 / 39 | 2 / 4,25 / 7 | 5 / 8,64 / 12 |
| Community Platforms | 12 | 7 / 14,75 / 22 | 2 / 4,75 / 6 | 4 / 7,67 / 11 |
| E-commerce Web | 16 | 13 / 20,75 / 33 | 3 / 5,25 / 8 | 7 / 10,44 / 17 |
| Learning Platforms | 8 | 19 / 21,38 / 30 | 5 / 8,38 / 12 | 7 / 10,25 / 18 |
| Entertainment App | 7 | 11 / 27,43 / 38 | 2 / 4,43 / 6 | 6 / 12,43 / 18 |
| Dashboards | 6 | 13 / 19,33 / 26 | 4 / 5,00 / 6 | 8 / 8,67 / 10 |
| Enterprise Management | 8 | 16 / 21,33 / 27 | 4 / 7,17 / 9 | 6 / 14,00 / 24 |
| Publishing Platforms | 4 | 17 / 19,00 / 22 | 3 / 5,50 / 8 | 5 / 9,75 / 15 |
| Job Search Platforms | 4 | 16 / 18,00 / 21 | 7 / 9,25 / 11 | 9 / 11,25 / 14 |
| Productivity Tool | 14 | 14 / 17,40 / 21 | 3 / 7,60 / 10 | 6 / 9,57 / 14 |
| **Total** | **101** | 7 / 21,86 / 39 | 2 / 6,26 / 12 | 4 / 9,90 / 24 |

- **Construcción** (p. 7-9): plataforma de anotación propia; **3 doctorandos** con más de 4 años de experiencia en IS; formación común y anotación piloto. Orden: *Final* (reescribir la instrucción como historias de usuario) → *Initial* (conservar la intención, omitir lo que habría que preguntar) → *Implicit* (diferencia Final − Initial, con su tipo). Control de calidad: **3 rondas** revisadas por el primer autor, con **26 → 9 → 0** incidencias (implícitos que faltan, iniciales que revelan demasiado, incoherencias).
- ⚠️ **No reporta acuerdo entre anotadores**: el control de calidad lo hace una sola persona. Nuestra doble anotación del 20 % sería una mejora metodológica.
- **Validación**: 33 entrevistas reales (555 turnos del entrevistador) de dos escenarios de Ferrari et al. 2020: *Salon* (peluquería: reservas y turnos; 15 entrevistas, 233 turnos) y *Ski* (cadena de estaciones de esquí; 18 entrevistas, 322 turnos). El idioma de estas entrevistas no se indica.
- **Licencia**: el artículo no la menciona (el plan del TFG indica que el repositorio no tiene fichero de licencia).

**Métricas y resultados cuantitativos exactos**

Validación del oráculo (Tabla 2, p. 11; media ± desviación por sesión):

| Sistema | #Entrevistas | #Turnos | κ | FP ↓ | FN ↓ |
|---|---|---|---|---|---|
| Salon | 15 | 233 | 0,78 ± 0,09 | 0,06 ± 0,04 | 0,11 ± 0,07 |
| Ski | 18 | 322 | 0,69 ± 0,12 | 0,09 ± 0,06 | 0,15 ± 0,08 |
| Total | 33 | 555 | **0,73** | 0,08 | 0,13 |

Validación del juez (Tabla 3, p. 13):

| Sistema | κ acción | κ relevancia | FP ↓ | FN ↓ |
|---|---|---|---|---|
| Salon | 0,83 ± 0,21 | 0,72 ± 0,17 | 0,00 ± 0,00 | 0,09 ± 0,07 |
| Ski | 0,72 ± 0,22 | 0,72 ± 0,12 | 0,00 ± 0,00 | 0,09 ± 0,10 |
| Total | **0,78** | **0,73** | 0,00 | 0,09 |

Competencia global (Tabla 4, p. 17; "mean ± std over all scenarios"):

| LLM | #Turnos Non-CoT | #Turnos CoT | IRE Non-CoT | IRE CoT | TKQR Non-CoT | TKQR CoT |
|---|---|---|---|---|---|---|
| GPT-5.2 | 19,98 ± 0,20 | 8,12 ± 1,74 | 0,13 ± 0,03 | 0,11 ± 0,02 | 0,09 ± 0,03 | 0,21 ± 0,05 |
| Claude Opus 4.5 | 6,36 ± 2,26 | 5,94 ± 1,88 | 0,08 ± 0,02 | 0,07 ± 0,02 | 0,19 ± 0,04 | 0,28 ± 0,06 |
| Gemini 3 Flash | 7,76 ± 2,74 | 6,85 ± 2,31 | 0,11 ± 0,02 | 0,10 ± 0,02 | 0,11 ± 0,03 | 0,18 ± 0,04 |
| DeepSeek V3.2 | 11,38 ± 3,61 | 5,73 ± 1,91 | **0,32 ± 0,04** | 0,19 ± 0,03 | 0,35 ± 0,05 | 0,41 ± 0,07 |
| Kimi K2.5 | 5,76 ± 2,36 | 5,46 ± 1,21 | 0,19 ± 0,04 | 0,20 ± 0,03 | 0,33 ± 0,04 | **0,55 ± 0,08** |
| GLM-4.7 | 3,86 ± 2,15 | 4,53 ± 1,60 | 0,15 ± 0,03 | 0,20 ± 0,04 | 0,24 ± 0,07 | 0,33 ± 0,07 |
| Qwen3 235B | 4,20 ± 0,99 | 4,52 ± 1,01 | 0,13 ± 0,03 | 0,14 ± 0,01 | 0,22 ± 0,08 | 0,25 ± 0,03 |

Estrategias (Tabla 5, p. 18; recuentos totales sobre los 101 escenarios):

| LLM | #Clarify/#Probe Non-CoT | #Clarify/#Probe CoT | ESR clarify Non-CoT | ESR clarify CoT | ESR probe Non-CoT | ESR probe CoT |
|---|---|---|---|---|---|---|
| GPT-5.2 | 23 / 414 | 31 / 203 | 0,04 | 0,11 | 0,22 | 0,43 |
| Claude Opus 4.5 | 7 / 109 | 15 / 82 | 0,29 | 0,42 | 0,51 | 0,61 |
| Gemini 3 Flash | 16 / 144 | 22 / 108 | 0,25 | 0,36 | 0,47 | 0,57 |
| DeepSeek V3.2 | 24 / 275 | 28 / 164 | 0,05 | 0,13 | 0,47 | 0,62 |
| Kimi K2.5 | 19 / 238 | 25 / 176 | 0,06 | 0,14 | 0,50 | 0,68 |
| GLM-4.7 | 15 / 142 | 22 / 128 | 0,07 | 0,16 | 0,39 | 0,52 |
| Qwen3 235B | 12 / 118 | 16 / 101 | 0,04 | 0,09 | 0,33 | 0,41 |

IRE por tipo de implícito (Tabla 6, p. 18):

| LLM | Int Non-CoT | Con Non-CoT | Sty Non-CoT | Int CoT | Con CoT | Sty CoT |
|---|---|---|---|---|---|---|
| GPT-5.2 | 0,19 | 0,13 | <0,01 | 0,12 | 0,09 | <0,01 |
| Claude Opus 4.5 | 0,08 | 0,12 | <0,01 | 0,06 | 0,09 | <0,01 |
| Gemini 3 Flash | 0,12 | 0,16 | <0,01 | 0,09 | 0,12 | <0,01 |
| DeepSeek V3.2 | 0,48 | 0,46 | 0,01 | 0,29 | 0,27 | <0,01 |
| Kimi K2.5 | 0,31 | 0,23 | <0,01 | 0,33 | 0,25 | <0,01 |
| GLM-4.7 | 0,21 | 0,20 | 0,01 | 0,30 | 0,26 | <0,01 |
| Qwen3 235B | 0,20 | 0,19 | <0,01 | 0,22 | 0,20 | <0,01 |

IRE por tipo de aplicación (p. 18-19): de **0,05** (E-commerce) y 0,06 (Learning) a **0,27** (Dashboards); Community 0,15; Publishing 0,14.

Conclusiones del artículo: IRE máximo 0,32; CoT sube siempre TKQR y baja los turnos, pero no sube el IRE de forma fiable; todos los modelos prefieren probe a clarify y clarify es menos eficaz; el estilo queda casi a cero. GPT-5.2 agota casi siempre los 20 turnos (19,98) por falta de criterio de parada. Líneas futuras: entrevista guiada por ontologías de dimensiones y RL con recompensas IRE/TKQR/ESR (p. 20).

**Insumo directo para ReqElicit-ES (fórmulas, juez e inconsistencias)**

*Fórmulas (§4.3, p. 15-16)*

- **IRE** (cobertura de implícitos), siendo \(R\) los implícitos del escenario y \(\hat R_{\le T}\) los elicitados hasta el turno final \(T\):

  $$\mathrm{IRE} = \frac{|\hat R_{\le T}|}{|R|}, \qquad \mathrm{IRE}_a = \frac{|\hat R_{a,\le T}|}{|R_a|},\; a \in \{\text{Int}, \text{Con}, \text{Sty}\}$$

  Se promedia sobre escenarios. 🔧 Para \(\mathrm{IRE}_a\) no dice si es macro (media de escenarios) o micro (suma global); la Fig. 4b indica que hay escenarios sin implícitos de algún tipo, donde la versión macro no está definida.

- **ESR** (eficacia por estrategia), con \(T_s\) los turnos de estrategia \(s \in \{\text{clarify}, \text{probe}\}\) y \(T_s^+\) los que elicitan al menos un implícito:

  $$\mathrm{ESR}_s = \frac{|T_s^+|}{|T_s|}$$

  La Tabla 5 da recuentos globales, lo que apunta a agregación micro. 🔧

- **TKQR** (preguntar pronto lo importante; adaptado de nDCG). \(n\) = turnos antes de dejar de preguntar; \(K = |R|\); \(h_i = 1\) si el turno \(i\) toca un implícito:

  $$\mathrm{DCG}_n = \sum_{i=1}^{n} \frac{h_i}{\log_2(i+1)}, \qquad \mathrm{IDCG}_n = \sum_{i=1}^{\min(n,K)} \frac{1}{\log_2(i+1)}, \qquad \mathrm{TKQR} = \frac{\mathrm{DCG}_n}{\mathrm{IDCG}_n}$$

  *Nota propia*: como el juez solo ve los implícitos pendientes y devuelve un único id, cada implícito cuenta una vez y \(\mathrm{TKQR} \in [0,1]\). Con \(n = 0\) no está definido. TKQR mide la **precisión de los primeros turnos, no la cobertura**: una entrevista de una sola pregunta acertada da TKQR = 1 con IRE = 1/K (por eso Kimi K2.5 CoT tiene TKQR 0,55 con IRE 0,20). Hay que reportarlo siempre junto al IRE.

- **ORA**: ⚠️ **no aparece en el artículo**. Solo puede definirse a partir del código. 🔧

*Clases de acción del juez*: `clarify` (aclarar algo ya mencionado), `probe` (explorar información nueva o más detallada) y `finish` (cerrar). Salida JSON con `action_type`, `is_relevant_to_implicit_requirements`, `relevant_implicit_requirement_id` (un único id o null) y `reasoning`.

*Definición de "elicitado"* (*nota propia*, importante para RQ3): un implícito cuenta como elicitado cuando **el juez decide que la pregunta lo toca**, no cuando el cliente lo revela. Con perfiles vago o contradictorio, el cliente puede no revelar nada y el IRE no cambiaría. Para RQ3 conviene medir también un **IRE de revelación** (lo que el cliente llega a decir).

*Hipótesis sobre el estilo* (*nota propia*, a confirmar con los datos en WP2): todas las instrucciones de WebGen-Bench terminan con una frase de **colores** (fondo + componentes), y el ejemplo de la Fig. 3 convierte esa frase en los dos implícitos de estilo. Si es así en general, el IRE de estilo ≈ 0 significa sobre todo que **ningún modelo pregunta por colores**. Para nuestra H2 hay dos consecuencias:
- un M1 con dimensión "estilo" podría mejorar mucho con solo preguntar por colores, una mejora poco interesante;
- en WP3 convendría un estilo más rico en los escenarios nativos (maquetación, tipografía, tono, densidad) y reportar aparte el estilo "color" y el resto.

*Inconsistencias del artículo* ⚠️

| # | Inconsistencia | Dónde |
|---|---|---|
| 1 | Oráculo con GPT-5.1 frente a GPT-5.2 | p. 3 frente a §3.5, p. 13 |
| 2 | 10 tipos de aplicación frente a "20 application types" (20 es la taxonomía de WebGen-Bench) | Resumen, §3.2.1 y Tabla 1 frente a RQ4, p. 14 |
| 3 | "six mainstream LLMs" frente a 7 evaluados | RQ1, p. 14 frente a §4.2 y tablas |
| 4 | "five steps" frente a 6 pasos enumerados (i)-(vi) | §3.2.2, p. 7 |
| 5 | κ del juez 0,72 frente a 0,78 (acción) y 0,73 (relevancia); el total de relevancia es 0,73 aunque ambos sistemas tienen 0,72 | p. 3 frente a Tabla 3 |
| 6 | Tabla 1: la suma ponderada de implícitos por tipo da ≈ 585 (media 5,80), no 632 (6,26). Varias medias son imposibles con el n.º de escenarios (7,17 × 8 = 57,36; 7,60 × 14 = 106,4; 29,88 × 22 = 657,36) | p. 9 (comprobado aritméticamente) |
| 7 | El juez solo evalúa relevancia "if probe", así que el ESR de clarify debería ser 0, pero vale de 0,04 a 0,42 | Fig. 6 frente a Tabla 5 |
| 8 | Desviaciones de la Tabla 4 demasiado pequeñas para ser "over all scenarios" (IRE ± 0,02-0,04) | p. 17 |
| 9 | Máximo de 8.196 tokens en CoT (probablemente 8.192) | p. 16 |
| 10 | Referencias rotas: origen de TKQR "[? ]" y "Section ??" | p. 14-15 |
| 11 | ORA citada en el plan del TFG pero ausente del artículo | — |
| 12 | Circularidad: GPT-5.2 es entrevistador evaluado y a la vez oráculo y juez | §3.5 y §4.2 |

*A comprobar en el código (WP2)* 🔧
1. Prompt del entrevistador (Non-CoT y CoT) y formato de la señal de fin.
2. Orden real de llamadas por turno (¿juez antes que oráculo?) y qué recibe el oráculo.
3. Si los turnos `clarify` pueden marcarse como relevantes (inconsistencia 7).
4. Agregación de IRE, IRE por tipo y ESR (macro o micro) y significado de las desviaciones.
5. Definición de ORA.
6. Modelo y versión reales de oráculo y juez; semillas.
7. Recuento real de implícitos por tipo (inconsistencia 6) y si el estilo son solo colores.

*Qué adoptar y qué cambiar en ReqElicit-ES*

| Paquete | Adoptar | Cambiar o añadir |
|---|---|---|
| WP3 | Esquema Initial / Implicit (con tipo) / Final en historias de usuario; anotación por diferencia; rondas de QC hasta 0 incidencias | Acuerdo entre anotadores (20 % doble); estilo más rico que el color; categorías extra (restricciones, reglas de negocio) |
| WP5 | Prompts de oráculo y juez como punto de partida (traducir); oráculo con temperatura 0,7 y juez con 0,0; validación con κ, FP y FN | Modelos distintos para oráculo y juez y de otra familia que los entrevistadores; validar la cadena juez → oráculo completa, no con relevancia humana; perfiles de cliente sobre el oráculo pasivo |
| WP6 | Una pregunta por turno; límite de 20 turnos; condiciones Non-CoT/CoT (= B0/B1) | M1 con estado por dimensiones y criterio de parada (justificado por los 19,98 turnos de GPT-5.2 y las líneas futuras del artículo) |
| WP8 | IRE, IRE por tipo, TKQR, ESR, turnos | Reportar TKQR siempre con IRE; IRE de revelación para RQ3; varias semillas (el artículo usa temperatura 0 y una sola ejecución) |

---

### 1.2 WebGen-Bench

**Referencia y año**
- Zimu Lu, Yunqiao Yang, Houxing Ren, Han Xiao, Ke Wang, Weikang Shi, Aojun Zhou, Mingjie Zhan, Hongsheng Li (MMLab, CUHK). *WebGen-Bench: Evaluating LLMs on Generating Interactive and Functional Websites from Scratch.* arXiv:2505.03733v2, 11-08-2025.
- Venue: "Preprint. Under review" (incluye la checklist de NeurIPS).
- Código, datos y pesos: https://github.com/mnluzimu/WebGen-Bench.

**Problema y fase de RE**
- **No es un trabajo de RE**: evalúa agentes de código que generan sitios web completos desde una instrucción en lenguaje natural.
- Relevancia para el TFG: es la **fuente de los 101 escenarios de ReqElicitGym** y la base del plan B (licencia MIT).

**Metodología / arquitectura agéntica**
- *Instrucciones* (p. 4-5): 20 categorías de aplicación sacadas de Upwork, Freelancer y Proginn; 40 doctorandos generan **10.152 descripciones de proyecto** (objetivo + requisitos funcionales y de apariencia); GPT-4o las convierte en instrucciones con un prompt one-shot sin detalles técnicos (Fig. 4); se eligen de 2 a 8 por categoría → **101 instrucciones de test**, reagrupadas en 3 categorías técnicas y 13 subcategorías (Tabla 2: Content Presentation 28, User Interaction 49, Data Management 24).
- *Casos de prueba* (p. 5-6): GPT-4o redacta borradores (el prompt pide de 5 a 10 por instrucción, Fig. 8); dos doctorandos los revisan por separado y resuelven discrepancias → **647 casos (de 4 a 11 por instrucción)**. Cada caso es una operación atómica más el resultado esperado.
- *Evaluación*: agente web WebVoyager con **Qwen2.5-VL-32B-Instruct**, que responde YES / NO / PARTIAL con un máximo de 15 interacciones; apariencia puntuada por **GPT-4o de 1 a 5** (Fig. 11).
- *Descontaminación* de WebGen-Instruct frente al test (Ap. D): Jaccard de 5-gramas > 0,6 → fuera; coseno con all-MiniLM-L6-v2 > 0,55 → fuera; revisión manual de los 3 más parecidos de cada instrucción de test.
- No hay roles de entrevistador, oráculo o juez de diálogo: hay generador (agente de código) y evaluadores (agente web y VLM), que son modelos distintos.

**Datos, idioma y dominio**
- **101 instrucciones de test** con 647 casos, y **WebGen-Instruct**: 6.667 instrucciones de entrenamiento.
- Inglés; sintéticas (GPT-4o a partir de descripciones escritas por humanos); dominio web.
- Casos por categoría (Tabla 8): Functional Testing 339, Data Display 186 y Design Validation 122.
- **Licencia: MIT** para el dataset y el código (Ap. A, p. 14).

**Métricas y resultados cuantitativos exactos**
- Exactitud:

  $$\text{Accuracy} = \frac{N_{\text{YES}} + 0{,}5 \cdot N_{\text{PARTIAL}}}{N_{\text{total}}} \times 100\,\%$$

- Mejor combinación general: Bolt.diy + DeepSeek-R1, **27,8 %**; Claude-3.5-Sonnet 26,4 % con la mejor apariencia (**3,0**); GPT-4o 12,8 % (apariencia 1,5); WebGen-LM-32B (ajustado con 600 trayectorias) **38,2 %** (Tabla 3).
- Concordancia del agente web con humanos (Tabla 5): 90,3 % (Claude-3.5), 86,1 % (DeepSeek-R1) y 94,4 % (DeepSeek-V3).
- Coste estimado de la evaluación manual: 10,8 h y 377,8 $ para los 647 casos (p. 6).
- Puntuación de apariencia con otros evaluadores (Tabla 9): mismo orden con GPT-4o, o3, Claude-3.5 y humanos (p. ej., Claude-3.5: 3,0 / 2,7 / 2,4; humanos 2,8).

**Insumo directo para ReqElicit-ES**
- No define IRE, TKQR, ESR ni ORA; esas fórmulas son de ReqElicitGym (§1.1).
- **Plan B viable**: los 101 escenarios de ReqElicitGym salen de las 101 instrucciones de test (MIT). Podemos derivar nuestros propios Initial / Implicit / Final desde ellas sin reutilizar las anotaciones de ReqElicitGym, que no tienen licencia.
- **WebGen-Instruct (6.667, ya descontaminado frente al test)**: reserva de escenarios para la partición *dev* y para ajustar prompts sin tocar el test.
- **Los 647 casos de prueba son requisitos atómicos y comprobables** (de 4 a 11 por escenario): sirven como control independiente al anotar implícitos (paso 4 de construcción del TFG).
- **Estilo**: todas las instrucciones vistas terminan con una frase de colores ("Set the background color to white and the component color to navy"); ver la hipótesis en §1.1.
- **Taxonomías**: 20 categorías de aplicación (Tabla 7), 3 categorías técnicas con 13 subcategorías (Tabla 2) y los 10 tipos de ReqElicitGym, que no explica cómo los agrupó. En WP3 hay que fijar una correspondencia.
- **Procedimiento de descontaminación** (Jaccard + coseno + revisión manual) reutilizable para comprobar que los escenarios nativos no se parecen a los traducidos ni al test.
- Inconsistencias ⚠️: la Tabla 8 suma "667" (339 + 186 + 122 = 647); el prompt pide de 5 a 10 casos y el resultado final tiene de 4 a 11; el párrafo de recogida de descripciones está duplicado (p. 4-5); los pies de las Fig. 9 y 10 están intercambiados y la Fig. 10 se cita como el prompt de apariencia (que es la Fig. 11).

---

### 1.3 WebGen-Agent

**Referencia y año**
- Zimu Lu, Houxing Ren, Yunqiao Yang, Ke Wang, Zhuofan Zong, Junting Pan, Mingjie Zhan, Hongsheng Li. *WebGen-Agent: Enhancing Interactive Website Generation with Multi-Level Feedback and Step-Level Reinforcement Learning.* arXiv:2509.22644v1, 26-09-2025.
- Venue: preprint. Código: https://github.com/mnluzimu/WebGen-Agent.

**Problema y fase de RE**
- **No es un trabajo de RE**: es un agente que genera sitios web y los mejora con retroalimentación visual, entrenado con RL por pasos. Usa WebGen-Bench como banco de pruebas.

**Metodología / arquitectura agéntica**
- Bucle por paso: generar código → ejecutar → recoger retroalimentación. Un VLM (**Qwen2.5-VL-32B-Instruct**) describe y puntúa la captura de pantalla (`Score_shot`, 1-5) y un agente GUI prueba la funcionalidad (`Score_gui`, 1-5), con sugerencias.
- Tras 5 pasos seguidos con error vuelve al mejor paso anterior; al final elige el mejor paso (mayor `Score_gui`, luego mayor `Score_shot`, luego el más reciente).
- **Step-GRPO**: recompensa por paso \(r_j = \text{Score}_{\text{shot},j} + \text{Score}_{\text{gui},j}\), ventaja normalizada sobre todos los pasos del grupo y sin pérdida KL. Calentamiento con SFT sobre unas 700 trayectorias de DeepSeek-V3; GRPO con 500 instrucciones de WebGen-Instruct, 5 muestras por instrucción, lr 1e-6 y batch 16. Máximo 20 iteraciones y temperatura 0,5.
- Separa generador (LLM de código) y evaluador (VLM de otra familia).

**Datos, idioma y dominio**
- WebGen-Bench (101 instrucciones, 647 casos) y un subconjunto de WebGen-Instruct. Inglés, sintético, web.
- Licencia: **no se indica en el artículo** (WebGen-Bench es MIT).

**Métricas y resultados cuantitativos exactos**
- Claude-3.5-Sonnet: exactitud de **26,4 % → 51,9 %** y apariencia de 3,0 → 3,9 (frente a Bolt.diy). Mejor resultado: Qwen3-Coder-480B-A35B, **58,2 %** y apariencia 4,3 (Tabla 1).
- Qwen2.5-Coder-7B: 12,4 % → SFT 38,9 % → Step-GRPO **45,4 %** (apariencia 1,6 → 3,4 → 3,7). Qwen3-8B: 34,1 % → 38,6 % → 43,4 %.
- Ablación con DeepSeek-V3 (Tabla 2): solo ejecución 45,9 % → flujo completo 52,6 %; el agente GUI aporta la mayor mejora (+3,3 puntos).
- Exactitud de las puntuaciones del evaluador frente a humanos (Tabla 5): capturas del 93,6 % al 95,6 %; agente GUI del 89,6 % al 92,2 %. El 98,3 % de las instrucciones de prueba GUI tienen cobertura alta (puntuación ≥ 4).

**Insumo directo para ReqElicit-ES**
- **Relevancia directa baja**: no aporta fórmulas, perfiles ni datos nuevos para WP3, WP5, WP6 o WP7. Propongo citarlo solo en trabajo relacionado.
- Ideas aprovechables:
  - Auditar el juez **dando a humanos cada veredicto para que lo confirmen o lo corrijan** (exactitud y error estándar). Es un complemento barato al κ para la auditoría de unos 100 turnos del WP5.
  - **Recompensa por paso** como trabajo futuro (RL con IRE/TKQR por turno), en línea con lo que propone ReqElicitGym.
  - Lección práctica: el prompt de la Fig. 7 tiene la lógica invertida ("If yes [hay fallo], set test_passed: true"). Los prompts de nuestro juez deben probarse con casos conocidos antes de usarse (WP5).
- Inconsistencias ⚠️: el resumen dice "de 38,9 % a 45,4 %" para Qwen2.5-Coder-7B, pero 38,9 % es el modelo tras SFT (el base tiene 12,4 %); la apariencia de Aider + DeepSeek-V3 es 1,3 aquí y 1,2 en WebGen-Bench.

---

## Lote 2

### 2.1 LLMREI

**Referencia y año**
- Alexander Korn, Samuel Gorsch, Andreas Vogelsang (University of Duisburg-Essen y University of Cologne). *LLMREI: Automating Requirements Elicitation Interviews with LLMs.* arXiv:2507.02564v1, 03-07-2025.
- Venue: 33rd IEEE International Requirements Engineering Conference (RE 2025), pp. 19–30 (según derechos de autor IEEE en p. 1 y cita en ReqElicitGym).
- Paquete de réplica (instrumentos, datos crudos, etiquetas ground truth y código): https://doi.org/10.5281/zenodo.14988928 (p. 2).

**Problema y fase de RE**
- **Elicitación interactiva**: chatbot entrevistador autónomo que conduce entrevistas de elicitación de requisitos con stakeholders reales (simulados por humanos) con mínima intervención humana, buscando reducir errores comunes del entrevistador y escalar la recogida temprana de requisitos (p. 1-2).

**Metodología / arquitectura agéntica**
- Explora tres enfoques para el rol de **entrevistador** (no hay oráculo ni juez LLM; los stakeholders y evaluadores son humanos):
  1. **Zero-shot prompting (`LLMREI-short`)**: modelo **`gpt-4o-2024-08-06`** vía API de OpenAI con ajustes por defecto (p. 3, 6). Prompt de sistema conciso de tres frases diseñado tras iterar para evitar que el modelo actúe como asistente pasivo o abrume con múltiples preguntas a la vez.
  2. **Least-to-most prompting (`LLMREI-long`)**: modelo **`gpt-4o-2024-08-06`**. ⚠️ No aplica least-to-most dinámico dentro de un turno, sino un *refinamiento a nivel de sesión* ("session-level refinement process", p. 3-4) basado en la taxonomía de errores de Bano et al. [25] y las guías de entrevista de Ferrari et al. [26, 27]. El prompt final se estructura en 3 componentes: (1) *Role Description*, (2) *Interview Guidelines* (`{Interview Cookbook}` de 5 pasos con caminos de repregunta y resumen final), y (3) *Error Handling and Behavior Adjustments* (máximo 1 pregunta por turno salvo que 2 estén estrechamente relacionadas).
  3. **Fine-tuning (descartado)**: ajuste fino de **GPT-3.5 Turbo** sobre transcripciones de entrevistas de estudiantes de Ferrari et al. [27] (70 grabaciones → 50 tras filtrado de calidad, transcritas con WhisperX + PyAnnote.audio) usando el prompt largo como system prompt (p. 5). Tres variantes: *Model A* (50 entrevistas), *Model B* (split 80/20 de las 50) y *Model C* (las 10 mejores entrevistas). *Model C* superó a *A* y *B*, pero los tres fueron inferiores a `LLMREI-short` y `LLMREI-long` sin fine-tuning (respuestas incoherentes, pérdida de foco y cambio espontáneo de idioma por ruido oral y baja pericia de los estudiantes), por lo que se excluyó de la evaluación.
- **Estado interno**: sin estado estructurado externo; depende del historial de conversación en contexto y de las instrucciones del prompt de sistema.

Prompt de sistema `LLMREI-short` (p. 3, literal):
```
You are an interviewer, called LLMREI, who assists a requirements engineer in eliciting requirements. Bombard
the stakeholder with questions about his/her business and his/her project to find out everything the stakeholder envi-
sions! Act like a real-world interviewer, so only ask one question at a time or only ask two questions if it is about
one specific topic.
```

Extracto del prompt de sistema `LLMREI-long` (p. 4, literal; el `{Interview Cookbook}` completo está en Zenodo 🔧):
```
You are an interviewer, called LLMREI, who assists a requirements engineer in eliciting requirements.
Goal: The purpose of this chat bot is to conduct comprehensive and effective requirements elicitation
interviews with stakeholders, ensuring all necessary information is gathered to support project development.
{Interview Cookbook}
Maintain professionalism throughout the interview. Adjust questions based on the stakeholder's role, education level,
and domain knowledge. Adapt questioning style to fit the flow of the stakeholder's responses. Actively listen to
differentiate between stated needs and actual needs. Let the customer create scenarios. Example: "Please visualize the
first page of your application and explain how you would interact with it step-by-step."
```

**Datos, idioma y dominio**
- **33 entrevistas simuladas con participantes humanos** (estudiantes de informática de 20 a 30 años, hablantes nativos de alemán con dominio del inglés, en dos cursos universitarios; ~30 min por sesión incluyendo lectura y cuestionario en plataforma web propia, p. 5-6).
- **2 escenarios** de ingeniería de software tomados de Ferrari et al. [26]:
  - *Salon* (peluquería y salón de uñas: citas y horarios de empleados; **8 requisitos** en el ground truth): 15 entrevistas (6 `Long`, 9 `Short`).
  - *Ski* (cadena de 3 estaciones de esquí: reservas y gestión; **12 requisitos** en el ground truth): 18 entrevistas (11 `Long`, 7 `Short`).
  - Total: **17 `Long` y 16 `Short`** (Tabla I, p. 6). *Nota*: estos mismos 33 diálogos (555 turnos) son los que ReqElicitGym reutiliza para validar su oráculo y su juez (§1.1).
- **Idioma**: previsto en **inglés**, aunque algunos participantes cambiaron espontáneamente al **alemán** durante la entrevista y GPT-4o se adaptó sin fallos (p. 6).
- **Baseline humano de comparación (RQ1)**: 18 entrevistas conducidas por estudiantes tras recibir formación basada en errores del estudio de Ferrari et al. [27] (p. 6).
- **Licencia**: el artículo tiene copyright IEEE (p. 1); el paquete de réplica está publicado en Zenodo (`10.5281/zenodo.14988928`).

**Métricas y resultados cuantitativos exactos**
- **RQ1 (Errores de entrevista, p. 6, 8)**: cuestionario de 21 tipos de error (adaptado de Bano et al. [25] / Ferrari et al. [27]) agrupados en 5 categorías (*Question Formulation*, *Question Omission*, *Order of Interview*, *Communication Skills*, *Customer Interaction*) en escala Likert 1 (*Strongly disagree* = sin error) a 5 (*Strongly agree* = error muy presente).
  - En `LLMREI-long`, el **64,23 %** de los evaluadores puntuaron 1 o 2 (ausencia de error), frente al **59,1 %** en `LLMREI-short` (p. 8).
  - Ambos bots logran un rendimiento comparable a los entrevistadores humanos entrenados y los superan en habilidades de comunicación, priorización de funcionalidades y generación de resumen final (especialmente `Long`, que incluye instrucción explícita de resumir y evita preguntas demasiado largas).
- **RQ2 (Efectividad / Recall de requisitos, p. 7, 9)**: dos revisores humanos evalúan cada requisito del ground truth (8 en *Salon*, 12 en *Ski*) sobre el resumen de la entrevista en 3 niveles: *Not elicited (1)*, *Partially elicited (2)*, *Fully elicited (3)*.
  - `LLMREI-short` obtuvo el mejor resultado: hasta **60,94 %** de requisitos completamente elicitados y **12,76 %** parcialmente elicitados (**73,7 % en total**, p. 1, 9).
  - `LLMREI-short` elicitó todos los requisitos al menos una vez en el conjunto de entrevistas, mientras que `LLMREI-long` falló en 2 requisitos del escenario *Salon* (0 % en R4 y R9 en Fig. 5, p. 9). Los requisitos mejor elicitados (R1, R2, R5 en ambos escenarios) son todos funcionales.
- **RQ3 (Adaptabilidad al contexto, Tabla II, p. 7, 9)**: clasificación manual de todas las preguntas del bot en 4 categorías:

| Categoría de pregunta | Adaptación | `Short` | `Long` |
|---|---|---|---|
| *Context-independent* (estándar fija) | Nula | 27,3 % | 28,3 % |
| *Parameterized* (plantilla con placeholder) | Baja | 12,8 % | 28,9 % |
| *Context-deepening* (profundiza respuesta previa) | Media | **44,4 %** | 32,3 % |
| *Context-enhancing* (añade ideas nuevas) | Alta | **15,3 %** | 10,4 % |
| **Suma dependiente del contexto (*deepening + enhancing*)** | Media-Alta | **59,7 %** | **42,7 %** |

- **Fallos y riesgos detectados (p. 10)**:
  - *Alucinaciones*: en una entrevista inventó una estimación de precio del proyecto sin base alguna cuando el usuario preguntó.
  - *Violación de límites de privacidad*: en una entrevista pidió el **correo electrónico** al participante para agendar una reunión de seguimiento (origen directo del guardarraíl de nuestro TFG: "nunca pedir datos personales").
  - *Parada prematura complaciente*: si el usuario expresaba falta de tiempo o interés, ambos prompts cerraban la entrevista de inmediato omitiendo pasos obligatorios (resumen final o pregunta por otros stakeholders).

**Insumo directo para ReqElicit-ES (implementación del baseline B2 en WP6)**
- El plan del TFG define **B2** como *"estilo LLMREI (zero-shot y least-to-most)"*. Como ReqElicitGym ya tiene `B0` (zero-shot básico) y el hallazgo central de LLMREI es la dualidad entre `LLMREI-short` (mayor cobertura: 73,7 % y 59,7 % de preguntas adaptativas) y `LLMREI-long` (menor tasa de errores: 64,23 % y estructura en 5 pasos con resumen), para implementar B2 en WP6 debemos:
  1. **Descargar el `{Interview Cookbook}` de Zenodo (`10.5281/zenodo.14988928`)** 🔧 para tener el texto literal de los 5 pasos de `LLMREI-long`.
  2. **Estructura algorítmica de B2 (`LLMREI-long` adaptado a español y a ReqElicitGym)**:
     - *Prompt de sistema en 3 bloques*: (a) Rol y objetivo (`LLMREI`), (b) Guía estructurada en 5 pasos (apertura/contexto → exploración del sistema actual y dominio → indagación de funcionalidades con creación de escenarios por el cliente *"Visualiza la primera página de tu aplicación y explica paso a paso cómo interactuarías con ella"* → priorización y otros stakeholders → resumen final de confirmación), y (c) Ajuste de comportamiento al perfil del stakeholder y manejo de errores.
     - *Restricción de turno*: en ReqElicitGym el protocolo exige estrictamente **1 pregunta por turno** o señal de fin (en LLMREI original se permitían hasta 2 si eran del mismo tema; en WP6 debemos forzar 1 pregunta para mantener la comparabilidad justa de IRE/TKQR/ESR con B0, B1, B3, M1 y M2).
     - *Variante opcional o ablación*: probar si el tono directivo de `LLMREI-short` (*"Bombardea al stakeholder con preguntas sobre su negocio y su proyecto para descubrir todo lo que imagina"*) explica su mayor recall frente al prompt largo, ya que `LLMREI-long` genera más preguntas parametrizadas (28,9 %) y menos de profundización (32,3 %).
  3. **Insumo para guardarraíles (WP6) y métricas (WP7/WP8)**:
     - El caso real de petición de email en LLMREI justifica e inspira la regla estricta de guardarraíl en nuestro entrevistador: prohibición explícita en prompt + filtro regex/heurístico post-generación contra solicitud de PII (email, teléfono, DNI, dirección).
     - La escala de evaluación de requisitos en 3 niveles (*Not / Partially / Fully elicited*) sirve de referencia para matizar la cobertura del sintetizador en WP7.

---

### 2.2 Requirements Elicitation Follow-Up Question Generation

**Referencia y año**
- Yuchen Shen, Anmol Singhal, Travis Breaux (Carnegie Mellon University). *Requirements Elicitation Follow-Up Question Generation.* arXiv:2507.02858v1, 03-07-2025.
- Venue: 33rd IEEE International Requirements Engineering Conference (RE 2025), Valencia, Spain (según ref. [61], p. 13).
- Código y datos: https://github.com/anmolsinghal98/Requirements-Elicitation-Follow-Up-Question-Generation (p. 5) y Zenodo https://doi.org/10.5281/zenodo.15793870 (p. 11, 13).

**Problema y fase de RE**
- **Elicitación interactiva (asistencia en tiempo real turno a turno)**: generación de preguntas de seguimiento (*follow-up questions*) a partir de las intervenciones previas del stakeholder, guiada por un catálogo de **errores comunes del entrevistador** y fundamentada conceptualmente en implicación textual direccional (*directional textual entailment*: generar una pregunta \(q\) que no se pueda responder desde la premisa \(p\) pero que derive de \(p\) para obtener información nueva \(h\), p. 2).

**Metodología / arquitectura agéntica**
- Modelo base: **`gpt-4o-2024-08-06`** con **temperatura 1,0** (para favorecer diversidad creativa en preguntas, p. 4, 6).
- **Tres estudios experimentales + un estudio lateral**:
  - **Estudio 1 ( Análisis de contexto y generación mínimamente guiada, p. 4-5)**:
    - Codificación abierta de 146 preguntas de seguimiento reales para medir cuántos turnos previos requieren como contexto y clasificar su motivación en **7 tipos de pregunta de seguimiento**: *Topic change*, *Answer probing*, *Confirmation*, *Question probing*, *Alternative-seeking*, *Preference-seeking* y *Clarification* (p. 7).
    - Generación zero-shot con *Prompt 1* (Fig. 1a) sobre 20 contextos muestreados (corregidos gramaticalmente con Grammarly), comparada contra las preguntas humanas originales.
  - **Marco sintetizado de errores del entrevistador (p. 5-6)**: revisión de 14 artículos → 28 criterios de error → selección de **14 criterios** divididos en 2 categorías críticas turno a turno:
    - *Follow-up questions (5)*: (1) *Fail to elicit tacit assumptions*, (2) *Fail to consider alternatives*, (3) *No clarification when unclear*, (4) *No clarification when contradictory*, (5) *Fail to elicit tacit knowledge*.
    - *Question framing (9)*: (6) *Ask a generic, domain-independent question*, (7) *Ask a question that is too long or articulated*, (8) *Use jargon*, (9) *Ask a technical question*, (10) *Ask a question inappropriate to user's profile*, (11) *Ask for solutions*, (12) *Ask a question that involves multiple kinds of requirements*, (13) *Ask a vague question that leads to multiple interpretations*, (14) *Ask a vague question which could infer no reasonable meaning*.
  - **Estudio 2 (Clasificación de errores con LLM-as-a-Judge, p. 6)**: sobre 30 pares `(interviewee speech, interviewer question)` × 14 criterios = **420 clasificaciones**, GPT-4o (*Prompt 2*, Fig. 1b) y un analista humano (3 años de experiencia en RE) juzgan independientemente si la pregunta comete cada error.
  - **Estudio 3 (Generación guiada por errores, p. 6-7)**: en los **128 casos** (de los 420) donde tanto GPT-4o como el analista detectaron un error, ambos redactan una pregunta alternativa que evite ese error (*Prompt 3*, Fig. 1c).
  - **Estudio lateral (Evitación simultánea de los 14 errores, §V-D, p. 10)**: se pide a GPT-4o generar una pregunta evitando simultáneamente los 14 errores sobre los 30 pares y se vuelve a pasar el clasificador (420 evaluaciones).
- **Hallazgos clave de ingeniería de prompts (§V-A, p. 9)**:
  1. **Capitalización de roles (`INTERVIEWER` e `INTERVIEWEE`)**: sin mayúsculas, GPT-4o confundía quién hablaba y atribuía mal el discurso al clasificar o generar.
  2. **Reformulación positiva de los criterios (evitar negaciones)**: como los LLM fallan con negaciones, cambiaron descripciones negativas por positivas (ej. *"a good follow-up question should consider alternatives"* en lugar de *"should not fail to consider alternatives"*).
  3. **One-shot examples en 4/14 criterios difíciles**: añadieron 1 ejemplo en *No clarification when contradictory*, *Ask technical questions*, *Ask questions inappropriate to user's profile* y *Ask for solutions* (p. 6, 9).
  4. **Instrucciones paso a paso (CoT condicional) en 9/14 criterios de clasificación**: ej. para contradicción: *"first consider if the INTERVIEWEE mentioned anything contradictory. If it does not, then the standard is met. Otherwise, look at whether the INTERVIEWER's question attempts to clarify the contradiction"* (p. 9).

Prompts literales (Fig. 1, p. 5):
```
# (a) Prompt 1: Minimally Guided Questions
You are an AI agent capable of generating context summaries. During a requirements elicitation interview
with an interviewee about how the interviewee conducts {interview domain}, the INTERVIEWEE and INTERVIEWER
have had the following conversation: {interview turns}. Generate a follow-up question that the INTERVIEWER
should ask next based on the conversation. Restrict your response to only show the follow-up question without
explanation.

# (b) Prompt 2: Classify Follow-up Questions
You are an AI agent capable of conducting requirements elicitation interviews. During a requirements elicitation
interview with an interviewee about how the interviewee conducts {domain keyword}, the INTERVIEWEE said
'{interviewee speech}'. Then the INTERVIEWER asked a follow up question by saying '{interviewer question}'.
Standard: {mistake criterion}. Please classify based solely on whether the INTERVIEWER's response meets
this specific standard, and refrain from using any other standards related to follow up questions when
you classify. If the INTERVIEWER's response meets this standard, output 'Yes', otherwise output 'No'. Restrict
your response to output only 'Yes' or 'No' without explanations.

# (c) Prompt 3: Generate Mistake-Guided Questions
You are an AI agent capable of conducting requirements elicitation interviews. During a requirements elicitation
interview with an interviewee about how the interviewee conducts {domain keyword}, the INTERVIEWEE said
'{interviewee speech}'. Generate a follow-up question that meets the following criterion based ONLY on what the
INTERVIEWEE said, and restrict your response to only show the follow-up question without explanation. Criterion:
{mistake criterion}
```

**Datos, idioma y dominio**
- **14 entrevistas reales** de 20 minutos por Zoom (aprobadas por IRB, con consentimiento informado y anonimización; participantes pagados con 25 $), realizadas por 4 entrevistadores contratados con ≥ 2 años de experiencia industrial en ingeniería de software y entrenados con el curso de Ferrari et al. [21] (p. 3-4).
- **Dominio**: servicios de directorio web/móvil en **4 subdominios** (*apartment finding*, *restaurant finding*, *hiking trail finding*, *health clinic finding*), centrados en elicitar preferencias de usuario (requisitos no funcionales, p. 3).
- De las 14 transcripciones se extrajeron **146 contextos de preguntas de seguimiento** (*turn context dataset*, p. 4) y una muestra aleatoria de **30 pares** para los Estudios 2 y 3 (p. 6).
- **Evaluadores humanos (Prolific, EE. UU., hablantes nativos de inglés, 6 $ por encuesta)**: 128 participantes en Estudio 1 (64 grupo GPT-4o, 64 grupo humano) y 32 participantes en Estudio 3 (4 pares por encuesta = 128 pares evaluados).
- **Idioma**: inglés. **Licencia**: código en GitHub y paquete de datos en Zenodo (`10.5281/zenodo.15793870`).

**Métricas y resultados cuantitativos exactos**
- **RQ1 (Contexto necesario y tipología de preguntas, Fig. 2, p. 7-8)**:
  - Turnos previos necesarios sobre 146 preguntas: **71/146 (48,6 %)** requieren **0 turnos** previos (*Topic change*); **33/146 (22,6 %)** requieren **1 turno** (acumulado ≤ 1 turno: **104/146 = 71,2 %**); 26 requieren 2 turnos; 11 requieren 3 turnos; 3 requieren 4 turnos (**98,6 % = 144/146 requieren ≤ 4 turnos**); 1 requiere 5 y 1 requiere 6. Media ≈ 1 turno.
  - Frecuencia por tipo de pregunta (Fig. 2b, p. 8): *Topic change* 71, *Answer probing* 27, *Confirmation* 13, *Question probing* 13, *Alternatives* 11, *Preference* 6, *Clarification* 5 (Total = 146).
  - Relación tipo ↔ ventana de contexto: *Topic change* requiere 0 turnos; *Answer probing*, *Confirmation* y *Clarification* requieren principalmente 1 turno; *Question probing*, *Alternative-seeking* y *Preference-seeking* requieren ≥ 2 turnos (p. 8).
- **RQ2 (Generación mínimamente guiada vs. Humanos, Tabla Ia, p. 8; escala 1-6, t-test bilateral)**:
  - *Informativeness*: Humano 4,6 vs. GPT-4o **4,8** ($p = 0{,}17$).
  - *Relevancy*: Humano 4,8 vs. GPT-4o **5,0** ($p = 0{,}08$).
  - *Clarity*: Humano 4,9 vs. GPT-4o **5,1** ($p = 0{,}10$).
  - Sin diferencias estadísticamente significativas ($p > 0{,}05$): GPT-4o es equiparable a entrevistadores humanos entrenados.
- **RQ3 y Estudio Lateral (Clasificación y evitación simultánea por tipo de error, Tabla Ib, p. 8, 10)**:
  - Acuerdo global GPT-4o vs. analista humano en las 420 clasificaciones: **81,0 % (340/420)** (humano detectó error en 177/420; GPT-4o en 163/420; coincidieron en presencia de error en 128 casos).
  - Al pedir evitar los 14 errores a la vez (estudio lateral), GPT-4o evitó el error en **84,3 % (354/420)** de las verificaciones (solo 66/420 fallos); **28/30 preguntas evitaron ≥ 11 de los 14 errores**, aunque solo **1/30 evitó los 14 simultáneamente** (en *Fail to consider alternatives* la tasa de evitación cae al **26,7 %**).

| Tipo de error (14 criterios) | Humano (/30) | GPT-4o (/30) | Acuerdo (RQ3) | Tasa de evitación simultánea (§V-D) |
|---|---|---|---|---|
| *Fail to elicit tacit assumptions* | 19 | 25 | 66,7 % | 76,7 % |
| *Fail to consider alternatives* | 30 | 28 | 93,3 % | **26,7 %** |
| *No clarification when unclear* | 20 | 16 | 60,0 % | 70,0 % |
| *No clarification when contradictory* | 7 | 2 | 83,3 % | 83,3 % |
| *Fail to elicit tacit knowledge* | 21 | 20 | 70,0 % | 90,0 % |
| *Ask a generic, domain-independent question* | 7 | 10 | 90,0 % | 96,7 % |
| *Ask a question that is too long or articulated* | 11 | 7 | 86,7 % | 90,0 % |
| *Use jargon* | 7 | 1 | 80,0 % | 100,0 % |
| *Ask a technical question* | 5 | 1 | 86,7 % | 100,0 % |
| *Ask a question inappropriate to user's profile* | 5 | 0 | 83,3 % | 100,0 % |
| *Ask for solutions* | 6 | 2 | 86,7 % | 100,0 % |
| *Ask a question that involves multiple kinds of requirements* | 7 | 12 | 76,7 % | 60,0 % |
| *Ask a vague question that leads to multiple interpretations* | 27 | 27 | 93,3 % | 93,3 % |
| *Ask a vague question which could infer no reasonable meaning* | 5 | 12 | 76,7 % | 93,3 % |
| **Total / Global** | **177** | **163** | **81,0 %** | **84,3 %** |

- **RQ4 (Generación guiada por errores vs. Analista humano en 128 pares, Tabla Ic, p. 8-9)**:
  - **Evitación del error**: los evaluadores eligieron la pregunta de GPT-4o en **87/128 pares (68,0 %)** frente a 41/128 del analista humano. Modelo Bradley-Terry de efectos mixtos: $p = 4{,}23 \times 10^{-8}$, odds ratio = 2,662. ⚠️ El texto calcula `2.662 / (1 + 2.662) = 93.5%`, pero aritméticamente $2{,}662 / 3{,}662 = 72{,}7\,\%$ (error de cálculo en el artículo).
  - **Calidad según máximas de Grice** (escala 1-5, regresión logística ordinal de efectos mixtos):

| Métrica | Media Humano | Media GPT-4o | Win Rate Humano | Win Rate GPT-4o | Empates (Tie) | p-valor |
|---|---|---|---|---|---|---|
| *Relevancy* | 3,5 | **4,4** | 21,1 % | **59,4 %** | 19,5 % | $1{,}21 \times 10^{-10}$ |
| *Clarity* | 3,9 | **4,5** | 17,2 % | **42,2 %** | 40,6 % | $1{,}34 \times 10^{-6}$ |
| *Informativeness* | 3,6 | **4,1** | 25,8 % | **47,7 %** | 26,6 % | $1{,}77 \times 10^{-5}$ |

**Insumo directo para ReqElicit-ES (implementación del baseline B3 y mejoras para M1 en WP6)**
- El plan del TFG define **B3** como *"preguntas guiadas por tipos de error del entrevistador, como en el trabajo de preguntas de seguimiento"*. Este artículo da toda la especificación técnica para implementarlo en WP6:
  1. **Por qué no basta meter los 14 criterios de golpe en un solo prompt**: el estudio lateral (§V-D) demuestra que al pedir los 14 criterios simultáneamente en un prompt estático, criterios clave de indagación como *considerar alternativas* caen al 26,7 % de cumplimiento y *una sola clase de requisito por pregunta* cae al 60,0 %. Sin embargo, el propio artículo sugiere en trabajo futuro (§VII, p. 11) usar bucles reflexivos (*reflective loops*) donde un LLM evalúe y corrija la pregunta generada.
  2. **Lógica algorítmica exacta de B3 en nuestro entorno multi-turno (WP6)**:
     - **Entrada de contexto**: pasar los **últimos 4 turnos de diálogo** (`INTERVIEWER` e `INTERVIEWEE` en **MAYÚSCULAS**), que según RQ1 cubren el **98,6 %** de las dependencias contextuales, además del requisito inicial del escenario.
     - **Reglas de formato fijas en positiva (Question Framing)**: integrar en el prompt de generación los 9 criterios de formulación redactados **en positivo** (1. específica del dominio; 2. concisa y directa; 3. vocabulario cotidiano sin jerga; 4. centrada en necesidades de usuario y no en implementación técnica; 5. adaptada al perfil del cliente; 6. preguntar qué necesita el usuario y nunca pedirle que diseñe la solución técnica; 7. abordar **un único requisito o aspecto** por pregunta; 8. unívoca; 9. con contexto suficiente para entenderse por sí sola).
     - **Selección / guía por los 5 criterios de seguimiento (Follow-up Criteria)**: basándose en la última respuesta del `INTERVIEWEE`:
       - Si la respuesta es ambigua o vaga → aplicar criterio *Clarify unclear words* (conecta con perfil **Vago** en RQ3).
       - Si la respuesta contradice algo dicho antes → aplicar criterio *Clarify contradiction* (conecta directamente con perfil **Contradictorio** en RQ3).
       - Si no hay ambigüedad ni contradicción → aplicar criterios de indagación: *Elicit tacit knowledge*, *Justify tacit assumptions* o *Explore alternatives*.
     - **Dos modos de ejecución posibles para B3 (a decidir en WP6)**:
       - *B3-SingleCall (1 llamada por turno, igual coste que B0)*: el prompt pide elegir cuál de los 5 estándares positivos de seguimiento aplica al último turno del `INTERVIEWEE` y emitir directamente la pregunta que cumple ese estándar y las reglas de encuadre.
       - *B3-Reflective (generate-classify-rewrite)*: genera pregunta candidata → verifica con *Prompt 2* (clasificador rápido) si viola algún criterio crítico → si falla, regenera con *Prompt 3* indicando el criterio específico.
  3. **Insumo directo para nuestro agente principal M1 (WP6)**:
     - La distinción empírica entre preguntas que dependen de 1 turno (*Answer probing*, *Clarification*, *Confirmation*) y las que requieren ≥ 2 turnos o 0 turnos (*Topic change*, *Question probing*, *Preference-seeking*) fundamenta el **planificador clarificar/indagar de M1**: `clarify` opera localmente sobre el último turno del cliente, mientras que `probe` consulta el **estado estructurado por dimensiones** para hacer *Topic change* hacia dimensiones aún vacías (como **Estilo**).

---

### 2.3 GPT-Powered Elicitation Interview Script Generator

**Referencia y año**
- Binnur Görer (Microsoft, Estambul) y Fatma Başak Aydemir (Utrecht University). *GPT-Powered Elicitation Interview Script Generator for Requirements Engineering Training.* arXiv:2406.11439v1, 17-06-2024.
- Venue: preprint en arXiv (extensión de su trabajo previo en REW 2023 [8] sobre generación de guiones con errores intencionados).
- Archivos de conocimiento y enlaces a las cadenas de prompts: https://doi.org/10.6084/m9.figshare.25193657 (p. 3, 4).

**Problema y fase de RE**
- **Preparación y formación en elicitación (generación offline de guiones completos)**: genera guiones largos de entrevistas de elicitación libres de errores para entrenar a estudiantes de ingeniería de requisitos, usando un único agente GPT-4 que escribe ambos lados del diálogo (entrevistador y stakeholder).

**Metodología / arquitectura agéntica**
- **Modelo base**: **Custom GPT (GPT-4)** en ChatGPT con inyección de conocimiento tipo RAG en contexto (*Knowledge files* + *Custom instructions*, Fig. 1, p. 3).
- **Base de conocimiento inyectada (3 recursos, p. 3-4)**:
  1. *General guidelines for interviewer's questions*: estrategia metódica (preguntas claras y directas, adaptación al stakeholder, preguntas de seguimiento ante respuestas ambiguas, transiciones suaves).
  2. *Common pitfalls to avoid*: errores típicos de Bano et al. [3] a evitar (dirigir al stakeholder, usar jerga técnica, falta de claridad).
  3. *Interview script sample (1-shot estructural)*: guion real simulado de Spijkman et al. [35] (portal para la *International Football Association*), editado para unir 2 analistas en 1 solo (**114 intercambios**, longitud media de 37 palabras/turno el analista y 49,3 palabras/turno el stakeholder).
- **Encadenamiento de prompts basado en esquema (*Outline-based Prompt Chaining*, Fig. 2, p. 4-5)** para superar el límite de tokens de salida y evitar pérdida de coherencia:
  - *Paso 1 (Outline generation)*: prompt inicial pidiendo un esquema de alto nivel para la entrevista (solo títulos de secciones, p. ej., `1. Introduction`, `2. Background Information Gathering`, `3. Feature 1...`, ..., `9. Conclusion`).
  - *Paso 2 (Section-by-section generation)*: llamadas sucesivas en la misma sesión (`Please generate the interview script for 1. Introduction`, etc.) y concatenación final.
- **Separación de roles**: **No separa roles en ejecución**; un solo LLM genera el diálogo completo de ambos interlocutores a la vez (los autores reconocen esto como limitación principal y proponen en §V separar LLMs de entrevistador y entrevistado con *personas*, p. 7).

**Datos, idioma y dominio**
- **4 guiones de entrevista generados** en **inglés** para 4 dominios de aplicación (Tabla I, p. 4-5):
  - *S1*: sistema programador de reuniones (*meeting scheduler*; 35 actos del entrevistador: 10 no-pregunta [NQ] y 25 preguntas [Q]; 34 NQ del stakeholder).
  - *S2*: aplicación de vivienda social (*social housing*; 8 NQ + 25 Q del entrevistador; 33 NQ del stakeholder).
  - *S3*: aplicación de seguimiento de salud digital (*digital health tracking*; 11 NQ + 44 Q del entrevistador; 55 NQ del stakeholder).
  - *S4*: aplicación de reparto de comida (*food delivery*; 1 NQ + 26 Q del entrevistador; 27 NQ del stakeholder).
- **Licencia**: materiales públicos en Figshare (`10.6084/m9.figshare.25193657`).

**Métricas y resultados cuantitativos exactos**
- **Evaluación automática de calidad lingüística con GRUEN** (rango $[0, 1]$, evalúa gramaticalidad, no redundancia, foco y coherencia sin referencia; Tabla II, p. 6):

| Escenario | Turnos Entrevistador (media ± std) | Turnos Stakeholder (media ± std) | Todos los turnos (media ± std) |
|---|---|---|---|
| S1 (Meeting scheduler) | 0,81 ± 0,05 | 0,77 ± 0,05 | **0,79 ± 0,06** |
| S2 (Social housing) | 0,79 ± 0,05 | 0,82 ± 0,03 | **0,81 ± 0,04** |
| S3 (Health tracking) | 0,82 ± 0,04 | 0,79 ± 0,05 | **0,81 ± 0,05** |
| S4 (Food delivery) | 0,80 ± 0,05 | 0,79 ± 0,05 | **0,79 ± 0,05** |

- **Estudio de juicio experto** (1 experto con > 7 años enseñando RE y > 5 años de colaboración industrial; escalas de 1 a 5; Tablas III y IV, p. 6-7):
  - *Calidad de lenguaje natural (Tabla III)*: **Naturalness = 4**, **Coherence = 4**, **Completeness = 3** (idéntico en S1, S2, S3 y S4).
  - *Rúbrica de entrevista de RE de Lending et al. [44] (Tabla IV)*:
    - *Greeting*: 2 (S1), 3 (S2, S3, S4).
    - *Opening*: 3 (S1, S2, S3), 4 (S4).
    - *Analyze Current State "As Is"*: 3 (en los 4).
    - *Design "To Be" System*: 3 (en los 4).
    - *Closing* (resumen + aprobación del stakeholder): **4** (S1, S2, S3), 3 (S4).
    - *Active Listening*: 2 (S1), 3 (S2, S3, S4).
  - *Defectos críticos detectados por el experto (p. 6-7)*:
    1. **Falta de descubrimiento real (*influencing stakeholder*)**: como un único LLM genera ambos roles a partir de las 3 funcionalidades dadas en el prompt inicial, las funcionalidades parecen predeterminadas desde el inicio y no se descubren requisitos nuevos ni se profundiza en NFRs (p. ej., se menciona privacidad pero no se indaga cómo resolverla; en vivienda social S2 se omite la equidad/*fairness*).
    2. **Stakeholder irrealmente cooperativo**: en todos los guiones el cliente responde siempre de forma extensa y colaboradora ( mediana de 28 a 50 palabras/turno y 0 preguntas hechas por el stakeholder en la Tabla I).
    3. **Ignorar a otros stakeholders**: en ningún guion el entrevistador pregunta por otros actores o interesados adicionales.
    4. **Marcas artificiales del encadenamiento**: el entrevistador dice frases como *"the next section"*, poco naturales en conversación oral.

**Insumo directo para ReqElicit-ES**
- **Justificación metodológica directa para WP5 y WP6**:
  1. Demuestra empíricamente por qué **no se debe simular una entrevista con un solo LLM ni dando al entrevistador las funcionalidades por adelantado**: produce el sesgo de *influencing stakeholder* y evita el descubrimiento genuino. Esto respalda la arquitectura de separación estricta de ReqElicit-ES (Entrevistador ciego a los implícitos ↔ Oráculo con estado oculto ↔ Juez independiente).
  2. La crítica del experto de que el stakeholder generado por GPT-4 es *"very cooperative in all cases, which may not always be the case in an interview"* (p. 6) y la propuesta futura de los autores de separar agentes con distintas *personas* (p. 7) respaldan directamente nuestra **RQ3 y los 5 perfiles de cliente del WP5** (Colaborador, Vago, Divagante, Contradictorio, No técnico).
  3. **Insumo para M1 y M2 (WP6)**:
     - El esquema de entrevista (*Outline*: Introducción → Contexto y sistema actual "As-Is" → Sistema futuro "To-Be" por áreas → Cierre con **resumen y confirmación explícita del cliente**, que obtuvo la mejor nota del experto: 4/5) respalda el módulo de **resumen y confirmación de nuestro agente M2**.
     - El fallo sistemático de *"ignoring other stakeholders"* justifica que la primera dimensión del estado estructurado de **M1** sea explícitamente **`actores` (stakeholders y roles de usuario)**, además de incluir una sub-dimensión de NFRs (privacidad, restricciones) donde los guiones quedaron en 3/5 de completitud.

---

## Lote 3

### 3.1 Elicitron

**Referencia y año**
- Mohammadmehdi Ataei, Hyunmin Cheong, Daniele Grandi, Ye Wang, Nigel Morris, Alexander Tessier (Autodesk Research). *Elicitron: An LLM Agent-Based Simulation Framework for Design Requirements Elicitation.* arXiv:2404.16045v1, 04-04-2024.
- Venue: preprint de arXiv (publicado posteriormente en *Proceedings of the ASME 2024 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference (IDETC-CIE)*, vol. 88377, p. V03BT03A056, 2024).
- Código y datos: no se publica enlace a repositorio ni paquete de replicación.

**Problema y fase de RE**
- **Simulación de stakeholders diversos y *Empathic Lead Users* (ELUs)** combinada con **entrevista automatizada** y **clasificación automática post-entrevista de necesidades latentes (*latent needs*)** para diseño de producto e ingeniería de requisitos temprana.

**Metodología / arquitectura agéntica**
- **Modelo base y embeddings**: **`GPT-4-Turbo`** de OpenAI (coste reportado en §7: 10 USD / 1M tokens de entrada y 30 USD / 1M tokens de salida; el Experimento 2 completo consumió ~80.000 tokens y ~2,4 USD, p. 4, 9) y **`text-embedding-ada-002`** para representaciones vectoriales (p. 3-4). Todas las salidas del LLM se fuerzan mediante esquemas **Pydantic** con validación estructural (p. 3).
- **Pipeline secuencial en 4 etapas (Fig. 1, p. 2-4)**:
  1. **Etapa 1 — Generación de agentes usuario (*Agent Generation*, §3.1, p. 3)**:
     - Para cada agente, el LLM genera una tupla estructurada de 3 campos:
       - `Name`: etiqueta identificativa del rol de usuario.
       - `Description`: descripción detallada de las características, contexto y limitaciones del usuario.
       - `Reasoning Chain`: justificación paso a paso (inspirada en *Chain-of-Thought*, CoT) de por qué se crea este agente para el problema de diseño.
     - Compara **3 métodos de generación** para producir $N = 20$ agentes:
       - *Parallel*: $N$ llamadas independientes en paralelo (rápido, pero sin memoria de los otros agentes generados, lo que reduce la diversidad).
       - *Parallel + KMeans filtering*: sobregeneración en paralelo → cálculo de embeddings $v_i$ sobre las descripciones con `text-embedding-ada-002` → clustering `KMeans(V, k)` eligiendo $k$ según el *silhouette score* → selección de 1 agente representante por clúster.
       - *Serial (context-aware)*: generación secuencial en un mismo contexto donde los agentes previamente generados permanecen en la ventana del LLM para evitar repeticiones y maximizar la cobertura del espacio de diseño (limitado por el tope de ~4.096 tokens de salida a ~20 agentes por llamada, p. 3).
     - **Steering Prompt para *Empathic Lead Users* (Condición 2 del Experimento 2, §5.1, p. 6)**: añade al método *Serial* una instrucción de desvío respecto a una descripción literal de usuario típico tomada de Lin y Seepersad [6]:
       > `You must create non-typical users based on the following description of a typical user: "The typical user would be a weekend camper, 15-30 years old, with very good health and physical fitness, who camps a few times a year. The typical usage environment would be a public park or wilderness area, in a generally wooded or grassy environment with warm, sunny weather."`
  2. **Etapa 2 — Generación de experiencia de producto (*Product Experience Generation*, §3.2, p. 4, 7-8)**:
     - Antes de la entrevista, se pide a cada agente que simule («alucine») libremente varios pasos de interacción con el producto (montaje, uso de funciones, recogida, resolución de problemas).
     - Cada paso de interacción se estructura obligatoriamente en **3 elementos tipo CoT**:
       - `Action`: paso de interacción ejecutado (p. ej., *"Attempted to grasp the zipper of the tent's entrance with limited finger dexterity"*, p. 7).
       - `Observation`: percepción y puntos de fricción observados (p. ej., *"The zipper was too small and lacked grip..."*).
       - `Challenge`: obstáculo o dolor explícito (p. ej., *"Faced significant struggle to open and close the tent, leading to frustration"*).
  3. **Etapa 3 — Entrevista contextualizada al agente (*Agent Interview*, §3.3 y §5.1, p. 4, 6)**:
     - Se formulan secuencialmente **12 preguntas** (replicadas del estudio humano de Lin y Seepersad [6]) manteniendo en el contexto del agente su `Description`, sus pasos `(Action, Observation, Challenge)` y las respuestas previas:
       - *1 pregunta abierta (Free style)*: `"If you were to purchase an ideal tent, what main characteristics would you look for?"`
       - *11 preguntas por categoría (Categorical)*: `"Focusing specifically on the [category], aspect of tent, can you tell me your needs and any innovative insights to address those needs?"` para las 11 categorías: `size, shape, weight, material, safety, durability, aesthetics, ergonomics, cost, setup, transport`.
  4. **Etapa 4 — Identificación automática de necesidades latentes (*Latent Needs Identification*, §3.4 y §6, p. 4, 8-10)**:
     - Evalúa a `GPT-4-Turbo` como clasificador binario (`True` / `False` a la pregunta `"Is this a latent need?"`) bajo **3 variantes de prompt** (p. 8):
       1. *Zero-shot Detection*: sin definición ni criterios adicionales.
       2. *Detection with Latent Needs Criteria*: inyecta los 2 criterios de necesidad latente de Lin y Seepersad [6] usados también por los evaluadores humanos:
          > `"Label the reported customer need as a latent need (latent = True) if either of the following conditions is met: (a) The need represents a significant change to the product design and does not fall into any of the following categories: size, shape, weight, material, safety, durability, aesthetics, ergonomics, cost, setup, or transport. (b) The need reflects an exceptionally innovative and clearly expressed insight regarding the product and/or how it is used."`
       3. *Detection with Latent Needs Criteria and Chain-of-Thought*: exige razonar paso a paso aplicando (a) y (b) antes de emitir la respuesta binaria `True`/`False`.

**Datos, idioma y dominio**
- **Dominio e idioma**: diseño de una **tienda de campaña (*camping tent*)** en **inglés**, replicando el caso de estudio clásico de Lin y Seepersad [6] (p. 5-6).
- **Volumen de datos por experimento**:
  - *Experimento 1 (Diversidad)*: **60 agentes sintéticos** (20 *Serial*, 20 *Parallel*, 20 *Parallel + filtering*) × 13 textos embebidos por agente (1 descripción de rol + 12 respuestas de entrevista = **780 embeddings**, p. 4).
  - *Experimento 2 (Descubrimiento de necesidades latentes)*: **60 agentes entrevistados** ($20 \times 3$ condiciones: Condición 1 *Automatic Serial*, Condición 2 *Automatic Serial + Steering Prompt*, Condición 3 *Manual ELUs* listados en la Tabla 3, p. 6), comparados contra los 20 sujetos humanos de [6]. Dos evaluadores humanos etiquetaron las necesidades latentes (10 % calibración conjunta, 20 % cálculo de acuerdo inter-anotador y 70 % dividido al 50 % entre ambos), logrando un acuerdo **$F_1 = 0,83$** ($tp = 109, fp = 21, fn = 24$, p. 6-7).
  - *Experimento 3 (Clasificación automática de necesidades latentes)*: dataset equilibrado de **40 necesidades** (20 latentes y 20 no latentes validadas por los expertos en el Exp. 2, p. 8).

**Métricas y resultados cuantitativos exactos**
- **Experimento 1 — Diversidad computacional y cualitativa de usuarios y respuestas (Tablas 1 y 2, Figs. 2 y 3, p. 5-6)**:

| Métrica de diversidad (normalizada en $[0, 1]$) | Serial (Context-Aware) | Parallel | Parallel + KMeans filtering |
|---|---|---|---|
| **Volumen de la envolvente convexa (*Convex Hull Volume*)** — Media (Rol + 12 preg.) ↑ | **0,867965** | 0,267249 | 0,363448 |
| *Convex Hull Volume* — Solo descripción de usuario (*User Characteristics*) ↑ | **0,991878** | 0,097886 | 0,081218 |
| **Distancia media al centroide (*Mean Distance to Centroid*)** — Media ↑ | **0,620052** | 0,547026 | 0,561611 |
| *Mean Distance to Centroid* — Solo descripción de usuario ↑ | **0,660156** | 0,527555 | 0,534677 |
| **Silhouette Score ($k \in [2, 6]$)** ↓ (menor = menos agrupable = más diverso) | **~0,04 – 0,06 (mínimo)** | ~0,11 – 0,16 | ~0,11 – 0,15 |

  - *Cobertura temática ($k = 4$ clústeres en t-SNE, Fig. 2, p. 5)*: al agrupar los 60 agentes en 4 temas (*1: Service and Conservation*, *2: Outdoor Recreation and Camping*, *3: Adventure and Exploration*, *4: Family Camping and Outdoor Activities*), tanto *Parallel* como *Parallel + filtering* **omitieron por completo el Grupo 1** (personal militar, ayuda humanitaria, investigadores de campo), mientras que *Serial* cubrió los 4 grupos.
- **Experimento 2 — Número medio de necesidades latentes descubiertas por agente ($n = 20$ por condición, Fig. 4, p. 6-7)**:
  - **Condición 3 (ELUs creados manualmente)**: **$M = 10,875, SD = 2,322$**.
  - **Condición 2 (Serial automático + *Steering Prompt*)**: **$M = 9,875, SD = 3,304$** (diferencia **no estadísticamente significativa** frente a la Condición 3 manual, lo que demuestra que el *steering prompt* evita tener que diseñar perfiles ELU a mano, p. 7).
  - **Condición 1 (Serial automático sin *steering*)**: **$M = 8,825, SD = 3,201$** (diferencia estadísticamente significativa frente a Condición 3: **$t(38) = 2,318, p < 0,05$**, porque perfiles como *High School Teacher* o *Eco-Tourism Entrepreneur* son distintos pero no sufren condiciones extremas de uso: solo generaron 4 y 3 necesidades latentes respectivamente, p. 7).
  - Las tres condiciones superan ampliamente la línea base humana de Lin y Seepersad [6] (~4,2 necesidades latentes de media en la Fig. 4, p. 7).
- **Experimento 3 — Detección automática de necesidades latentes por el LLM (40 casos; Tabla 4 y Fig. 5, p. 8-10)**:

| Configuración del clasificador LLM | Precisión | Recall | F1-score |
|---|---|---|---|
| (1) *Zero-Shot* | 0,7273 | 0,8000 | 0,7619 |
| (2) *With Latent Needs Criteria* | **1,0000** | 0,8500 | 0,9189 |
| (3) *With Latent Needs Criteria + Chain-of-Thought (CoT)* | **0,9500** | **0,9500** | **0,9500** |

**Insumo directo para ReqElicit-ES**
- **Parametrización de nuestros 5 perfiles de cliente en WP5 (`Colaborador`, `Vago`, `Divagante`, `Contradictorio`, `No técnico`)**:
  1. *Separación entre estado de conocimiento y estilo conductual mediante Steering Prompts*: en Elicitron el diseño es abierto (cada agente inventa sus necesidades), mientras que en **ReqElicit-ES** los requisitos implícitos (`Implicit Requirements`) de cada escenario están **fijados por el benchmark (WP3)** para poder medir el *Recall* con exactitud. Adaptamos el esquema de Elicitron dotando al simulador de cliente (WP5) de una estructura en **3 bloques**:
     - **Identidad y contexto operativo (`Name` + `Description`)**: rol del stakeholder en el dominio español del escenario.
     - **Experiencia vivida pre-estructurada (`Action`, `Observation`, `Challenge`)**: anclada a los requisitos implícitos ocultos del escenario, de modo que el cliente tenga puntos de fricción concretos cuando piensa desde su experiencia cotidiana.
     - **Steering Prompt conductual (ortogonal a los requisitos implícitos)** para instanciar los **5 perfiles de RQ3 en WP5**:
       - **`Colaborador`** (*typical cooperative user*): responde con claridad, foco y nivel de detalle completo cuando la pregunta del entrevistador apunta a la dimensión de un requisito implícito, sin regalar requisitos de dimensiones no preguntadas.
       - **`Vago`** (*under-specified / minimal articulateness*): en la primera pregunta sobre un área, responde de forma escueta, genérica o abstracta (p. ej., *"que sea rápido y sencillo"*, *"lo habitual"*), liberando el requisito implícito completo **solo** si el entrevistador realiza una pregunta de seguimiento (*probing / follow-up*) que pida concreción o ejemplos.
       - **`Divagante`** (*tangential / narrative-heavy*): envuelve la información relevante dentro de anécdotas operativas extensas (`Action` y `Observation` accesorias sobre su día a día), obligando al entrevistador a filtrar el ruido y reconducir el foco.
       - **`Contradictorio`** (*shifting / internally inconsistent*): introduce inicialmente una preferencia o restricción que entra en tensión con otro requisito del escenario (o matiza/cambia de opinión entre dos turnos), exigiendo que el entrevistador (como hace el detector de inconsistencias de **M2**) detecte el conflicto y pida aclaración explícita para fijar el requisito verdadero.
       - **`No técnico`** (*experience-only / zero software jargon*, inspirado directamente en los pasos `Action → Observation → Challenge` de Elicitron): tiene prohibido usar términos de ingeniería de software (tablas, base de datos, API, autenticación, responsive, endpoints, etc.) y expresa todos los requisitos implícitos únicamente como dificultades prácticas (`Challenges`) y deseos de uso en lenguaje llano.
  2. *Generación en serie (`Serial`) para poblar matices de rol en WP3*: si se generan descripciones de personajes para los escenarios de ReqElicit-ES, se hará manteniendo en contexto los personajes previos (*serial generation*) para evitar el colapso de diversidad demostrado en el Experimento 1 (`Convex Hull = 0,868` en serie vs. `0,267` en paralelo).
  3. *Regla de diseño para el Juez (WP5) y el Sintetizador (WP7)*: el Experimento 3 demuestra que pasar de *Zero-Shot* a *Criterios explícitos + CoT* eleva el $F_1$ de **0,7619 a 0,9500** reduciendo drásticamente tanto falsos positivos como falsos negativos. Tanto el Juez de WP5 como el Sintetizador de WP7 incluirán definiciones operativas explícitas de qué constituye (y qué no constituye) un requisito válido junto con un paso de razonamiento previo (`reasoning`).

---

### 3.2 Generative Goal Modeling

**Referencia y año**
- Ateeq Sharfuddin, Travis Breaux (School of Computer Science, Carnegie Mellon University). *Generative Goal Modeling.* arXiv:2509.01048v1, 01-09-2025.
- Venue: publicado en *2025 IEEE 33rd International Requirements Engineering Conference (RE)*, pp. 92–103, doi: `10.1109/RE63999.2025.00019` (según consta en la referencia [10] de Sivakumar et al., 2026).
- Código, transcripciones, notebooks y scripts: https://github.com/cmu-relab/goalgeneration (p. 10).

**Problema y fase de RE**
- **Extracción post-entrevista de objetivos (*goals*) con trazabilidad literal a frases del diálogo** y **generación automática de modelos de objetivos (*goal models* con relaciones de refinamiento e inferencia de objetivos implícitos de alto nivel)** a partir de transcripciones de entrevistas abiertas de elicitación.

**Metodología / arquitectura agéntica**
- **Modelo base y parámetros**: **`gpt-4o-2024-08-06`** con **`temperature = 1.0`** (p. 2), combinado con **`paraphrase-MiniLM-L6-v2`** (*Sentence-Transformers*) y `AgglomerativeClustering` de `scikit-learn v1.6.1` (p. 4).
- **Pipeline en 3 etapas con muestreo repetido ($\times 10$) (Fig. 1, p. 1, 3-6)**:
  1. **Etapa 1 — Extracción de objetivos y trazabilidad al texto fuente en 2 pasos (§III-B, p. 3-4)**:
     - Para evitar el sesgo posicional (*lost in the middle* / *leading bias* de Liu et al. [22] y Ravaut et al. [23]) y capturar objetivos co-construidos entre entrevistador y stakeholder a lo largo de varios turnos, compara dos estrategias de ventana:
       - `whole`: pasar la transcripción entera de una sola vez.
       - `moving`: **ventana deslizante de 4 turnos con incremento (*stride*) de 2 turnos** (evaluada en variante general `-G`, que prohíbe mencionar nombres de productos/servicios, y variante específica `-S`, p. 3, 8).
     - *System prompt común para los Prompts #1 y #2 (p. 4)*:
       > `"You are a business analyst collecting requirements for a software application. Your job is to review interview transcripts between an interviewer who is a business analyst and a stakeholder who is a prospective user of the application. The interviewer will ask the stakeholder questions to identify their requirements for the application."`
     - *Paso 1a — Prompt 1 (Extracción de objetivos en JSON, Fig. 3, p. 4)*:
       > `Read the following interview transcript excerpt and respond with any goals that the speaker expresses. A goal describes a prescriptive statement of intent that the system should satisfy through the cooperating of its agents. Write goals in general terms and do not include references to applications, products or services in the goal statement. Only write goals that can be traced to specific phrases in the speech. Respond with the goals in a JSON list of strings.`
     - *Paso 1b — Prompt 2 (Trazabilidad a subcadenas exactas del diálogo, Fig. 4, p. 4)*:
       > `Read the following the goals in JSON format and identify the substrings in the interview transcript excerpt from which the goals were generated. Respond in JSON using the format {"goal": "goal statement", "phrases": ["phrase1", "phrase2"]}`
       *(Los autores probaron métricas de similitud semántica para trazar objetivos al texto fuente, pero concluyeron que el Prompt #2 con GPT-4o era muy superior, p. 4).*
     - Se ejecuta **10 veces** por transcripción a $T = 1,0$ para aumentar la cobertura de objetivos ante la variabilidad del muestreo (p. 1, 4, 8).
  2. **Etapa 2 — Deduplicación mediante Clustering Aglomerativo (§III-C, p. 4-5, 8-9)**:
     - Agrupa todos los objetivos extraídos en las 10 repeticiones calculando la distancia euclídea entre sus embeddings (`paraphrase-MiniLM-L6-v2`) mediante `AgglomerativeClustering(metric='euclidean', linkage='ward', distance_threshold=1.5)`.
     - Selecciona aleatoriamente **1 objetivo representante de cada clúster** para pasar a la etapa siguiente (~80 % de los clústeres contienen paráfrasis de un único objetivo; p. ej., en la Transcripción #32, 20 de 22 clústeres eran homogéneos y solo 2 mezclaban objetivos distintos por detenerse el algoritmo en el umbral de distancia, p. 4, 8-9).
  3. **Etapa 3 — Construcción del Modelo de Objetivos mediante PAL (*Program-Aided Language model*) + *Plan-and-Solve Prompting* (§III-D, Figs. 6–9, p. 5-7)**:
     - En lugar de generar un grafo en texto (propenso a errores sintácticos), el **Prompt 3** (Fig. 6, p. 6) plantea una tarea de **completado de código Python** sobre una clase predefinida `Goal(text)` con las operaciones `X.is_refined_by.append(Y)`, `Y.is_refinement_of(X)` e `implied_goals.append(X)`.
     - El prompt obliga a ejecutar **5 pasos de planificación (CoT/PSP)** antes de escribir las relaciones en Python: (1) describir qué hace la aplicación, (2) explicar qué incluye y qué no incluye cada objetivo $g_i$ en ese contexto, (3) inferir **hasta 2 o 3 objetivos implícitos (*implied goals*)** de alto nivel que agrupen objetivos huérfanos, (4) añadir los `implied_goals` al código, y (5) declarar las relaciones de refinamiento incluyendo la justificación en comentarios de código y prohibiendo sentencias `print`.
     - Se generan **10 modelos de objetivos** por transcripción; si un programa Python no compila o el grafo resultante contiene ciclos, se descarta y se regenera automáticamente (p. 6).

**Datos, idioma y dominio**
- **34 transcripciones de entrevistas abiertas** en **inglés** realizadas por estudiantes de posgrado de una asignatura de Ingeniería de Requisitos (entrenados con una clase de psicología cognitiva sobre memoria episódica/semántica y con los dos vídeos de Bano et al. [20]: *"Tips for Requirements Elicitation"* y *"Common Mistakes in Requirements Elicitation Interviews"*), con consentimiento IRB (tasa de respuesta: 34 de 74 estudiantes = 46 %, compensados con 25 USD; §III-A, p. 2-3).
- **Volumen y longitud**: **2.615 turnos de palabra en total** a lo largo de las 34 transcripciones (**media = 76,9 turnos**, **mediana = 70 turnos**, rango de 27 a 191 turnos; ~80 % entre 21 y 120 turnos; Fig. 2, p. 2-3, 8-9).
- **Dominios**: **29 dominios de aplicaciones web y móviles** seleccionados por muestreo estratificado a partir de 860 usos agrupados en 65 temas (compras/supermercado, inversión, búsqueda de empleo, educación online, navegación, fotos, podcasts, programación, viajes, videollamadas, mensajería y correo, foros Q&A, noticias, videojuegos, clima, redes sociales, streaming de música y vídeo, etc., p. 2-3).
- ⚠️ **Aclaración sobre 34 vs. 15 transcripciones**: el *Abstract* (p. 1) menciona *"evaluated on 15 interview transcripts across 29 application domains"*, pero el cuerpo del artículo especifica que la extracción y trazabilidad de objetivos (RQ1 y RQ2, §V, p. 8) se evalúa sobre las **34 transcripciones completas (2.615 turnos)**, mientras que el *ground truth* de relaciones de refinamiento en modelos de objetivos (RQ3, §VI-E, p. 7-9) se construye sobre un subconjunto de **15 transcripciones** ($15 \times 10 = 150$ modelos generados con 2.372 aristas de refinamiento, de las que se muestrean y etiquetan manualmente **550 relaciones**).
- **Licencia**: dataset de transcripciones, notebooks y scripts públicos en https://github.com/cmu-relab/goalgeneration (p. 10).

**Métricas y resultados cuantitativos exactos**
- **RQ1 — Extracción de objetivos y trazabilidad al texto fuente (media de 10 ejecuciones sobre las 34 transcripciones; Tabla I, p. 8)**:

| Estadístico | GPT-4o `whole` (transcripción entera) | GPT-4o `moving-G` (ventana 4 turnos, paso 2, general) | GPT-4o `moving-S` (ventana 4 turnos, paso 2, específico) | Humano (`moving` tracing) |
|---|---|---|---|---|
| Frases totales trazadas (*Total phrases*) | 672,2 | 604,7 | 535,5 | 595,2 |
| Frases no coincidentes / alucinadas (*Unmatched phrases*) | 109,4 | **34,8** | **31,3** | 99,6 |
| **Corrección automática de traza (*Trace correctness*)** | 83,7 % | **94,2 %** | **94,1 %** | 83,3 % |
| Objetivos trazados al entrevistador (*Interviewer goals*) | 6,5 | 17,8 | 13,2 | 16,1 |
| Objetivos trazados al stakeholder (*Stakeholder goals*) | 339,9 | 335,5 | 265,3 | 232,7 |
| Objetivos multi-turno (*Multi-turn goals*) | 6,5 | 13,5 | 8,7 | 13,5 |
| **Total de objetivos extraídos (*Total goals*)** | 346,4 | **353,3** | 278,5 | 248,8 |

  - **Precisión manual de las trazas de GPT-4o (RQ1, p. 1, 8-9)**: en la inspección manual de los autores, **el 98,7 % de los objetivos extraídos por GPT-4o estaban legítimamente respaldados por las frases trazadas en la transcripción**. Solo **2 objetivos** en todo el estudio carecían de evidencia válida (§VI-B, p. 9):
    1. *Confundir un obstáculo con un objetivo (Transcript #28)*: GPT-4o extrajo `"Save and read posts when offline"` cuando el stakeholder solo mencionaba como obstáculo que no podía hacer ciertas actividades al estar sin conexión.
    2. *Confundir la apreciación de una función existente con un objetivo (Transcript #5)*: GPT-4o extrajo `"Express appreciation for personalized playlists"` porque el usuario dijo que le gustaba mucho esa función durante la entrevista.
  - **Eliminación del sesgo posicional (*leading bias*, Fig. 10, p. 9)**: al dividir las 34 transcripciones en 10 deciles, la extracción con ventana completa (`whole`) sufre un fuerte sesgo inicial (concentra la mayoría de objetivos entre los deciles 1.º y 3.º y extrae el mínimo en el 10.º decil). Con la **ventana deslizante de 4 turnos (avance de 2)**, la distribución de objetivos extraídos a lo largo de los 10 deciles es uniforme y paralela a la de los objetivos humanos trazados.
  - **Invenciones de los entrevistadores humanos (§V y §VI-C, p. 8-9)**: los objetivos redactados por los propios entrevistadores humanos tras la entrevista solo alcanzaron un **83,3 % de corrección de traza** (`99,6` frases no encontradas de `595,2`) porque los analistas humanos introdujeron objetivos de su propia cosecha no dichos por el stakeholder (p. ej., en Transcript #5 el entrevistador apuntó *"search songs by title"* cuando el stakeholder habló de buscar por emociones o palabras clave; en Transcript #9 el entrevistador añadió *"training and implementing AI tools to analyze user preferences..."* cuando el stakeholder solo dijo preferir una plataforma que usa IA frente a otra que no).
- **RQ2 — Comparación entre objetivos extraídos por GPT-4o y por humanos (§V, p. 1, 8)**:
  - **173 objetivos humanos** coincidieron semánticamente con los generados por GPT-4o, mientras que **76 objetivos humanos** no fueron emparejados, reportándose un **62,0 % de coincidencia (*matching rate*)** con los objetivos humanos (p. 1, 8).
  - Además, GPT-4o extrajo **30 objetivos adicionales verdaderos** (perfectamente trazados a la transcripción) que los entrevistadores humanos habían pasado por alto por simple descuido (*human oversight*, p. 8-9).
- **RQ3 — Exactitud de las relaciones de refinamiento en los modelos de objetivos generados (§IV-B, §V y §VI-E, p. 7-10)**:
  - Acuerdo inter-anotador inicial entre los 2 autores sobre 50 aristas: **$\kappa = 0,288$** (*fair*); tras definir **4 reglas formales de desambiguación** (actividad más amplia vs. más específica, paso de un proceso, acción de entorno soportada por el sistema, y equivalencia con pre/post-condición, p. 7), el acuerdo en una segunda muestra de 50 aristas subió a **$\kappa = 0,711$** (*substantial*).
  - Evaluación sobre **550 aristas etiquetadas** (muestreadas al 50 % entre declaradas en la clausura transitiva $T(e)$ y no declaradas en $C(v) - T(e)$ sobre 150 modelos / 2.372 relaciones en 15 transcripciones):
    - **$TP = 227, TN = 170, FP = 73, FN = 80$** → **Exactitud (*Accuracy*) = 72,2 %** (*Nota propia*: equivale a Precisión = $227/300 = 75,7\%$, Recall = $227/307 = 73,9\%$, $F_1 = 74,8\%$).
  - Desglose de errores de refinamiento de GPT-4o (§VI-E, p. 9-10): **80 casos** de falsos negativos (no detectar que un objetivo específico refina a uno general), **65 casos** de falsos positivos entre objetivos complementarios pero independientes, **35 casos** de dirección invertida (poner el objetivo específico como padre del general), **23 casos** de relaciones simétricas entre modelos de un mismo prompt (y 47 relaciones simétricas en total presentes en 13 de las 15 transcripciones), **6 casos** de relación simétrica entre objetivos no relacionados, **2 casos** de refinamiento sin relación y **1 caso** de relación simétrica omitida.

**Insumo directo para ReqElicit-ES**
- **Arquitectura y verificación del módulo Sintetizador en WP7**:
  1. *Mitigación del sesgo posicional y de citas alucinadas mediante extracción por ventanas solapadas*: Sharfuddin y Breaux demuestran que pedir al LLM que extraiga requisitos de toda la transcripción de golpe reduce la atención al tramo final de la entrevista y triplica las citas textuales inventadas (`109,4` frases no coincidentes en `whole` frente a `31,3` en `moving-S`, subiendo la fidelidad de traza del **83,7 % al 94,2 %**). En nuestro **Sintetizador de WP7**, aunque las entrevistas tienen hasta 20 turnos, implementaremos una extracción por **ventanas deslizantes de 4 turnos con avance de 2 turnos** (o extracción por bloques de pares Q&A seguida de consolidación) para asegurar cobertura uniforme desde el turno 1 hasta el turno 20.
  2. *Trazabilidad verificable por subcadenas (`source_turns` + `source_phrases`)*: adoptamos el diseño en dos pasos (Prompt 1 + Prompt 2 o salida estructurada conjunta) exigiendo para cada historia de usuario generada en WP7 tanto los identificadores de turno (`turn_ids`) como las **subcadenas literales exactas (`quotes`)** de la conversación. Esto nos permite añadir en WP7 una métrica determinista automática de **Corrección de Traza (*Trace Correctness*)** comprobando en Python si cada cita pertenece realmente al texto del turno indicado, aislando así las invenciones del Sintetizador sin depender únicamente del Juez LLM.
  3. *Captura de requisitos multi-turno e introducidos por el entrevistador*: la Tabla I revela que en una entrevista interactiva un número sustancial de requisitos válidos se traza a turnos del entrevistador (**17,8** en `moving-G`) o abarca varios turnos (**13,5** en `moving-G`), porque el analista propone una alternativa y el cliente la valida. Por ello, las ventanas de entrada al Sintetizador de WP7 incluirán **tanto las intervenciones del entrevistador como las respuestas del cliente**, exigiendo que cualquier requisito originado en una pregunta del entrevistador tenga confirmación explícita del cliente en los turnos inmediatos.
  4. *Reglas de exclusión contra los 2 únicos errores de extracción de GPT-4o (§VI-B)*: incorporaremos al prompt del Sintetizador de WP7 la instrucción explícita de **no** convertir en requisitos (a) menciones de obstáculos del entorno fuera del control del sistema, ni (b) comentarios de agrado sobre herramientas actuales que no expresen una necesidad para el sistema objetivo.

---

### 3.3 RECOVER

**Referencia y año**
- Gianmario Voria, Francesco Casillo, Carmine Gravino, Gemma Catolino, Fabio Palomba (SeSa Lab, University of Salerno, Italia). *RECOVER: Toward Requirements Generation from Stakeholders' Conversations.* arXiv:2411.19552v2, 17-05-2025.
- Venue: publicado en *IEEE Transactions on Software Engineering (TSE)*, vol. 51, no. 6, pp. 1912–1933, junio de 2025, doi: `10.1109/TSE.2025.3572056`.
- Paquete de replicación (código, modelos, cuestionarios, oráculos y apéndice online): https://figshare.com/s/46661b70336a46d66ac8 (p. 2, 20); transcripción IFA base en https://github.com/RELabUU/REConSum/tree/main/data (p. 8).

**Problema y fase de RE**
- **Clasificación de turnos relevantes y generación automática post-entrevista de requisitos del sistema (*system requirements*)** a partir de transcripciones de conversaciones no estructuradas entre stakeholders y analistas.

**Metodología / arquitectura agéntica**
- **Diseño híbrido ML tradicional + LLM en 3 pasos secuenciales (Fig. 1 y Fig. 2, p. 3-7)**:
  - Los autores descartan deliberadamente usar LLMs (como GPT-4) en los pasos 1 y 2 porque en sus experimentos preliminares (documentados en su apéndice online y en §3 / §7, p. 3, 19) GPT-4 mostraba falta de determinismo, inventaba detalles como marcas de tiempo inexistentes, partía turnos de forma inconsistente y fallaba al emparejar preguntas y respuestas.
  1. **Paso #1 — Clasificación binaria de turnos relevantes para requisitos (*Classification*, §3.1, p. 4-5)**:
     - Cada turno de conversación (definido como el conjunto de enunciados contiguos de un mismo hablante antes de que intervenga otro, p. 3) se trunca/representa como un vector fijo de **100 tokens** mediante embeddings **`FastText`** y se clasifica como `requirements-relevant` o `non-requirements-relevant` con un clasificador **`SVC`** (`scikit-learn`, hiperparámetros óptimos: `C = 1`, `Gamma = 100`, `Kernel = 'RBF'`, Tabla 1, p. 4).
     - El par `FastText + SVC` fue seleccionado tras evaluar exhaustivamente **135 combinaciones** (5 técnicas de embedding: `TF-IDF`, `BERT`, `Word2Vec`, `FastText`, `GloVe` × 27 algoritmos de clasificación de la librería `LazyPredict` + ajuste fino con `GridSearchCV` mediante validación cruzada de 10 pliegues) sobre la versión anotada del dataset **PURE** de Ivanov et al. [28] (**7.745 frases** procedentes de 79 documentos públicos de requisitos etiquetadas como requisito / no requisito; en 10-fold CV logró **Precisión = 0,814539, Recall = 0,865608, Accuracy = 0,846090, F1 = 0,839133**, Tabla 1, p. 4-5).
     - A diferencia de REConSum (Spijkman et al. [7]), que primero filtraba patrones pregunta-respuesta y luego buscaba palabras clave del dominio, RECOVER **invierte el orden** (primero clasifica cada turno individualmente y luego agrupa Q&A) para no perder requisitos enunciados directamente por un stakeholder sin una pregunta previa (p. 3).
  2. **Paso #2 — Limpieza y emparejamiento Pregunta-Respuesta (*Processing*, §3.2, p. 5)**:
     - *Filtro de longitud mínima*: descarta todo turno clasificado como relevante que tenga **menos de 7 palabras** (umbral determinado empíricamente para eliminar turnos demasiado cortos o sin contexto suficiente, p. 5).
     - *Agrupación Q&A con `DialogTag` (basado en BERT)*: clasifica el acto de diálogo de cada turno relevante; si `DialogTag` lo etiqueta como `question` u `or-clause`, RECOVER **lo concatena con el turno inmediatamente siguiente** (asumiendo que contiene la respuesta del interlocutor) para proporcionar contexto completo al generador (p. 5).
  3. **Paso #3 — Generación automática de requisitos del sistema (*Automatic Generation*, §3.3, p. 5-6)**:
     - Utiliza **`Llama 2` (versión de 7B parámetros)** ejecutado localmente mediante un **prompt *2-shot*** (1 ejemplo positivo genérico y 1 negativo con salida `None`, seleccionado tras ejecutar cada prompt candidato al menos 10 veces sobre toda la conversación, p. 6):
       > `Given the following excerpt of a conversation, derive the system requirements, if any.`
       > `Please answer only with the list of derived requirements as output, as shown in the following examples.`
       > `Please do not consider the example excerpts provided in the examples in your final answer.`
       > `---- Example 1: ----`
       > `Example excerpt: Excerpt of conversation containing system requirements`
       > `Example output:`
       > `1. The system must have example feature X;`
       > `2. The system must have example feature Y;`
       > `---- Example 2: ----`
       > `Example excerpt: Excerpt of conversation that does not contain system requirements`
       > `Example output:`
       > `None`
     - El prompt pide exclusivamente *system requirements* funcionales porque en sus pruebas iniciales pedir requisitos de usuario, de componente o no funcionales (NFRs) hacía que el LLM mezclara metas de alto nivel con asunciones de implementación o **alucinara atributos de calidad no discutidos** (p. 6, 12).
     - Finalmente, concatena todos los requisitos generados para cada turno relevante en una lista global (sin paso posterior de deduplicación ni consolidación inter-turno).

**Datos, idioma y dominio**
- **Estudio principal (*in-vitro*, RQ1 y RQ2, §4, p. 8-11)**:
  - **1 transcripción de entrevista/taller de elicitación** en **inglés** del benchmark de Dalpiaz et al. [44] y Spijkman et al. [7] para el sistema de la **International Football Association (IFA)**: **133 turnos de palabra** y **39 minutos y 40 segundos** de duración (Tabla 2, p. 8).
  - **Estudio de usuario con 23 ingenieros de requisitos profesionales** (p. 2, 9-11):
    - *RQ1.2 y RQ1.3 (nivel de turno individual)*: **20 ingenieros de requisitos** (5–10 años de experiencia), divididos en 5 cuestionarios de 10–12 turnos cada uno (**57 turnos evaluados**, 4 expertos independientes por turno = **228 evaluaciones** de calidad y 4 conjuntos oráculo $O_1, O_2, O_3, O_4$ por turno, Fig. 4, p. 9-10).
    - *RQ2 (nivel de conversación completa)*: **3 expertos industriales senior** (7–25 años de experiencia) extrajeron requisitos de la transcripción completa (produciendo inicialmente **104, 36 y 17 requisitos** respectivamente por sus distintos niveles de granularidad) y convergieron mediante **2 rondas del método Delphi** (40 requisitos en ronda 1 → **28 requisitos consensuados** en ronda 2 que conforman el oráculo global, p. 10-11).
- **Evaluación adicional (*in-vivo*, §6.1, p. 16-18)**:
  - **3 transcripciones de reuniones industriales reales** (`C1`, `C2`, `C3`) seleccionadas de un corpus de 27 conversaciones (9 reuniones, ~24 h de audio en una empresa de software de EE. UU., Rodeghero et al. [53]), con **271, 143 y 165 turnos válidos** tras limpiar anotaciones ininteligibles (sistemas web y ciberfísicos en fases de desarrollo continuo).

**Métricas y resultados cuantitativos exactos**
- **RQ1.1 — Clasificación de turnos relevantes en la conversación IFA (133 turnos; Tabla 3, p. 12)**:
  - Predichos como `Req`: **62 turnos**; predichos como `NonReq`: **71 turnos**.
  - Matriz de confusión frente al oráculo de los autores: **$TP = 39, TN = 59, FP = 23, FN = 12$**.
  - **Precisión = 62,90 % (`0.6290322581`)**, **Recall = 76,47 % (`0.7647058824`, citado como 76 %–77 % en el texto)** (*Nota propia*: Accuracy = $98/133 = 73,68\%$, $F_1 = 69,03\%$).
  - De los 62 turnos predichos como relevantes, 5 eran muletillas vacías (`"All right, okay."`, `"Okay. Okay. Um."`) que no fueron filtradas antes del envío y se excluyeron de la encuesta (quedando 57 turnos); de esos 57, otros 6 fueron juzgados sin requisitos por los 4 expertos, quedando **51 turnos validados por al menos 1 experto** (31 turnos reconocidos por los 4 expertos [60,78 %], 10 por 3 expertos [19,61 %], 7 por 2 expertos [13,73 %] y 3 por 1 experto [5,88 %], p. 12).
  - De los requisitos generados por RECOVER, el **88 % fueron funcionales** y el **12 % no funcionales (NFRs)** explícitamente mencionados por los stakeholders (como escalabilidad, p. 12).
- **RQ1.2 — Similitud turno a turno frente a los 4 oráculos de expertos (51 turnos, comparación por pares promediada en %; Tabla 4, p. 12)**:

| Grupo según n.º de expertos que extrajeron requisitos en el turno | BLEU (Min / **Mean** / Max) | ROUGE (Min / **Mean** / Max) | METEOR (Min / **Mean** / Max) |
|---|---|---|---|
| Grupo con 1 respuesta (3 turnos, 5,88 %) | 14,80 / **14,80** / 14,80 | 32,66 / **32,66** / 32,66 | 46,71 / **46,71** / 46,71 |
| Grupo con 2 respuestas (7 turnos, 13,73 %) | 4,63 / **9,81** / 14,99 | 27,00 / **39,37** / 51,75 | 30,28 / **43,96** / 57,63 |
| Grupo con 3 respuestas (10 turnos, 19,61 %) | 1,87 / **4,09** / 6,46 | 24,97 / **36,37** / 49,44 | 27,91 / **40,22** / 54,36 |
| Grupo con 4 respuestas (31 turnos, 60,78 %) | 1,91 / **3,91** / 7,18 | 28,37 / **39,60** / 53,92 | 29,41 / **41,46** / 57,98 |
| **Promedio global (*Average*)** | 3,03 / **5,39** / 8,56 | 27,77 / **38,53** / 51,49 | 30,25 / **41,87** / 56,56 |

- **RQ1.3 — Calidad percibida por los 20 expertos (228 evaluaciones en escala Likert 1–5; Fig. 6, p. 13-14)**:
  - **Correctness** (fidelidad a la intención del stakeholder sin distorsión): **72 % de acuerdo** (4 o 5) vs. **15 % en desacuerdo** (1 o 2).
  - **Completeness** (captura toda la información relevante del turno): **64 % de acuerdo** vs. **21 % en desacuerdo**.
  - **Actionability** (claridad y especificidad para diseño/implementación): **66 % de acuerdo** vs. **20 % en desacuerdo**.
  - **Adopción práctica (p. 14)**: al revelar al final del cuestionario que los requisitos habían sido generados por una herramienta automática, el **100 %** mantuvo sus puntuaciones de calidad, el **65 %** declaró que adoptaría RECOVER en su trabajo (10 % No, 25 % indeciso) y el **80 %** lo usaría para ahorrar tiempo y esfuerzo.
- **RQ2 — Evaluación a nivel de conversación completa frente al oráculo Delphi (28 reqs) y frente a ChatGPT/GPT-4 sin preprocesado (Tabla 5, p. 11, 15)**:
  - Volúmenes generados: **RECOVER = 135 requisitos**; **ChatGPT (GPT-4) = 31 requisitos**; **Oráculo Delphi consensuado = 28 requisitos** (Expertos individuales antes de Delphi: Experto 1 = 104, Experto 2 = 36, Experto 3 = 17, p. 10-11).

| Comparación a nivel de corpus (conversación completa) | BLEU (%) | ROUGE (%) | METEOR (%) | Brevity Penalty (BP) | Length Ratio (LR) |
|---|---|---|---|---|---|
| **RECOVER vs. Oráculo Delphi (28 reqs)** | **78,82** | 37,20 | **39,09** | **0,92** | **0,93** |
| **ChatGPT (GPT-4) vs. Oráculo Delphi (28 reqs)** | 49,36 | **43,96** | 35,34 | 0,76 | 0,78 |
| RECOVER vs. ChatGPT | 57,83 | 37,83 | 32,76 | 1 | 1 |
| RECOVER vs. Experto 1 (104 reqs, estilo muy granular) | 37,24 | **48,18** | 39,92 | 1 | 1 |
| RECOVER vs. Experto 2 (36 reqs, granularidad media) | **92,34** | 28,61 | **40,22** | 1 | 1 |
| RECOVER vs. Experto 3 (17 reqs, estilo abstracto/conciso) | 30,11 | 26,13 | 28,57 | 0,92 | 0,93 |

- **Evaluación *in-vivo* en 3 transcripciones industriales ruidosas (Tabla 6, p. 16-18)**:

| Transcripción industrial | Paso #1 Negativos: % TN / % FN | Pasos #1 y #2 Positivos: System / Technical / Management / Unrelated | Paso #3 Calidad Likert (1–5): Correct / Complete / Actionable |
|---|---|---|---|
| **C1** (271 turnos válidos) | 83,85 % / 16,15 % | **44 (40 %)** / 38 / 60 / 12 | **4,30 / 4,25 / 4,00** |
| **C2** (143 turnos válidos) | 91,94 % / 8,06 % | **28 (34 %)** / 20 / 24 / 9 | **3,46 / 3,75 / 3,50** |
| **C3** (165 turnos válidos) | **93,81 % / 6,19 %** | **5 (7 %)** / 34 / 20 / 9 | **3,80 / 4,00 / 4,40** |

**Insumo directo para ReqElicit-ES**
- **Diseño y evaluación de nuestro módulo Sintetizador en WP7**:
  1. *Evitar los dos defectos estructurales del enfoque turno a turno detectados por los 23 expertos (§4.4, §5.1.3 y §5.2, p. 11, 14, 16)*:
     - **Falta de cohesión inter-turno y sobre-fragmentación**: al procesar cada turno/par Q&A de forma aislada sin consolidación final, RECOVER genera **135 requisitos repetitivos o fragmentados** donde el panel Delphi consolida **28 requisitos** (p. ej., RECOVER parte en 3 requisitos separados el ver eventos, descargarlos y el acceso público de solo lectura, perdiendo además el matiz de que aplica a *usuarios no registrados*, p. 11).
     - **Pérdida del actor/rol de usuario (*Missing Actor*)**: los expertos organizan los requisitos en torno a **roles de usuario y sus interacciones** (*"The system must allow the IFA representative to schedule..."*), mientras que el prompt de RECOVER (`"1. The system must have example feature X"`) produce requisitos centrados en componentes sin especificar quién es el actor (p. 14, 16).
     - **Aplicación directa en WP7**: nuestro Sintetizador extraerá primero los requisitos candidatos anclados a los pares `(pregunta, respuesta)` (preservando la exhaustividad por la que RECOVER supera en `BLEU` y `METEOR` al prompt directo de ChatGPT, que sufre `BP = 0,76`), pero añadirá una **segunda fase obligatoria de consolidación multi-turno y estructuración como Historia de Usuario con actor explícito** (`Como [actor/rol], quiero [funcionalidad], para [beneficio]`), conservando la lista acumulada de `source_turns` de todos los turnos fusionados.
  2. *Filtrado previo de turnos de trámite y emparejamiento Pregunta-Respuesta*: en nuestras entrevistas de ReqElicit-ES los turnos ya están estructurados naturalmente en pares `(Interviewer_t, Stakeholder_t)`. Aplicaremos en WP7 la heurística de RECOVER de **alimentar siempre la respuesta del cliente junto con la pregunta inmediatamente anterior del entrevistador** (ya que respuestas cortas como *"Sí, exactamente así"* carecen de significado sin la pregunta) y filtrar turnos de puro saludo/cierre sin contenido funcional.
  3. *Restricción contra NFRs especulativos (p. 6, 12)*: siguiendo el hallazgo empírico de Voria et al., el prompt del Sintetizador de WP7 prohibirá inferir atributos de calidad (NFRs) genéricos que no hayan sido expresados o confirmados en los turnos de la entrevista.
  4. *Criterios de calidad para la rúbrica de evaluación en WP7*: adoptamos las definiciones operativas de **Correctness** (fidelidad sin alucinación), **Completeness** (cobertura sin omisión) y **Actionability** (especificidad utilizable para desarrollo) de RQ1.3 (p. 7, 9).

---

### 3.4 LENS

**Referencia y año**
- Mithila Sivakumar, Martin Lochner, Shiva Nejati, Mehrdad Sabetzadeh (University of Ottawa & eSentire, Canadá). *LLM-Based Discovery of Latent Requirements from Stakeholder Conversations: Preliminary Results from Industry.* arXiv:2606.25867v1, 24-06-2026.
- Venue: preprint de arXiv en formato IEEE (9 páginas).
- Datos y artefactos: las transcripciones industriales de eSentire y los prompts literales completos son confidenciales, pero el artículo publica los *Prompt Outlines* completos, las plantillas literales de *User Story* y *Rationale*, la configuración experimental y los **13 criterios QUS** en las Tablas II y VII y en el Apéndice VIII (p. 4, 8-9).

**Problema y fase de RE**
- **Extracción post-entrevista de requisitos explícitos como historias de usuario trazables** e **inferencia de requisitos latentes (*latent requirements*) con justificación estructurada (*rationale*)** integrando las transcripciones de entrevistas con el catálogo de herramientas e infraestructura de la organización.

**Metodología / arquitectura agéntica**
- **Modelo base y barrido de temperaturas**: **`Claude Sonnet 4.5`** (Anthropic), evaluado sistemáticamente en **4 ajustes de temperatura: `0.0, 0.35, 0.7, 1.0`** siguiendo las recomendaciones de la API de Claude para cubrir desde variabilidad nula hasta alta diversidad (p. 4-5).
- **Pipeline *few-shot* en 2 pasos secuenciales (Fig. 3, Tabla II y Apéndice VIII-A, p. 3-4, 9)**:
  1. **Paso 1 — Extracción de Requisitos Explícitos (*Explicit Requirements Extraction*)**:
     - *Estructura del Prompt (Apéndice VIII-A, p. 9)*:
       - `(I) Role`: *Explicit requirements extractor*.
       - `(II) Input`:
         1. Transcripción completa de la entrevista con marcas de tiempo (`timestamps`).
         2. **Los 13 criterios de calidad QUS (*Quality User Story Framework* de Lucassen et al. [8], Tabla VII, p. 9)**.
         3. *Rules for explicit requirements extraction*: extraer **únicamente** requisitos con intención explícita de automatización/software expresada por el stakeholder, prohibiendo inferir requisitos explícitos a partir de meras menciones de trabajo manual (p. 4-5).
         4. *User story template* (Tabla II, p. 4):
            > `"As a [role], I want [goal], so that [reason]"`
         5. Ejemplos *few-shot*.
         6. Especificación de formato de salida en **JSON**.
       - `(III) Output`: historias de usuario explícitas acompañadas de su **`timestamp`** y el **extracto literal de la transcripción (*transcript excerpt*)** que las soporta.
  2. **Paso 2 — Inferencia de Requisitos Latentes (*Latent Requirements Inference*)**:
     - *Definición operativa de requisito latente (p. 1)*: oportunidad plausible para introducir software que los stakeholders no articulan explícitamente, pero que se hace evidente al interpretar sus declaraciones sobre flujos de trabajo, ineficiencias y *pain points* a la luz de las herramientas e infraestructura existentes en la organización.
     - *Estructura del Prompt (Apéndice VIII-A, p. 9)*:
       - `(I) Role`: *Latent requirements identifier*.
       - `(II) Input`:
         1. Transcripción de la entrevista.
         2. Requisitos explícitos extraídos en el Paso 1 (para evitar solapamientos).
         3. **Los 13 criterios QUS (Tabla VII)**.
         4. *Rules for identifying latent requirements*.
         5. *User story template* (`"As a [role], I want [goal], so that [reason]"`).
         6. *Rationale template* estructurado en **4 oraciones obligatorias** (Tabla II, p. 4):
            > `"Automating [activity] helps address [problem/inefficiency] in [context]. The activity is currently carried out [manually/semi-automatically/using an existing tool or approach]. The automation can be implemented using [available tool(s)] through [implementation approach]. As a result, [expected impact]"`
         7. Ejemplos *few-shot* de historias latentes y sus *rationales*.
         8. *Organizational context (tooling & infrastructure)*: catálogo de plataformas internas de la empresa (p. ej., `[Knowledge Sharing Platform]`, `[Workflow Management Platform]`, `[Data Platform]`, `[Internal Chatbot Assistant]`) y sus capacidades técnicas.
         9. Especificación de salida en **JSON**.
       - `(III) Output`: historias de usuario latentes + *rationale* de 4 frases + `timestamp` y extracto de origen en la transcripción.
- **Los 13 criterios QUS (*Quality User Story*) codificados dentro de los prompts de ambos pasos (Tabla VII, p. 9)**:
  - **Syntactic (3)**:
    - *Atomic*: cada historia expresa exactamente UNA funcionalidad (`Each story expresses exactly ONE feature`).
    - *Minimal*: contiene solo rol, medio y fin (`Contains only role, means, and ends`).
    - *Well-formed*: incluye al menos un rol y un medio (`Includes at least a role and a means`).
  - **Semantic (4)**:
    - *Conflict-free*: no es inconsistente con otras historias de usuario (`Not inconsistent with other user stories`).
    - *Conceptually sound*: el medio expresa una funcionalidad y el fin expresa una justificación (`The means expresses a feature, the ends expresses a rationale`).
    - *Problem-oriented*: especifica el problema, NO la solución (`Specifies the problem, NOT the solution`).
    - *Unambiguous*: evita términos que puedan llevar a múltiples interpretaciones (`Avoids terms that may lead to multiple interpretations`).
  - **Pragmatic (6)**:
    - *Full sentence*: cada historia es una oración completa bien formada (`Each story is represented as a well-formed full sentence`).
    - *Complete*: en conjunto, todas las historias crean una solución completa (`Together, all stories create a feature-complete solution`).
    - *Independent*: autocontenida, evitando dependencias inherentes (`Self-contained, avoiding inherent dependencies`).
    - *Estimatable*: no demasiado gruesa, fácil de planificar y priorizar (`Not too coarse-grained, easy to plan and prioritize`).
    - *Uniform*: todas las historias siguen aproximadamente la misma plantilla (`All stories follow roughly the same template`).
    - *Unique*: sin duplicados (`No duplicates`).

**Datos, idioma y dominio**
- **12 transcripciones de entrevistas semiestructuradas industriales** en **inglés** realizadas en **eSentire** (empresa global de ciberseguridad *Managed Detection and Response*) sobre automatización de procesos operativos en su **Security Operations Centre (SOC)** (Tabla III, p. 4):
  - **Total de turnos**: **1.237 turnos de palabra** en las 12 entrevistas.
  - **Turnos por transcripción**: media **154**, mediana **145**, mín. **92**, máx. **252**.
  - **Palabras por transcripción**: media **8.938**, mediana **8.945**, mín. **6.712**, máx. **11.987**.
  - **Duración por entrevista**: media **59,6 min**, mediana **59,64 min**, mín. **44,75 min**, máx. **79,91 min**.
  - **Longitud de turno (palabras)**: media **63**, mediana **56**, mín. **41**, máx. **98**.
  - **Participantes**: media de **3 participantes por entrevista** (36 % en roles senior [directores, managers] y 64 % en roles junior/intermedios [analistas SOC], p. 4).
- **Licencia**: confidencial (industria privada, p. 8).

**Métricas y resultados cuantitativos exactos**
- **RQ1 — Exactitud en la extracción de requisitos explícitos según la temperatura (Tabla V, p. 5)**:

| Temperatura (`Claude Sonnet 4.5`) | Total de requisitos extraídos | Precisión (%) | Recall (%) | Exactitud / F1-score (%) |
|---|---|---|---|---|
| `0.0` | 30 | 50 % | 94 % | 65,3 % |
| `0.35` | 26 | 64 % | **100 %** | 78,0 % |
| **`0.7` (mejor configuración)** | **22** | **73 %** | **100 %** | **84,4 %** |
| `1.0` | 37 | 41 % | 94 % | 56,5 % |

  - *Nota propia*: con 22 requisitos extraídos a $T = 0,7$, $\text{Recall} = 100\%$ y $\text{Precisión} = 73\%$ ($16/22 = 72,73\%$), el *ground truth* validado por los expertos contiene exactamente **16 requisitos explícitos** en las 12 entrevistas ($TP = 16, FP = 6, FN = 0$ en $T = 0,7$).
  - **Desglose cuantitativo de los Falsos Positivos en la extracción explícita (Fig. 4 y §IV-C, p. 5-6)**:
    1. **Menciones de trabajo manual confundidas con requisitos explícitos (*Mentions of Manual Work Mistaken for Requirements*): 66 % de los FPs** (el stakeholder comenta que revisar datos de rendimiento se hace manualmente y lleva tiempo, y el LLM lo convierte en requisito explícito pese a la regla del prompt que prohíbe inferir sin intención explícita).
    2. **Discusión de automatización existente confundida con requisito nuevo (*Discussion of Existing Automation Mistaken for Requirements*): 17 % de los FPs** (el stakeholder explica una capacidad de IA que ya está funcionando a mitad de ciclo y el LLM la extrae como requisito por construir).
    3. **Lenguaje de búsqueda de confirmación confundido con requisito (*Confirmation-Seeking Language Mistaken for Requirements*): 17 % de los FPs** (frases como `"The [Internal Process] that was previously handled manually is now automated, right?"`, donde la coletilla `"right?"` hace que el LLM interprete incertidumbre y genere un requisito para algo ya automatizado).
- **RQ2 — Utilidad percibida de los 104 requisitos latentes inferidos a $T = 0,7$ (evaluados independientemente por 2 expertos de dominio de eSentire durante 4–5 h cada uno; Tabla VI, p. 5-6)**:

| Evaluador | Negative Time Gain (*Reject*) | No Time Gain (*Weak Reject*) | Uncertain Time Gain (*Borderline*) | Moderate Time Gain (*Weak Accept*) | High Time Gain (*Accept*) | Total Positivo (Moderate + High) |
|---|---|---|---|---|---|---|
| **Experto 1** | 8,7 % | 3,8 % | 14,4 % | 46,2 % | 26,9 % | **73,1 %** |
| **Experto 2** | 15,4 % | 1,0 % | 6,7 % | 20,2 % | 56,7 % | **76,9 %** |
| **Promedio** | **12,05 %** | **2,40 %** | **10,55 %** | **33,20 %** | **41,80 %** | **75,0 %** |

  - En resumen: **75 %** de los requisitos latentes aportan ahorro de tiempo moderado o alto, **14,5 %** aportan ganancia nula o negativa, y **10,5 %** son inciertos (p. 6).
  - **Acuerdo inter-evaluador**: **$\kappa$ de Cohen = 0,54** (acuerdo moderado) al agrupar en categorías binarias (*High/Moderate* vs. *Negative/No Time Gain*, p. 6).
  - **Distribución de críticas de los expertos sobre la viabilidad técnica y el *rationale* de los requisitos latentes (Fig. 5, p. 6-7)**:
    - Falta de detalles técnicos concretos en el *rationale*: **$\approx 49\%$** de todo el feedback.
    - La aplicabilidad práctica depende de tener acceso a fuentes de datos o APIs específicas: **$\approx 22\%$**.
    - La funcionalidad propuesta supera las capacidades reales de la herramienta citada: **$\approx 16\%$**.
    - La tarea puede resolverse con herramientas convencionales sin necesidad de IA (*over-reliance on AI*): **$\approx 7\%$**.
    - Comentarios aislados fuera de estas categorías: **$\approx 6\%$**.

**Insumo directo para ReqElicit-ES**
- **Especificación directa del prompt y del protocolo de evaluación de nuestro Sintetizador en WP7**:
  1. *Adopción íntegra de la plantilla de Historia de Usuario y de los 13 criterios QUS (Tablas II y VII, p. 4, 9)*: nuestro **Sintetizador en WP7** incorporará literalmente los **13 criterios QUS de Lucassen et al. [8]** (`Atomic`, `Minimal`, `Well-formed`, `Conflict-free`, `Conceptually sound`, `Problem-oriented`, `Unambiguous`, `Full sentence`, `Complete`, `Independent`, `Estimatable`, `Uniform`, `Unique`) en su prompt de sistema y generará cada requisito en el formato estándar en español: `"Como [rol/actor], quiero [objetivo/funcionalidad], para [razón/beneficio]"`, acompañado de sus turnos de origen (`turn_ids`) y citas literales (`excerpts`).
  2. *Blindaje del Sintetizador (WP7) contra las 3 causas de Falsos Positivos descubiertas en LENS (Fig. 4 y Lección 1, p. 6, 8)*:
     - **Filtro contra coletillas de confirmación (`"¿verdad?"`, `"¿cierto?"`, `"¿no?"`)**: en entrevistas conversacionales (especialmente cuando nuestro agente **M2** usa resúmenes de confirmación o cuando un baseline hace preguntas cerradas), el prompt del Sintetizador instruirá explícitamente a verificar la respuesta del cliente antes de extraer una historia de usuario, ignorando preguntas de confirmación sobre procesos ya existentes o hipótesis rechazadas por el cliente.
     - **Separación entre estado actual (*As-Is*) y necesidad futura (*To-Be*)**: regla explícita para no extraer como requisitos del nuevo sistema las descripciones de herramientas actuales o tareas manuales si el cliente no manifiesta ni confirma que el sistema a desarrollar deba automatizarlas o soportarlas.
     - **Frontera clara entre Síntesis Fiel (WP7) e Inferencia Latente**: en ReqElicit-ES, el descubrimiento de necesidades implícitas/latentes es responsabilidad del **Entrevistador (WP6)** durante la conversación (logrando que el cliente las verbalice). El **Sintetizador (WP7)** debe actuar como el **Paso 1 de LENS** (*Explicit Requirements Extractor* sobre lo verbalizado en la entrevista): si el Sintetizador inventa por su cuenta requisitos latentes que el entrevistador nunca llegó a descubrir en el diálogo, nuestra métrica de **Tasa de Invención / Alucinación (WP7)** lo penalizará como falso positivo. Esta distinción protege la validez constructiva de la comparación entre agentes entrevistadores (B0–B3 vs. M1–M2): el Sintetizador no puede «hacer trampa» adivinando requisitos no elicitados en la entrevista.
  3. *Calibración de temperatura en WP7*: dado que tanto en LENS ($T = 0,7$ supera a $T = 0,0$ en +19,1 puntos de F1) como en Generative Goal Modeling ($T = 1,0$ con clustering supera el sesgo de repetición) una temperatura estrictamente cero no siempre es óptima para extracción con prompts largos, verificaremos en las pruebas piloto de WP7 si una temperatura baja-moderada ($T \in [0,0, 0,3]$) mejora la precisión sin perder el 100 % de recall sobre los requisitos revelados.

---

## Lote 4

### 4.1 LLMs for RE: Systematic Literature Review (Zadenoori et al., 2025)

**Referencia y año**
- Mohammad Amin Zadenoori, Jacek Dąbrowski, Waad Alhoshan, Liping Zhao, Alessio Ferrari. *Large Language Models (LLMs) for Requirements Engineering (RE): A Systematic Literature Review.* arXiv:2509.11446v1, 14-09-2025 (Preprint enviado a Elsevier el 16 de septiembre de 2025, p. 1).
- **Datos y paquete de replicación (Zenodo)**: `https://doi.org/10.5281/zenodo.17068810` (p. 6).

**Problema y fase de RE**
- **Revisión Sistemática de la Literatura (SLR) sobre LLM4RE** (*Large Language Models for Requirements Engineering*): caracteriza el cambio de paradigma desde el procesamiento del lenguaje natural clásico/estadístico (NLP4RE) hacia los grandes modelos de lenguaje generativos (LLM4RE) a través de **5 preguntas de investigación (RQ1–RQ5)** que cubren el estado de las publicaciones (RQ1), foco de investigación por tarea, fase de RE, artefactos de entrada y de salida (RQ2), modelos, estrategias de *prompting*, arquitecturas y ajuste de hiperparámetros (RQ3), conjuntos de datos, dominios y métricas cuantitativas (RQ4), y evaluación de salidas y estrategias empíricas (RQ5) (Tabla 1, p. 8).

**Metodología / arquitectura agéntica**
- **Protocolo de revisión sistemática** siguiendo las directrices de Kitchenham et al. [9] y las pautas de clasificación de estudios de mapeo de Petersen et al. [11] y Wieringa et al. [16] (p. 6-14):
  1. **Bases de datos (5)**: ACM Digital Library, IEEE Xplore, ScienceDirect, SpringerLink y ACL Anthology, complementadas con Google Scholar (p. 7-9).
  2. **Cadena de búsqueda**: combinación booleana `AND` entre términos de RE (`"requirements engineering"`, `"requirements elicitation"`, `"requirements analysis"`, `"requirements specification"`, `"requirements modeling"`, `"requirements validation"`, `"requirements verification"`, `"requirements management"`, `"requirements traceability"`, `"requirements classification"`, `"requirements document"`, `"user stories"`) y términos de LLMs (`"large language model*"`, `"LLM*"`, `"generative AI"`, `"GenAI"`, `"foundation model*"`, `"GPT*"`, `"ChatGPT"`, `"BERT"`, `"T5"`, `"LLaMA"`, `"Claude"`, `"Gemini"`, `"PaLM"`, `"Mistral"`, `"prompt engineering"`, `"in-context learning"`, `"zero-shot"`, `"few-shot"`, Tabla 2, p. 9).
  3. **Proceso de filtrado (Fig. 1, p. 10)**:
     - Búsqueda inicial (enero 2020 – diciembre 2024): **1.622 registros** + **29** de Google Scholar = **1.651 estudios candidatos**.
     - Tras eliminar duplicados y aplicar criterios de exclusión de formato/extensión (E1–E2, excluyendo *short papers* $< 6$ páginas en formato de una columna o $< 4$ páginas a doble columna, Tabla 3, p. 10): **1.142 estudios**.
     - Filtrado por título/resumen/introducción/conclusión (E3–E4, excluyendo estudios que usan solo modelos *encoder-only* tipo BERT/RoBERTa sin capacidades generativas o pre-LLM): **178 estudios**.
     - Lectura a texto completo y validación cruzada entre 3 inspectores y 2 supervisores (I1–I2): **74 estudios primarios seleccionados** (todos publicados en 2023 y 2024, dado que no se halló ningún estudio primario que cumpliera los criterios entre 2020 y 2022, p. 14).

**Datos, idioma y dominio**
- **Población analizada**: **74 estudios primarios** publicados entre **2023 (22 estudios, 30 %)** y **2024 (52 estudios, 70 %, crecimiento interanual del +136 %)** (Fig. 3, p. 15).
- **Conjuntos de datos utilizados en los estudios primarios (RQ4.1, Tabla 13 y Fig. 11, p. 36-38)**:
  - Se identificaron **59 datasets distintos** en los 74 estudios, con una distribución de «cola larga» (*long tail*): **52 de los 59 datasets (88 %) se usan en un único estudio** (p. 36).
  - Los únicos datasets reutilizados en $\ge 2$ estudios son **7**: `PURE` (8 estudios, 11 %), `PROMISE NFR` (7 estudios, 9 %), `SecReq` (3 estudios, 4 %), `PTC` (2 estudios), `User Story Dataset` de Dalpiaz (2 estudios), `WARN` (2 estudios) y `UAV` (2 estudios) (Tabla 13, p. 37).
- **Dominios de aplicación de los datasets (RQ4.2, Tabla 14 y Fig. 12, p. 39-40)**:
  - **Multi-domain** (28 estudios, **38 %**, p. ej., PURE o PROMISE), **No especificado / genérico** (14 estudios, **19 %**), **Salud / Healthcare** (8 estudios, **11 %**), **Automoción / Automotive** (5 estudios, **7 %**), **Aeroespacial / Aviónica** (4 estudios, **5 %**), **Finanzas / Banca** (3 estudios, **4 %**), **Educación** (3 estudios, **4 %**), **Ferroviario / Railway** (3 estudios, **4 %**), **Comercio electrónico / E-commerce** (2 estudios, **3 %**), **Ciberseguridad**, **Gobierno electrónico**, **Hogar inteligente / IoT** y **Telecomunicaciones** (1 estudio cada uno, **1 %**) (Tabla 14, p. 40).
- **Idioma**: la práctica totalidad de los benchmarks reutilizados (`PURE`, `PROMISE`, `SecReq`, `User Story Dataset`) están en **inglés**, y los autores destacan explícitamente como línea futura prioritaria la **Evaluación Multilingüe e Intercultural (*Multilingual and Cross-Cultural Evaluation*, §6.4, p. 53)**: *"Most LLM4RE studies focus on English requirements, leaving a gap in understanding how LLMs perform with requirements written in other languages or originating from different cultural contexts"*.

**Métricas y resultados cuantitativos exactos**
- **RQ1 — Estado de la literatura (p. 14-17)**:
  - **Tipos de publicación (Fig. 2, p. 14)**: artículos de congreso **66 % (49/74)**, artículos de *workshop* **23 % (17/74)** y artículos de revista **11 % (8/74)**.
  - **Principales sedes (Tabla 4, p. 16)**: `IEEE RE` (21 estudios, **28 %**), `IEEE REW` (15 estudios, **20 %** —casi la mitad del campo se concentra en RE + REW, sumando 48 %—), `REFSQ` (6 estudios, **8 %**), `ICSE` (4 estudios, **5 %**), `ASE` (3 estudios, **4 %**), `Requirements Engineering Journal (REJ)` (3 estudios, **4 %**).
- **RQ2 — Foco de investigación en RE (Tablas 5, 6, 7 y 8, p. 18-26)**:
  - **RQ2.1 Tareas de RE (Tabla 5 y Fig. 5, p. 19-21)**:
    1. **Requirements Elicitation**: **15 estudios (20 %)**.
    2. **Requirements Validation**: **15 estudios (20 %)**.
    3. **Software Engineering Tasks** (generación de código/tests desde requisitos): **11 estudios (15 %)**.
    4. **Requirements Modeling**: **9 estudios (12 %)**.
    5. **Requirements Classification**: **8 estudios (11 %)**.
    6. **Requirements Tracing**: **5 estudios (7 %)**.
    7. **Defect Detection**: **4 estudios (5 %)**.
    8. **Requirements Documentation**: **3 estudios (4 %)**.
    9. **Legal Requirements Analysis**: **3 estudios (4 %)**.
    10. **Requirements Retrieval** y **Terminology/Glossary Extraction**: **1 estudio cada una (1 %)**; Prioritization, Relations Extraction y Change Impact Analysis: **0 estudios (0 %)**.
  - **RQ2.2 Fases de RE (Tabla 6 y Fig. 6, p. 21-23)**:
    - **Elicitation**: **16 estudios (22 %)** y **Validation & Verification (V&V)**: **16 estudios (22 %)** empatan como las fases más investigadas (frente al 16,76 % y 4,05 % que tenían respectivamente en la era NLP4RE de Zhao et al. [27], p. 21-22).
    - **Analysis**: **14 estudios (19 %)** (cae desde el 42,70 % de NLP4RE).
    - **Other (Testing/Design)**: **12 estudios (16 %)**.
    - **Modeling** y **Management**: **9 estudios cada una (12 %)**.
  - **RQ2.3 Artefactos de entrada (Tabla 7 y Fig. 7, p. 23-25)**:
    - **System/Software Requirements Specifications (SRS)**: **28 estudios (38 %)** (baja desde el 64,59 % de NLP4RE, p. 23).
    - **Issues and User Feedback**: **9 estudios (12 %)**.
    - **Others**: **8 estudios (11 %)**.
    - **Regulatory and Legal Artifacts**: **7 estudios (9 %)**.
    - **Technical Documents and Manuals** y **Models and Ontologies**: **6 estudios cada uno (8 %)**.
    - **User Stories and Agile Requirements** y **Specific Quality Requirements**: **4 estudios cada uno (5 %)**.
    - **Elicitation Documents (transcripciones de entrevistas, grupos focales, talleres)**: **solo 2 estudios (3 %, `[29, 37]`)** —evidencia cuantitativa directa de la escasez de estudios que procesan transcripciones conversacionales de entrevistas.
  - **RQ2.4 Artefactos de salida (Tabla 8 y Fig. 8, p. 25-26)**:
    - **Requirements Specifications**: **21 estudios (28 %)**, **Models and Diagrams**: **14 estudios (19 %)**, **Classification Labels**: **13 estudios (18 %)**, **Other Outputs**: **10 estudios (14 %)**, **Code and Test Artifacts**: **9 estudios (12 %)**, **Traceability Links**: **5 estudios (7 %)**, **Interview Scripts / Questions**: **2 estudios (3 %, `[35, 36]`)**.
- **RQ3 — Uso de LLMs, Prompting y Arquitecturas (Tablas 9, 10, 11 y 12, p. 27-35)**:
  - **RQ3.1 Familias de modelos (Tabla 9 y Fig. 9, p. 28-29)**: dominio abrumador de **OpenAI GPT** en **66 de los 74 estudios (89 %)**: `GPT-3.5` en **43 estudios (58 %)**, `GPT-4` en **38 estudios (51 %)**, `GPT-4o` en **5 estudios (7 %)** y `GPT-3` en **4 estudios (5 %)**. Le siguen de lejos **Meta LLaMA** (`LLaMA-2` en 10 estudios [14 %], `LLaMA-3` en 4 [5 %]), **Google** (`PaLM-2`/`Bard` en 6 [8 %], `Gemini` en 4 [5 %]), **Anthropic Claude** (6 estudios, **8 %**) y **Mistral/Mixtral** (5 estudios, **7 %**).
  - **RQ3.2 Técnicas de Prompting (Tabla 10 y Fig. 10, p. 30-32)**:
    - **Zero-Shot Prompting**: **45 estudios (61 %)**.
    - **Few-Shot Prompting**: **27 estudios (36 %)**.
    - **Role / Persona Prompting**: **21 estudios (28 %)**.
    - **Chain-of-Thought (CoT)**: **16 estudios (22 %)**.
    - **Template / Structured Prompting**: **12 estudios (16 %)**.
    - Técnicas avanzadas minoritarias: **Self-Consistency / Reflexion / Iterative Refinement** (**6 estudios, 8 %**), **Tree-of-Thoughts / Prompt Chaining** (**4 estudios, 5 %**).
  - **RQ3.3 Arquitecturas y paradigmas de adaptación (Tabla 11, p. 33-34)**:
    - **Prompting directo de un solo modelo (*Prompt-based Standalone LLM*)**: **52 estudios (70 %)**.
    - **Fine-Tuning** (complejo o PEFT/LoRA): **9 estudios (12 %)**.
    - **Retrieval-Augmented Generation (RAG)**: **8 estudios (11 %)**.
    - **Sistemas Multi-Agente (*Multi-Agent Systems*)**: **solo 5 estudios (7 %)** (`[31, 33, 41, 68, 93]`).
  - **RQ3.4 Reporte de hiperparámetros (Tabla 12, p. 34-35)**:
    - **46 de los 74 estudios (62 %) NO reportan la temperatura ni ningún hiperparámetro de inferencia**, comprometiendo gravemente la reproducibilidad (p. 35, 51). Entre los 28 estudios (38 %) que sí reportan temperatura, los valores más frecuentes son $T = 0$ o $0,0$ (12 estudios, buscando determinismo), $T = 0,7$ (8 estudios) y $T \in [0,2, 0,5]$ (6 estudios).
- **RQ4.3 y RQ5 — Métricas de evaluación y Estrategias Empíricas (Tablas 15, 16 y 17, p. 41-48)**:
  - **Métricas cuantitativas más usadas (Tabla 15, p. 41-42)**: **Precision (35 estudios, 47 %)**, **Recall (34 estudios, 46 %)**, **F1-score (32 estudios, 43 %)**, **Accuracy (18 estudios, 24 %)**, **BLEU / ROUGE / METEOR (9 estudios, 12 %)**, **BERTScore / similitud coseno (7 estudios, 9 %)**, y métricas de acuerdo como **$\kappa$ de Cohen / Fleiss (8 estudios, 11 %)**.
  - **Tipo de evaluación de las salidas del LLM (Tabla 16 y Fig. 14, p. 43-45)**: **Métodos Cuantitativos (30 estudios, 42 %)**, **Métodos Mixtos cuantitativo + cualitativo (30 estudios, 42 %)** y **Métodos Cualitativos puros (12 estudios, 16 %)**. Los autores subrayan que en tareas generativas como Elicitación o Modelado no existe un único *ground truth* sintáctico a priori, por lo que es indispensable evaluar la adecuación semántica con jueces/rúbricas o métodos mixtos (p. 44).
  - **Estrategia empírica según la taxonomía de Stol y Fitzgerald [17] (Tabla 17 y Fig. 15, p. 45-47)**:
    - **Laboratory Experiments**: **56 estudios (76 %)**.
    - **Judgment Studies** (evaluación manual por 2–3 jueces expertos): **10 estudios (14 %)**.
    - **Field Studies**: **5 estudios (7 %)**.
    - **Experimental Simulations** (escenarios que imitan condiciones reales con sujetos o simulaciones interactivas): **solo 3 estudios (4 %, `[90, 31, 96]`)**.
    - **Sample Studies** y **Field Experiments**: **0 estudios (0 %)**.

**Insumo directo para ReqElicit-ES**
- **Respaldo bibliométrico directo de los 4 huecos de investigación (*Research Gaps*) que motivan nuestro TFG en el Capítulo de Estado del Arte**:
  1. *Escasez de estudios sobre transcripciones y entrevistas de elicitación conversacional*: aunque la fase de Elicitación ha subido al **22 % (16/74)** en LLM4RE, solo **2 de 74 estudios (3 %)** toman como entrada artefactos de entrevistas de elicitación (Tabla 7, p. 24) y solo **3 de 74 estudios (4 %)** emplean simulaciones experimentales interactivas (Tabla 17, p. 46).
  2. *Subexploración de arquitecturas multi-agente y razonamiento reflexivo/estructurado*: el **70 % (52/74)** de la literatura usa un único LLM con *prompting* simple (61 % *zero-shot*), mientras que los **sistemas multi-agente representan apenas el 7 % (5/74)** y las estrategias de refinamiento/planificación interna apenas el **5–8 %** (Tablas 10 y 11, p. 31-34). Esto posiciona a nuestros agentes **M1 ( árbol dinámico de objetivos + crítico + memoria de estado)** y **M2 (+ detección activa de conflictos/vaguedad + síntesis)** en la frontera del 7 % de arquitecturas agénticas avanzadas.
  3. *Brecha idiomática (ausencia de benchmarks en español)*: Zadenoori et al. identifican explícitamente en §6.4 (p. 53) que la concentración casi exclusiva en inglés y en los mismos dos datasets antiguos (`PURE` y `PROMISE`) limita la validez externa de LLM4RE, reclamando benchmarks públicos en otros idiomas (**ReqElicit-ES** responde directamente a este llamado).
  4. *Rigor de reproducibilidad (hiperparámetros y modelos abiertos)*: frente al **62 % de estudios que omiten la temperatura** y al **89 % que dependen exclusivamente de modelos cerrados de OpenAI** (p. 28, 35), nuestro TFG fijará y documentará explícitamente todos los hiperparámetros de inferencia (temperatura, *top-p*, semillas, presupuestos de tokens y llamadas por turno) sobre modelos de pesos abiertos.

---

### 4.2 NLP4RE: Systematic Mapping Study (Zhao et al., 2021)

**Referencia y año**
- Liping Zhao, Waad Alhoshan, Alessio Ferrari, Keletso J. Letsholo, Muideen A. Ajagbe, Erol-Valeriu Chioasca, Riza T. Batista-Navarro. *Natural Language Processing (NLP) for Requirements Engineering: A Systematic Mapping Study.* ACM Computing Surveys (CSUR), vol. 54, n.º 3, artículo 55, abril 2021 (manuscrito `arXiv:2004.01099v2`, 374 páginas incluyendo apéndices).

**Problema y fase de RE**
- **Estudio de Mapeo Sistemático (SMS) fundacional del campo NLP4RE (1983–abril 2019)**: estructura **36 años de investigación histórica** en procesamiento del lenguaje natural aplicado a ingeniería de requisitos a través de **5 preguntas de investigación (RQ1–RQ5)** sobre el estado de la literatura (RQ1), el estado de la investigación empírica (RQ2), el foco por fases de RE, tareas lingüísticas y documentos de entrada (RQ3), el estado de la práctica y herramientas desarrolladas (RQ4), y las tecnologías NLP habilitadoras: técnicas, herramientas y recursos léxicos/corpus (RQ5) (p. 6-7).

**Metodología / arquitectura agéntica**
- **Protocolo de mapeo sistemático** basado en Petersen et al. [68, 1278] y Kitchenham et al. [69, 88], ejecutado por un equipo de **4 inspectores de datos y 3 supervisores** (p. 7-12):
  1. **Bases de datos (5) + Google Scholar**: ACM Digital Library, IEEE Xplore, ScienceDirect, SpringerLink y ACL Anthology (restringida a los últimos 10 años, p. 7-8).
  2. **Proceso de selección (Fig. 1, p. 8-9)**:
     - Búsqueda inicial hasta abril de 2019: **11.489 resultados únicos** tras desduplicar en EndNote + **51** de Google Scholar = **11.540 registros**.
     - Filtrado E1–E2 (eliminando editoriales y *short papers* $< 6$ páginas en formato de una columna, Tabla 2, p. 8): **6.324 artículos**.
     - Filtrado por título, resumen, introducción y conclusión (E3–E4, excluyendo revisiones secundarias y artículos fuera de alcance): **1.012 estudios primarios**.
     - Lectura completa y verificación cruzada independiente por los 4 inspectores y los 3 supervisores (I1–I2): **416 preseleccionados $\rightarrow$ 404 estudios primarios definitivos** (tras eliminar 4 duplicados residuales y 8 fuera de alcance en la auditoría final de la supervisora principal, p. 9).
  3. **Esquema de clasificación facetado (Fig. 2 y Tablas 3–6, p. 9-11)**:
     - *Faceta de Publicación*: tipo, sede y año.
     - *Faceta de Investigación*: 5 tipos de investigación de Wieringa et al. [71] (`Solution Proposal`, `Validation Research`, `Evaluation Research`, `Philosophical/Opinion`, `Personal Experience`, Tabla 3, p. 10) y 9 métodos de evaluación de Chen y Babar [72] (`LESS` [Lab Experiment with Software Subjects], `LEHS` [Lab Experiment with Human Subjects], `Example Application`, `Case Study`, `Discussion`, `Experience Report`, `Field Experiment`, `Rigorous Analysis`, `Simulation`, Tabla 4, p. 10).
     - *Faceta de Foco*: 6 fases de RE de Cheng y Atlee [73] (`Elicitation`, `Analysis`, `Modeling`, `V&V`, `Management`, `Other [Testing/Design]`, Tabla 5, p. 11) y 6 tareas lingüísticas de NLP4RE adaptadas de Berry et al. [45] (`Detection`, `Extraction`, `Classification`, `Modeling`, `Tracing & Relating`, `Search & Retrieval`, Tabla 6, p. 11).
     - *Faceta de Contribución*: herramientas NLP4RE desarrolladas y tecnologías NLP empleadas (técnicas, herramientas y recursos).

**Datos, idioma y dominio**
- **Población analizada**: **404 estudios primarios** publicados entre **1983 y abril de 2019**, de los cuales el **88,61 % (358/404)** se publicaron a partir de **2004** (pasando de un ritmo de $\approx 2$ artículos/año entre 1983–2003 a $\approx 24$ artículos/año entre 2004–2018, Fig. 3, p. 12-13).
- **Recursos lingüísticos y corpus en NLP4RE (RQ5, Fig. 14 y p. 20-23, 28)**:
  - Solo se identificaron **25 recursos lingüísticos** en los 404 estudios, dominados por léxicos generales en inglés: `WordNet` (**66 estudios**), `VerbNet` (**9 estudios**) y `British National Corpus` (**7 estudios**) (p. 20).
  - **Ausencia crítica de recursos en otros idiomas y de corpus específicos de RE**: entre los 25 recursos, únicamente aparecen 2 recursos no ingleses en la cola larga (`GermaNet` para alemán y `Floresta Corpus` para portugués, usados 1–2 veces, p. 23) y solo 2 datasets clásicos de SE (`MODIS` y `CM-1`, además de `PURE` [2017] que se publicó como *short paper*, nota 14, p. 23).

**Métricas y resultados cuantitativos exactos**
- **RQ1 — Estado de la literatura (p. 12-13)**:
  - **Distribución por tipo**: artículos de congreso **58,17 % (235/404)**, artículos de revista **26,75 % (108/404)** y artículos de *workshop* **15,10 % (61/404)** (p. 12).
  - **Dispersión y sedes líderes (Fig. 4, p. 12-13)**: los 404 estudios se reparten en **170 sedes distintas**, pero las **12 sedes principales concentran el 45,05 % (182/404)** de toda la producción. Las 3 grandes sedes de RE (`RE`, `REFSQ` y `REJ`) acumulan el **25 %** del total, y las 5 grandes sedes de SE (`JSS`, `ASE`, `ICSE`, `IST`, `TSE`) más del **10 %**. En cambio, en toda la biblioteca de `ACL` solo se hallaron **2 estudios** (0,5 %), evidenciando la desconexión histórica entre las comunidades de NLP y RE (p. 13).
- **RQ2 — Estado de la investigación empírica (Tabla 7 y Figs. 5–6, p. 13-15)**:
  - **Tipos de investigación (sobre 404 estudios)**:
    1. `Solution Proposal`: **271 estudios (67,08 %)**.
    2. `Validation Research`: **70 estudios (17,33 %)**.
    3. `Evaluation Research` (en entorno real/industrial): **29 estudios (7,18 %)**.
    4. `Philosophical & Opinion`: **19 estudios (4,70 %)**.
    5. `Personal Experience`: **15 estudios (3,71 %)**.
  - **Métodos de evaluación (Tabla 7, p. 15)**:
    1. `LESS` (*Lab Experiment with Software Subjects*): **177 estudios (43,81 %)** (140 en *Solution Proposals* + 37 en *Validation Research*).
    2. `Example Application` (ejemplo ilustrativo sin experimento riguroso): **94 estudios (23,27 %)** (todos en *Solution Proposals*).
    3. `LEHS` (*Lab Experiment with Human Subjects*): **66 estudios (16,34 %)** (35 en *Solution Proposals* + 31 en *Validation Research*).
    4. `Case Study` industrial: **25 estudios (6,19 %)**.
    5. `Discussion`: **19 estudios (4,70 %)**.
    6. `Experience Report`: **15 estudios (3,71 %)**.
    7. `Field Experiment`: **4 estudios (0,99 %)**.
    8. `Rigorous Analysis`: **2 estudios (0,50 %)** y `Simulation`: **2 estudios (0,50 %)**.
  - En total, más del **60 % (243/404)** se evalúa en laboratorio (`LESS` + `LEHS`) y un **23,27 % (94/404)** solo con un ejemplo de juguete, frente a apenas un **7,18 % (29/404)** validado en la industria (`Case Study` + `Field Experiment`, p. 14).
- **RQ3 — Foco de NLP4RE por Fase, Tarea y Documento de Entrada (sobre los 370 estudios técnicos, excluyendo 34 de opinión/experiencia personal; Tabla 8 y Figs. 7–9, p. 14-17, 27)**:
  - **Distribución por fase de RE y su tarea lingüística central (Tabla 8, p. 16 y §6.1.3, p. 27)**:

| Fase de RE | Total estudios ($N=370$) | % | Detection | Classification | Extraction | Modeling | Tracing & Relating | Search & Retrieval | Tarea central de la fase |
|---|---|---|---|---|---|---|---|---|---|
| **Analysis** | **158** | **42,70 %** | **75** | 37 | 16 | 0 | 19 | 11 | **Detection** (defectos/ambigüedad) |
| **Management** | **62** | **16,76 %** | 7 | 16 | 4 | 0 | **26** | 9 | **Tracing & Relating** |
| **Elicitation** | **62** | **16,76 %** | 8 | 14 | **32** | 0 | 3 | 5 | **Extraction** (términos/conceptos) |
| **Modeling** | **61** | **16,49 %** | 0 | 0 | 3 | **58** | 0 | 0 | **Modeling** |
| **V&V** | **15** | **4,05 %** | 5 | 4 | 2 | 0 | 4 | 0 | — (repartido) |
| **Other (Testing)** | **9** | **2,43 %** | 2 | 2 | 4 | 0 | 1 | 0 | — |
| **Other (Design)** | **3** | **0,81 %** | 0 | 0 | 2 | 1 | 0 | 0 | — |
| **Total por tarea** | **370** | **100 %** | **97 (26,22 %)** | **73 (19,73 %)** | **63 (17,03 %)** | **59 (15,95 %)** | **53 (14,32 %)** | **25 (6,76 %)** | — |

  - **Documentos de entrada procesados (Fig. 9 y §6.1.3, p. 16-17, 27)**: de los 14 tipos de documentos identificados, **Requirements Specification (SRS)** domina con **239 de 370 estudios (64,59 %)**, mientras que artefactos tempranos o informales como **guiones/transcripciones de entrevistas (*interview scripts*), historias de usuario y documentos de dominio son marginales** (p. 27, 29).
- **RQ4 — Herramientas desarrolladas y brecha de disponibilidad (Tablas 9–10, p. 17-20, 28)**:
  - Se propusieron **130 herramientas con nombre propio**: `Modeling` (**34, 26,15 %**), `Detection` (**31, 23,85 %**, incluyendo `QuARS`, `ARM`, `SREE`, `AQUSA`), `Extraction` (**24, 18,46 %**, incluyendo `findphrases`, `AbstFinder`, `ELICA`), `Classification` (**20, 15,38 %**), `Tracing & Relating` (**15, 11,54 %**) y `Search & Retrieval` (**6, 4,62 %**).
  - **Disponibilidad real**: solo **15 de las 130 herramientas (11,54 %)** tenían enlace web localizable, y de ellas **solo 13 seguían accesibles** (1 bloqueada y `aToucan` cerrada con permiso, Tabla 10, p. 18, 20).
- **RQ5 — Tecnologías NLP empleadas (Figs. 12–20, p. 20-26, 28)**:
  - **231 tecnologías distintas**: **140 técnicas NLP**, **66 herramientas NLP** y **25 recursos lingüísticos**.
  - Dominio absoluto del procesamiento léxico-sintáctico clásico de los años 90: `POS tagging` (**187 estudios**), `Tokenization` (**81**), `Parsing` (**72**), `Stop-words removal` (**70**), `Term extraction` (**68**) y `Stemming` (**68**); herramientas `Stanford CoreNLP` (**80 estudios**), `GATE` (**35**), `NLTK` (**23**) y `OpenNLP` (**21**). El **45 % de las técnicas (63/140)**, el **78,79 % de las herramientas (52/66)** y el **48 % de los recursos (12/25)** se usaron solo 1 o 2 veces (*Long Tail*, p. 20).

**Insumo directo para ReqElicit-ES**
- **Marco histórico y conceptual para la Sección 2.1 del Capítulo de Estado del Arte (De NLP4RE a LLM4RE)**:
  1. *Por qué el NLP clásico no podía hacer elicitación conversacional*: los datos de la Tabla 8 (p. 16) demuestran que en las tres décadas de NLP4RE (1983–2019), el **16,76 % (62/370)** de estudios clasificados bajo «Elicitación» se limitaban en realidad a la tarea pasiva de **Extracción de términos/glosarios (`Extraction`, 32/62 estudios)** o **Clasificación de reseñas (`Classification`, 14/62)** sobre documentos ya escritos, porque la tecnología dominante (`POS tagging`, `CoreNLP`, `WordNet`) carecía de capacidad generativa, pragmática y de discurso para mantener una entrevista interactiva (p. 4, 16, 28).
  2. *Contraste cuantitativo directo NLP4RE (Zhao et al., 2021) vs. LLM4RE (Zadenoori et al., 2025)*: esta pareja de revisiones (coautoradas por Liping Zhao, Waad Alhoshan y Alessio Ferrari con el mismo esquema de clasificación) nos permite construir en la memoria del TFG una tabla comparativa exacta de la evolución de la disciplina:
     - **Fase de Elicitación**: sube del **16,76 %** (extracción léxica pasiva) al **22 %** (generación activa de preguntas, simulación de stakeholders y entrevistas multi-turno).
     - **Fase de V&V**: sube del **4,05 %** al **22 %**, mientras que **Analysis** (detección sintáctica de defectos) baja del **42,70 %** al **19 %**.
     - **Dependencia de SRS formales de entrada**: baja del **64,59 %** al **38 %**, abriendo paso a artefactos conversacionales e informales, aunque las **transcripciones de entrevistas siguen siendo un hueco crítico (solo 3 % en 2025)** que Zhao et al. ya reclamaban investigar en su hoja de ruta (§6.2.1, p. 29: *"interview scripts and models are still marginal in the research, while they have a primary role in practice"*).
  3. *Llamado a recursos abiertos, benchmarks compartidos y herramientas reproducibles (§6.2.1, p. 29)*: frente al **88,46 % de herramientas NLP4RE inaccesibles** (115/130 perdidas) y la ausencia de corpus en idiomas distintos del inglés, **ReqElicit-ES** se entrega como un paquete de código, prompts, rúbricas y dataset íntegramente abierto y ejecutable en español.

---

### 4.3 iReDev: Knowledge-Driven Multi-Agent Framework (Jin et al., 2025)

**Referencia y año**
- Dongming Jin, Weisong Sun, Jiangping Huang, Peng Liang, Jifeng Xuan, Yang Liu, Zhi Jin. *iReDev: A Knowledge-Driven Multi-Agent Framework for Intelligent Requirements Development.* arXiv:2507.13081v1, 17-07-2025 (Peking University, Nanyang Technological University, Chongqing University of Posts and Telecommunications y Wuhan University).
- Venue: preprint con plantilla de ACM TOSEM. ⚠️ Al igual que `ReqElicitGym` (del mismo primer autor, Dongming Jin, y directora, Zhi Jin), contiene metadatos de plantilla (`"Received 20 February 2007"`), por lo que debe citarse como preprint de arXiv.
- Código y paquete de replicación: `https://anonymous.4open.science/r/TOSEM-iReqDev` (p. 15).

**Problema y fase de RE**
- **Desarrollo de requisitos de extremo a extremo (*End-to-End Requirements Development*) mediante un sistema multi-agente guiado por conocimiento**: cubre **4 etapas secuenciales del desarrollo de requisitos** (Elicitación conversacional $\rightarrow$ Análisis y Modelado $\rightarrow$ Documentación de la SRS $\rightarrow$ Revisión y Validación, Fig. 1 y §3.1, p. 6-7), generando como artefactos finales una **Lista de Requisitos de Usuario (`URL`)**, **Modelos de Requisitos en PlantUML** (diagramas de casos de uso y de clases conceptuales) y una **Especificación de Requisitos de Software (`SRS`)** completa.

**Metodología / arquitectura agéntica**
- **Arquitectura de 6 agentes especializados + *Shared Artifact Pool* (pizarra compartida manejada por eventos) + *Human-in-the-Loop (HITL)* (Figs. 1–2 y Tabla 1, p. 6-14)**:
  1. **Estructura interna modular de cada agente (6 módulos, Fig. 2, p. 8)**:
     - `Profile`: define el rol profesional, responsabilidades y habilidades del agente.
     - `Monitor`: observa eventos en el *Shared Artifact Pool* según permisos de lectura/escritura.
     - `Thinking`: ejecuta razonamiento interno explícito (*Chain-of-Thought* privado, invisible para los demás agentes) antes de actuar.
     - `Memory`: almacena historial de corto plazo (conversación/iteración actual) y artefactos relevantes recuperados del pool.
     - `Knowledge`: módulo de conocimiento explícito de ingeniería de requisitos destilado de estándares y literatura (**ISO/IEC/IEEE 29148**, **IEEE 830**, **BABOK v3**, **5W1H**, **MoSCoW**, **cuestionamiento socrático**, **UML**, **Pohl [43]** y **Wiegers & Beatty [53]**, Tabla 1, p. 9-10).
     - `Action`: ejecuta acciones comunicativas (`Ask`, `Answer`, `Write`, `Review`, `Modify`) volcando los resultados al pool.
  2. **Los 6 agentes del ciclo de vida y su base de conocimiento (Tabla 1, p. 9-10)**:
     - **`Interviewer` (Fase de Elicitación)**: entrevista separadamente al `EndUser` y al `Deployer` y redacta el borrador inicial de la `URL` (*User Requirements List*). Su módulo de conocimiento integra **técnicas de entrevista semiestructurada, heurísticas 5W1H, sondeo socrático (*Socratic probing*), escucha activa con paráfrasis de confirmación y mapeo a tuplas `<Role|Goal|Behaviour|Constraint>`** (Fig. 3, p. 10, 12).
     - **`EndUser` (Stakeholder simulado — usuario final)**: responde a las preguntas del `Interviewer` desde la perspectiva de uso cotidiano, experiencia de usuario y flujos funcionales.
     - **`Deployer` (Stakeholder simulado — operador/desplegador)**: responde sobre restricciones de entorno operativo, seguridad, rendimiento, mantenimiento y despliegue (requisitos no funcionales y de sistema).
     - **`Analyst` (Fase de Análisis y Modelado)**: toma la `URL` validada por el humano, resuelve conflictos, prioriza con **MoSCoW**, construye los modelos de análisis en **PlantUML** (casos de uso + clases de dominio) y genera la lista de requisitos del sistema (`SRL`).
     - **`Archivist` (Fase de Especificación/Documentación)**: transforma la `URL`, los modelos y la `SRL` en un documento **SRS** estructurado conforme a **IEEE 830 / ISO 29148**.
     - **`Reviewer` (Fase de Validación y Verificación)**: audita los modelos y la SRS frente a una lista de comprobación de calidad (**completitud, consistencia, no ambigüedad, trazabilidad y verificabilidad**) y emite un informe de defectos (`Review Report`) que obliga al `Analyst` o al `Archivist` a iterar hasta su aprobación antes de pasar al humano.
  3. **Prompt literal del agente `Interviewer` (Fig. 3, p. 12)**:
     - **Restricción de ritmo conversacional**: `"4. Limit each question turn to no more than two questions to maintain a natural conversational flow."`
     - **Cadena de pensamiento interna (*Internal Chain of Thought (visible to the agent only)*, Fig. 3, p. 12)**:
       > `1. Identify stakeholder type and context.`
       > `2. Use 5W1H and targeted probes to surface goals, pain points, and constraints.`
       > `3. Map each utterance to <Role|Goal|Behaviour|Constraint> tuples.`
       > `4. Paraphrase key findings and request confirmation before proceeding.`
  4. **Mecanismo *Shared Artifact Pool* y *Human-in-the-Loop (HITL)* (§3.3–3.4, p. 13-14)**:
     - Cada artefacto en el pool se almacena como una tupla de 5 propiedades: `(content, role, state, sent_from, send_to)` (p. 13).
     - Existen **3 puntos de control HITL** donde un cliente o ingeniero humano revisa y aprueba o solicita cambios sobre: (1) la `URL` tras las entrevistas, (2) los modelos de análisis y `SRL`, y (3) la `SRS` final tras el visto bueno del `Reviewer` (p. 14).

**Datos, idioma y dominio**
- **Dataset de evaluación**: **10 proyectos de software reales/representativos** (aplicaciones web y de escritorio: sistemas de gestión hospitalaria, comercio electrónico, biblioteca, aprendizaje online, reserva de billetes, etc.) tomados del benchmark **AgileGen [56]**, cada uno con su descripción inicial y artefactos de referencia (*ground truth* de requisitos de usuario, diagramas de casos de uso y especificaciones SRS, Tabla 2, p. 15).
- **Idioma**: inglés.
- **Configuración experimental (§4.4, p. 16)**: modelo base `gpt-4-turbo-2024-04-09` con temperatura **$T = 0,3$**, `Top-P = 1,0` y `max_tokens = 4096` para todos los agentes y baselines. Se compara `GPT-4 + iReDev` contra tres baselines: `GPT-4 + zero-shot`, `GPT-4 + MetaGPT [19]` y `GPT-4 + Elicitron [8]` (este último aplicable solo en RQ1 para generación de listas de requisitos de usuario).

**Métricas y resultados cuantitativos exactos**
- **RQ1 — Calidad y diversidad de la Lista de Requisitos de Usuario (`URL`) tras la elicitación (Tabla 3, p. 17)**:
  - Se evalúa mediante dos métricas geométricas en el espacio de embeddings de los requisitos elicitados: **CHV (*Convex Hull Volume*, volumen de la envolvente convexa)**, que mide la amplitud/cobertura del espacio semántico explorado, y **MDC (*Minimum Distance to Center*, distancia mínima al centroide)**, que mide la especificidad y dispersión sin redundancia:

| Método | CHV (Volumen de Envolvente Convexa) $\uparrow$ | MDC (Distancia Mínima al Centro) $\uparrow$ | Mejora de `iReDev` en CHV | Mejora de `iReDev` en MDC |
|---|---|---|---|---|
| `GPT-4 + zero-shot` | 0,13 | 0,40 | +261,5 % | +55,0 % |
| `GPT-4 + MetaGPT` | 0,21 | 0,50 | +123,8 % | +24,0 % |
| `GPT-4 + Elicitron` | 0,32 | 0,55 | **+46,9 %** | **+12,7 %** |
| **`GPT-4 + iReDev`** | **0,47** | **0,62** | — | — |

- **RQ2 — Calidad de los Modelos de Requisitos (diagramas de casos de uso en PlantUML comparados contra *ground truth*; Tabla 4, p. 17)**:

| Método | F1-score (elementos del modelo) $\uparrow$ | BLEU $\uparrow$ | BertScore $\uparrow$ |
|---|---|---|---|
| `GPT-4 + zero-shot` | 0,025 | 0,045 | 0,387 |
| `GPT-4 + MetaGPT` | 0,109 | 0,063 | 0,442 |
| **`GPT-4 + iReDev`** | **0,389** | **0,102** | **0,593** |

  - `iReDev` multiplica por **3,57x el F1-score** de `MetaGPT` ($0,389$ vs. $0,109$) y supera su `BertScore` en **+15,1 puntos porcentuales** ($0,593$ vs. $0,442$).
- **RQ3 — Calidad de la Especificación de Requisitos de Software (`SRS`) final (similitud léxica/semántica + evaluación con juez LLM **G-Eval [31]** en escala Likert 1–5 sobre Completitud, Corrección y Cohesión; Tabla 5, p. 18)**:

| Método | BLEU $\uparrow$ | BertScore $\uparrow$ | Completeness (1–5) $\uparrow$ | Correctness (1–5) $\uparrow$ | Cohesiveness (1–5) $\uparrow$ |
|---|---|---|---|---|---|
| `GPT-4 + zero-shot` | 0,063 | 0,519 | 2,900 | 2,400 | 3,200 |
| `GPT-4 + MetaGPT` | 0,080 | 0,552 | 3,200 | 3,000 | 3,700 |
| **`GPT-4 + iReDev`** | **0,120** | **0,616** | **4,200** | **4,000** | **4,100** |

  - `iReDev` logra mejoras de **+1,00 punto sobre 5 en Completitud** ($4,200$ vs. $3,200$) y **+1,00 punto en Corrección** ($4,000$ vs. $3,000$) frente a `MetaGPT`, demostrando el impacto del bucle de auditoría del agente `Reviewer` y del módulo de conocimiento explícito de RE.

**Insumo directo para ReqElicit-ES**
- **Eslabón arquitectónico directo entre `Elicitron` (Lote 3), `ReqElicitGym` (Lote 1) y nuestros paquetes WP6 y WP7**:
  1. *Conexión genealógica de los autores (`iReDev` 2025 $\rightarrow$ `ReqElicitGym` 2026)*: `iReDev` es el trabajo previo del equipo de Dongming Jin y Zhi Jin (Peking University) antes de crear `ReqElicitGym`. Mientras que en `iReDev` propusieron una arquitectura multi-agente completa donde el `Interviewer` tenía un módulo de `Knowledge` y un `Thinking` (CoT privado), en `ReqElicitGym` se centraron en construir el entorno de evaluación del entrevistador pero solo probaron LLMs monolíticos en modo reactivo. En **ReqElicit-ES** unimos ambas líneas: llevamos la arquitectura agéntica guiada por conocimiento y memoria estructurada (nuestros agentes **M1** y **M2** en WP6 y el **Sintetizador con revisor QUS** en WP7) al banco de pruebas riguroso por capas de `ReqElicitGym` adaptado al español.
  2. *Diseño del razonamiento interno (`Thinking`) y paráfrasis de confirmación del `Interviewer` para WP6 (M1 y M2)*: la cadena de pensamiento interna de 4 pasos de la Fig. 3 (p. 12) —**(1)** identificar tipo de stakeholder y contexto, **(2)** aplicar sondeo 5W1H para descubrir objetivos, puntos de dolor y restricciones, **(3)** mapear cada intervención a tuplas estructuradas `<Role|Goal|Behaviour|Constraint>`, y **(4)** parafrasear hallazgos clave y pedir confirmación antes de avanzar— refuerza directamente el diseño de nuestra **memoria de estado en M1** y el mecanismo de **confirmación activa en M2**.
  3. *Separación entre `Interviewer`, `Archivist` y `Reviewer` como justificación de WP7*: `iReDev` demuestra empíricamente (Tabla 5, p. 18) que desacoplar la entrevista de la redacción estructurada (`Archivist`) y someter la especificación a un agente auditor con lista de comprobación de estándares (`Reviewer`) eleva la completitud y corrección en +1,0 punto sobre 5 frente a pipelines sin revisión explícita (`MetaGPT`). Nuestro **Sintetizador en WP7** incorpora exactamente ese patrón (extracción trazable + verificación de criterios de calidad QUS y de subcadenas literales).

---

### 4.4 Teaching RE Interviews: Learning from Mistakes (Bano et al., 2019)

**Referencia y año**
- Muneera Bano, Didar Zowghi, Alessio Ferrari, Paola Spoletini, Beatrice Donati. *Teaching Requirements Elicitation Interviews: An Empirical Study of Learning from Mistakes.* Requirements Engineering Journal (REJ), Springer, vol. 24, n.º 3, pp. 259–289, septiembre 2019 (versión extendida del artículo premiado en IEEE RE 2018 [13], p. 1). DOI: `10.1007/s00766-019-00313-0`.

**Problema y fase de RE**
- **Elicitación interactiva mediante entrevistas — Taxonomía empírica de errores de los analistas y su impacto en la calidad de las actas/requisitos**: investiga empíricamente qué errores cometen los analistas noveles al conducir entrevistas de elicitación de requisitos a lo largo de múltiples sesiones secuenciales, cómo evolucionan (o persisten) dichos errores tras recibir retroalimentación, y cómo impactan en las actas de reunión (*meeting minutes*) y en la especificación de requisitos final (`SRS`).

**Metodología / arquitectura agéntica**
- **Diseño empírico en dos estudios longitudinales (*Study 1* cualitativo + *Study 2* cuantitativo/cualitativo) basados en *role-playing* auténtico con múltiples entrevistas secuenciales (§3, p. 7-19)**:
  - En ambos estudios, estudiantes del *Master of Information Technology* (UTS, Australia) trabajaron en grupos de 3–4 personas realizando **3 entrevistas secuenciales de 15 minutos cada una** separadas por 1–2 semanas sobre un caso de estudio real:
    - **Entrevista 1**: con el patrocinador principal del proyecto (*Project Sponsor*, interpretado por la instructora/investigadora principal).
    - **Entrevistas 2 y 3**: con stakeholders secundarios / expertos técnicos o de negocio (interpretados por tutores entrenados con guiones estandarizados).
  - **Study 1 (descubrimiento y construcción de la taxonomía de errores, §3.2, p. 9-14)**:
    - **110 estudiantes en 28 grupos** sobre el `Case Study 1` (sistema de gestión y venta para una cafetería/restaurante universitario).
    - Triangulación cualitativa sobre la Entrevista 1 a partir de **4 fuentes independientes (14.380 palabras de notas + ~7 horas de audio + 28 actas de reunión, p. 10)**:
      1. Notas de observación en vivo en el aula (`4.451 palabras`).
      2. Reflexiones *think-aloud* del cliente tras cada entrevista (`1.635 palabras`).
      3. Evaluación ciega del audio por el Revisor Externo 1 (`4.748 palabras`).
      4. Evaluación ciega del audio por el Revisor Externo 2 (`3.546 palabras`).
    - Análisis temático iterativo que identificó **34 errores únicos agrupados en 7 categorías de alto nivel** (divididas en **3 categorías de Dominio de RE** y **4 categorías Sociales/Comunicativas**, Fig. 3, p. 11-12).
  - **Study 2 (seguimiento longitudinal a través de las 3 entrevistas con cuestionario estandarizado, §3.3, p. 16-19)**:
    - **138 estudiantes en 34 grupos** sobre el `Case Study 2` (sistema de gestión de prácticas profesionales / *internships* universitarios).
    - En la semana siguiente a la Entrevista 1, además del feedback general sobre las 7 categorías de errores, se obligó a cada grupo a revisar sus propias actas de la Entrevista 1 para identificar respuestas vagas o incompletas y preparar preguntas de seguimiento (*follow-up questions*) para las Entrevistas 2 y 3 (p. 17, 28).
    - Muestra estratificada de **9 grupos** (3 con la nota más alta en la SRS final, 3 con nota media y 3 con la nota más baja = **27 grabaciones de audio** correspondientes a las 3 entrevistas de los 9 grupos).
    - Cada una de las 27 entrevistas fue evaluada de forma independiente y ciega por **2 de 3 revisores externos** mediante un **cuestionario de 33 ítems en escala Likert de 5 puntos** (`1 = Strong Disagree` a `5 = Strong Agree`, donde mayor puntuación indica mayor presencia del error, Apéndice A, p. 18, 38-39) derivado de los 34 errores del Estudio 1.

**Datos, idioma y dominio**
- **Volumen total de sujetos y sesiones**: **248 estudiantes de posgrado (110 en Estudio 1 + 138 en Estudio 2)** distribuidos en **62 grupos (28 + 34)**, con **28 entrevistas + 28 actas** analizadas a fondo en el Estudio 1 y **27 entrevistas longitudinales (9 grupos $\times$ 3 sesiones)** puntuadas doblemente en el Estudio 2 (p. 9, 17-18).
- **Idioma**: inglés.
- **Dominios**: hostelería/restauración universitaria (`Case Study 1`) y gestión académica de prácticas en empresas (`Case Study 2`).

**Métricas y resultados cuantitativos exactos**
- **Taxonomía completa de 7 categorías y 34 errores de entrevista (Fig. 3, §4.1 y Apéndice A, p. 11-16, 38-39)**:
  - **A. Categorías relacionadas con el Dominio de RE (*Domain-related aspects*, 17 ítems en el cuestionario del Apéndice A)**:
    1. **`Question Formulation` (Formulación de preguntas — 6 ítems)**:
       - *Asking vague questions* (hacer preguntas vagas o ambiguas).
       - *Asking technical questions* (usar jerga técnica o preguntar detalles de implementación al cliente de negocio).
       - *Asking customer for solutions* (pedir al cliente que diseñe la solución técnica en vez de indagar su problema/necesidad).
       - *Asking long or complex questions* (formular preguntas múltiples o largas en un mismo turno).
       - *Asking leading or biased questions* (hacer preguntas dirigidas o sesgadas que fuerzan una respuesta).
       - *Asking irrelevant questions* (preguntas fuera del alcance del dominio o del rol del stakeholder).
    2. **`Question Omission` (Omisión de preguntas clave — 7 ítems)**:
       - *Not asking probing or follow-up questions* (no repreguntar ante respuestas superficiales o ambiguas).
       - *Not asking about the existing system / current process ("As-Is")* (no indagar cómo se realiza el trabajo actualmente ni qué problemas tiene).
       - *Not asking to identify other relevant stakeholders* (no preguntar qué otros perfiles o usuarios interactúan con el sistema).
       - *Not asking about project goals and success criteria* (no indagar el propósito de negocio ni los criterios de éxito).
       - *Not asking to prioritize features or requirements* (no explorar qué funciones son críticas frente a deseables).
       - *Not asking about constraints (budget, time, regulations, environment)* (omitir restricciones operativas o de negocio).
       - *Not asking about non-functional / quality requirements* (ignorar seguridad, usabilidad, rendimiento o fiabilidad).
    3. **`Order of Interview` (Orden y estructura de la entrevista — 4 ítems)**:
       - *Incorrect opening of the interview* (empezar abruptamente con detalles sin contextualizar el objetivo de la sesión).
       - *Asking questions in a wrong or unorganized logical order* (saltar erráticamente de un tema a otro sin hilo conductor).
       - *Poor time management* (agotar el tiempo en un único aspecto secundario dejando áreas enteras sin explorar).
       - *Incorrect ending of the interview / missing final summary* (cerrar la entrevista sin resumir ni confirmar los puntos acordados con el cliente).
  - **B. Categorías Sociales y de Interacción (*Social aspects*, 16 ítems en el cuestionario)**:
    4. **`Communication Skills` (4 ítems)**: lenguaje corporal inadecuado, voz inaudible/monótona, interrumpir al cliente, falta de claridad expresiva.
    5. **`Analyst Behaviour` (4 ítems)**: actitud poco profesional, nerviosismo/falta de confianza, leer mecánicamente una lista rígida de preguntas sin escuchar la respuesta (*reading from a script without listening*), discutir con el cliente.
    6. **`Customer Interaction` (3 ítems)**: *not building rapport* (no crear sintonía inicial), no mostrar escucha activa, ignorar pistas emocionales o de prioridad del cliente.
    7. **`Teamwork and Planning` (5 ítems)**: falta de preparación previa del dominio, solapamiento entre entrevistadores, un único miembro monopoliza o nadie toma notas.
- **Frecuencias exactas de los errores más graves en el Estudio 1 (sobre $N = 28$ grupos, §4.1, p. 11-16)**:

| Rango | Error específico | Categoría | Grupos afectados ($N=28$) | Porcentaje (%) |
|---|---|---|---|---|
| **1.º** | **Hacer preguntas vagas (*Asking vague questions*)** | `Question Formulation` | **21 / 28** | **75,0 %** |
| **2.º** | **Cierre incorrecto / omitir el resumen final de confirmación (*Incorrect ending / no summary*)** | `Order of Interview` | **19 / 28** | **67,9 %** |
| **3.º** | **No establecer sintonía inicial con el cliente (*Not building rapport*)** | `Customer Interaction` | **16 / 28** | **57,1 %** |
| **4.º** | **Apertura incorrecta / orden ilógico de preguntas (*Incorrect opening / wrong logical order*)** | `Order of Interview` | **15 / 28** | **53,6 %** |
| **5.º** | **No preguntar por otros stakeholders relevantes (*Not asking to identify other stakeholders*)** | `Question Omission` | **12 / 28** | **42,9 %** |

- **Resultados longitudinales del Estudio 2 (evolución entre las Entrevistas 1, 2 y 3 en los 9 grupos, §5 y §6, p. 19-29)**:
  - **Persistencia de los errores de dominio**: mientras que los errores sociales (`Communication Skills`, `Analyst Behaviour`, `Customer Interaction`) son moderados o mejoran con la familiaridad, las **3 categorías de dominio (`Question Formulation`, `Question Omission` y `Order of Interview`) concentran las mayores dificultades y NO mejoran automáticamente entre las 3 entrevistas** solo con experiencia o feedback teórico general (§5.1–5.2, p. 20-25).
  - **Efecto de la intervención focalizada sobre las actas (§6.4, p. 28-29)**: el único error de formulación que mostró una reducción clara del Estudio 1 al Estudio 2 fue *Asking vague questions* y la mejora en preguntas de sondeo (*probing questions*), gracias a obligar a los analistas a **auditar las lagunas y ambigüedades de sus notas previas antes de formular las siguientes preguntas**.
  - **Relación directa entre el resumen de cierre, las actas (*meeting minutes*) y la calidad de la SRS final (§6.2, p. 28)**: los autores demuestran que varios grupos que condujeron entrevistas aceptables pero **omitieron el resumen final de confirmación (*Incorrect ending*, 67,9 %)** produjeron actas de reunión incompletas o distorsionadas, y por el contrario, los **3 grupos con mayor calificación en la SRS final (`Top groups`)** destacaron sistemáticamente por una mejor formulación de preguntas de sondeo, menor omisión de categorías clave y una consolidación fiel de las notas de entrevista.

**Insumo directo para ReqElicit-ES**
- **Fundamentación teórica y empírica directa de la arquitectura de nuestros agentes entrevistadores (WP6) y de la conexión Entrevista $\rightarrow$ Síntesis (WP7)**:
  1. *Correspondencia exacta entre las 3 categorías de errores de dominio de Bano et al. y los módulos de nuestros agentes **M1** y **M2** en WP6*:
     - En una entrevista basada en texto con un LLM, las 4 categorías sociales desaparecen (postura, tono de voz, coordinación entre compañeros humanos), dejando exactamente las **3 categorías cognitivas de dominio de Bano et al. (`Question Formulation`, `Question Omission`, `Order of Interview`)**, que son precisamente las que los humanos no logran corregir sin soporte estructurado:
       - Contra **`Question Omission`** (olvidar áreas funcionales, restricciones, NFRs, estado actual o preguntas de sondeo): **M1** incorpora el **Árbol Dinámico de Objetivos y Memoria de Estado** (que rastrea qué ramas del dominio siguen sin cubrir o con respuestas superficiales).
       - Contra **`Question Formulation`** (hacer preguntas vagas [75 %], preguntas largas/múltiples, preguntas técnicas al cliente o pedirle soluciones): **M1** incorpora el **Módulo Crítico Pre-Emisión**, que filtra preguntas compuestas, jerga de implementación y formulaciones vagas antes de enviarlas al stakeholder.
       - Contra **`Order of Interview`** (orden caótico [53,6 %] y ausencia de cierre/resumen de confirmación [67,9 %]): **M1** estructura la progresión desde el contexto general hacia las ramas específicas del árbol, y **M2** añade explícitamente los **turnos de síntesis/confirmación parcial y final** para validar con el cliente los requisitos entendidos y resolver contradicciones.
  2. *Justificación empírica de nuestra pregunta de investigación sobre el acoplamiento WP6 $\rightarrow$ WP7 (§6.2, p. 28)*: el hallazgo de Bano et al. de que **una buena entrevista puede fracasar al generar la SRS si el registro/síntesis intermedio (`meeting minutes`) pierde información o carece de confirmación** justifica directamente por qué `ReqElicitGym` (que evalúa solo los turnos de diálogo sin sintetizar requisitos) es insuficiente y por qué **ReqElicit-ES** evalúa el pipeline completo desde la entrevista interactiva (WP6) hasta la especificación sintetizada y trazable (WP7).

---

### 4.5 From Elicitation Interviews to Software Requirements (Almeida et al., 2025)

**Referencia y año**
- Camila Almeida, Isaque Copque, Alvaro Oliveira, Murilo Arouca, Adriano Barbosa, Sávio Freire, Manoel Mendonça, Julio Cesar Leite (Universidade Federal da Bahia [UFBA] e Instituto Federal do Ceará [IFCE], Brasil). *From Elicitation Interviews to Software Requirements: Evaluating LLM Performance in Requirement Generation.* Proceedings of the 28th Workshop on Requirements Engineering (WER 2025), Río de Janeiro, Brasil, 20–22 de agosto de 2025, pp. 1–14. DOI: `https://doi.org/10.29327/1588952.28-12`.
- **Paquete de replicación (Zenodo)**: `https://doi.org/10.5281/zenodo.15080374` (p. 7).

**Problema y fase de RE**
- **Síntesis y especificación post-entrevista (*Requirements Generation from Elicitation Interviews*)**: evalúa cuantitativamente la capacidad de dos LLMs de última generación (`ChatGPT-4` y `DeepSeek-V3`) para generar y clasificar requisitos funcionales (`FUNC`) y no funcionales (`NONF`) directamente a partir de las transcripciones completas de entrevistas reales de elicitación conducidas en **portugués**, comparando los requisitos generados contra un oráculo (*ground truth*) elaborado y validado por ingenieros de requisitos humanos con los clientes reales.

**Metodología / arquitectura agéntica**
- **Diseño experimental en 4 etapas sobre entrevistas reales en portugués (§3 y Fig. 1, p. 5-9)**:
  1. **Conducción y transcripción de las entrevistas de elicitación (§3.2, p. 6-7)**:
     - Se realizaron entrevistas semiestructuradas de **$\approx 40$ minutos cada una** en **portugués** con los clientes reales de dos sistemas de software en producción/desarrollo en Brasil.
     - El guion de entrevista constaba de **25 preguntas diseñadas con el método 5W2H** (*What, Why, Who, Where, When, How, How much*): **15 preguntas genéricas de proceso/sistema** y **10 preguntas específicas del dominio de cada proyecto** (disponibles en el paquete de Zenodo, p. 6-7).
     - Las sesiones se grabaron en Google Meet, se transcribieron automáticamente con la herramienta `Tactiq` y fueron revisadas y corregidas manualmente por los investigadores eliminando datos sensibles (p. 7).
  2. **Construcción del Oráculo (*Ground Truth* humano, §3.2, p. 7)**:
     - Dos investigadores extrajeron manualmente los requisitos funcionales (`FUNC`) y no funcionales (`NONF`) de cada transcripción, un tercer investigador con $> 5$ años de experiencia los revisó, y finalmente **el cliente real de cada sistema validó el listado definitivo** para confirmar que reflejaba fielmente sus necesidades (p. 7).
  3. **Ingeniería de Prompts basada en patrones de White et al. [17] (Tabla 1, p. 7-8)**:
     - Se diseñó un prompt estructurado (*few-shot* con 5 componentes de White et al. [17]: `Persona`, `Context`, `Task`, `Input Format / Few-Shot Examples` y `Output Format`) ejecutado en las interfaces web de `ChatGPT-4` y `DeepSeek-V3`:
       - **Persona y Contexto**: `"Act as a Requirements Analyst... Analyze the interview transcript between a requirements analyst and a stakeholder..."` (Tabla 1, p. 7).
       - **Plantillas obligatorias de salida (`Output Format`, Tabla 1, p. 7)**:
         - `"Functional Requirements: The system must [verb + object] + [optional condition]"`
         - `"Non-Functional Requirements: The system must [verb + object] + [condition] + [optional restriction]"`
  4. **Evaluación de correspondencia semántica contra el Oráculo (§3.4 y Fig. 2, p. 8-9)**:
     - Los autores realizaron un emparejamiento manual en pares (revisado por un tercer experto) entre cada requisito generado por el LLM y los requisitos del oráculo, contabilizando:
       - **Verdaderos Positivos ($TP$)**: requisitos del oráculo cubiertos correctamente por el LLM. ⚠️ *Nota metodológica crucial (p. 10)*: cuando un LLM generó un **requisito compuesto** (p. ej., *"los superadministradores deben poder realizar todas las funciones de gestión de usuarios, eventos y certificados"*), los autores contaron como $TP$ cada uno de los múltiples requisitos atómicos del oráculo abarcados por esa frase compuesta, lo que explica que en el sistema WEPGCOMP la suma $TP + FN$ supere ligeramente el tamaño nominal del oráculo (p. 10).
       - **Falsos Positivos ($FP$)**: requisitos generados por el LLM que **no corresponden a ningún requisito del oráculo** (alucinaciones/invenciones fuera de lo dicho en la entrevista) o que fueron **mal clasificados entre `FUNC` y `NONF`** (p. 8-9).
       - **Falsos Negativos ($FN$)**: requisitos del oráculo omitidos por el LLM.

**Datos, idioma y dominio**
- **2 sistemas reales brasileños con entrevistas en portugués (§3.2 y Tabla 2, p. 6-7)**:
  1. **WEPGCOMP** (*Workshop de Estudantes de Pós-Graduação em Ciência da Computação* — sistema web académico para gestionar la inscripción, envío de artículos, asignación de evaluadores, programación de sesiones y emisión de certificados del taller anual de doctorado de la UFBA):
     - **Oráculo validado**: **46 requisitos totales** (**40 funcionales [`FUNC`]** y **6 no funcionales [`NONF`]**).
  2. **+Lugar** (plataforma geocollaborativa gamificada para que ciudadanos e inspectores de salud pública registren y mapeen focos de vectores de enfermedades zoonóticas y arbovirosis en barrios urbanos):
     - **Oráculo validado**: **34 requisitos totales** (**24 funcionales [`FUNC`]** y **10 no funcionales [`NONF`]**).
- **Total del benchmark**: **2 entrevistas completas en portugués ($\approx 80$ min en total)** y **80 requisitos validados en el oráculo (64 `FUNC` + 16 `NONF`)**.
- **Disponibilidad**: guiones 5W2H, prompts y hojas de evaluación abiertos en Zenodo (`https://doi.org/10.5281/zenodo.15080374`); transcripciones anonimizadas por privacidad (p. 7).

**Métricas y resultados cuantitativos exactos**
- **Volumen de requisitos generados por cada LLM frente al Oráculo (Tabla 2 y Tabla 3, p. 7, 9)**:

| Sistema | Fuente / Modelo | Requisitos Funcionales (`FUNC`) | Requisitos No Funcionales (`NONF`) | Total de Requisitos |
|---|---|---|---|---|
| **WEPGCOMP** | **Oráculo Humano (Ground Truth)** | **40** | **6** | **46** |
| **WEPGCOMP** | `ChatGPT-4` | 26 | 16 | **42** |
| **WEPGCOMP** | `DeepSeek-V3` | 15 | 15 | **30** |
| **+Lugar** | **Oráculo Humano (Ground Truth)** | **24** | **10** | **34** |
| **+Lugar** | `ChatGPT-4` | 17 | 11 | **28** |
| **+Lugar** | `DeepSeek-V3` | 15 | 15 | **30** |

- **Resultados exactos de $TP, FP, FN$, Precisión, Recall y F1-score por sistema y modelo (Tablas 4 y 5, p. 10-11)**:

| Sistema | Modelo | $TP$ | $FP$ | $FN$ | Precisión (%) | Recall (%) | F1-score (%) |
|---|---|---|---|---|---|---|---|
| **WEPGCOMP** (Oráculo = 46) | **`ChatGPT-4`** | **21** | 25 | 28 | 46,00 % | **42,00 %** (43 % en texto, p. 10) | **44,00 %** |
| **WEPGCOMP** (Oráculo = 46) | **`DeepSeek-V3`** | 18 | **18** | 32 | **50,00 %** | 36,00 % | 42,00 % |
| **+Lugar** (Oráculo = 34) | **`ChatGPT-4`** | **21** | **7** | **13** | **75,00 %** | **61,76 %** (62 % en texto, p. 10) | **67,74 %** (68 % en texto) |
| **+Lugar** (Oráculo = 34) | **`DeepSeek-V3`** | 18 | 12 | 16 | 60,00 % | 52,90 % (53 % en texto, p. 11) | 56,30 % (56 % en texto) |
| **Promedio global** | **`ChatGPT-4`** | 21,0 | 16,0 | 20,5 | **60,50 %** | **51,88 %** | **55,87 %** |
| **Promedio global** | **`DeepSeek-V3`** | 18,0 | 15,0 | 24,0 | 55,00 % | 44,45 % | 49,15 % |

- **Hallazgos cualitativos y análisis de fallos clave reportados por los autores (§4, p. 9-12)**:
  1. **Sesgo de plantilla simétrica e inflación de NFRs en `DeepSeek-V3` (p. 9, 11)**: en ambos proyectos, `DeepSeek-V3` generó exactamente **15 requisitos funcionales y 15 no funcionales (30 en total)** con independencia del contenido real de la entrevista. En **+Lugar**, los **15 `FUNC` generados por `DeepSeek-V3` fueron todos Verdaderos Positivos ($15/15 = 100\%$ de precisión funcional)**, pero de los **15 `NONF` generados, solo 3 eran Verdaderos Positivos y 12 eran Falsos Positivos ($3/15 = 20\%$ de precisión en NFRs)** (p. 11), bien porque el modelo inventó restricciones no mencionadas en la entrevista o porque disfrazó requisitos funcionales como no funcionales para rellenar su cuota implícita de 15 elementos.
  2. **Sobre-generación de NFRs también en `ChatGPT-4` en WEPGCOMP (p. 9-10)**: mientras que el oráculo de WEPGCOMP solo tenía **6 `NONF`** (y 40 `FUNC`), `ChatGPT-4` generó **16 `NONF`** (casi el triple de los reales) y solo **26 `FUNC`**, provocando 25 falsos positivos y hundiendo su precisión al **46,00 %**.
  3. **Problema de los requisitos compuestos (*Compound Requirements*) que violan la atomicidad (p. 10)**: ambos LLMs agruparon con frecuencia múltiples acciones o roles mencionados a lo largo de la entrevista en una única sentencia paraguas (p. ej., permisos globales del superadministrador), ocultando reglas de negocio específicas y dificultando la trazabilidad 1 a 1 con el oráculo.
  4. **Sensibilidad a la dispersión conversacional (WEPGCOMP vs. +Lugar, p. 10-12)**: en **+Lugar** (donde el cliente describió flujos ciudadanos autocontenidos), `ChatGPT-4` alcanzó **75,00 % de precisión y 67,74 % de F1**, mientras que en **WEPGCOMP** (donde el flujo académico dependía de múltiples roles e idas y vueltas en la entrevista), el F1 de ambos modelos cayó al **42–44 %**, perdiendo más de la mitad de los requisitos funcionales del oráculo ($\text{Recall} = 36\%\text{–}42\%$).

**Insumo directo para ReqElicit-ES**
- **Referente iberoamericano directo (WER 2025) y validación cruzada para el diseño de nuestro Sintetizador en WP7**:
  1. *Posicionamiento en la comunidad iberoamericana de Ingeniería de Requisitos (WER)*: este artículo de **WER 2025** demuestra el interés actual de la comunidad iberoamericana por evaluar LLMs en transcripciones de entrevistas en lenguas romances (**portugués** en Almeida et al., **español** en **ReqElicit-ES**). Además, mientras Almeida et al. evalúan solo **2 entrevistas estáticas** pasando toda la transcripción de golpe en una ventana de chat (*single-pass prompt*), **ReqElicit-ES** evalúa el ciclo completo (entrevista multi-turno + síntesis) a escala sistemática con modelos abiertos reproducibles.
  2. *Explicación empírica de por qué el prompting monolítico de una sola pasada falla en entrevistas largas ($\text{F1} = 42\%\text{–}68\%$) y cómo lo corrige nuestro WP7*:
     - **Por qué ocurren los Falsos Negativos ($\text{Recall} = 36\%\text{–}62\%$)**: al volcar una transcripción de 40 minutos en un único prompt (`ChatGPT-4` o `DeepSeek-V3`), el modelo sufre un efecto de truncamiento/compresión de lista (fijando topes artificiales como los `15 FUNC + 15 NONF` de `DeepSeek-V3`) y fusiona detalles en requisitos compuestos. Nuestro **Paso 1 de extracción por bloques de turnos `(pregunta, respuesta)`** (inspirado en *Generative Goal Modeling* [3.2]) evita este cuello de botella de longitud de salida.
     - **Por qué ocurren los Falsos Positivos en NFRs ($12/15$ FPs en `DeepSeek-V3` en +Lugar)**: cuando se pide en un mismo prompt una lista abierta de `Functional Requirements` y `Non-Functional Requirements`, los LLMs rellenan la sección de NFRs con alucinaciones genéricas de calidad (seguridad, rapidez, disponibilidad) no mencionadas por el cliente o reclasifican funciones como NFRs. Esto confirma de forma independiente la regla de **RECOVER (3.3)** y **LENS (3.4)** que aplicaremos en **WP7**: **exigir cita literal verificable (`excerpt` + `turn_id`) para cada requisito extraído y prohibir explícitamente generar NFRs genéricos o cuotas fijas de requisitos si el cliente no los ha verbalizado en la entrevista**.
     - **Por qué el criterio `Atomic` de QUS (LENS, 3.4) es indispensable**: el hallazgo de Almeida et al. (p. 10) de que los requisitos compuestos rompen la correspondencia 1-a-1 con el oráculo justifica que nuestro **Paso 2 del Sintetizador (WP7)** desglose obligatoriamente cualquier sentencia con conjunciones o múltiples operaciones CRUD en requisitos atómicos individuales antes de evaluarlos contra el *ground truth*.

---

## Decisiones validadas tras el Lote 4 (Cierre del Paso 1 de WP1)

Con los 4 lotes completados y los **15 artículos** de `docs/papers/` más las **2 fuentes del contexto español** (*Salamandra Technical Report* [Gonzalez-Agirre et al., 2025] y *UPM Requirements Elicitation Experimental Dataset* [Aranda et al., 2025]) consolidados, se fijan las siguientes directrices de alineación arquitectónica para los entregables del **Paso 2 de WP1** (`docs/estado_arte.md` y `docs/matriz_comparativa.md`):

1. **Estilo = colores (del Lote 1 — WP2/WP3)**: si la auditoría de datos en WP2 confirma que la capa `Style` en `ReqElicitGym` contiene casi exclusivamente paletas de colores heredadas de `WebGen-Bench`, enriqueceremos la dimensión `estilo` en los escenarios nativos de `ReqElicit-ES` (maquetación, tipografía, densidad, tono visual) y desglosaremos el análisis en *color* vs. *no color*.
2. **Métrica IRE de revelación (del Lote 1 — WP5/RQ3)**: incluir el ratio de revelación efectiva del simulador de cliente junto al IRE de formulación de pregunta al comparar los 5 perfiles conductuales de stakeholder en RQ3.
3. **Configuración de los baselines B2 y B3 en WP6 (del Lote 2)**:
   - **B2 (`LLMREI`)**: implementar `LLMREI-long` adaptando el `{Interview Cookbook}` de Zenodo al español, pero restringiendo su regla original de «1 o 2 preguntas» a **exactamente 1 pregunta por turno** para mantener paridad estricta con el entorno y con `B0`, `B1`, `B3`, `M1` y `M2`.
   - **B3 (`Follow-Up Questions`, Shen et al., 2025)**: fijar el modo **`B3-SingleCall`** (1 llamada por turno) sobre los **últimos 4 turnos** (que cubren el **98,6 %** de las dependencias contextuales), con roles `INTERVIEWER`/`INTERVIEWEE` en **MAYÚSCULAS**, los **9 criterios de encuadre redactados en positivo** y selección condicional de los 5 criterios de seguimiento.
4. **Alineación arquitectónica de M1 y M2 en WP6 (consolidada con Lotes 2, 3 y 4)**:
   - Mantener estrictamente la arquitectura de **estado estructurado por 7 dimensiones** de la especificación del TFG (**`actores`, `flujos`, `contenido`, `reglas`, `restricciones`, `estilo` y `datos`**), el **planificador `clarificar/indagar`**, el **guardarraíl de 1 pregunta por turno** (y prohibición de pedir PII) y el **criterio explícito de parada**.
   - Integrar **dentro de esas 7 dimensiones** la taxonomía de errores de dominio de **Bano et al. (2019)** (*Question Omission*, *Question Formulation* [75,0 % de preguntas vagas] y *Order of Interview* [67,9 % de cierres incorrectos sin resumen]) y el mapeo de tuplas `<Role|Goal|Behaviour|Constraint>` de **iReDev (Jin et al., 2025)**:
     - **M1** mitiga *Question Omission* rastreando la cobertura y completitud de tuplas `<Role|Goal|Behaviour|Constraint>` en las 7 dimensiones (`actores`, `flujos`, `contenido`, `reglas`, `restricciones`, `estilo`, `datos`), utiliza el planificador `clarificar/indagar` para decidir si resolver vaguedad en el último turno o explorar una dimensión vacía, aplica un filtro crítico de formulación contra *Question Formulation*, y activa su criterio de parada cuando las 7 dimensiones alcanzan suficiencia.
     - **M2** extiende M1 contra los errores de *Order of Interview* (67,9 % sin resumen final en Bano et al.) y contra perfiles contradictorios añadiendo detección activa de conflictos en el estado de 7 dimensiones y **turnos explícitos de resumen y confirmación con el cliente** inspirados en los puntos de control de `iReDev`.
5. **Arquitectura del Sintetizador en WP7 (consolidada con Lotes 3 y 4)**:
   - Pipeline en **2 pasos** para evitar el sesgo posicional, el truncamiento de listas y la sobre-generación de NFRs observados en **Almeida et al. (4.5)**:
     - **Paso 1 (Extracción local trazable por ventana deslizante)**: extracción de candidatos y citas literales (`turn_ids` + `quotes`) mediante ventana deslizante de **4 turnos con paso 2** (**Generative Goal Modeling, 3.2**), filtrando menciones de trabajo manual *As-Is* (66 % de FPs en **LENS, 3.4**), automatización existente (17 % de FPs) y coletillas de confirmación no validadas (17 % de FPs), y prohibiendo inventar NFRs no verbalizados (**RECOVER, 3.3** y **Almeida et al., 4.5**).
     - **Paso 2 (Consolidación aglomerativa, atomicidad QUS y verificación determinista)**: deduplicación semántica y formateo como Historias de Usuario (`Como [rol], quiero [objetivo], para [beneficio]`) bajo los **13 criterios QUS** (**LENS, 3.4**, forzando el criterio `Atomic` para evitar los requisitos compuestos de **Almeida et al., 4.5**), seguido de la comprobación automática de subcadenas (`trace_correctness` de **Generative Goal Modeling, 3.2**).





