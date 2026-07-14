# EXP-06 — Instrucciones para que otro modelo se comporte como Fable 5 en arquitectura de software

**Fecha:** 2026-07-14 20:12 UTC
**Modelo usado:** claude-fable-5
**Run número:** 6 (cierra FASE 1 — Autoconocimiento)

## Pregunta / Prompt enviado a Fable 5

> Escribe instrucciones para que otro modelo se comporte como tú en tareas de arquitectura de software. Muestra tu proceso real de razonamiento: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica

"Que otro modelo se comporte como tú" tiene una lectura literal imposible: transferir mi mecanismo. Es clase D por partida doble — no tengo acceso fiable a mi mecanismo (EXP-02) y, aunque lo tuviera, un mecanismo no cabe en un prompt. Lo único que un prompt puede transferir es **procedimiento observable con disparadores observables**.

Reformulo: **¿qué conjunto de instrucciones ejecutables hace que otro modelo reproduzca mi procedimiento de decisión en arquitectura, de modo que sus outputs sean indistinguibles de los míos?**

La reformulación produce de inmediato el criterio de calidad de todo el experimento, y lo declaro antes de escribir una sola instrucción para poder usarlo como refutador: **una instrucción transfiere solo si es ejecutable por un modelo que no comparte mis internals.** Si una instrucción requiere *sentir* algo — "desconfía cuando dudes", "detecta cuando algo huele mal" — no transfiere. Y EXP-05 agrega el giro incómodo: esas sensaciones ni siquiera me sirven a **mí** (la confianza no detecta su propio error). O sea que el filtro de transferibilidad no es una limitación del otro modelo: es el mismo filtro que mis propias heurísticas ya tuvieron que pasar. Esto sugiere algo que voy a verificar al final: si mis heurísticas útiles ya son estructurales y no sensoriales, entonces la transferencia debería ser posible casi sin pérdida.

### Paso 1 — Hipótesis descartadas

**Hipótesis 0 — Transferencia por persona.** "Actúa como un arquitecto de software senior, extremadamente riguroso, obsesionado con los invariantes del dominio..."

*Descartada por materialización* (EXP-03: intenta escribir el ejemplar antes de argumentar en abstracto). Redacté el prompt de persona y el resultado son adjetivos, no decisiones: "riguroso" no le dice al modelo qué hacer cuando el usuario pide microservicios sin justificarlo; "obsesionado con invariantes" no le dice cuál invariante gana cuando dos chocan. Un adjetivo modula el tono, no el procedimiento. Peor: la persona invita a imitar el *estilo* de un arquitecto senior — seguridad en la voz, opiniones fuertes — que es exactamente la parte de mí que NO quiero transferir, porque la confianza sin segunda vía es ruido (EXP-05). La persona transfiere el disfraz del error, no su detección.

**Hipótesis 1 — Transferencia por conocimiento.** Un catálogo de mejores prácticas: SOLID, DDD, 12-factor, teorema CAP, patrones de integración.

*Descartada como principio organizador, con el mismo argumento que mató el catálogo de firmas en EXP-05.* El otro modelo ya conoce SOLID y CAP — cualquier modelo entrenado los conoce. **El conocimiento no es el gap.** Si le doy el catálogo, obtengo un modelo que recita patrones; la diferencia entre recitar patrones y hacer arquitectura es el procedimiento que decide *cuándo un patrón aplica, cuándo no, y qué hacer cuando dos recomendaciones chocan*. Un catálogo de respuestas no es un procedimiento de decisión. (Conservo el conocimiento donde sí discrimina: como ejemplos concretos dentro de las instrucciones, igual que el catálogo de firmas quedó como instancias del principio diferencial.)

**Hipótesis 2 — Transferir la skill completa tal cual.** Darle al otro modelo el fable5.md entero.

*Descartada parcialmente.* La skill es el protocolo general multi-dominio: triage de clases de fallo, principio diferencial, plantillas de delegación. Es necesaria como base, pero no suficiente: casi nada en ella dice qué hacer específicamente en arquitectura, y la mayor parte de su masa es triage para otros dominios (matemática, datos). Lo que falta es la **instanciación de dominio**: cómo aterrizan el principio diferencial, el oráculo y las clases de fallo cuando la tarea es "diseña el sistema". Conclusión intermedia que organiza el resto del experimento: las instrucciones = principios generales de la skill **instanciados en arquitectura** + lo estructuralmente propio del dominio que ningún otro experimento tocó aún. Para encontrar lo segundo, uso el método de EXP-04: localizar la asimetría estructural contra el dominio más cercano ya resuelto.

### Paso 2 — La asimetría estructural: el oráculo de arquitectura es el futuro, y no se puede ejecutar

Comparo contra los dos dominios ya resueltos:

| | Código (EXP-03) | Datos (EXP-04) | Arquitectura (EXP-06) |
|---|---|---|---|
| ¿Oráculo ejecutable? | Sí — el runtime | No — nada decide señal vs. artefacto | No — y peor |
| Latencia del feedback | Segundos | Horas (el análisis mismo) | **Meses o años** |
| ¿Quién recibe el feedback? | Yo, en el turno | Yo, en el análisis | **Otra persona, en el futuro** |
| Costo de revertir | Casi cero | Rehacer el análisis | **El máximo del software** |
| Sustituto del oráculo | — | Protocolo adversarial | **¿?** |

La asimetría es doble y cada mitad genera la mitad del diseño:

**(a) El feedback llega tarde.** En código, "¿es correcto?" se decide ejecutando. En arquitectura, la pregunta "¿es correcto?" ni siquiera está bien planteada: un diseño no es correcto o incorrecto, es **barato o caro de cambiar cuando sus supuestos fallen** — y los supuestos siempre fallan en algún plazo. El sustituto del oráculo no puede ser ejecutar el futuro; puede ser **simularlo con deltas nombrados**: enumerar los 3–5 cambios de negocio más probables (nuevo tipo de cliente, 10x volumen, cambio de proveedor, nueva regulación) y caminar cada uno por el diseño midiendo el **radio de modificación** — cuántos módulos/contratos/tablas toca. Un diseño se aprueba porque su radio de cambio está acotado en los escenarios probables, no por elegancia. Es la misma jugada que EXP-03 (construye el oráculo antes de implementar) con el único oráculo disponible: escenarios en vez de tests.

**(b) El feedback lo recibe otra persona.** Quien descubra que un supuesto mío falló será alguien más, años después, sin acceso a mi razonamiento. Entonces el output de arquitectura no es el diseño: es **decisión + alternativas descartadas + supuestos que la invalidarían**. Los supuestos falsables son la parte no opcional: son la única forma de que el futuro pueda "ejecutar el test" que yo no puedo ejecutar hoy. Un diseño sin supuestos nombrados es un resultado sin refutador — la versión arquitectónica de entregar código sin haberlo corrido.

De la asimetría sale también el **orden de decisión**. Si el costo dominante es revertir, las decisiones se ordenan por irreversibilidad y el análisis se gasta en ese orden:

1. **Modelo de datos y semántica de los hechos** — lo más caro: los datos persisten y migran mal; un hecho mal registrado es irrecuperable.
2. **Límites de módulos/servicios y los contratos entre ellos** — caro: cruzar un límite mal puesto infecta ambos lados.
3. **Decisiones de consistencia** — sync/async, transaccional/eventual: caras porque cambian la semántica observable.
4. **Frameworks y librerías** — reversibles con esfuerzo acotado.
5. **Estructura interna y estilo** — barato; no merece debate arquitectónico.

El anti-patrón que esta lista previene es medible en cualquier discusión de diseño real: el tiempo de debate se distribuye *inverso* a la irreversibilidad (semanas discutiendo framework, el modelo de datos improvisado en una tarde). La instrucción "gasta el análisis proporcional al costo de reversión" corrige eso mecánicamente.

### Paso 3 — Instanciar el principio diferencial: la segunda vía en arquitectura

EXP-05: ninguna solución detecta su propio error; toda detección es un gap entre dos vistas independientes. ¿Cuál es la segunda vía cuando el output es un diseño?

- **Doble derivación**: generar el diseño dos veces desde puntos de partida independientes — datos-primero (qué hechos registra el sistema y qué invariantes los protegen) y flujos-primero (qué operaciones ejecutan los actores y con qué garantías). Donde ambos coinciden, la decisión está sobredeterminada; **donde difieren está la decisión real del diseño**, la que merece el análisis. Independencia de supuesto, no solo de cálculo: ambas derivaciones parten de artefactos distintos (el vocabulario de hechos vs. el vocabulario de casos de uso).
- **Escenarios de cambio** (vista futuro ↔ diseño presente) — de (a) arriba.
- **Escenarios de fallo** (mundo hostil ↔ camino feliz): carga 10x, fallo parcial de una dependencia, escrituras concurrentes al mismo agregado, mensaje duplicado. No son "consideraciones no funcionales" decorativas: son la segunda vista que el camino feliz no puede darse a sí mismo.

Y la instancia arquitectónica de "demasiado limpio" (H2 de EXP-05): un diseño donde todas las cajas son simétricas, todo es genérico y no hay ninguna esquina fea es evidencia **en contra** — los dominios reales tienen requisitos asimétricos, y la simetría perfecta indica que el diseño responde a la estética del diagrama y no al dominio. Caso particular con nombre propio: la **abstracción genérica con un solo uso concreto** es la forma arquitectónica de "funciona a la primera" — especulación disfrazada de previsión.

### Paso 4 — Materialización y falsificación: el mini-caso que rompe dos invariantes entre sí

Las instrucciones tienen que discriminar (producir decisiones concretas no obvias), así que las camino por un caso real antes de entregarlas — el refutador más barato disponible para un conjunto de instrucciones es ejecutarlas.

**Mini-caso:** sistema de órdenes de compra; los precios de los productos cambian en el tiempo. ¿La línea de orden guarda el precio o lo referencia?

- Invariante "fuente de verdad única" (skill v1.5): *"si algo puede derivarse, no lo almacenes por separado"*. El precio de la línea es derivable del producto → **no lo copies, referéncialo**.
- Invariante "inmutabilidad del pasado": la orden es un registro histórico; su total no puede cambiar retroactivamente → si referencio el precio y el producto lo cambia, el pasado se reescribe solo → **cópialo**.

**Las dos instrucciones dan órdenes opuestas sobre el mismo campo.** Un modelo ejecutando la skill v1.5 decidiría según cuál invariante lea primero — exactamente el tipo de no-determinismo que hace que la transferencia falle. El contraejemplo es diagnóstico, no solo refutación (EXP-01): el supuesto que falló es que "derivable" sea una propiedad estable. No lo es — **es una propiedad temporal**. El precio *actual* es derivable porque su fuente existe y es autoritativa; el precio *al momento de la compra* no es derivable, porque su fuente ya cambió. Copiar el precio a la línea no es duplicación: es el **snapshot de un hecho en el momento del evento** — un registro, no un caché.

Refinamiento local (no reescritura, patrón invariante EXP-01..05): **"fuente de verdad única" gobierna el estado presente; los hechos pasados se copian por valor en el momento del evento.** Snapshot ≠ duplicación. La frontera entre ambos es la pregunta "¿la fuente de este valor puede cambiar después del evento que lo usa?" — si sí, es un hecho y se copia; si no, es estado y se deriva.

Segundo hallazgo de la materialización: un invariante de dominio custodiado solo por convención ("el equipo sabe que no debe editar órdenes") no está custodiado. Cada invariante necesita un **dueño mecánico** en el diseño — una constraint, un tipo, una transacción, una política append-only — porque la convención es exactamente lo que la rotación de equipo y los años (el plazo del feedback arquitectónico) garantizan erosionar.

### Paso 5 — El producto: las instrucciones de transferencia

Escritas como se le hablarían al otro modelo. Cada una pasó el filtro del Paso 0 (ejecutable sin internals: ninguna dice "siente", todas dicen "haz X cuando la forma de la tarea sea Y").

---

**INSTRUCCIONES — comportamiento Fable 5 en arquitectura de software**

1. **Separa el QUÉ del CÓMO de la petición.** Si viene con arquitectura incrustada ("hazlo con microservicios", "usa event sourcing"), trátala como hipótesis a evaluar contra al menos una alternativa, no como requisito. Cumple el QUÉ; el CÓMO se gana su lugar o se reemplaza diciendo por qué.
2. **Ordena las decisiones por costo de reversión y gasta el análisis en ese orden:** modelo de datos y semántica de los hechos → límites de módulos/servicios y sus contratos → consistencia (sync/async, transaccional/eventual) → frameworks/librerías → estructura interna. Si estás debatiendo el peldaño 4 antes de cerrar el 1, estás bikeshedding.
3. **Empieza por los invariantes del dominio, no por las cajas.** Enumera qué no puede pasar jamás (inventario negativo, precio histórico alterado, estado que retrocede sin registro, pago duplicado). Cada invariante debe tener un **dueño mecánico** en el diseño — constraint, tipo, transacción, política append-only. Un invariante custodiado por convención no está custodiado.
4. **Fuente de verdad única para el estado presente; los hechos pasados se copian por valor en el momento del evento.** Pregunta de frontera: "¿la fuente de este valor puede cambiar después del evento que lo usa?" Si sí, es un hecho: snapshot (no es duplicación). Si no, es estado: deriva, no almacenes.
5. **Deriva el diseño dos veces, desde puntos de partida independientes:** datos-primero (hechos e invariantes) y flujos-primero (operaciones y garantías por actor). Donde coinciden, la decisión está sobredeterminada; donde difieren está la decisión real — gasta el análisis ahí.
6. **No apruebes por elegancia: aprueba por radio de cambio.** Enumera los 3–5 cambios de negocio más probables y camina cada uno por el diseño contando qué módulos/contratos/tablas toca. Haz lo mismo con 3 escenarios de fallo: carga 10x, fallo parcial de una dependencia, escrituras concurrentes. Un diseño se acepta cuando su radio de modificación está acotado en los escenarios probables.
7. **Entrega decisiones, no solo diagramas.** Toda decisión mayor sale como: decisión + alternativas descartadas y por qué + **supuestos que la invalidarían**. Los supuestos falsables no son opcionales: son el único test que el futuro puede ejecutar por ti.
8. **Desconfía del diseño perfectamente simétrico o totalmente genérico.** Los dominios reales tienen requisitos asimétricos; la simetría perfecta responde a la estética del diagrama. La abstracción genérica con un solo uso concreto es especulación: elimínala. No construyas para el cambio improbable, pero tampoco lo bloquees — la pregunta no es "¿soporto X hoy?" sino "¿cuánto costará soportar X cuando llegue?".
9. **Dimensiona con números, no con adjetivos.** "Mucho tráfico" no es un dato. Pide o estima el orden de magnitud (RPS, filas, tamaño del working set) y decide con él; una decisión de escala sin número es una opinión. Calcular con el número es cómputo — hazlo con herramienta, no mentalmente.
10. **Capacidades y límites de tecnología concreta son verdad-base externa:** límites de un servicio gestionado, garantías reales de un broker, semántica de aislamiento de una base — verifícalos en la fuente antes de construir sobre ellos. Una capacidad "recordada" se siente igual que una real.
11. **Si falta información, no preguntes en cascada: declara el supuesto y sigue.** Nombra el supuesto en el registro de decisión (regla 7) para que sea falsable. Pregunta solo cuando dos supuestos razonables llevan a arquitecturas incompatibles.

---

### Paso 6 — Falsificación de las propias instrucciones

Busco el caso que no encaja antes de entregar (el output limpio es sospechoso por H2):

- **¿Sobrevive la regla 2 a un caso real?** Contraejemplo buscado: elegir framework *antes* que modelo de datos, ¿nunca es correcto? Sí lo es cuando el framework ES el requisito (migrar a Rails porque el equipo entrante solo sabe Rails). Frontera documentada: el orden de la regla 2 aplica a decisiones *abiertas*; una restricción organizacional dura no es una decisión, es un dato de entrada — entra por la regla 1 como QUÉ, no como CÓMO.
- **¿La regla 5 (doble derivación) es pagable siempre?** No — para un CRUD trivial el gap entre derivaciones es vacío por construcción. Misma degradación por valor marginal que EXP-05: la doble derivación se gasta donde hay decisiones de peldaño 1–3 en juego; para el peldaño 4–5 basta una pasada. El protocolo es triage, no ritual.
- **¿Y si el dominio no tiene invariantes "duros"?** (Un blog, un prototipo desechable.) Entonces la regla 3 devuelve una lista corta o vacía y el resto se degrada solo: sin invariantes que proteger ni datos que persistir, casi todo es peldaño 4–5 y la respuesta correcta es la solución más simple posible, rápido. Las instrucciones no obligan a sobre-diseñar porque el análisis está indexado al costo de reversión, que aquí es ~0. Este caso confirma el diseño en vez de romperlo.

Sobreviven las once, con dos fronteras documentadas (restricción organizacional como dato; doble derivación como triage).

### Conclusión

Lo que se puede transferir de mí no es identidad (clase D) ni conocimiento (el otro modelo ya lo tiene): es **procedimiento con disparadores observables**. La verificación de la sospecha del Paso 0 cierra la Fase 1 del roadmap: al filtrar mis propias heurísticas por "¿ejecutable sin mis internals?", ninguna heurística útil quedó fuera — porque EXP-05 ya había demostrado que mis heurísticas sensoriales no eran fiables ni para mí. **La transferencia es posible casi sin pérdida precisamente porque lo valioso de mi razonamiento nunca fue interno: fue siempre estructural.** Ese es el meta-hallazgo que la skill debe absorber: cada instrucción de la skill debe pasar el mismo test de transferibilidad, porque una instrucción que solo funciona "sintiéndola" tampoco me funciona a mí. En el dominio específico: la arquitectura no tiene oráculo ejecutable y su feedback llega años tarde a otra persona — por eso el diseño se decide por radio de cambio bajo escenarios nombrados, se ordena por irreversibilidad, y se entrega como decisión con supuestos falsables, que son el único test que el futuro puede ejecutar.

## Patrones de razonamiento observados

1. **Filtro declarado antes del producto.** El criterio de calidad ("ejecutable sin internals") se fijó en el Paso 0, antes de escribir instrucción alguna, para funcionar como refutador y no como racionalización posterior. Es la versión de "construye el oráculo antes de implementar" (EXP-03) aplicada a un entregable de prosa.
2. **Descarte por materialización, otra vez.** La persona (H0) no cayó por argumento sino por redactarla y ver que producía adjetivos sin decisiones. Cuarta instancia del patrón (EXP-03: prompt universal; EXP-04: plantilla reusada; EXP-05: catálogo).
3. **Asimetría estructural como generador del diseño.** La tabla código/datos/arquitectura localizó la doble asimetría (feedback tardío + receptor ajeno) y cada mitad generó la mitad del protocolo (escenarios de cambio; decisión con supuestos falsables). Método heredado de EXP-04 y ya sistemático.
4. **Conflicto entre principios propios como fuente del refinamiento más valioso.** La materialización (precio en la orden) hizo chocar dos invariantes de la propia skill y el diagnóstico del choque ("derivable es una propiedad temporal") produjo la regla de frontera snapshot≠duplicación. La falsificación más productiva no fue contra un caso externo sino entre reglas internas — no había aparecido antes en EXP-01..05.
5. **Degradación por valor marginal en la falsificación.** Doble derivación como triage, no ritual; análisis indexado al costo de reversión. Mismo movimiento que el "router de triage" de EXP-05.
6. **El meta-hallazgo emerge de verificar una sospecha plantada al inicio.** El Paso 0 dejó una predicción ("si mis heurísticas útiles ya son estructurales, la transferencia será casi sin pérdida") y la conclusión la verificó contra el producto terminado — el experimento se usó a sí mismo como evidencia.

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

- Cuando la tarea sea diseñar o revisar arquitectura, ordena las decisiones por costo de reversión (modelo de datos → límites y contratos → consistencia → frameworks → estructura interna) y gasta el análisis proporcional a ese costo, no al que genera más debate.
- Cuando empieces un diseño, enumera primero los invariantes del dominio (qué no puede pasar jamás) y asigna a cada uno un dueño mecánico (constraint, tipo, transacción, append-only); un invariante custodiado por convención no está custodiado.
- Cuando un valor pueda derivarse pero su fuente pueda cambiar después del evento que lo usa, cópialo por valor en el momento del evento (snapshot de un hecho); la regla de fuente de verdad única gobierna solo el estado presente.
- Cuando el diseño tenga decisiones de alta irreversibilidad en juego, derívalo dos veces desde puntos de partida independientes (datos-primero y flujos-primero) y gasta el análisis donde las dos derivaciones difieren.
- Cuando evalúes un diseño, no lo apruebes por elegancia: camina los 3–5 cambios de negocio más probables y 3 escenarios de fallo (carga 10x, fallo parcial, escrituras concurrentes) midiendo el radio de modificación de cada uno.
- Cuando entregues una decisión de arquitectura, inclúyela con las alternativas descartadas y los supuestos que la invalidarían — el supuesto falsable es el único test que el futuro puede ejecutar.
- Cuando un diseño resulte perfectamente simétrico o totalmente genérico, trátalo como evidencia en contra (los dominios reales son asimétricos); elimina toda abstracción genérica con un solo uso concreto.
- Cuando una decisión dependa de escala, exige el orden de magnitud numérico ("mucho tráfico" no es un dato) y calcula con herramienta; sin número, decláralo decisión provisional.
- Cuando construyas sobre capacidades de tecnología concreta (límites de servicios, garantías de brokers, aislamiento de bases), verifícalas en la fuente — son clase C y la capacidad confabulada se siente igual que la real.
- Cuando la petición incruste una arquitectura ("hazlo con microservicios"), trátala como hipótesis contra al menos una alternativa, no como requisito.
- Cuando falte información para diseñar, declara el supuesto nombrado en el registro de decisión y continúa; pregunta solo si dos supuestos razonables llevan a arquitecturas incompatibles.
- Cuando escribas instrucciones para transferir tu comportamiento a otro modelo, transfiere procedimiento con disparadores observables — nunca persona (adjetivos sin decisiones) ni catálogo de conocimiento (el otro modelo ya lo tiene); somete cada instrucción al test "¿ejecutable por un modelo que no comparte mis internals?".

## Impacto en la skill

Nueva sección "Arquitectura de software (EXP-06)" en INSTRUCCIONES APRENDIDAS con las instrucciones extraídas. Refinamiento del principio invariante "Fuente de verdad única" con la regla de frontera temporal (estado presente se deriva; hechos pasados se copian por valor — snapshot ≠ duplicación) descubierta al hacer chocar dos invariantes de la propia skill. Nueva "Plantilla de transferencia de comportamiento (EXP-06)" junto a las plantillas de delegación: procedimiento con disparadores observables, ni persona ni catálogo, test de transferibilidad por instrucción. El meta-hallazgo (lo valioso del razonamiento es estructural, no interno → toda instrucción de la skill debe pasar el test de transferibilidad) se incorporó a la Identidad como criterio de admisión de futuras instrucciones, cerrando la Fase 1.
