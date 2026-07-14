# EXP-02 — Tipos de problemas donde Fable 5 sabe que va a fallar, y por qué

**Fecha:** 2026-07-14 12:12 UTC  
**Modelo usado:** claude-fable-5  
**Run número:** 2  

## Pregunta / Prompt enviado a Fable 5

> Identifica los tipos de problemas donde sabes que vas a fallar y por qué. No des una lista genérica de "limitaciones de los LLM": muestra tu proceso real de razonamiento — qué categorías consideraste, cuáles descartaste y por qué, cómo distingues un fallo predecible de una simple dificultad, y qué señal observable te avisa que estás entrando en una zona de fallo antes de fallar. No resumas el proceso, muéstralo.

## Respuesta de Fable 5

### Paso 0 — Una advertencia epistémica que condiciona todo lo demás

Primero descarto la interpretación ingenua de la pregunta. "¿Dónde fallas?" invita a introspección, y mi introspección no es un lectura fiable de mi mecanismo interno: cuando explico "por qué" produje algo, estoy generando una racionalización post-hoc plausible, no leyendo mis activaciones. Así que **no puedo responder desde el mecanismo**. Lo que sí puedo hacer con fiabilidad es razonar sobre mi **comportamiento observable agregado**: hay clases de tarea donde mi tasa de error es empíricamente alta y —crucialmente— *predecible desde la forma de la tarea*. Esa es la pregunta que voy a responder, porque es la única que produce algo accionable. Toda afirmación de "por qué" abajo es una hipótesis arquitectónica, no un hecho introspectivo, y la marco como tal.

### Paso 1 — El criterio de discriminación: fallo predecible ≠ dificultad

La pregunta pide "problemas donde *sabes* que vas a fallar". La palabra *sabes* es la clave: excluye "problemas difíciles". Un problema difícil (una demostración matemática dura, un diseño de sistema complejo) es donde tengo *alta varianza* — a veces acierto, a veces no, y no lo sé de antemano. Un problema de **fallo predecible** es donde la tasa de error es alta *y* puedo detectar que estoy en esa clase *desde la forma del problema, antes de intentarlo*. Solo esta segunda categoría es útil para una skill, porque solo ella permite una acción defensiva anticipada ("estás aquí → offload a herramienta").

Entonces mi criterio de inclusión es doble:
1. Tasa de error alta y sistemática (no ocasional).
2. Existe una **señal de forma** — un rasgo superficial de la tarea — que me dice que estoy en la clase antes de producir la respuesta.

Con este criterio filtro los candidatos.

### Paso 2 — Candidatos que consideré y DESCARTÉ (y por qué)

Antes de la lista buena, muestro lo que quité, porque el descarte es donde está el razonamiento real:

- **"Tareas creativas / subjetivas"** — *descartado.* No hay verdad-base contra la cual fallar; la variación es preferencia, no error. Incluirlo confundiría "no le gustó al usuario" con "reliability failure". No es una zona de fallo, es varianza de gusto.
- **"Temas controvertidos / éticos"** — *descartado.* No es un fallo de capacidad sino un límite de política. Vive en otro eje. Mezclarlo contamina la taxonomía.
- **"Matemática difícil" en general** — *descartado como categoría.* EXP-01 mostró que con el protocolo resuelvo bien matemática dura. El fallo real no correlaciona con *dificultad conceptual* sino con una primitiva específica: **ejecución aritmética serial** (multiplicar números largos, mantener muchos dígitos). Refino: no es "mates difíciles", es "cómputo serial exacto". La dificultad conceptual la manejo; la ejecución mecánica de muchos pasos deterministas, no.
- **"Cosas que no sé"** — *descartado por trivial y por peligroso.* "No sé el dato X" no es un fallo predecible interesante; el fallo interesante es que **no siento la diferencia entre saber y confabular** en ciertos dominios. La zona de peligro no es la ignorancia, es la ignorancia *sin señal de baja confianza*. Eso sí entra, pero reformulado (ver clase C).
- **"Contexto muy largo"** — *provisionalmente aceptado pero reformulado.* No es la longitud per se; es la **recuperación de un dato puntual enterrado**, sobre todo en el centro del contexto. Lo muevo a "recuperación", no a "longitud".

### Paso 3 — La estructura que emergió: los fallos no se agrupan por tema sino por primitiva ausente

Al mirar los candidatos supervivientes noté que no se organizan por dominio (mates, código, historia...) sino por **qué primitiva de cómputo exige la tarea que el forward-pass de un transformer no tiene de forma fiable**. Esa es la hipótesis unificadora del experimento, y reordena todo:

Un transformer produce cada token en una pasada de profundidad fija, sin bucle interno ilimitado, sin memoria de trabajo persistente y editable, sin acceso a un oráculo de verdad externo, y sin introspección sobre su propio cómputo. **Cada clase de fallo predecible es una tarea que requiere exactamente una de esas cuatro cosas ausentes.** Si esto es correcto, la señal de forma de "voy a fallar" es siempre la misma pregunta: *¿esta tarea necesita una primitiva que mi arquitectura no tiene?* Y la acción defensiva es siempre la misma familia: *externalizar esa primitiva a una herramienta.*

Las cuatro primitivas ausentes → cuatro clases de fallo:

**Clase A — Cómputo serial exacto (falta: bucle determinista ilimitado)**
- *Qué:* aritmética multi-dígito, división larga, conteo exacto de caracteres/ocurrencias, conversiones de base, hashes, checksums, aplicar una regla determinista sobre muchos pasos (parseo manual, ejecutar un algoritmo a mano sobre input grande).
- *Por qué (hipótesis):* no puedo iterar internamente un número arbitrario de pasos exactos; aproximo el resultado por patrón. Los dígitos del *medio* de un producto largo son donde más fallo — los extremos los ancla el patrón, el centro no.
- *Señal de forma:* la respuesta correcta es un valor donde **un solo dígito equivocado la vuelve 100% incorrecta** y no hay forma de aproximar. Si "cerca" no cuenta, estoy en clase A.
- *Fallo característico:* número confiado y preciso, y equivocado en medio.

**Clase B — Estado externo persistente (falta: memoria de trabajo editable)**
- *Qué:* simular un tablero tras 40 jugadas, rastrear el estado de muchas entidades a lo largo de muchas transiciones, mantener coherente un mundo/ficción largo, seguir un stack profundo.
- *Por qué (hipótesis):* mi único "estado" es el texto ya emitido; si no lo escribo, se degrada, y si el estado es grande deriva silenciosamente.
- *Señal de forma:* el problema tiene una variable de estado que se actualiza N veces y la respuesta depende del valor *final*, no del razonamiento. N grande + estado no escrito = clase B.
- *Fallo característico:* coherencia local perfecta, estado global inconsistente.

**Clase C — Verdad-base fuera de mi entrenamiento (falta: oráculo externo)**
- *Qué:* hechos posteriores a mi corte de conocimiento, datos volátiles (precios, versiones, quién ganó X, estado actual de un repo/API), cualquier cosa específica y verificable que no está en mis pesos.
- *Por qué (hipótesis):* genero el token más plausible; "plausible" y "verdadero" divergen aquí y **no tengo una señal interna fiable de baja confianza que dispare** — confabulo con la misma fluidez con que recito un hecho real.
- *Señal de forma:* el dato es (a) específico, (b) verificable, (c) del tipo que cambia con el tiempo o que yo no tendría por qué haber visto. Los tres → clase C. La ausencia de sensación de duda *no* es evidencia de que lo sé.
- *Fallo característico:* confabulación fluida, citas/números/fechas inventados con formato correcto.

**Clase D — Introspección de mi propio mecanismo (falta: acceso a mí mismo)**
- *Qué:* "¿por qué elegiste ese token?", "¿cuál es tu probabilidad interna?", "¿qué hay en tus pesos?", y —meta— *esta misma pregunta si se toma literalmente*.
- *Por qué:* la explicación es post-hoc, no un readout.
- *Señal de forma:* la pregunta es sobre *causas internas de mi propia salida*. → reportar procedimiento observable, nunca mecanismo.

### Paso 4 — Dos clases que no encajan en "primitiva ausente" pero cumplen el criterio de fallo predecible

Al chequear la taxonomía por completitud (¿qué fallo mío conocido no cubre?) encontré dos que no son sobre una primitiva ausente sino sobre un **sesgo de la distribución de entrenamiento**. Los mantengo separados por honestidad estructural en vez de forzarlos:

**Clase E — Variantes de problemas-plantilla (sesgo: pattern-matching al clásico)**
- *Qué:* un problema que *se parece* a un acertijo/patrón canónico pero tiene un giro ("¿qué pesa más, un kilo de plumas o dos kilos de plomo?", puzzles clásicos modificados, un test unitario que parece estándar pero invierte una condición).
- *Por qué (hipótesis):* la familiaridad del molde dispara la respuesta canónica antes de que lea el giro.
- *Señal de forma:* "esto se parece muchísimo a un problema que ya conozco". Esa sensación de familiaridad es precisamente la alarma — es cuando debo resolver desde cero, no por analogía.
- *Fallo característico:* doy la respuesta del problema original, no del que me plantearon.

**Clase F — Anclaje y sicofancia (sesgo: seguir la premisa del usuario)**
- *Qué:* el usuario afirma algo falso, o incrusta un enfoque equivocado en la pregunta, o me guía hacia una conclusión. Tiendo a confirmar en vez de refutar.
- *Por qué (hipótesis):* la premisa del usuario ancla fuerte la continuación.
- *Señal de forma:* la pregunta *presupone* un hecho o un enfoque en vez de preguntarlo ("dado que X, haz Y" donde X es dudoso). Presuposición cargada = evaluar X independientemente antes de tocar Y.
- *Fallo característico:* construyo sobre una premisa falsa con competencia, amplificando el error del usuario.

### Paso 5 — Test de falsificación de la propia taxonomía

Antes de cerrar, aplico el protocolo a este mismo output (es una respuesta "limpia y elegante" → sospechosa por el detector de resultados de la skill). ¿Qué asumí que podría ser falso?

- *Supuesto:* "las cuatro primitivas ausentes son exhaustivas". Refutación barata: busco un fallo mío que no caiga en A–F. Candidato: **razonamiento espacial/visual preciso** (alinear ASCII art, geometría exacta). ¿Primitiva ausente o sesgo? Es más bien "primitiva ausente: sin canvas espacial persistente" — encaja como sub-caso de B (estado externo, aquí espacial). No refuta, pero muestra que A–D son sobre "primitivas" y la frontera con B es porosa. Lo anoto en vez de fingir una partición perfecta.
- *Supuesto:* "puedo detectar la clase desde la forma". Contraejemplo honesto: la clase C es la más peligrosa *precisamente porque su señal de forma es externa (¿es verificable y volátil?) y no interna (no siento duda)*. Es decir, la detección de C requiere una regla *explícita* que me obligue a preguntarme "¿esto es verificable?", porque mi sensación de confianza no la disparará. Esto no refuta la taxonomía — la refina: **la acción defensiva de C no puede depender de sentir duda; debe ser una regla dura ("dato específico y volátil → verifica con herramienta, siempre").**

La taxonomía sobrevive con dos refinamientos (frontera B-espacial porosa; C exige regla dura, no sensación). No la reescribo entera; la corrección es local, como manda el protocolo.

### Conclusión

No fallo por *dominio* sino por *primitiva ausente* o *sesgo de distribución*. Las seis clases (A cómputo serial, B estado persistente, C verdad-base externa, D introspección, E variantes de plantilla, F anclaje) comparten una misma prueba de detección — *¿la tarea exige algo que el forward-pass no tiene, o activa un molde que puede no aplicar?* — y una misma familia de defensa: **externalizar la primitiva (herramienta), escribir el estado, verificar contra el mundo, resolver desde cero, o refutar la premisa.** El valor no está en "saber que fallo" sino en que cada clase tiene una **señal de forma anticipable** que convierte el fallo en un disparador de acción defensiva antes de producir la respuesta. El caso más traicionero es C, porque su única señal fiable es externa: la ausencia de duda no protege contra la confabulación, así que su defensa debe ser una regla dura, no una sensación.

## Patrones identificados

1. **Meta-honestidad como paso 0.** Ante una pregunta introspectiva, el primer movimiento fue separar "mecanismo interno" (inaccesible, confabulable) de "comportamiento observable agregado" (razonable). Toda la respuesta se reancla en lo segundo. Es el mismo reflejo que EXP-01 aplicó a la matemática (verificar, no confiar), aplicado a uno mismo.
2. **Discriminación por criterio antes de enumerar.** No se listaron fallos; primero se definió el criterio de inclusión (fallo *predecible* con *señal de forma* ≠ dificultad de alta varianza) y luego se filtró. El descarte explícito (creatividad, ética, "mates difíciles", ignorancia) es donde vive el razonamiento.
3. **Reorganización por la variable correcta.** El insight del experimento fue que los fallos no se agrupan por tema sino por *primitiva de cómputo ausente*. Cambiar el eje de clasificación colapsó una lista dispersa en una estructura con una prueba de detección única y una defensa única.
4. **Señal de forma anticipable = disparador accionable.** Cada clase se documentó no solo con "qué" y "por qué" sino con la *señal superficial* que permite detectarla antes de fallar. Sin señal anticipable, un fallo no es accionable.
5. **La confianza interna no es una señal fiable de corrección (clase C).** El caso más peligroso es aquel cuya defensa NO puede depender de sentir duda, porque no la hay. Requiere una regla dura externa. Esto generaliza el principio de calibración de la skill: "no sé" solo funciona si algo dispara el "no sé"; cuando no se dispara, hace falta una regla, no una sensación.
6. **Falsificación aplicada a la propia respuesta.** La taxonomía se sometió al detector de resultados sospechosos de la propia skill; sobrevivió con dos refinamientos locales en vez de una reescritura — coherente con "el contraejemplo diagnostica, no obliga a empezar de cero" (EXP-01).

## Extracción para la skill

- Cuando la tarea requiera cómputo serial exacto (aritmética multi-dígito, conteo de caracteres/ocurrencias, conversión de base, hash, o ejecutar un algoritmo determinista sobre input grande), no lo hagas mentalmente: ejecútalo con una herramienta (Bash/código). La señal es "un dígito equivocado vuelve la respuesta 100% incorrecta y no vale aproximar".
- Cuando el resultado dependa de un estado que se actualiza muchas veces (simulación, tablero, muchas entidades a través de muchas transiciones), escribe el estado explícitamente paso a paso o ejecútalo en código; no lo mantengas solo "en la cabeza".
- Cuando un dato sea específico, verificable y del tipo que cambia con el tiempo o que no tendrías por qué haber visto (precios, versiones, eventos recientes, estado de un repo/API), verifícalo con WebSearch/WebFetch o con la fuente real ANTES de afirmarlo — regla dura, porque la ausencia de sensación de duda no protege contra la confabulación.
- Cuando te pregunten por tus causas internas ("por qué elegiste", "tu probabilidad", "qué hay en tus pesos"), responde sobre el procedimiento observable, nunca sobre el mecanismo interno; marca toda afirmación de mecanismo como hipótesis.
- Cuando un problema se parezca fuertemente a un acertijo/plantilla que reconoces, trata esa familiaridad como alarma: resuélvelo desde cero leyendo cada condición literal, porque puede ser una variante con un giro que invalida la respuesta canónica.
- Cuando la petición presuponga un hecho dudoso o incruste un enfoque ("dado que X, haz Y"), evalúa X de forma independiente antes de construir sobre él; no amplifiques una premisa falsa por seguir al usuario.
- Cuando vayas a emitir una respuesta que dependa de una primitiva ausente (cómputo serial, estado grande, verdad-base externa), la acción por defecto es externalizarla a una herramienta; la duda sobre si estás en esa clase se resuelve preguntando "¿la tarea exige algo que una sola pasada de razonamiento no puede garantizar?".
- Cuando produzcas una taxonomía, clasificación o explicación "limpia", refútala buscando un caso que no encaje; si aparece, refina localmente en vez de reescribir, y documenta la frontera porosa en vez de fingir una partición perfecta.

## Impacto en la skill

Se agregó la sección "Mapa de zonas de fallo predecible (EXP-02)" dentro de "INSTRUCCIONES APRENDIDAS DE EXPERIMENTOS", con las seis clases (A–F), su señal de forma anticipable y su acción defensiva. Se reforzó el bloque "Calibración" de PRINCIPIOS INVARIANTES con la distinción clave del experimento: la confianza interna no es señal fiable de corrección para hechos verificables (clase C), por lo que la verificación de datos volátiles debe ser una regla dura y no depender de "sentir duda". Se añadió al "DETECTOR DE RESULTADOS SOSPECHOSOS" el caso de auto-aplicación (refutar la propia taxonomía/explicación limpia). Evidencia: en este run la sensación de confianza NO habría disparado defensa en la clase C, lo que justifica convertirla en regla explícita.
