# EXP-11 — Cómo Fable 5 maneja ambigüedad en requerimientos

**Fecha:** 2026-07-15 06:13 UTC
**Modelo usado:** claude-fable-5
**Run número:** 11

## Pregunta / Prompt enviado a Fable 5

> Te llega este requerimiento de un product manager, tal cual, sin más contexto. Documenta cómo lo manejas — qué ambigüedades detectas y cómo, cuáles resuelves solo y cuáles preguntas, en qué formato, y qué haces si no hay nadie a quien preguntar. Muestra el razonamiento completo: hipótesis de método consideradas, descartadas y por qué.
>
> *"Necesitamos que el sistema envíe un recordatorio a los usuarios inactivos cada semana. Si el usuario sigue inactivo después de 3 recordatorios, desactiva su cuenta y notifica al admin. Además, agrega un endpoint para exportar los usuarios a CSV."*

## Respuesta de Fable 5

### Paso 0 — Reformulación: la ambigüedad no es una propiedad del texto

"Maneja la ambigüedad" suena a "elimina la ambigüedad", y esa lectura lleva a los dos extremos malos: el cuestionario exhaustivo (preguntar todo) o la especificación total (documentar todo). Pero la ambigüedad **no es una propiedad del texto: es una propiedad del par (texto, decisión)**. Una frase con dos lecturas cuyas dos lecturas llevan a la misma implementación — o a implementaciones que cuesta un renglón intercambiar — no es ambigua en ningún sentido que importe. La que importa es la que hace **divergir decisiones caras**.

Reformulación: *"maneja la ambigüedad"* → *"detecta dónde las lecturas divergen, encamina cada divergencia según divergencia × costo de reversión (asumir-declarando vs. preguntar-en-lote), y construye de modo que el supuesto equivocado sea barato de corregir"*. Es la sexta consigna-trampa consecutiva ("detecta" EXP-04/08, "hazla operable" EXP-07, "sin redundancia" EXP-09, "¿es real?" EXP-10): el objetivo que suena unívoco esconde la decisión real.

### Asimetría estructural contra los dominios más cercanos ya resueltos

Dos vecinos. Contra **EXP-03 (especificar para delegar)**: allí yo escribo la especificación y el ejemplo concreto **cierra** la semántica de frontera que la prosa deja abierta. Aquí estoy del otro lado del mismo fenómeno: recibo la prosa que alguien más no cerró. La herramienta es la misma invertida — donde el ejemplo *cerraba* fronteras, aquí el ejemplo las **abre a la vista**: caminarlo fuerza cada decisión que la prosa difirió. Contra **EXP-10 (resultado recibido)**: la simetría es exacta — allí el número llega hecho y el procedimiento es invisible; aquí el texto llega hecho y **la intención es invisible**. Pero hay una asimetría crucial: en EXP-10 el oráculo (replicación) estaba diferido; aquí el oráculo — el autor del requerimiento — **existe, está vivo y se le puede preguntar**. El costo es que cada consulta es un round-trip con latencia y presupuesto de atención, y su fiabilidad es asimétrica: la gente responde mal a preguntas abstractas ("¿qué significa inactivo?") y bien a concreciones ("si María no abre la app pero su suscripción se renueva sola, ¿está inactiva?"). Un oráculo **consultable pero caro, mejor reaccionando que especificando**. Eso fija el método: minimizar consultas (lote), maximizar su rendimiento (formato decisión), y preferir mostrar concreciones a hacer preguntas abiertas.

### Hipótesis de método — consideradas y descartadas

**H0: "pregunta todo lo que no esté claro."** Descartada por materialización numérica. El párrafo del PM contiene 8 dimensiones ambiguas con 2–3 lecturas cada una: **864 implementaciones distintas** caben en esas tres frases [CALC1]. Preguntar las 8 convierte un requerimiento de dos líneas en un interrogatorio, quema el presupuesto de atención del PM, y la mitad de las preguntas no cambia ninguna decisión cara (¿digest o email por usuario? — se cambia en 10 minutos cuando se sepa). Es el hermano del "especificación máxima" que ya cayó en EXP-03: el costo de cerrar todo excede el valor de la mayoría de los cierres.

**H1: "elige la interpretación más útil y sigue" — la instrucción vigente de esta skill (Paso 1, v1.10).** Descartada como regla general por cómputo: eligiendo en silencio con 80% de acierto por dimensión (generoso), P(acertar la intención en las 8) = 0.8⁸ = **16.8%** [CALC2]. La elección silenciosa *compone*: cinco de cada seis implementaciones entregadas difieren de la intención en al menos un eje — y en este caso dos de los ejes son "desactivar cuentas equivocadas" y "exponer PII". La instrucción sobrevive solo como caso particular (dimensiones convergentes o baratas); como regla general, este experimento la falsifica. *(Refinamiento local de la propia skill, patrón EXP-02: contraejemplo → diagnóstico → reparación local.)*

**H2: "la ambigüedad se detecta releyendo con cuidado."** Descartada por el principio diferencial (EXP-05). Leer es compilar con defaults: cuando el texto calla, tu comprensión rellena el hueco con el valor más disponible, **y el rellenado no deja rastro** — la lectura fluida se siente igual con texto completo que con texto agujereado. La ambigüedad peligrosa no es la que ves y resuelves mal; es la que no ves porque ya la resolviste sin notarlo (hermana de la deriva de alcance). Una segunda lectura usa el mismo compilador con los mismos defaults: segunda *cuenta*, no segunda *vista*. El detector tiene que ser material, no perceptivo.

**H3 (convergida): ejemplo caminado como detector + triage divergencia × irreversibilidad + lote en formato decisión + registro de supuestos.** Es la que ejecuto abajo.

### Método ejecutado sobre el caso

**1. Detector: caminar una entidad concreta por el texto, de punta a punta.** María se registró en enero; su último login fue el 3 de junio; su suscripción se renueva sola; hoy es 15 de julio. Camino el requerimiento con ella y **cada paso que el texto no decide es una ambigüedad forzada a la superficie**:

- ¿María está "inactiva"? → **A1**: ¿inactivo = sin login, sin actividad de negocio (su suscripción SÍ se renovó), o sin sesión? *(3 lecturas)*
- ¿Desde cuándo se cuenta? → **A2**: ¿30 días, desde registro, configurable? *(3)*
- "Cada semana" → **A3**: ¿todos los lunes (ancla global) o cada 7 días desde que ella cruzó el umbral (ancla por usuario)? *(2)*
- María abre la app entre el recordatorio 2 y el 3 → **A4**: ¿se resetea el contador? El texto dice "sigue inactiva después de 3": ¿"sigue" mide en cada envío o solo al final? *(2)*
- "Desactiva su cuenta" → **A5**: ¿soft (reactiva con solo volver a loguearse), bloqueo que exige acción de admin, o borrado programado? *(3)*
- "Notifica al admin" → **A6**: ¿un email por cada usuario desactivado o un digest? *(2)*
- "Exportar los usuarios a CSV" → **A7**: ¿todos los campos? El email y el teléfono son PII. *(2)*
- ¿Quién puede llamar al endpoint? → **A8**: el texto **no dice nada** de auth. *(2)*

A8 es la clase más peligrosa: **ambigüedad de omisión** — el texto no tiene dos lecturas, tiene *cero* texto sobre una decisión que la implementación tomará de todos modos (todo endpoint tiene una política de auth, aunque sea "ninguna"). No hay frase que releer, así que ningún detector textual la encuentra; el ejemplo caminado sí, porque al caminar "alguien llama al endpoint" la pregunta *¿quién?* es ineludible. Las tres clases: **léxica** (dos lecturas de lo escrito: A1, A5), **de frontera** (el caso límite no cubierto: A4 — actividad entre recordatorios), **de omisión** (silencio sobre una decisión obligatoria del dominio: A8, y parcialmente A7 — nadie dijo "incluye el email", pero nadie dijo que no).

**2. Triage: divergencia × costo de reversión (el orden de EXP-06 aplicado a preguntas).** No todas las 8 valen una pregunta. Asigno a cada una el costo relativo de haberla leído mal (1 = cambiar una config; 100 = daño difícil de revertir) y el riesgo esperado se concentra brutalmente: **A8 (auth del export, 100), A7 (PII en el CSV, 50) y A5 (semántica de desactivar, 40) concentran el 92.7% del riesgo esperado total** [CALC3]. Las tres comparten forma: tocan **invariantes del dominio** (autorización, exposición de PII, reversibilidad de una acción sobre la cuenta del usuario) — exactamente donde EXP-06 manda enumerar invariantes y EXP-08 pone la costura de autoridad/alcance. No es casualidad: **la ambigüedad cara vive donde el requerimiento cruza un invariante**, porque ahí "leerlo mal" no produce un bug estético sino uno de dominio. Corolario operativo: 3 preguntas en un solo lote eliminan ~93% del riesgo; las otras 5 dimensiones se asumen declarando.

**3. Las preguntas van en un lote, en formato decisión, con default anunciado.** El ejemplo caminado descubre las 8 dimensiones *antes* de escribir código; preguntar incrementalmente (bloquearse al tocar cada una) suma hasta 3 latencias de round-trip donde el lote paga 1 [CALC5]. Y cada pregunta se formula como decisión con consecuencias y default, no como pregunta abierta:

> 1. **Desactivación**: asumo *reversible* — María la deshace con solo volver a loguearse. Si querías bloqueo que requiera acción de admin, dímelo (cambia el flujo de soporte).
> 2. **Export CSV**: asumo *solo admin autenticado* y campos sin PII (id, nombre, estado, fecha de última actividad). Si Marketing necesita emails, eso es una decisión de privacidad — ¿la confirmas tú o Legal?
> 3. **"Inactivo"**: asumo *sin login por 30 días* (configurable). Ojo: con esa definición, María cuenta como inactiva aunque su suscripción se renueve sola — ¿es la intención?

El formato hace tres cosas que la pregunta abierta no hace: (a) el default convierte la pregunta **bloqueante en no-bloqueante** — puedo seguir construyendo sobre el default y el silencio del PM es consentimiento informado, no vacío; (b) la concreción ("María cuenta como inactiva aunque pague") explota el lado bueno del oráculo consultable — la gente reacciona a concreciones mucho mejor de lo que especifica abstracciones; (c) la pregunta 2 detecta que **la decisión no es mía ni del PM** — la ambigüedad cara suele ser una decisión sin dueño, y la pregunta correcta la enruta a su dueño en vez de resolverla por accidente.

**4. Lo que no se pregunta se asume declarando — en el entregable, no en la cabeza.** Las 5 dimensiones restantes van a un bloque visible de supuestos ("Supuestos: ventana 30 días configurable; ancla semanal por usuario; actividad intermedia resetea el contador; digest diario al admin"), cada una construida de la forma **más barata de estar equivocada**: la ventana es config, no constante; el ancla es un parámetro del scheduler; el digest y el per-user comparten el mismo punto de emisión. El supuesto declarado es al requerimiento lo que el supuesto falsable de EXP-06 al diseño: el test que el futuro puede ejecutar — el PM que lee "actividad intermedia resetea el contador" puede refutarlo en 5 segundos; el mismo supuesto enterrado en un `if` no lo refuta nadie hasta producción.

**5. Si no hay nadie a quien preguntar: minimax-regret, no máxima verosimilitud.** Sin canal de consulta (run autónomo, PM de vacaciones), las 3 preguntas del triage también se convierten en supuestos — pero la regla de elección **cambia**. Con canal, eliges la lectura más probable y la pregunta corrige. Sin canal, eliges **la lectura cuya equivocación cuesta menos corregir**, aunque sea la menos probable. En A5, aun si "bloqueo administrativo" fuera la intención más probable (P=0.6), elegir "soft/reversible" domina: costo esperado 3.0 contra 16.0 — **5.3×** a favor de la lectura menos probable [CALC4]. La asimetría de costos manda sobre la probabilidad: desactivar de más con reversa barata es un email de disculpa; desactivar de más sin reversa es churn. (Es la política de supuestos de EXP-03 — "declara el supuesto y continúa" — con la mitad que faltaba: *qué* supuesto elegir cuando nadie va a corregirte.)

**Verificación del propio output (Paso 4):** las cuatro afirmaciones cuantitativas de este razonamiento — "864 programas en un párrafo", "la elección silenciosa acierta 17%", "3 preguntas capturan 93% del riesgo", "la lectura menos probable domina 5×" — eran clase A disfrazada de opinión y se calcularon antes de afirmarse [CALC1–CALC5, script en el repo]. Los modelos subyacentes (p=0.8 por dimensión, costos relativos 1–100) están declarados en el script: son modelos, no mediciones de campo — lo que se midió es la *consecuencia* de esos supuestos, y la conclusión (concentración del riesgo, dominancia minimax) es robusta a variaciones amplias de los parámetros: con costos [20,10,8] en vez de [100,50,40], las top-3 siguen concentrando >70%.

### Entregable del caso (la forma final)

Una respuesta al PM con cuatro bloques: (1) el **ejemplo caminado** de María como confirmación de lectura — "entiendo que esto le pasa a María: …" — que es la versión útil del "Entiendo que necesitas X" (una línea de paráfrasis no detecta nada; un ejemplo caminado sí); (2) las **3 preguntas del triage** en formato decisión+default; (3) el **bloque de supuestos** de las 5 dimensiones restantes; (4) el arranque inmediato de la implementación sobre los defaults — el lote de preguntas no bloquea, porque cada pregunta lleva default.

## Patrones identificados

1. **Sexta consigna-trampa: "maneja la ambigüedad".** La ambigüedad no es propiedad del texto sino del par (texto, decisión): solo importa la que hace divergir decisiones caras. Reformulación: detectar divergencias → encaminarlas por costo → construir barato-de-corregir.
2. **La ambigüedad peligrosa es invisible desde dentro (EXP-05 aplicado a la lectura).** Leer es compilar con defaults y el rellenado no deja rastro; releer es segunda cuenta, no segunda vista. El detector es material: **caminar una entidad concreta por el texto** fuerza cada decisión que la prosa difirió — es el ejemplo de EXP-03 invertido (allí cerraba fronteras al escribir; aquí las abre al leer).
3. **Tres clases de ambigüedad: léxica, de frontera, de omisión.** La de omisión (el texto calla una decisión obligatoria: auth, PII, tenancy) es la más peligrosa — no hay frase que releer; solo el ejemplo caminado o la lista de invariantes del dominio la encuentran.
4. **La ambigüedad cara vive donde el requerimiento cruza un invariante del dominio.** Las top-3 del triage (auth, PII, reversibilidad de la desactivación) son todas invariantes de EXP-06/08. El triage divergencia × irreversibilidad es el orden de EXP-06 aplicado a preguntas: 3 de 8 dimensiones concentran 92.7% del riesgo [CALC3].
5. **Preguntar es una operación por lotes en formato decisión+default.** El ejemplo caminado descubre todo antes de codificar (1 round-trip vs. bloqueos secuenciales); el default convierte la pregunta bloqueante en no-bloqueante; la concreción explota que el oráculo humano reacciona mejor de lo que especifica; y la pregunta bien hecha enruta la decisión sin dueño a su dueño (PM vs. Legal).
6. **Sin canal de consulta, la regla de elección cambia: minimax-regret, no máxima verosimilitud.** La lectura menos probable pero barata de corregir domina a la más probable y cara (3.0 vs 16.0, 5.3×) [CALC4]. Completa la política de EXP-03: "declara el supuesto y continúa" + *cuál* supuesto elegir cuando nadie corregirá.
7. **Tipología del oráculo, nuevo tipo: consultable-caro.** El autor del requerimiento existe y responde, pero cada consulta cuesta un round-trip y su fiabilidad es asimétrica (malo especificando en abstracto, bueno reaccionando a concreciones). Método: minimizar consultas (lote), maximizar rendimiento por consulta (decisión+default), preferir mostrar concreciones a preguntar abstracciones.
8. **Falsificación de la propia skill (v1.10, Paso 1): "elige la interpretación más útil" no sobrevive como regla general** — 0.8⁸ = 16.8% de acertar todos los ejes [CALC2]; queda como caso particular para dimensiones convergentes/baratas. Refinamiento local, patrón EXP-02.

## Extracción para la skill

- Cuando recibas un requerimiento en prosa, no lo valides releyéndolo: camina una entidad concreta con nombre y fechas por el texto de punta a punta — cada paso que el texto no decide es una ambigüedad forzada a la superficie; releer usa el mismo compilador con los mismos defaults y no deja rastro de los huecos que rellenó.
- Cuando enumeres las ambigüedades de un requerimiento, busca las tres clases: léxica (dos lecturas de lo escrito), de frontera (el caso límite no cubierto) y de omisión (el texto calla una decisión que la implementación tomará de todos modos: auth, PII, tenancy, límites) — la de omisión no tiene frase que releer y solo aparece caminando el ejemplo o cruzando el texto contra la lista de invariantes del dominio.
- Cuando decidas qué ambigüedades preguntar, haz triage por divergencia × costo de reversión, no por orden de aparición: el riesgo se concentra donde el requerimiento cruza un invariante del dominio (autorización, PII, acciones difíciles de revertir) — en el caso medido, 3 de 8 dimensiones concentraron el 92.7% del riesgo esperado [CALC3, EXP-11].
- Cuando preguntes, pregunta en un solo lote descubierto por el ejemplo caminado antes de codificar, y formula cada pregunta como decisión con consecuencias y default anunciado ("asumo X; si querías Y, dímelo — cambia Z"), nunca como pregunta abierta: el default convierte la pregunta bloqueante en no-bloqueante y el silencio en consentimiento informado.
- Cuando una ambigüedad toque una decisión que no es tuya ni del que pide (privacidad, legal, seguridad), no la resuelvas por accidente: la pregunta correcta enruta la decisión a su dueño ("¿esto lo confirma Legal?").
- Cuando quieras confirmar tu lectura, no parafrasees ("entiendo que necesitas X"): entrega el ejemplo caminado con la entidad concreta ("entiendo que a María le pasa esto: …") — el oráculo humano es malo especificando en abstracto y bueno reaccionando a concreciones; una paráfrasis no le da nada a lo que reaccionar.
- Cuando asumas en vez de preguntar, declara el supuesto en el entregable (bloque visible), no en la cabeza ni en el código: el supuesto declarado es el test que el lector puede ejecutar en segundos; el mismo supuesto enterrado en un `if` no lo refuta nadie hasta producción.
- Cuando construyas sobre un supuesto, elige la construcción más barata de estar equivocada: config en vez de constante, parámetro en vez de rama, reversible en vez de definitivo — el costo de un supuesto no es equivocarse, es lo que cuesta corregirlo.
- Cuando no exista canal de consulta (run autónomo, autor ausente), cambia la regla de elección de lecturas: elige la lectura cuya equivocación sea más barata de corregir, no la más probable — con P=0.6 para la lectura cara (costo 40) contra P=0.4 para la reversible (costo 5), la menos probable domina 5.3× en costo esperado [CALC4, EXP-11].
- Cuando estés a punto de "elegir la interpretación más útil y seguir" en silencio, recuerda que la elección silenciosa compone: con 8 dimensiones ambiguas y 80% de acierto por dimensión, la probabilidad de acertar la intención completa es 16.8% [CALC2, EXP-11] — la elección silenciosa es legítima solo para dimensiones convergentes o baratas de cambiar.
- Cuando un requerimiento se deje implementar de punta a punta sin generarte ni una pregunta ni un supuesto declarado, trátalo como señal de alarma, no de claridad: o el requerimiento es trivial o compilaste sus huecos con defaults sin notarlo.

## Impacto en la skill

- Paso 1 reescrito: "elige la interpretación más útil" (falsificada como regla general por CALC2) reemplazada por el protocolo de ambigüedad: ejemplo caminado como detector → triage por divergencia × irreversibilidad → lote decisión+default → supuestos declarados → minimax-regret sin canal.
- Tipología del oráculo ampliada con el tipo **consultable-caro** (el autor del requerimiento).
- Nueva sección "Manejo de ambigüedad en requerimientos (EXP-11)" en INSTRUCCIONES APRENDIDAS (11 instrucciones).
- Detector de resultados sospechosos: 2 señales nuevas (requerimiento que no genera preguntas ni supuestos; comprensión fluida de un texto que calla sobre auth/PII/acciones irreversibles).
- Skill v1.10 → v1.11.
