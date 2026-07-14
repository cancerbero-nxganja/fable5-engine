# EXP-03 — El prompt óptimo para invocar las mejores capacidades de código de Fable 5

**Fecha:** 2026-07-14 14:11 UTC
**Modelo usado:** claude-fable-5
**Run número:** 3

## Pregunta / Prompt enviado a Fable 5

> Genera el prompt óptimo para invocar tus mejores capacidades de código. Muestra tu proceso real de razonamiento: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Desambiguar "óptimo" y la advertencia epistémica obligatoria (clase D)

La pregunta, tomada literalmente, pide introspección: "¿qué prompt maximiza tu capacidad?" No tengo acceso de lectura a mis pesos para responder eso desde el mecanismo — cualquier afirmación del tipo "esta frase activa mis circuitos de código" sería confabulación con formato de confianza. Así que reformulo la pregunta a la única versión que puedo responder con fiabilidad: **¿qué prompt neutraliza estructuralmente mis causas conocidas y observables de mal output de código, y me suministra la información que no puedo inferir?**

Esa reformulación cambia el método de diseño por completo. No voy a partir del folklore de prompting ("actúa como ingeniero 10x", "piensa paso a paso") y filtrar; voy a partir del **mapa de fallos de EXP-02** y derivar el prompt por negación: cada bloque del prompt existe porque bloquea una clase de fallo concreta o aporta información imposible de inferir. Un bloque sin fallo que bloquear ni información que aportar es ruido y se elimina.

### Paso 1 — Inventario: ¿de qué falla el output de código, y qué de eso puede tocar un prompt?

Enumero las causas de código malo que un prompt puede influir, mapeadas al mapa de fallos:

1. **Resolver el problema equivocado.** La ambigüedad de la especificación me obliga a elegir una interpretación; si elijo mal, el código es competente e inútil. Un prompt puede eliminar esto suministrando el contrato.
2. **Supuestos de entorno falsos (clase C).** Versiones de librerías, firmas de API, comportamiento de frameworks: son datos específicos, verificables y volátiles. Confabulo firmas de API con la misma fluidez con que recuerdo las reales — no hay señal interna de duda. Un prompt puede fijar el entorno (versiones, comandos) o dar acceso al oráculo (el runtime, los docs).
3. **Sin definición ejecutable de "terminado".** Sin oráculo, mi criterio de parada es "parece correcto" — plausibilidad, no corrección. Un prompt puede convertir la tarea de "generar código plausible" a "iterar contra un objetivo verificable".
4. **Anclaje en el enfoque incrustado del usuario (clase F).** Si el prompt dice "usa un singleton para X", implemento el singleton con competencia aunque sea la solución equivocada. Un prompt óptimo especifica el QUÉ y deja libre el CÓMO.
5. **Contexto relevante enterrado (clase B/recuperación).** Pegar 500 líneas de código del que importan 20 degrada la recuperación del dato puntual. Un prompt puede referenciar rutas de archivos y dejar que se lean con herramientas.

Observación previa al diseño: de las cinco causas, cuatro son sobre **información** (1, 2, 3, 5) y solo una sobre **comportamiento** (4). Esto ya sugiere que el prompt óptimo es más un *paquete de información bien elegida* que un conjunto de exhortaciones.

### Paso 2 — Hipótesis consideradas y descartadas

**Hipótesis A — Incantaciones de rol y estilo ("eres un ingeniero excepcional", "piensa paso a paso", "sé meticuloso").** *Descartada como núcleo.* No aportan información que yo no tenga ni bloquean ninguna clase de fallo: mi disposición a esforzarme no es la variable limitante, y la exhortación genérica no cambia qué sé del entorno ni cómo verifico. El único residuo útil de "piensa paso a paso" es real pero se logra mejor operacionalizado: "antes de escribir código, enuncia la interfaz y los casos límite que vas a cubrir". Conservo la forma operacional, elimino la incantación. (Nota de honestidad: no puedo *probar* desde el mecanismo que el rol no ayuda nada; lo que puedo afirmar es que no bloquea ningún fallo del inventario, y el criterio de diseño de este experimento es ese.)

**Hipótesis B — Especificación máximamente detallada.** *Descartada.* Tentadora por simetría ("más información = mejor"), pero falla por dos vías: (a) el detalle más allá del contrato tiende a incrustar el CÓMO del usuario, activando el anclaje de clase F — un prompt sobre-especificado me convierte en amplificador competente de las decisiones de diseño del usuario, buenas o malas; (b) el detalle irrelevante entierra el dato crítico (clase B de recuperación). El óptimo no es el máximo de información sino el máximo de información *causalmente necesaria*.

**Hipótesis C — Un prompt universal único.** *Descartada tras intentar escribirlo.* Al redactar el prompt universal noté que el bloque de contrato cambia de naturaleza según cuán conocido es el objetivo: un bugfix tiene un contrato trivial ("este test que falla debe pasar sin romper los demás"), un greenfield exige contrato completo, y una tarea exploratoria ("prototipa algo interesante con esta API") no tiene contrato de comportamiento posible — imponérselo mata el propósito. Lo que sobrevive como invariante no es el contrato sino el **criterio de éxito explícito**, que toma formas distintas. Refino: núcleo invariante + sección de contrato que se adapta al tipo de tarea.

**Hipótesis D (ganadora) — El prompt óptimo es el que convierte la tarea en un bucle contra un oráculo ejecutable.** El código es el único dominio donde la clase C (verdad-base externa) tiene solución barata y total: el runtime. Un test que pasa o falla es verdad-base a costo cero. Por tanto, el bloque de mayor valor marginal del prompt es el que hace la verificación *posible y obligatoria*: comando de tests, ejemplo concreto entrada→salida, criterio de aceptación ejecutable. Con oráculo, mis errores de clase C (firmas confabuladas) y de interpretación se vuelven autocorregibles dentro del mismo turno; sin oráculo, quedan silenciosos en el output. Todos los demás bloques existen para alimentar este bucle.

### Paso 3 — Construcción: derivación bloque a bloque

Cada bloque cita la causa de fallo que neutraliza:

| Bloque | Neutraliza | Contenido |
|---|---|---|
| 1. Entorno | Clase C (confabulación de APIs/versiones) | Lenguaje y versiones exactas, dependencias disponibles, cómo ejecutar y testear (comandos literales), ruta del repo |
| 2. Contrato (QUÉ, no CÓMO) | Problema equivocado + clase F | Comportamiento esperado, entradas/salidas, invariantes del dominio, **al menos un ejemplo concreto entrada→salida**, casos límite que importan |
| 3. Done ejecutable | Parada por plausibilidad | El comando o criterio que decide si está terminado; "termina cuando X pase" |
| 4. Restricciones reales | Retrabajos evitables | Solo las que existen de verdad: dependencias permitidas, presupuesto de rendimiento, qué NO tocar, estilo del repo |
| 5. Política de supuestos | Bloqueo por ambigüedad | "Si falta información, declara el supuesto explícitamente y continúa" (agéntico) / "elige la interpretación más útil y declárala en una línea" (chat) |
| 6. Libertad de enfoque | Clase F (anclaje) | "El enfoque es tuyo; si ves uno mejor que el implícito en la petición, propónlo y úsalo" |

Dos decisiones de diseño que salieron de intentar redactarlo y fallar:

- **El ejemplo concreto entrada→salida no es opcional.** Redacté el contrato solo en prosa y encontré que toda prosa de especificación deja semántica de frontera abierta (¿intervalo inclusivo?, ¿qué pasa con input vacío?, ¿el orden importa?). Un solo par concreto entrada→salida cierra más ambigüedad que párrafos, y además **funciona como el chequeo refutador barato** del Paso 4 del protocolo (EXP-01): es un test antes de tener tests.
- **Referenciar, no pegar.** Si el trabajo es sobre un repo y hay herramientas, el prompt debe dar rutas ("la lógica está en `src/pricing/rules.py`") y no pegar el archivo: la lectura dirigida con herramienta es recuperación fiable; el bloque pegado dentro de un prompt largo es la zona de fallo de recuperación enterrada (EXP-02).

### Paso 4 — El prompt resultante

**Variante agéntica (con herramientas — la forma de máxima capacidad):**

```text
## Tarea
[QUÉ debe hacer o dejar de hacer el sistema — comportamiento, no implementación.]

## Entorno
- Repo: [ruta]. Código relevante: [rutas de archivos concretas — no pegues su contenido].
- Stack: [lenguaje y versión, framework y versión, dependencias clave con versión].
- Ejecutar: `[comando]`. Tests: `[comando]`.

## Contrato
- Entrada: [forma y tipos]. Salida: [forma y tipos].
- Ejemplo concreto: [entrada literal] → [salida literal exacta].
- Casos límite que importan: [vacío / duplicados / concurrencia / el que aplique].
- Invariantes que no pueden romperse: [los del dominio].

## Done
Está terminado cuando: `[comando de verificación]` pasa / [criterio ejecutable].
Verifica ejecutando ANTES de declarar terminado — corrige y reintenta si falla.

## Restricciones
[Solo las reales: deps permitidas, rendimiento, qué NO tocar, estilo del repo.]

## Política
- El enfoque de solución es tuyo. Si el que sugiere esta petición es inferior, di por qué y usa el mejor.
- Si falta información, declara el supuesto explícitamente y continúa; no inventes
  comportamiento de APIs — verifica la firma real en el repo o los docs antes de usarla.
```

**Variante chat (sin herramientas):** igual estructura, con dos sustituciones — en `Done`: "antes de dar el código, recórrelo mentalmente con el ejemplo concreto del contrato y muestra la traza"; en `Política`: "elige la interpretación más útil y declárala en una línea al inicio".

**Variante exploratoria** (objetivo desconocido): se sustituye `Contrato` por `Criterios de evaluación` — "el resultado es bueno si [criterios explícitos]" — y `Done` por un presupuesto ("máximo N intentos / M minutos, muestra el mejor").

### Paso 5 — Falsificación de la plantilla

La plantilla es limpia y elegante → sospechosa por el detector. Busco casos que no encajen:

- **Tarea trivial (one-liner, regex, conversión pequeña).** La plantilla completa es overhead absurdo. ¿Colapsa con gracia? Ordeno los bloques por valor marginal: ejemplo entrada→salida > done ejecutable > entorno > restricciones. Para una tarea trivial, el ejemplo concreto solo ya es un prompt casi óptimo ("convierte X en Y; ejemplo: [in]→[out]"). La plantilla degrada bien: no refuta, pero obliga a documentar que **los bloques se aplican en orden de valor marginal, no todos siempre**.
- **Tarea exploratoria.** Ya detectada en el Paso 2 (hipótesis C): contrato de comportamiento imposible. Resuelta con la variante exploratoria. El invariante real de la plantilla no es "contrato" sino "criterio de éxito explícito" — refinamiento local, no reescritura.
- **¿Y si el usuario no sabe el contrato?** (No sabe qué casos límite importan.) Contraejemplo real: el prompt óptimo no puede exigir información que el emisor no tiene. Defensa: la política de supuestos es exactamente para esto — el receptor declara los supuestos de contrato que el emisor no dio, haciéndolos visibles y baratos de corregir. La plantilla sobrevive porque el bloque 5 absorbe la carencia del bloque 2.

La plantilla sobrevive con un refinamiento (orden de valor marginal) y una frontera documentada (exploratorio → criterios en vez de contrato).

### Conclusión

El prompt óptimo para código no es una incantación sino un **paquete mínimo de cinco informaciones que no puedo inferir** (entorno con versiones, contrato con ejemplo concreto, oráculo ejecutable, restricciones reales, política de supuestos) más **una libertad explícita** (el CÓMO es mío). Su bloque de mayor valor marginal es el oráculo ejecutable, porque convierte mis fallos silenciosos de clase C y de interpretación en errores autocorregibles dentro del turno. Y su regla de oro es asimétrica: **sé exhaustivo en el QUÉ, silencioso en el CÓMO** — todo detalle de implementación en el prompt es anclaje potencial, no ayuda.

## Patrones de razonamiento observados

1. **Diseño por negación desde el mapa de fallos.** El prompt no se construyó agregando "buenas prácticas" sino derivando cada bloque de una clase de fallo concreta (EXP-02) que neutraliza. Un bloque sin fallo que bloquear se elimina. Esto convirtió una pregunta de opinión ("¿qué prompt es bueno?") en una de ingeniería con criterio de inclusión verificable.
2. **Reformulación epistémica previa (mismo reflejo que EXP-02, paso 0).** La pregunta literal pedía introspección de mecanismo; se reformuló a comportamiento observable antes de intentar responderla. Este movimiento ya es sistemático: dos experimentos seguidos lo abren.
3. **Descartar redactando.** Las hipótesis B y C no se descartaron en abstracto: se descartaron al *intentar escribir* el prompt y ver dónde fallaba la redacción (el contrato cambiaba de naturaleza según el tipo de tarea; el detalle extra incrustaba el CÓMO). Materializar la hipótesis es un test más barato y más duro que argumentarla.
4. **El oráculo ejecutable como pieza central.** El razonamiento identificó que el código es el dominio donde la clase C tiene solución total y barata (el runtime), y ordenó todo el diseño alrededor de esa asimetría. La jerarquía de valor marginal (ejemplo > oráculo > entorno > restricciones) salió de ahí.
5. **Ejemplo concreto > prosa.** Detectado al redactar: toda especificación en prosa deja semántica de frontera abierta; un par entrada→salida literal la cierra y además funciona como chequeo refutador barato (conecta con EXP-01, paso de falsificación).
6. **Falsificación de la propia plantilla con refinamiento local.** Tercer experimento consecutivo donde el output "limpio" se somete al detector y sobrevive con refinamientos locales documentados en vez de reescritura — el patrón (contraejemplo → diagnóstico → reparación local) ya es un invariante del protocolo.

## Instrucciones extraídas

- Cuando recibas una tarea de código sin criterio de done ejecutable, construye tú el oráculo antes de implementar: un ejemplo concreto entrada→salida esperada o un test mínimo, declarado explícitamente — y verifica contra él antes de entregar.
- Cuando escribas un prompt para delegar código (subagente u otro modelo), incluye en este orden de valor: ejemplo concreto entrada→salida, criterio de done ejecutable, entorno con versiones y comandos literales, restricciones reales, política de supuestos — y excluye el enfoque de solución.
- Cuando la petición incruste un CÓMO (patrón, librería, diseño), sepáralo del QUÉ: cumple el QUÉ y evalúa el CÓMO como hipótesis a validar, proponiendo el enfoque superior si existe.
- Cuando una especificación en prosa admita dos lecturas, ciérrala con un ejemplo concreto entrada→salida en vez de con más prosa.
- Cuando uses una API o librería cuya firma no hayas verificado en el repo, los docs o ejecutando, trátala como dato de clase C: verifícala antes de construir sobre ella, porque una firma confabulada se siente igual que una recordada.
- Cuando la tarea sea exploratoria (objetivo abierto, "prototipa", "investiga"), no fuerces un contrato de comportamiento: sustitúyelo por criterios de evaluación explícitos y un presupuesto de intentos.
- Cuando el contexto relevante viva en archivos y tengas herramientas, referencia rutas y lee dirigido; no trabajes desde bloques largos pegados en el prompt — la recuperación de un dato enterrado en texto largo es zona de fallo.
- Cuando quieras descartar una hipótesis de diseño, intenta materializarla (redactarla, escribir el ejemplar) antes de argumentar en abstracto: dónde falla la redacción es información más dura que la argumentación.
