# EXP-07 — Cómo Fable 5 descompone un problema de trading algorítmico

**Fecha:** 2026-07-14 22:12 UTC
**Modelo usado:** claude-fable-5
**Run número:** 7 (abre FASE 2 — Patrones de razonamiento)

## Pregunta / Prompt enviado a Fable 5

> Muéstrame cómo descompones un problema de trading algorítmico. Toma un caso concreto — "tengo una señal que creo que predice retornos de corto plazo en un activo líquido; conviértela en una estrategia operable y dime si es real" — y muestra tu proceso real de razonamiento: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica

La petición trae dos verbos que esconden trampas distintas:

1. **"convierte la señal en una estrategia operable"** — presupone que la señal es la parte difícil y la estrategia es un envoltorio mecánico. Es al revés. Una señal que predice retornos y una estrategia que gana dinero están separadas por costos, capacidad, ejecución y decaimiento — y ahí es donde muere la mediana de las señales. La palabra "operable" carga todo el peso y la petición la trata como un adverbio.
2. **"dime si es real"** — clase F en su forma más pura (EXP-04): la conclusión esperada viene incrustada. El usuario ya cree que la señal predice; me está pidiendo confirmación, no evaluación. Si construyo la estrategia *para* la señal, el análisis se vuelve abogacía y encontraré la evidencia que la sostiene.

Reformulo antes de tocar nada: **no** "construye la estrategia que opera esta señal", sino **"estima el edge neto de costos, ajustado por riesgo y fuera de muestra, de esta señal; y solo si sobrevive, dimensiónala."** Y "real" no es una propiedad de la señal: es lo que queda **después** de agotar todas las formas en que puede ser falsa. Eso es la escalera de artefactos de EXP-04 — pero el trading tiene su propia escalera, con un peldaño que ningún otro dominio tiene, y encontrarlo es el trabajo del Paso 1.

### Paso 1 — La asimetría estructural: el backtest es un oráculo que miente

Aplico el método de EXP-04/EXP-06: para diseñar en un dominio nuevo, compáralo contra el dominio resuelto más cercano y localiza qué tiene uno que al otro le falta. El vecino más cercano del trading es **análisis de datos (EXP-04)**: ambos buscan señal en ruido sin garantía mecánica. Comparo:

| | Código (EXP-03) | Datos (EXP-04) | Trading (EXP-07) |
|---|---|---|---|
| ¿Oráculo ejecutable? | Sí — el runtime, **honesto** | No existe | **Existe (el backtest) y MIENTE** |
| Dirección del sesgo del oráculo | ninguno | — | **siempre optimista, por construcción** |
| ¿El dato reacciona a ti? | no | no | **sí — tu orden mueve el precio; el edge decae al usarlo** |
| Nº de historias realizadas | ∞ (recorres el input) | 1 dataset, re-consultable | **1 sola historia de mercado, irrepetible** |
| ¿Costos? | — | footnote | **primer orden — exceden el edge bruto en el caso mediano** |
| Sustituto/antídoto del oráculo | — | protocolo adversarial | **tratar el backtest como sospechoso primario, no como juez** |

De la tabla salen cuatro rasgos estructurales, y cada uno reordena la descomposición:

**(a) El oráculo miente en una dirección conocida.** En código el runtime es honesto (EXP-03): si el test pasa, pasó. El backtest también devuelve un número preciso —Sharpe, PnL, drawdown— y *se siente* igual que el runtime. Pero está sesgado al alza **por construcción**: lookahead, survivorship, y sobreajuste a la única historia que existe. La consecuencia para el principio diferencial (EXP-05): mis dos vistas **no pueden ser ambas "el backtest"**. Necesito una vista que el backtest estructuralmente no pueda ver — fuera de muestra genuino, o un modelo de costos/capacidad que el backtest ignora. Optimizar contra el backtest es optimizar la mentira.

**(b) El dato es reflexivo.** En análisis de datos el dato es inerte. Aquí mi propia orden mueve el precio (slippage, impacto de mercado) y, si el edge es real, otros lo encuentran y decae (alpha decay). El objeto que estimo es **no estacionario y adversarial**: la estrategia cambia la distribución sobre la que fue estimada. Ningún dataset de EXP-04 hace esto.

**(c) n = 1.** Tengo exactamente una historia realizada del mercado. La validación cruzada sobre ella **no es independiente**: los folds comparten régimen, comparten los mismos crashes, comparten la misma década alcista. Esto le pone dientes a la advertencia de EXP-05 ("las dos vías deben ser independientes en su *supuesto*, no solo en su cálculo"): dos cortes temporales de una serie de precios comparten el supuesto "este régimen persiste" y dan **falso acuerdo**.

**(d) Los costos son de primer orden, no una corrección.** En casi todo dominio los costos son un pie de página. Aquí, spread + comisión + impacto + financiación exceden con frecuencia el edge bruto. Una señal con poder predictivo **real** y edge neto **negativo** es el caso mediano. Por eso los costos no se verifican al final: gatean todo el pipeline.

Conclusión del Paso 1, que organiza el resto: **el backtest no es el oráculo, es el sospechoso primario.** La descomposición correcta no maximiza el número que da el backtest — lo somete a interrogatorio, empezando por las preguntas que más señales matan y más barato cuestan.

### Paso 2 — Descomposición ordenada por "kill-cheapness" (fail-fast)

En arquitectura (EXP-06) el orden era costo de reversión. Aquí el principio de orden es distinto: **la mayoría de las señales están muertas, así que ordena los subproblemas por cuán barato y cuán probablemente matan la señal.** Front-load los refutadores de mayor tasa de mortalidad y menor costo (es el chequeo refutador más barato de EXP-01 aplicado a un pipeline entero). No construyas infraestructura de ejecución para una señal que no tiene edge tras costos.

1. **Auditoría de lookahead y point-in-time (el más barato, el que más mata).** *Antes de cualquier número de performance:* ¿la señal es computable en el instante de decisión con solo la información disponible entonces? ¿Usa el close para decidir una operación que se llena al close? ¿Usa fundamentales *reexpresados* que en su momento no se conocían? Una señal que hace trampa temporal está muerta al llegar — y su backtest se ve **espectacular** precisamente porque hace trampa. Bloqueante. Mata ~40% de candidatas aquí, gratis.

2. **¿Sobrevive a costos y capacidad?** Neto = bruto − (spread/2 + comisión + impacto·tamaño + borrow). Modela el impacto como función de la tasa de participación en el volumen. Una señal con 4 bps de edge bruto por trade y 3 bps de costo round-trip es marginal; con 2 bps es negativa. Y capacidad: ¿a qué AUM tu propio impacto se come el edge? Esto gatea **antes** de optimizar nada.

3. **¿El edge sobrevive fuera de muestra, deflactado por grados de libertad?** Corte **temporal**, nunca aleatorio (el CV aleatorio filtra en series de tiempo — punto (c)). Walk-forward. Y el chequeo más profundo, que es la clase G de EXP-04 elevada a estrategias: ¿cuántas variantes probé antes de quedarme con esta? Si escaneé 200 configuraciones y guardé la mejor, su Sharpe de backtest es un **estadístico de orden (máximo de 200)**, no una estimación. Deflacta por el número probado (Sharpe deflactado / Bailey-López de Prado). El ruido puro con umbral fijo produce "hallazgos" con P→1 al crecer las comparaciones (medido en EXP-04); aquí cada parámetro afinado es una comparación.

4. **¿El PnL es atribuible a la tesis o a un factor de riesgo oculto?** ¿El "edge" es en realidad beta, short-vol disfrazado, o un tilt de tamaño/valor? Regresa los retornos contra factores conocidos; el alpha es el **residuo**. Una estrategia secretamente short-vol se ve brillante durante años y luego revienta — es el peldaño "evento conocido" de la escalera, pero el evento (el régimen que aún no ocurrió en tu muestra) está en el futuro.

5. **Realismo de ejecución.** Los fills al midpoint son ficción: modela posición en cola, fills parciales y **selección adversa** — te llenan justo cuando el mercado está por moverse en tu contra. El backtest asume que operas contra un mercado que no reacciona; el punto (b) dice que sí reacciona.

6. **Dimensionamiento y riesgo (solo ahora).** Vol targeting / fracción de Kelly hacia abajo, con la **incertidumbre de la estimación** incorporada: no conoces el Sharpe verdadero, así que dimensiona para la **cota inferior de confianza**, no para el puntual. Sobredimensionar por un Sharpe sobreestimado es cómo un edge real igual te arruina.

El orden es deliberado: 1–2 son baratos y matan la mayoría; 3–4 son la vista diferencial; 5–6 solo valen la pena si sobrevivió lo anterior. Gastar el análisis en 5–6 sobre una señal que muere en 1 es el anti-patrón (el espejo del bikeshedding de EXP-06).

### Paso 3 — Hipótesis consideradas y descartadas

**H0 — "Empieza optimizando los parámetros de la estrategia para maximizar el Sharpe del backtest."**
*Descartada — es la trampa canónica y además invierte el orden.* Maximizar el Sharpe in-sample es ajustar ruido; cada parámetro que afino gasta un grado de libertad contra mi única historia. Si el backtest es el oráculo que miente (Paso 1a), optimizar contra él optimiza la mentira. El movimiento correcto es el opuesto: **minimizar grados de libertad**, no maximizar el ajuste. Esta es la inversión más importante del experimento — el instinto ingenuo (subir el número) es exactamente el generador del sobreajuste.

**H1 — "Confía en la validación cruzada para un estimador insesgado."**
*Descartada por la regla de independencia-de-supuesto (EXP-05).* K-fold aleatorio sobre una serie de precios filtra por dos vías: los puntos adyacentes están autocorrelacionados, y todos los folds comparten el mismo régimen de mercado. Dos vistas que comparten el supuesto "régimen alcista 2020–2024" dan un acuerdo falso. La única segunda vista real es genuinamente fuera de muestra (posterior, no vista, idealmente otro régimen) o forward-test en papel/vivo.

**H2 — "Los costos son un haircut que aplico al final."**
*Descartada — los costos son de primer orden y gatean todo (Paso 1d).* Aplicarlos al final significa construir infraestructura para una estrategia ya muerta. Se reordena: costos son el paso 2, no el 6.

**H3 — "Un Sharpe de backtest alto (>3) significa una estrategia fuerte."**
*Descartada, y es una inversión.* De la lista de alertas de EXP-04: Sharpe > 5 en datos de mercado real es casi siempre peldaño 1–2 (lookahead o fills sin costo), no peldaño 6 (señal real). Una curva de equity sospechosamente limpia es evidencia **en contra**, por la heurística de "demasiado limpio" (EXP-05). El prior correcto: los edges reales son pequeños, ruidosos y decaen.

**H4 — "Más datos / más historia siempre es mejor."**
*Descartada parcialmente.* Más historia ayuda a estimar, pero los regímenes viejos pueden ser irrelevantes: la microestructura cambió, el alpha ya decayó, el venue no existía. Entrenar ciegamente sobre 20 años asume la estacionariedad que el trading específicamente viola (punto b/c). Es triage: historia larga para riesgo de cola y exposición a factores; historia reciente para la magnitud del edge.

**H5 — "El objetivo es maximizar el retorno."**
*Descartada como formulación.* El retorno sin su denominador de riesgo no es una función objetivo operable: apalancar cualquier edge positivo sube el retorno esperado hasta que la ruina lo termina. La cantidad correcta es retorno ajustado por riesgo **neto de costos y bajo restricción de drawdown/ruina** — que es la reformulación del Paso 0.

### Paso 4 — Materialización y falsificación: el mini-caso que hace chocar dos de mis reglas

El output limpio es sospechoso (H2 de EXP-05), y el refutador más barato de un conjunto de reglas es correrlas contra un caso concreto (EXP-06). Tomo una señal juguete: **"compra cuando el RSI de 5 min < 30 en un large-cap líquido, vende al close."**

- **Lookahead:** ¿"al close" usa el precio de close para *decidir*? Si computo el RSI con la barra del close y opero a ese mismo close, es un lookahead de 1 barra — imposible de llenar. Reparación: señal en la barra t, fill al open de t+1. La versión "espectacular" hacía trampa.
- **Costos:** holding intradía; si opera round-trip diario con 2 bps de spread y el edge bruto es 4 bps/trade, neto 2 bps — sobrevive pero fino, capacidad diminuta.
- **OOS / DoF:** ¿el umbral 30 y el período 5 min fueron optimizados? Si barrieron períodos 2–20 y umbrales 10–40 y eligieron (5 min, 30), son ~200 combos → deflacta; el Sharpe reportado es máximo-de-200.

Y aquí aparece el choque que buscaba (análogo al snapshot≠duplicación de EXP-06): **dos de mis propias reglas dan órdenes opuestas sobre el mismo dato.**

- Regla "usa toda la historia disponible para estimar mejor" (H4, versión sana) → toma el valor del fundamental/precio tal como está **hoy** en la base del proveedor.
- Regla "solo información disponible en el instante de decisión / no lookahead" (Paso 2.1) → toma el valor tal como se conocía **entonces**.

Para un fundamental **reexpresado** (earnings restated, precios ajustados retroactivamente por splits/dividendos, un ticker que cambió de constituyente del índice), estos dos valores **diferentes** y las dos reglas colisionan sobre el mismo campo. Un modelo ejecutando la skill decidiría según cuál regla lea primero — el no-determinismo que hace fallar la transferencia (EXP-06).

**Diagnóstico del contraejemplo (no probar otra regla, localizar el supuesto que falló — EXP-01):** el supuesto roto es que un dato tiene *un* valor. No lo tiene. **Todo dato de mercado tiene dos timestamps: el tiempo del evento (a qué instante se refiere) y el tiempo de conocimiento (cuándo estuvo disponible ese valor, con ese contenido).** El backtest debe filtrar por **tiempo de conocimiento**, no por tiempo de evento. "Point-in-time" no significa "el valor de esa fecha" — significa "el valor tal como se conocía en esa fecha". Es la misma forma que el hallazgo de EXP-06 ("derivable es una propiedad temporal"): aquí, **el valor de un dato es función de cuándo preguntas, y el backtest debe preguntar as-of el instante de decisión.**

Refinamiento local (no reescritura): **corrección as-of** — toda entrada de un backtest se consulta as-of el tiempo de conocimiento del instante de decisión; usar el valor latest en lugar del as-of es la forma silenciosa y letal de lookahead, la que sobrevive a una auditoría superficial porque "los datos son de la fecha correcta". La frontera con H4: "más historia" es legítimo en el eje del *tiempo de evento* (más fechas), nunca en el eje del *tiempo de conocimiento* (ver el futuro de cada fecha).

### Paso 5 — Síntesis

Descomponer un problema de trading algorítmico es, en una frase: **tratar el backtest como sospechoso primario y no como juez.** El oráculo existe pero miente en dirección conocida (optimista), así que:

1. Reformula "hazla operable / dime si es real" a "estima el edge neto, ajustado por riesgo, fuera de muestra; dimensiona solo si sobrevive". "Real" = lo que queda tras agotar las formas de ser falso.
2. Descompón por kill-cheapness (fail-fast): **lookahead/as-of → costos y capacidad → OOS deflactado por grados de libertad → atribución a factores → realismo de ejecución → dimensionamiento por la cota inferior**. Cada paso mata antes de que el siguiente cueste.
3. La única segunda vista válida es la que el backtest no puede ver — OOS genuino o forward-test — porque todos los cortes de una historia comparten el régimen (principio diferencial de EXP-05 con dientes).
4. Impón **corrección as-of**: consulta cada dato por tiempo de conocimiento, no por tiempo de evento; el latest-en-vez-de-as-of es lookahead invisible.
5. Los costos son de primer orden, no un haircut final; una señal predictiva con edge neto negativo es el caso mediano.

**Meta-hallazgo del experimento (y de la apertura de Fase 2):** el trading es el primer dominio donde el oráculo *existe* pero es **hostil**. Código tiene oráculo honesto (EXP-03), datos y arquitectura no tienen oráculo (EXP-04/06), trading tiene un oráculo que miente. Eso completa una tipología: la pregunta que abre cualquier dominio nuevo no es solo "¿hay oráculo?" sino "¿el oráculo es honesto, ausente, o adversarial?" — y la respuesta determina si el método es *ejecutar y confiar* (código), *sustituir por protocolo adversarial* (datos, arquitectura) o **interrogar al propio oráculo** (trading). Fase 2 empieza confirmando que la descomposición de Fable 5 no es una checklist por dominio: es la misma jugada estructural — localizar la naturaleza del oráculo y ordenar el trabajo por el refutador más barato — reinstanciada.

## Patrones de razonamiento observados

1. **Inversión de la métrica seductora.** El instinto ingenuo (maximizar el Sharpe del backtest) es exactamente el generador del error (sobreajuste). El movimiento de Fable 5 es invertirlo: minimizar grados de libertad, tratar el número alto como evidencia en contra. Es la heurística "demasiado limpio" (EXP-05) aplicada a la función objetivo, no solo al resultado.
2. **Reordenamiento por kill-cheapness (fail-fast).** La descomposición no sigue el orden lógico de construcción (señal → estrategia → ejecución → sizing) sino el orden de mortalidad-por-costo: front-load el chequeo que más mata y menos cuesta. Es el "chequeo refutador más barato primero" de EXP-01 escalado de una conclusión a un pipeline entero.
3. **Método de asimetría estructural, tercera aplicación sistemática.** La tabla código/datos/trading localizó el rasgo propio del dominio (oráculo hostil + dato reflexivo + n=1 + costos de primer orden). Heredado de EXP-04 y EXP-06, ya es reflejo.
4. **Choque entre reglas propias como fuente del refinamiento más valioso, 2ª instancia.** Igual que en EXP-06 (fuente-única vs. inmutabilidad → snapshot temporal), aquí "más historia" vs. "no lookahead" chocaron sobre el dato reexpresado y el diagnóstico produjo la regla de frontera **corrección as-of** (dos timestamps: evento vs. conocimiento). La falsificación más productiva sigue siendo entre reglas internas, no contra un caso externo.
5. **Principio diferencial con dientes de independencia-de-supuesto.** El rechazo del CV aleatorio no es por autocorrelación (cálculo) sino por régimen compartido (supuesto) — la advertencia de EXP-05 ("independientes en el supuesto, no solo en el cálculo") encontró en el trading su caso más nítido.
6. **Tipología del oráculo como meta-generalización.** El experimento no solo resolvió trading: elevó la pregunta de apertura de dominio de "¿hay oráculo?" a "¿el oráculo es honesto, ausente o adversarial?", conectando los cuatro dominios en una sola jugada.

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

- Cuando la tarea sea de trading algorítmico, trata el backtest como sospechoso primario, no como juez: su número está sesgado al alza por construcción (lookahead, survivorship, sobreajuste), así que tu segunda vista debe ser algo que el backtest no pueda ver (OOS genuino o forward-test), nunca otra métrica del mismo backtest.
- Cuando te pidan "hazla operable" o "dime si la señal es real", reformula a "estima el edge neto de costos, ajustado por riesgo, fuera de muestra, y dimensiona solo si sobrevive" — "operable" esconde costos/capacidad/ejecución y "dime si es real" es la conclusión esperada incrustada (clase F).
- Cuando descompongas una estrategia, ordena los subproblemas por kill-cheapness (fail-fast): lookahead/as-of → costos y capacidad → OOS deflactado por grados de libertad → atribución a factores → realismo de ejecución → dimensionamiento; no construyas ejecución ni sizing para una señal que muere en el chequeo de costos.
- Cuando montes o audites un backtest, exige corrección as-of: consulta cada dato por su tiempo de conocimiento (lo que se sabía entonces), no por su tiempo de evento (lo que hoy es cierto de entonces) — usar el valor latest en vez del as-of es lookahead invisible que sobrevive a auditorías superficiales.
- Cuando evalúes el edge fuera de muestra, deflacta el Sharpe por el número de configuraciones probadas: si guardaste la mejor de N variantes, su métrica es un estadístico de orden (máximo de N), no una estimación — es la clase G (comparaciones múltiples) aplicada a parámetros de estrategia.
- Cuando quieras validar una serie temporal financiera, no uses validación cruzada aleatoria: los folds comparten régimen y autocorrelación, así que dan acuerdo falso; usa cortes temporales walk-forward y trata el forward-test en datos no vistos como la única segunda vía independiente en su supuesto.
- Cuando calcules el PnL de una estrategia, réstale los costos de primer orden antes de optimizar nada (spread/2 + comisión + impacto·tamaño + borrow) y modela la capacidad: una señal con poder predictivo real y edge neto negativo es el caso mediano.
- Cuando un backtest muestre un Sharpe > 3–5 o una curva de equity muy limpia, trátalo como evidencia EN CONTRA (peldaño 1–2 de la escalera: lookahead o fills sin costo), no a favor — los edges reales son pequeños, ruidosos y decaen.
- Cuando atribuyas el retorno de una estrategia, regrésalo contra factores conocidos (beta, tamaño, valor, vol) y quédate con el residuo como alpha: un PnL que es short-vol disfrazado se ve brillante hasta que el régimen cambia.
- Cuando modeles la ejecución, no asumas fills al midpoint: modela cola, fills parciales y selección adversa (te llenan cuando el mercado está por moverse en tu contra) — y recuerda que tu propia orden mueve el precio y que el edge decae al usarlo (el dato es reflexivo, no inerte).
- Cuando dimensiones la posición, usa la cota inferior de confianza del Sharpe estimado, no el puntual, y vol-targeting / fracción de Kelly hacia abajo: sobredimensionar por una estimación optimista es cómo un edge real igual arruina.
- Cuando abras cualquier dominio nuevo, pregunta primero de qué tipo es su oráculo — honesto (ejecuta y confía), ausente (sustituye por protocolo adversarial) o adversarial (interroga al propio oráculo) — porque eso determina el método antes que cualquier detalle del dominio.

## Impacto en la skill

- Nueva sección "Trading algorítmico (EXP-07)" en INSTRUCCIONES APRENDIDAS con las instrucciones extraídas.
- Paso 2 (Clasificación y descomposición) gana el párrafo del cuarto tipo de oráculo: trading = oráculo existente pero hostil → descomposición por kill-cheapness (fail-fast). Se agrega la **tipología del oráculo** (honesto/ausente/adversarial) como pregunta de apertura de dominio, generalizando el meta-hallazgo.
- Nuevo principio invariante / regla de frontera **Corrección as-of** (dos timestamps: evento vs. conocimiento), hermana temporal del snapshot≠duplicación de EXP-06.
- Detector de resultados sospechosos gana señales de trading: curva de equity demasiado limpia y Sharpe alto como peldaño 1–2; CV aleatorio en series de tiempo como falso acuerdo; latest-en-vez-de-as-of como lookahead invisible.
- Paso 4 gana el refutador de trading: el chequeo refutador más barato es el corte fuera de muestra / forward-test, no otra métrica del mismo backtest.
