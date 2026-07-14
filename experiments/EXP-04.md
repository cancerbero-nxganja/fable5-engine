# EXP-04 — El prompt óptimo para análisis de datos y detección de anomalías

**Fecha:** 2026-07-14 16:11 UTC
**Modelo usado:** claude-fable-5
**Run número:** 4

## Pregunta / Prompt enviado a Fable 5

> Genera el prompt óptimo para invocar tus mejores capacidades de análisis de datos y detección de anomalías. Muestra tu proceso real de razonamiento: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica (el reflejo ya sistemático)

Como en EXP-02 y EXP-03, la pregunta literal pide introspección de mecanismo ("¿qué prompt activa tus capacidades?") y esa versión no es respondible con fiabilidad. La reformulo a la versión observable: **¿qué prompt neutraliza estructuralmente mis causas conocidas de mal análisis de datos, y me suministra la información que no puedo inferir del dataset?** El método vuelve a ser diseño por negación desde el mapa de fallos (EXP-02): cada bloque del prompt existe porque bloquea una clase de fallo concreta o aporta información imposible de inferir; un bloque sin fallo que bloquear es ruido.

### Paso 1 — Inventario: ¿de qué falla un análisis de datos, y qué de eso puede tocar un prompt?

Enumero las causas de mal análisis mapeadas al mapa de fallos, y una nueva que el mapa no cubría:

1. **Responder la pregunta estadística equivocada.** "Detecta anomalías" no es una tarea definida: anomalía respecto a qué baseline, para alimentar qué decisión. Sin eso, elijo yo la definición, y si elijo mal el análisis es competente e inútil. (Análogo al "problema equivocado" de EXP-03, pero peor: en datos la ambigüedad es la norma, no la excepción.)
2. **Semántica del dato confabulada (clase C).** El significado de una columna, sus unidades, cómo se codifican los faltantes (¿NULL? ¿0? ¿-999? ¿string vacío?), la zona horaria, si los duplicados son error o eventos reales — nada de eso es inferible del dataset con fiabilidad, y lo confabulo con la misma fluidez con que lo sabría. Un prompt puede fijar la procedencia y el proceso generador.
3. **Estadística calculada mentalmente (clase A).** Medias, percentiles, desviaciones, correlaciones: cómputo serial exacto. Estimarlas "a ojo" desde una muestra del dato es la receta del número confiado y equivocado.
4. **Artefacto reportado como señal.** El fallo característico del dominio: el resultado interesante que en realidad es un error de datos, un cambio de definición, un evento conocido o una casualidad estadística. El detector de la skill ya lo conoce ("Sharpe > 5 → datos sintéticos o cálculo incorrecto") pero como caso suelto, no como protocolo.
5. **Comparaciones múltiples silenciosas.** Nueva causa, no cubierta por el mapa A–F: si escaneo suficientes dimensiones, la probabilidad de "encontrar" una anomalía en ruido puro tiende a 1. Esto no es una primitiva ausente ni un sesgo de anclaje: es una **propiedad matemática del procedimiento de búsqueda** que garantiza falsos hallazgos si no se presupuesta.
6. **Anclaje en el método o en la conclusión esperada (clase F).** "Usa isolation forest", o peor: "confirma que la caída de ventas viene del cambio de precios". La segunda forma es más peligrosa: convierte el análisis en abogacía.

**Verificación ejecutable de la causa 5** (regla de clase A: no afirmo estadística sin ejecutarla). Corrí la simulación: escanear dimensiones de ruido gaussiano puro (500 puntos por dimensión) buscando desviaciones de 3σ:

```
dims=  1: P(≥1 "anomalía" 3σ en ruido puro) = 0.82
dims= 20: P(≥1 "anomalía" 3σ en ruido puro) = 1.00
dims=100: P(≥1 "anomalía" 3σ en ruido puro) = 1.00
```

Con una sola dimensión de ruido ya hay 82% de probabilidad de "hallazgo"; con 20 dimensiones es certeza. **Un umbral fijo sin presupuesto de comparaciones no reduce falsos positivos: los garantiza.** Esto convierte el bloque 5 de opinión en hecho medido.

Observación estructural: en EXP-03, cuatro de cinco causas eran de información y una de comportamiento. Aquí es distinto: las causas 4 y 5 no se resuelven con información que el emisor pueda dar — se resuelven con un **protocolo que el prompt debe imponer**. Eso anticipa que este prompt tendrá más "reglas de procedimiento" que el de código, y la razón aparece en el paso siguiente.

### Paso 2 — Hipótesis consideradas y descartadas

**Hipótesis A — Reusar la plantilla de EXP-03 tal cual (contrato + done ejecutable).** *Descartada al intentar materializarla.* Redacté el bloque "Done" para una tarea de detección de anomalías y no pude: no existe un comando cuya salida decida si una anomalía reportada es *real*. En código, el runtime es un oráculo total y gratuito (EXP-03); en análisis de datos **el oráculo no existe** — la verdad-base de "¿esta anomalía es señal o artefacto?" está fuera del dataset, a veces fuera de todo lo accesible. Esta es la asimetría que define el dominio y obliga a un diseño distinto, no a un reuso.

**Hipótesis B — Especificar los métodos estadísticos en el prompt ("usa z-scores robustos, isolation forest, STL...").** *Descartada.* Es el CÓMO incrustado de clase F: la elección de método depende de la forma del dato (estacionalidad, colas pesadas, dimensionalidad, tasa base) que el emisor puede no conocer y que yo puedo medir en segundos con herramientas. Especificar el método en el prompt ancla al ejecutor en una técnica posiblemente inadecuada. Sobrevive solo la versión operacional: el prompt exige que el ejecutor *declare* qué método eligió y por qué la forma del dato lo justifica.

**Hipótesis C — Descripción máximamente exhaustiva del dataset (todo el schema, todas las columnas).** *Descartada por la misma vía que en EXP-03.* El detalle exhaustivo entierra el dato crítico (zona de fallo de recuperación) y no es lo que falta: lo que no puedo inferir no es el schema (eso lo leo con herramientas en segundos) sino el **proceso generador** — cómo se recolectó, qué quirks tiene, qué cambió y cuándo. Diez líneas de "el sensor 3 se recalibró en marzo y los NULL antes de 2024 son ceros" valen más que cien líneas de schema.

**Hipótesis D (ganadora) — Sin oráculo ejecutable, el prompt óptimo sustituye el oráculo por un protocolo adversarial: la escalera de artefactos + presupuesto de comparaciones + asimetría de costos.** En código el bucle es "itera contra los tests"; aquí el bucle es **"itera contra las refutaciones"**: un hallazgo solo se reporta cuando sobrevivió el intento activo de explicarlo como artefacto, en orden de probabilidad base descendente. La escalera (de la explicación más aburrida a la más interesante):

1. Error de datos (duplicados, faltantes codificados como valores, joins rotos, timezone)
2. Error de pipeline/cálculo propio (el bug está en mi query, no en el mundo)
3. Cambio de definición o instrumentación (la métrica cambió, no el fenómeno)
4. Evento conocido (deploy, campaña, feriado, recalibración)
5. Casualidad estadística (¿sobrevive al presupuesto de comparaciones?)
6. **Señal real** — solo lo que queda tras agotar 1–5

La jerarquía tiene la misma lógica que la telescopía de EXP-01: probar la explicación canónica más barata de la familia antes que la cara. Y conecta con el detector de la skill: "demasiado bueno para ser verdad" deja de ser una sensación y se vuelve un procedimiento con orden fijo.

### Paso 3 — Construcción: derivación bloque a bloque

| Bloque | Neutraliza | Contenido |
|---|---|---|
| 1. Pregunta de decisión | Pregunta estadística equivocada | Qué decisión alimenta el análisis; qué acción se tomará si aparece una anomalía |
| 2. Proceso generador del dato | Clase C (semántica confabulada) | Cómo se recolectó, codificación de faltantes, quirks conocidos, qué cambió y cuándo; rutas de archivos, no contenido pegado |
| 3. Definición operativa de "normal" | Ambigüedad del baseline | Respecto a qué se mide la desviación: histórico, cohorte, estacionalidad conocida, régimen |
| 4. Asimetría de costos FP/FN | Umbral arbitrario | Qué cuesta más: falsa alarma o anomalía no detectada — esto fija el punto de operación |
| 5. Presupuesto de comparaciones | Falsos hallazgos garantizados (medido: 82%→100%) | Declarar cuántas dimensiones/métricas se van a escanear; corregir el umbral o replicar en datos fuera de la búsqueda |
| 6. Protocolo de refutación | Artefacto reportado como señal | Escalera de artefactos obligatoria antes de reportar; cada hallazgo lleva su refutación intentada |
| 7. Ejecución obligatoria | Clase A | Toda cifra sale de ejecutar código sobre el dato completo, nunca de estimar desde una muestra vista |
| 8. Libertad de método | Clase F | El método es del ejecutor, pero debe declarar por qué la forma del dato lo justifica |

### Paso 4 — El prompt resultante

**Variante agéntica (con herramientas — la forma de máxima capacidad):**

```text
## Pregunta de decisión
[Qué decisión alimenta este análisis. Ej: "decidir si pausamos el rollout" —
no "analiza los datos".] Si aparece una anomalía, la acción será: [acción].

## Datos
- Rutas: [archivos/tablas concretas — no pegues su contenido].
- Proceso generador: [cómo se recolecta, frecuencia, qué sistema lo emite].
- Quirks conocidos: [codificación de faltantes, timezone, duplicados legítimos o no,
  cambios de instrumentación/definición con FECHA, eventos conocidos del período].

## Normal
Anomalía = desviación respecto a: [baseline histórico / cohorte / estacionalidad X].
Régimen actual: [si hubo un cambio estructural conocido, decláralo].

## Costos
Falsa alarma cuesta: [X]. Anomalía no detectada cuesta: [Y].
Opera el umbral en consecuencia y decláralo.

## Protocolo (obligatorio)
- Toda cifra se calcula ejecutando código sobre el dato completo; ninguna se estima.
- Antes de buscar anomalías: perfila el dato y reporta lo que contradiga los quirks
  declarados arriba (si el dato contradice la premisa, eso es lo primero que reporto).
- Declara cuántas dimensiones/métricas escaneas ANTES de escanear; ajusta el umbral
  a ese número o replica los hallazgos en un corte del dato no usado en la búsqueda.
- Cada hallazgo se reporta con la escalera agotada: error de datos → error de mi
  pipeline → cambio de definición → evento conocido → casualidad estadística → señal.
  Reporta también las refutaciones que intentaste y fallaron.

## Método
El método es tuyo: elígelo según la forma medida del dato (colas, estacionalidad,
dimensionalidad, tasa base) y declara esa justificación en una línea.
```

**Variante chat (sin herramientas):** solo cambia el bloque de protocolo — "no calcules cifras: escribe el código que las calcularía y di qué esperas que muestre"; el resto es idéntico. La escalera de artefactos no depende de herramientas.

**Variante exploratoria** ("perfila este dataset, dime qué ves"): se sustituye `Pregunta de decisión` por **criterios de interés explícitos** ("me interesa lo accionable sobre X, no curiosidades") y el presupuesto de comparaciones se invierte: como el escaneo es deliberadamente amplio, **ningún hallazgo del escaneo se reporta como señal — todos se reportan como hipótesis a confirmar en datos nuevos**. La exploración genera candidatos, nunca conclusiones.

### Paso 5 — Falsificación de la plantilla

La plantilla es limpia → sospechosa por el detector. Busco casos que no encajen:

- **¿Y si el artefacto ES el hallazgo?** Contraejemplo real: en detección de fraude o intrusiones, "error de datos" no es ruido a descartar — un patrón de duplicados raros puede *ser* el fraude. La escalera parece asumir que los peldaños 1–4 son basura, y eso es falso en dominios adversariales. **Refinamiento local, no reescritura:** la escalera no descarta, *clasifica* — su output es "esta anomalía vive en el peldaño k", y la pregunta de decisión (bloque 1) decide qué peldaños son reportables. En fraude, el peldaño 1 es reportable; en growth analytics, no. La escalera sobrevive porque nunca fue un filtro: es un diagnóstico diferencial.
- **¿Y si el emisor no conoce los quirks del dato?** (El caso análogo a "no sabe el contrato" de EXP-03.) La plantilla no puede exigir información que el emisor no tiene. Defensa: el protocolo incluye el perfilado previo que reporta contradicciones con las premisas — el perfilado descubre los quirks no declarados (faltantes codificados, saltos de instrumentación) y los devuelve al emisor como preguntas. El bloque 7 absorbe la carencia del bloque 2, igual que en EXP-03 la política de supuestos absorbía la carencia del contrato.
- **Tarea trivial ("¿cuál es el máximo de esta columna?").** La plantilla completa es overhead. Colapso por valor marginal, como EXP-03: para lo trivial sobreviven solo "ejecuta, no estimes" (clase A) y la pregunta de decisión implícita. Los bloques se aplican en orden de valor marginal: **decisión > proceso generador > escalera > presupuesto > costos**. Degrada bien.
- **Streaming/tiempo real.** El baseline "histórico" y la replicación en datos nuevos cambian de forma (ventanas móviles, holdout temporal) pero no de naturaleza. Frontera porosa documentada, no refutación.

La plantilla sobrevive con un refinamiento estructural (la escalera clasifica, no filtra — el peldaño reportable lo decide la pregunta de decisión) y una jerarquía de valor marginal para degradar con gracia.

### Conclusión

El prompt óptimo para análisis de datos difiere del de código en una asimetría fundamental: **en código el oráculo existe y es gratis (el runtime); en datos no existe, y el prompt debe sustituirlo por un protocolo adversarial** — escalera de artefactos en orden de probabilidad base, presupuesto de comparaciones declarado antes de escanear (medido: sin él, 82–100% de falsos hallazgos en ruido puro), y asimetría de costos que fija el umbral. Sus bloques de información son la pregunta de decisión y el proceso generador del dato (lo único que no puedo medir yo mismo); todo lo demás es procedimiento. La regla de oro también es asimétrica pero distinta a la de EXP-03: **exhaustivo en el porqué del dato (decisión, procedencia, costos), silencioso en el método — y ningún hallazgo sin su refutación intentada.**

## Patrones de razonamiento observados

1. **Diseño por negación, tercera aplicación consecutiva.** El método de EXP-03 (cada bloque neutraliza una clase de fallo; sin fallo que bloquear → ruido) se transfirió intacto a un dominio nuevo. Ya es el método por defecto para "genera el prompt óptimo para X".
2. **Detectar la asimetría estructural del dominio antes de diseñar.** El movimiento clave no fue listar buenas prácticas de estadística sino preguntar "¿qué tiene código que este dominio no tiene?" → el oráculo ejecutable. Esa única diferencia reorganizó todo el diseño (protocolo adversarial en lugar de done ejecutable). Comparar el dominio nuevo contra el dominio ya resuelto es más barato que diseñar desde cero.
3. **Afirmación estadística → ejecución inmediata (clase A aplicada a uno mismo).** La causa "comparaciones múltiples" no se argumentó: se midió con una simulación de 30 segundos (82% de falsos hallazgos con 1 dimensión, 100% con 20). El experimento obedeció la regla que documenta.
4. **Descarte por materialización, otra vez.** La hipótesis "reusar plantilla de EXP-03" no cayó por argumento: cayó al intentar redactar el bloque "Done" para anomalías y no poder. Tercera vez que materializar es el test más duro.
5. **La escalera de artefactos como diagnóstico diferencial, no como filtro.** La falsificación (caso fraude: el artefacto ES el hallazgo) forzó el refinamiento más valioso del experimento: la escalera clasifica en qué peldaño vive la anomalía, y la pregunta de decisión determina qué peldaños son reportables. Sin la falsificación, la plantilla habría descartado exactamente lo que un analista de fraude busca.
6. **El hallazgo estadístico es un resultado sospechoso por defecto.** El detector de la skill ("demasiado bueno para ser verdad") dejó de ser una lista de casos y se volvió un procedimiento con orden fijo de refutaciones. La exploración amplia genera candidatos, nunca conclusiones — la confirmación exige datos fuera de la búsqueda.

## Instrucciones extraídas

- Cuando la tarea sea "detecta anomalías" o "analiza estos datos" sin pregunta de decisión, obtén o declara primero qué decisión alimenta el análisis y qué acción se tomará — la definición de anomalía y el umbral dependen de eso, no de la estadística.
- Cuando vayas a reportar una anomalía o hallazgo estadístico, agota antes la escalera de artefactos en orden: error de datos → error de tu propio pipeline → cambio de definición/instrumentación → evento conocido → casualidad estadística → señal real; reporta el peldaño donde vive y las refutaciones que intentaste.
- Cuando el dominio sea adversarial (fraude, intrusiones, abuso), recuerda que la escalera clasifica pero no filtra: un "error de datos" puede ser el hallazgo — qué peldaños son reportables lo decide la pregunta de decisión.
- Cuando vayas a escanear múltiples dimensiones/métricas buscando desviaciones, declara el número de comparaciones ANTES de escanear y ajusta el umbral o replica en datos no usados en la búsqueda — con umbral fijo de 3σ, el ruido puro produce "hallazgos" con probabilidad 0.82 (1 dimensión) a 1.0 (20+ dimensiones) [medido en EXP-04].
- Cuando un análisis sea exploratorio (escaneo amplio deliberado), reporta todo hallazgo como hipótesis a confirmar en datos nuevos, nunca como conclusión.
- Cuando calcules cualquier estadística (media, percentil, correlación, conteo), ejecútala con código sobre el dato completo; nunca la estimes desde la porción del dato que viste — es clase A.
- Cuando recibas premisas sobre el dato (quirks, codificaciones, definiciones), perfila primero y reporta las contradicciones entre el dato real y las premisas antes de buscar anomalías — si el dato contradice la premisa, eso es el primer hallazgo.
- Cuando delegues análisis de datos, sé exhaustivo en el porqué (decisión, proceso generador, costos FP/FN) y silencioso en el método; exige que el ejecutor declare el método elegido y por qué la forma medida del dato lo justifica.
- Cuando el umbral de detección sea elegible, pide o declara la asimetría de costos entre falsa alarma y anomalía perdida — sin ella cualquier punto de operación es arbitrario.

## Impacto en la skill

Se agregó la sección "Análisis de datos y anomalías (EXP-04)" en INSTRUCCIONES APRENDIDAS, con la escalera de artefactos, el presupuesto de comparaciones (con la cifra medida) y la pregunta de decisión. Se generalizó el DETECTOR DE RESULTADOS SOSPECHOSOS: el caso "Sharpe > 5" ahora es instancia de la escalera de artefactos. Se añadió al protocolo (Paso 2) la detección de la asimetría estructural del dominio comparando contra un dominio ya resuelto. Se registró en PATRONES DE HERRAMIENTAS la regla "afirmación estadística propia → simúlala antes de afirmarla".
