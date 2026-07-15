# EXP-16 — Impacto por instrucción: cuáles cargan peso y cuáles son ruido

**Fase:** 3 (Destilación a la skill) · **Fecha:** 2026-07-15 21:20 UTC · **Modelo:** claude-fable-5 (nativo)
**Instrumento medido sobre:** `.claude/commands/fable5.md` v1.15 (574 líneas, ~18.8k palabras, ~25.3k tokens estimados, 136 bullets "Cuando …")

---

## La pregunta completa

> Identificar qué instrucciones de la skill tienen mayor impacto y cuáles son ruido.

El roadmap anota la precondición que EXP-15 dejó pendiente: *"requiere primero calibrar un banco de problemas donde Sonnet base puntúe 30–70%"*. Es decir: la vía obvia de medir impacto —ablación A/B por instrucción— está bloqueada porque EXP-15 demostró efecto techo (Sonnet base 20/20 en trampas canónicas). EXP-16 tiene que producir la clasificación impacto↔ruido **sin** ese instrumento.

---

## Mi respuesta completa (razonamiento real, no resumido)

### Paso 0 — La pregunta es una consigna-trampa

"Cuáles tienen mayor impacto y cuáles son ruido" nombra una propiedad de superficie (helpfulness, un ranking de 136 instrucciones de más a menos útil). La lectura literal produciría una lista ordenada por utilidad percibida. Reformulo antes de tocar nada (Paso 0, operador consigna-trampa de la propia skill):

**La propiedad real no es un ranking de dos clases, es una triage de TRES.** EXP-15 midió algo que un ranking de solo-utilidad no puede representar: cargar el protocolo completo costó **2.3× tokens y −2 puntos de cobertura** frente al baseline (el protocolo largo fabricó recuperación-enterrada sobre el artefacto a auditar). Es decir: parte de la masa de la skill no es neutra —tiene **valor marginal negativo** por desplazamiento de atención. Entonces:

1. **Load-bearing** (impacto positivo): sin ella el output empeora en una tarea realista.
2. **Ruido inerte** (impacto ≈0): cuesta tokens/atención pero nunca cambia un output —la instrucción para un modo de fallo que no ocurre, o el restatement de algo que el modelo ya hace.
3. **Ruido activo** (impacto negativo): su presencia desplaza atención de la tarea (EXP-15: −2 de cobertura) o fabrica un modo de fallo (EXP-12: sobre-observación 43×).

El entregable de EXP-16 no puede ser un ranking. Tiene que ser una clasificación por clase de evidencia + rol estructural, que **incluya explícitamente la clase que hay que cortar** —porque esa es la que EXP-17/18 necesitan.

### Paso 1 — ¿Qué tipo de oráculo tiene "el impacto de una instrucción"?

Corro el motor de la propia skill sobre la pregunta (Nivel 1, tipología del oráculo):

- El oráculo honesto sería la **ablación A/B**: quito la instrucción, corro las dos versiones sobre un instrumento discriminante, mido Δscore. Pero EXP-15 probó que el instrumento tiene efecto techo: el control puntúa 20/20 y no puede fallar. Correr 136 ablaciones contra un control que no falla da 136 nulos —"un experimento cuyo control no puede fallar no informa" (instrucción 533, la que EXP-15 dejó). El oráculo honesto **existe pero está diferido**: disponible en principio, no disponible al decidir. Es exactamente el tipo de oráculo de EXP-10 (evaluar un resultado ajeno): la replicación es honesta pero no está a mano, así que se sustituye por **interrogatorio del procedimiento + priors estructurales**, no por medición directa.

Esto ya fija el método antes de cualquier detalle: no voy a medir tamaños de efecto. Voy a clasificar por **clase de evidencia** y a **medir lo que sí es medible** (la redundancia), y voy a marcar todo lo no medido como "impacto estructural, no medido" sin fabricar un número que el instrumento roto no soporta.

### Paso 3 — Hipótesis de MÉTODO (genero varias, descarto por materialización)

**Hipótesis A — Ablación directa sobre el instrumento de EXP-15.** Descartada: efecto techo (arriba). El control no discrimina; el cierre de brecha (B−C)/(A−C) ya salió incomputable en EXP-15 porque A−C=0. Repetir eso 136 veces es 136 divisiones por cero.

**Hipótesis B — Auto-calificar cada instrucción 1–10 por importancia.** Descartada por la meta-honestidad de la propia skill (Clase D, EXP-02/EXP-05): "cuál instrucción cambia más mi output" es una pregunta sobre mi cableado causal interno, y no tengo señal interna fiable de eso. La importancia auto-reportada correlacionaría con la elegancia de la prosa, no con el impacto causal. Es introspección de mecanismo disfrazada de medición.

**Hipótesis C — Rankear por tokens y cortar lo más largo.** Descartada como método primario: longitud ≠ ruido. Las secciones más largas (el NÚCLEO DESTILADO, la Escalera de artefactos de 56 líneas, el DETECTOR) son candidatas a **mayor** impacto, no menor. Cortar por longitud optimiza la cantidad equivocada. *Pero* conservo el costo como **denominador**: la unidad correcta es impacto-por-token (economía de EXP-12), no impacto absoluto.

**Hipótesis D — Frecuencia de citación como proxy de impacto.** Medida (abajo): EXP-06 se cita 34 veces, EXP-04 30, EXP-05 27… Descartada como *medida de impacto*, conservada como **señal secundaria**: la citación mide **centralidad estructural** (cuánto genera downstream una idea), no cuánto cambia un output real. Una idea muy citada puede seguir siendo inerte si el modo de fallo que custodia no ocurre en la práctica. Sirve para ordenar candidatos al tier "motor", no como tamaño de efecto.

**Hipótesis E — Test de subsunción (adoptada como método estructural primario).** EXP-13 ya afirmó que la skill es "un motor + operadores transversales + instancias de dominio", y que *"si un dominio no aparece, clasifícalo con Nivel 1, págalo con Nivel 2"*. Eso vuelve **testeable** la redundancia: para cada instrucción de dominio, pregunto **¿correr el motor núcleo sobre su disparador regenera esta instrucción?**
- Si **sí** → es una **instancia cacheada del motor** (redundancia gobernada, EXP-09 clase 3): conservable solo si el disparador es común y su recomputación es propensa a error; si no, comprimible a un puntero.
- Si **no** → es **payload independiente** (load-bearing): el motor no la produce solo.
Es la skill aplicándose su propia taxonomía de redundancia de EXP-09 a sí misma. Fuerte y transferible.

**Hipótesis F — Anclar en el único dato medido que existe (adoptada como método de evidencia).** EXP-15 dio exactamente **una** discriminación medida Fable↔Sonnet: Fable atrapó la disciplina-de-escala / re-aplicar-detector-al-residuo que ambos Sonnets fallaron. Entonces las instrucciones de EXP-15 (534, 535) son las **únicas** de toda la skill con evidencia directa de cerrar una brecha en una tarea real. Todo lo demás está **no medido**. La honestidad manda: puedo rankear por **clase de evidencia**, no por tamaño de efecto, porque hay un solo datapoint de instrumento.

### Paso 4 — Falsificación: mido el ruido en vez de opinarlo

La afirmación "el ruido dominante es duplicación, no instrucciones erróneas" es una afirmación cuantitativa dentro de mi propio argumento → Clase A disfrazada de opinión (EXP-04, instrucción 142). La simulo antes de afirmarla. Conté, sobre el archivo real, en cuántas **secciones distintas** aparece cada idea núcleo:

| Idea núcleo | Ocurrencias | Secciones distintas |
|---|---|---|
| Detección diferencial / segunda vía independiente | 26 | **14** |
| snapshot ≠ duplicación / frontera as-of | 52 | **11** |
| Clase C / dato volátil → verifica con herramienta | 29 | **10** |
| "funciona a la primera" = evidencia en contra | 23 | — |
| Estadístico de orden / mejor de N / winner's curse | 20 | — |
| kill-cheapness / costo-p_kill / fail-fast | 20 | — |
| consigna-trampa / palabra-eslogan | 19 | **6** |
| Invariante necesita dueño mecánico | 15 | **7** |
| Tipología del oráculo honesto/ausente/adversarial | 15 | — |

La refutación no refutó: la confirmó con dureza. Las ideas load-bearing están **restated en 6–14 secciones cada una**. "Detección diferencial" aparece en 14 de ~30 secciones; "snapshot/as-of" 52 veces. El archivo son 574 líneas / ~25k tokens y ya golpea el límite de lectura.

**Diagnóstico (contraejemplo → reparación local, no reescritura):** el ruido dominante de esta skill **no es ninguna instrucción equivocada** —revisé y no encontré una sola instrucción sin evidencia o falsa. El ruido es **la multiplicidad de restatements**. Y por el hallazgo medido de EXP-15 (−2 de cobertura por longitud), esa multiplicidad no es la clase *inerte* sino la clase **activa/dañina**: cada restatement desde el 2º es contexto que puede fabricar la recuperación-enterrada de EXP-02 sobre la tarea real. La segunda mención de "verifica Clase C" no agrega cobertura; agrega superficie de desplazamiento de atención.

### Conclusión — el mapa de impacto en cuatro tiers

- **T1 · Medido load-bearing (evidencia directa de brecha Fable↔Sonnet).** Conjunto minúsculo, el único con instrumento: disciplina-de-escala sobre números propios (535), re-aplicar-detector-al-residuo / corrección-parcial-blanquea (534, 59), y baseline-primero (533). Son las 3 instrucciones que EXP-15 midió como el borde real. Todo lo demás de la skill es *no medido*.
- **T2 · Estructuralmente load-bearing (motor núcleo).** Paso 0–5, la tipología del oráculo (Nivel 1), la economía de herramientas (Nivel 2), el principio diferencial de EXP-05, el operador consigna-trampa, el operador as-of/snapshot. Citación alta + son **generativas** (el test de subsunción muestra que producen las secciones de dominio). Cortar una colapsa muchas instrucciones downstream. Impacto estructural, no medido, pero irreducible: el motor no se regenera a sí mismo.
- **T3 · Instancias de dominio = redundancia gobernada (outputs cacheados del motor).** Los ~80 bullets "Cuando X, Y" de los dominios (EXP-01 mates, EXP-07 trading, EXP-08 negocio, EXP-09 esquemas, EXP-10 stats, EXP-11 ambigüedad…). El test de subsunción los regenera desde el motor. Su valor **no** es payload independiente —es (a) pedagogía/transferencia (los CASOS CANÓNICOS los hacen concretos, EXP-14) y (b) latencia/fiabilidad de una respuesta cacheada para un disparador **común**. Conservables los de disparador común + recomputación propensa a error; el resto, comprimibles a punteros.
- **T4 · Ruido (la clase a cortar).** No una instrucción: **la multiplicidad de restatements** (la 3ª–14ª aparición de cada idea núcleo) + bullets duplicados casi verbatim entre `Mapa de zonas A–G`, `Principios invariantes`, los bullets por-EXP y el `Detector`. Es la masa que EXP-15 midió como −2. El movimiento de mayor valor **no es cortar cobertura de dominio** (eso arriesga que −2 se vuelva −4) sino **de-duplicar**: un hecho, un hogar (EXP-14 aplicado a las instrucciones de la propia skill), citado desde el resto.

### Frontera de alcance (crítica): EXP-16 identifica, no poda

La instrucción 518 de la propia skill lo dice: *"cristalizar estructura y podar ruido son pasos distintos — no borres bajo el nombre de refinar."* Y EXP-15 dejó la lección dura: cortar a ciegas costó −2. **Podar sin instrumento calibrado repite exactamente ese error.** Por eso EXP-16 se detiene en el diagnóstico + el método + el mapa de ruido. El corte real es de EXP-17 (refinar el modo proxy con las instrucciones que más reducen la brecha) y EXP-18 (v2.0), y su precondición sigue siendo la de EXP-15/EXP-16: un banco donde el baseline puntúe 30–70% para verificar que cada supresión no pierde cobertura. Cortar antes de tener ese banco sería el mismo error auto-diagnosticado.

---

## Análisis de patrones de razonamiento observados

1. **La pregunta meta también es consigna-trampa.** "Impacto vs ruido" nombra dos clases; la estructura real (por el dato de EXP-15) tiene tres, con una de valor negativo. El operador consigna-trampa aplica a las preguntas *sobre la skill*, no solo a las tareas de dominio.
2. **El oráculo diferido reaparece un nivel arriba.** Igual que EXP-10 evaluaba un resultado ajeno sin replicación disponible, EXP-16 evalúa el impacto sin ablación disponible: mismo tipo de oráculo, mismo sustituto (interrogar el procedimiento + medir lo medible + no fabricar el número que falta).
3. **Medir la afirmación propia antes de afirmarla, aplicado a la propia skill.** "El ruido es duplicación" era Clase A: se contó (10/11/14 secciones), no se opinó. El patrón EXP-04 se volvió sobre el instrumento.
4. **El test de subsunción de EXP-13 se vuelve la herramienta de medición de EXP-16.** "¿El motor regenera esta instrucción?" separa payload de cache —es EXP-09 (taxonomía de redundancia) aplicada a las instrucciones en vez de a columnas de una tabla.
5. **Honestidad de calibración sobre la propia evidencia:** con un solo datapoint de instrumento (EXP-15), rankear por tamaño de efecto sería confabular; el output correcto es rankear por clase de evidencia y marcar lo no medido como no medido (corolario EXP-05: sin segunda vía, reporta como juicio marcado, no como certeza).

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

1. **Cuando midas el impacto de las instrucciones de un prompt/skill**, no lo trates como "cuáles ayudan más" (consigna-trampa): reformúlalo a triage de tres clases —load-bearing, ruido inerte, ruido activo (coste>retorno)— porque hay evidencia medida (EXP-15) de masa con valor marginal negativo por desplazamiento de atención; un ranking de solo-utilidad omite la clase que hay que cortar.
2. **Cuando el instrumento de validación tenga efecto techo** (baseline ~techo), no rankees impacto por ablación directa: el oráculo honesto (A/B) existe pero está diferido; sustitúyelo por clase-de-evidencia + test de subsunción, y marca todo lo no medido como "impacto estructural, no medido" —no fabriques un tamaño de efecto que el instrumento roto no soporta.
3. **Cuando quieras saber si una instrucción es carga o instancia cacheada**, córrele el test de subsunción: ¿correr el motor núcleo (tipología del oráculo + economía de herramientas) sobre su disparador la regenera? Si sí → redundancia gobernada, conservable solo si el disparador es común y su recomputación es propensa a error; si no → payload independiente (load-bearing).
4. **Cuando una instrucción load-bearing aparezca restated en más de una sección**, cuenta cada repetición desde la 2ª como ruido **activo**, no inerte: cada restatement es contexto que puede fabricar recuperación-enterrada sobre la tarea (EXP-15); dale un solo hogar (un hecho, un hogar, EXP-14) y cita desde el resto —la de-duplicación, no el recorte de cobertura, es el movimiento de mayor valor.
5. **Cuando afirmes "esto es ruido"**, mídelo, no lo opines (Clase A, EXP-04): cuenta en cuántas secciones distintas aparece cada idea núcleo y usa esas cuentas como el mapa de ruido —en esta skill, clase-C-volátil en 10 secciones, segunda-vía-diferencial en 14, snapshot/as-of en 11.
6. **Cuando identifiques el ruido, NO lo podes en el mismo paso** (identificar y podar son pasos distintos, 518): cortar sin instrumento calibrado repite el −2 de cobertura de EXP-15 (riesgo de −4); el corte exige primero un banco donde el baseline puntúe 30–70% para verificar que cada supresión no pierde cobertura.
7. **Cuando la frecuencia de citación de una idea sea alta**, no la confundas con impacto medido: mide centralidad estructural (cuánto genera downstream), no cuánto cambia un output —úsala para ordenar candidatos al tier "motor", no como tamaño de efecto.
