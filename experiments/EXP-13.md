# EXP-13 — Refinar la skill con los patrones de razonamiento de Fase 2 (destilación)

**Fecha:** 2026-07-15 12:14 UTC  
**Modelo usado:** claude-fable-5  
**Run número:** 13  
**Fase:** 3 (Destilación a la skill) — primer experimento de la fase

## Pregunta / Prompt enviado a Fable 5

> Refinar la skill con los patrones de razonamiento documentados en Fase 2 (EXP-07…EXP-12).

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica (la pregunta esconde una consigna-trampa sobre sí misma)

Aplico mi propio Paso 0 a la petición. "Refinar la skill con los patrones de Fase 2" admite dos lecturas, y no son cercanas:

- **Lectura A (acreción):** agregar el contenido de Fase 2 a la skill. Pero esto ya está hecho — cada uno de EXP-07…EXP-12 corrió su propia reingeniería y dejó su sección de dominio + sus refinamientos de la tipología del oráculo. Ejecutar la lectura A es no hacer nada, o peor, duplicar.
- **Lectura B (destilación):** la Fase 3 se titula literalmente "Destilación a la skill". Destilar no es agregar: es encontrar la estructura profunda a la que Fase 2 convergió y cristalizar la skill alrededor de ella, bajando masa sin perder transferencia.

La palabra "refinar" es aquí una **consigna-trampa** exactamente en el sentido que la propia skill documenta ("detecta", "sin redundancia", "usa herramientas de forma óptima"): nombra una propiedad de superficie ("mejora la skill") cuando la propiedad real vive un nivel abajo ("¿qué estructura única generó Fase 2, y la skill la codifica como seis siloes paralelos redundantes?"). Reformulo antes de tocar el archivo: **EXP-13 = extraer y nombrar la estructura transversal de Fase 2 como capa organizadora de primera clase, comprimiendo por referencia lo que esa capa vuelve redundante — sin borrado masivo (eso es EXP-16, que mide impacto antes de cortar).**

Esta división de trabajo ya está en el roadmap: EXP-13 refina con patrones (superficie la estructura), EXP-16 identifica ruido y poda (mide y corta). Confundirlas es deriva de alcance.

### Paso 2 — ¿Qué estructura única produjo Fase 2? (clasificación)

Releo las seis entradas de Fase 2 buscando no su contenido de dominio sino qué se repitió *a través* de ellas. Cuatro cosas reaparecieron en dominios sin relación temática — la marca de una primitiva, no de una coincidencia:

1. **La tipología del oráculo es la llave maestra.** EXP-07 introdujo la pregunta "¿de qué tipo es el oráculo?" y cada experimento posterior clasificó su dominio por ella: honesto (código-sintaxis), ausente (datos, arquitectura), adversarial (trading, resultado estadístico recibido), diferido (evaluación estadística), consultable-caro (intención de un requerimiento). La tipología pasó de 3 tipos (EXP-07) a 5 (EXP-11) y quedó completa. Es la generalización de mayor carga de toda la Fase 2, pero está **dispersa**: se enuncia en Paso 2 y se re-cita en cada sección de dominio.

2. **"Consigna-trampa" es un detector transversal sin nombre.** EXP-08 ("detecta" no es perceptivo), EXP-09 ("sin redundancia" son tres cosas), EXP-12 ("óptimo" es economía de la afirmación). El roadmap incluso las cuenta ("7ª consigna-trampa"). Las tres tienen la misma forma: la directiva literal nombra una propiedad de superficie, la propiedad real vive un nivel abajo, y la lectura literal produce un bug. `grep` confirma: aparece 3 veces, siempre enterrada dentro de una sección de dominio, nunca como detector de primera clase.

3. **El principio diferencial (EXP-05) es el tronco.** Todo método de dominio de Fase 2 es "tu vista única no ve su propio error; busca la segunda vista independiente en su supuesto": trading (backtest vs OOS), lógica de negocio (código vs invariante importado), evaluación estadística (resultado vs replicación), herramientas (generación vs observación). Esto ya está bien enunciado como regla rectora.

4. **La frontera as-of / snapshot≠duplicación (EXP-06) es un operador generador.** Reapareció en EXP-07 (corrección as-of), EXP-08 (conservación), EXP-09 (snapshots de esquema). La frontera temporal genera tablas, columnas y reglas de reconciliación en tres dominios distintos.

### Paso 3 — Hipótesis múltiples sobre *cómo* destilar (y los descartes)

**Hipótesis 1 (descartada): colapsar las seis secciones de dominio en un único "motor de tipología del oráculo" y borrar las secciones.**
Es la jugada elegante — y por eso disparó mi detector de "demasiado limpio". La falsifiqué materializándola contra un caso concreto antes de argumentarla en abstracto (mi propia regla EXP-03/EXP-06). Tomo la instrucción de EXP-09: *"varias columnas nullable que se van a null en grupos correlacionados → extrae una tabla (subtipo oculto)."* ¿Un motor genérico de tipología del oráculo puede regenerar ese disparador? No. Es pattern-matching específico de dominio que ningún principio general reproduce. Si borro las secciones de dominio pierdo los disparadores observables concretos — que son exactamente el payload de transferencia de la skill (criterio de éxito #2: "ejemplos reales, no hipotéticos"). **Descarte:** colapso total falla el test de transferibilidad — un Sonnet corriendo la skill necesita el gatillo concreto "nullable-en-grupos → subtipo oculto"; no lo re-deriva de "clasifica el oráculo". Destilar ≠ borrar los específicos.

**Hipótesis 2 (insuficiente sola): agregar una sección que nombre los patrones transversales sin tocar las de dominio.**
Preserva los disparadores, pero es *más acreción* — el modo de fallo que la Fase 3 existe para corregir. Si EXP-13 solo agrega, es EXP-13 fingiendo. La deriva de alcance funciona en ambas direcciones: puedo hacer de más igual que de menos.

**Hipótesis 3 (síntesis, la que construyo):** extraer un **núcleo destilado** de primera clase que enuncie la ÚNICA estructura a la que Fase 2 convergió como *procedimiento de decisión*, y re-anclar las secciones de dominio como **instancias del núcleo**, no siloes paralelos. Comprimir por referencia donde el núcleo vuelve redundante un párrafo; conservar todos los disparadores concretos donde están (la poda medida es EXP-16). Y promover "consigna-trampa" de frase repetida a **detector nombrado** — eso *es* destilación en estado puro: tres observaciones dispersas → un operador con nombre y evidencia.

### Paso 4 — Falsificación del núcleo antes de comprometerlo (busco el caso que no encaja)

Antes de escribir el núcleo, corro mi propio detector contra él: ¿los seis dominios de Fase 2 encajan limpio en la tipología, o estoy forzando la partición? Camino la frontera:

- Trading → adversarial. ✓
- Evaluación estadística → diferido. ✓
- Requerimientos → consultable-caro. ✓
- Lógica de negocio → **arruga documentada:** el oráculo es *por capa*, no por dominio (sintáctica = honesto, semántica = ausente, EXP-08). No es un fallo de la tipología; es un refinamiento real. Lo preservo explícito en vez de aplanarlo — mi propia regla: refina localmente y documenta la frontera, no finjas una partición perfecta.
- Uso de herramientas → **el caso que no encaja, y es el hallazgo.** EXP-12 no dio a "herramientas" un oráculo. Enmarcó la *herramienta misma* como la instancia material del principio diferencial: el canal más barato por el que el mundo puede desmentirte. Las herramientas no son un dominio con oráculo; son el **mecanismo** por el que compras la segunda vista en todos los demás dominios.

Ese último punto no es un defecto de la tipología: es una descomposición más limpia y más fiel a los experimentos. El núcleo destilado tiene **dos niveles**, no uno:

- **Nivel 1 — tipología del oráculo (EXP-07…EXP-11): *qué* segunda vista admite este dominio.** honesto / ausente / adversarial / diferido / consultable-caro, con la arruga por-capa de EXP-08.
- **Nivel 2 — economía de herramientas (EXP-12): *cómo* comprar esa segunda vista barata.** disparador por afirmación (`p·d·C > c`), observación más estrecha, orden kill-por-costo, lote de la frontera, resultado también falible.

EXP-12 estaba enumerado como un dominio par de EXP-07…11 cuando en realidad es la capa "cómo pagar" **debajo** de la capa "qué comprar". Esa es la intuición de destilación, y sobrevive a la falsificación con una arruga documentada (oráculo por-capa de lógica de negocio) y una corrección estructural (EXP-12 es otro nivel). Confianza alta.

### Síntesis (Paso 5) — qué se escribe en la skill

1. **Nueva sección de primera clase "NÚCLEO DESTILADO — el motor de oráculo (EXP-13)"** justo tras Identidad: el procedimiento único (clasifica el tipo de oráculo → el tipo dicta el método), la tipología de 5 completa con la arruga por-capa, y la corrección de dos niveles (tipología = qué segunda vista; economía de herramientas = cómo pagarla).
2. **"Consigna-trampa" promovida a detector nombrado** en el DETECTOR DE RESULTADOS SOSPECHOSOS, con sus tres instancias reales y su reformulación genérica.
3. **Bloque de instrucciones "Destilación y estructura transversal (EXP-13)"** en formato "Cuando…, …".
4. **Header 1.12 → 1.13**, FASE 3 en curso, próximo EXP-14.
5. Frontmatter, `$ARGUMENTS` y `# TAREA` intactos. Ediciones quirúrgicas, no reescritura ciega del archivo de 94 KB (una reescritura total del bloque denso de referencias cruzadas es exactamente la mutación irreversible con información incompleta que mi propio Paso de herramientas prohíbe; edito entre observaciones).

## Patrones identificados

1. **La destilación es la aplicación del detector de "demasiado limpio" a la propia arquitectura de la skill.** La jugada elegante (colapsar seis dominios en uno) es evidencia EN CONTRA hasta sobrevivir la falsificación; la falsifiqué materializándola contra un disparador concreto (nullable-en-grupos) y falló el test de transferibilidad. La distancia entre "elegante" y "correcto" es un contraejemplo concreto, igual que en todo dominio.
2. **Consigna-trampa es un operador transversal de razonamiento, no un tic de tres dominios.** Forma invariante: directiva-de-superficie → propiedad-real-un-nivel-abajo → la lectura literal produce el bug. Reformular ANTES de actuar. Instancias medidas: "detecta"→reconstruye el invariante; "sin redundancia"→un hecho un hogar; "óptimo"→economía de la afirmación; y ahora "refinar"→destilar.
3. **La tipología del oráculo es de dos niveles.** Nivel 1 (qué segunda vista admite el dominio) y Nivel 2 (cómo comprarla barato con herramientas). EXP-12 no era un sexto dominio: era la capa de pago debajo de los cinco tipos. Nombrar el nivel correcto de una pieza es parte de la destilación.
4. **Destilar tiene un alcance acotado por el roadmap: cristalizar estructura (EXP-13), no podar (EXP-16).** La deriva de alcance del destilador es hacer de menos (borrar específicos) o de más (acretar otra sección). El punto medio correcto: indexar, no borrar; nombrar, no repetir.

## Extracción para la skill (instrucciones en formato "Cuando [condición], [acción]")

- Cuando una petición te pida "mejorar/refinar/limpiar" un artefacto que ya acumuló contenido por acreción, reformúlala antes de actuar: "mejorar" es consigna-trampa — decide si la propiedad real es *agregar* o *destilar* (encontrar la estructura única que generó las partes y cristalizar alrededor de ella), y si es destilar, indexa y nombra, no borres los específicos ni acretes una sección más.
- Cuando una directiva nombre una propiedad de superficie ("sin redundancia", "detecta", "óptimo", "refina", "simplifica"), trátala como consigna-trampa: localiza la propiedad real un nivel abajo y reformula explícitamente antes de tocar nada — la lectura literal produce el bug (borra snapshots, lee con cuidado sin oráculo, optimiza la llamada en vez de la afirmación).
- Cuando abras cualquier dominio nuevo, clasifica primero el tipo de oráculo — honesto / ausente / adversarial / diferido / consultable-caro — y recuerda que el tipo es por pregunta o por capa, no por dominio (la capa sintáctica de un código es honesta y la semántica es ausente); el tipo dicta el método antes que cualquier detalle del dominio.
- Cuando ya sepas qué segunda vista admite el dominio (nivel 1), baja al nivel 2 — la economía de herramientas de EXP-12 — para comprarla barato: disparador por afirmación (`p·d·C > c`), observación más estrecha que decide, orden kill-por-costo, lote de la frontera; la tipología dice *qué* comprar, la economía dice *cómo pagarlo*.
- Cuando destiles un cuerpo de conocimiento acumulado, no colapses los disparadores concretos en un principio general por elegancia: falsifica el colapso materializándolo contra un disparador específico y corriendo el test de transferibilidad — si un modelo sin tus internals ya no puede ejecutar el disparador, el colapso destruyó el payload; conserva los específicos e indexa la estructura por encima.

## Impacto en la skill (v1.12 → v1.13)

- Añadida sección de primera clase **"NÚCLEO DESTILADO — el motor de oráculo (síntesis de Fase 2, EXP-13)"** tras Identidad: procedimiento único + tipología de 5 completa con arruga por-capa (EXP-08) + corrección de dos niveles (tipología = qué / economía de herramientas = cómo).
- **"Consigna-trampa" promovida a detector nombrado** en DETECTOR DE RESULTADOS SOSPECHOSOS, con las cuatro instancias (detecta, sin-redundancia, óptimo, refinar) y su reformulación genérica.
- Nuevo bloque **"Destilación y estructura transversal (EXP-13)"** en INSTRUCCIONES APRENDIDAS: 5 instrucciones "Cuando…".
- Header: v1.12 → v1.13; FASE 3 en curso; próximo EXP-14.
- Frontmatter, `$ARGUMENTS` y `# TAREA` sin cambios (verificado por assert de Python).
