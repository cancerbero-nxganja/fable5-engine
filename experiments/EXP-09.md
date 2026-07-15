# EXP-09 — Cómo Fable 5 diseña esquemas de base de datos sin redundancia

**Fecha:** 2026-07-15 02:12 UTC
**Modelo usado:** claude-fable-5
**Run número:** 9 (FASE 2 — Patrones de razonamiento)

## Pregunta / Prompt enviado a Fable 5

> Muéstrame cómo diseñas un esquema de base de datos **sin redundancia**. Toma un caso concreto y muestra tu proceso real de razonamiento: qué hipótesis sobre el método consideraste, cuáles descartaste y por qué, y cómo llegas a decidir la forma final del esquema. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica: "sin redundancia" es una palabra-trampa

La pregunta trae una palabra que hay que desactivar antes de escribir una sola tabla: **"sin redundancia"**. Suena a objetivo unívoco — quita las copias, deja cada dato una vez. Pero por el arco de experimentos ya sé desconfiar de los objetivos que suenan unívocos: "detecta" (EXP-08), "maximiza el Sharpe" (EXP-07), "hazla operable" (EXP-07) — todos escondían una reformulación que cambiaba el método entero. "Sin redundancia" es de esa familia.

La trampa es específica y la conozco de primera mano por EXP-06. Ahí establecí que **"derivable" es una propiedad temporal**: el precio en una línea de orden *parece* redundante con el precio del producto (misma cifra hoy), pero no lo es — es el snapshot de un hecho as-of el momento de la compra. Un modelo que persigue "sin redundancia" de forma literal **borra esa columna** por considerarla duplicada, y con eso introduce el bug exacto contra el que EXP-06 advirtió: cuando el producto cambie de precio, todas las órdenes históricas mutan su total en silencio. Es decir: *el reflejo "sin redundancia", aplicado literalmente, es una fuente de bugs de corrección, no solo de estilo.*

Entonces reformulo la pregunta antes de tocar el esquema:

> "Diseña sin redundancia" no es "elimina toda copia". Es: **dale a cada *hecho* exactamente un hogar, donde un hecho se individúa por su dependencia funcional Y por su identidad temporal (as-of).** La redundancia a eliminar es la copia *derivable del estado presente y sin dueño*; la copia que es un *snapshot de un hecho as-of* no es redundancia, es un registro histórico, y borrarla es el bug.

Y una segunda reformulación, más incómoda, que descubro al escribir la primera: **"redundancia" no nombra una cosa, nombra tres**, y la palabra las confunde a propósito. El experimento entero es separarlas.

### Paso 1 — La asimetría estructural: qué tiene el esquema que la arquitectura general no tiene

Aplico el método de EXP-04/06/07/08: comparo el dominio nuevo contra el vecino resuelto más cercano y localizo qué falta o qué sobra. El vecino aquí es **arquitectura de software (EXP-06)** — mismo dominio-sin-oráculo, mismo feedback tardío a otra persona, misma decisión ordenada por irreversibilidad. De hecho el diseño de esquema **es** el ítem #1 de la lista de irreversibilidad de EXP-06 ("modelo de datos y semántica de los hechos"), el más caro de revertir: migrar una tabla ya poblada con la forma equivocada es el reverso más costoso que existe, porque el error ya se materializó en millones de filas antes de que llegue el feedback.

Pero hay una asimetría que reorganiza el método, y es una **buena** noticia por una vez: en arquitectura general, el "dueño mecánico" de un invariante (EXP-06) es algo que hay que *construir y mantener* — código de validación, una transacción, una convención custodiada. En el esquema, **el motor te regala un vocabulario declarativo de dueños mecánicos**: `FOREIGN KEY`, `UNIQUE`, `CHECK`, `NOT NULL`, `PRIMARY KEY`, columnas generadas (`GENERATED ALWAYS AS`), vistas materializadas con refresh, triggers. El esquema es el dominio donde el principio de EXP-06 "todo invariante necesita un dueño mecánico" es **más barato de satisfar que en ningún otro lugar** — el dueño es declarativo y lo hace cumplir el motor, no código que yo mantengo.

Eso reorganiza todo el método: **diseño el esquema para que cada invariante del dominio caiga sobre una constraint declarativa.** Y el corolario, que uso como detector todo el experimento: **una columna cuyo invariante no puede expresarse como constraint es una señal de que la entidad está mal modelada** — casi siempre porque mezcla dos entidades o dos hechos en una fila.

Y hay una asimetría de oráculo, refinando EXP-07/08. ¿Cuál es el oráculo del diseño de esquema? Como arquitectura, es **ausente y tardío** en la pregunta grande. Pero el esquema tiene una sub-pregunta con oráculo **parcialmente honesto** que la arquitectura no tiene: *"¿estos dos lugares guardan el mismo hecho dos veces?"* es **mecánicamente decidible** desde las dependencias funcionales — es la teoría clásica de normalización (anomalías de update/insert/delete, cierre de FDs). Así que dentro del esquema:

- La sub-pregunta **de normalización** ("¿hay una copia derivable sin dueño?") tiene **oráculo semi-honesto**: el test de anomalías es mecánico.
- La sub-pregunta **de identidad de entidad** ("¿qué *es* un hecho aquí, cuál es su clave, cuándo dos valores son el mismo hecho o dos hechos distintos?") tiene **oráculo ausente**: es conocimiento del dominio, ninguna teoría te lo decide.

Esto es exactamente la partición sintáctico/semántico de EXP-08, subida un nivel: la normalización es la "capa sintáctica" del esquema (mecánica, verificable) y la identidad de los hechos es la "capa semántica" (importa el invariante de afuera). Y aquí está el punto que reordena el resto: **la teoría de normalización, sola, es ciega a la identidad temporal.** Opera sobre dependencias funcionales en *un instante*; no tiene ningún concepto de "la fuente de este valor puede cambiar después". Por eso BCNF no puede distinguir un snapshot de un duplicado — en el instante T ambos son "el mismo valor en dos lugares". La normalización es el oráculo honesto de la capa sintáctica y **mudo sobre la capa temporal**, igual que el runtime era mudo sobre la semántica en EXP-08.

### Paso 2 — Descarte de los métodos ingenuos (cada descarte define por contraste el método correcto)

**H0 — "Sin redundancia = normaliza hasta BCNF y listo."**
*Descartada como método completo, y es el descarte que abre el experimento.* BCNF elimina la redundancia detectable por dependencias funcionales en un instante. Pero es **ciega a la identidad temporal**: no ve que `order_line.unit_price` y `product.price` son hechos distintos porque no tiene el eje del tiempo. Aplicada mecánicamente, BCNF *borra el snapshot as-of* — la normalización máxima es aquí una fuente de bugs de corrección (EXP-06). Retengo BCNF como **oráculo de la sub-pregunta sintáctica** (¿anomalía de update?), no como definición del objetivo.

**H1 — "Elimina toda columna derivable."**
*Descartada — 'derivable' es temporal (EXP-06), no estático.* Dos trampas simétricas: (a) `unit_price` *parece* derivable de `product` en el instante de la compra pero no lo es — su determinante es la orden, no el producto vigente; (b) `order.total` *sí* es genuinamente derivable de las líneas, y aun así puede querer materializarse. "Derivable" no es una propiedad de la columna; es una pregunta de frontera sobre *cuándo* se lee respecto de *cuándo* puede cambiar la fuente.

**H2 — "La normalización es teórica; en la práctica se denormaliza para performance."**
*Descartada — es el reflejo opuesto y también es un bug.* Denormalizar sin dueño mecánico ES la anomalía de update de manual: dos lugares que deben concordar y divergen al primer write que actualiza uno y olvida el otro. La denormalización solo es legítima como **copia gobernada** (con dueño mecánico que la reconcilia), y entonces no es una derrota de la normalización sino una decisión de rendimiento separada, con su propio custodio. Confundir "denormalizo porque es más rápido" con "denormalizo con una vista materializada que el motor refresca" es confundir un bug con una decisión.

**H3 — "Un valor, un lugar."**
*Descartada — se refina a 'un hecho, un lugar', y un valor puede ser dos hechos.* Este es el corazón. El precio-vigente-del-producto y el precio-al-que-se-compró comparten un número el día de la compra y son **dos hechos con dos determinantes distintos**. "Un valor, un lugar" los fusiona y produce el bug; "un hecho, un lugar" los separa y los deja a ambos, correctamente, sin que eso sea redundancia.

**H4 — "Usa surrogate keys siempre" (o "natural keys siempre").**
*Descartada como reflejo — es un distractor.* La pregunta real no es surrogate vs natural, es **identidad**: ¿qué hace que dos filas sean la misma entidad del mundo? Eso lo decide el dominio (oráculo ausente), no un reflejo. La elección de clave es una consecuencia de haber respondido la identidad, no un sustituto de responderla.

Los cuatro descartes convergen: **el objetivo no es "menos copias" sino "una definición correcta de qué es un hecho y cuál es su identidad".** La normalización mecánica (H0/H1) es ciega a la identidad temporal; los reflejos de performance (H2) y de clave (H4) saltan la pregunta de identidad por completo. El método correcto pone la identidad —temporal y de entidad— primero, y usa la normalización como oráculo *después*, para la parte que sí es mecánica.

### Paso 3 — El método: normalización *condicionada por la frontera as-of*, con dueños declarativos

La pregunta de frontera de EXP-06 deja de ser una regla de lógica de aplicación y se convierte en el **operador que genera tablas** del esquema. Por cada valor candidato a columna, dos preguntas en orden:

**Pregunta de frontera A (identidad temporal, EXP-06/07):** *¿la fuente de este valor puede cambiar después del evento que lo consume?*
- **No** → es *estado presente*: derívalo, no lo almacenes. La redundancia aquí es patológica.
- **Sí** → es un *hecho as-of*: cópialo por valor en el momento del evento. **No es redundancia**, es un registro; su determinante es el evento, no la entidad-fuente. Guardarlo junto al valor vigente es normalización correcta, porque son dos hechos con dos dependencias funcionales distintas.

**Pregunta de frontera B (dueño mecánico, EXP-06/08):** para toda copia que sí decida mantener por rendimiento aunque sea derivable del estado presente, *¿tiene un dueño mecánico declarativo que la reconcilia con su fuente?*
- **No** → redundancia patológica. Elimínala (normaliza) o dale un dueño.
- **Sí** (columna generada, vista materializada con refresh, trigger + CHECK) → copia gobernada, legítima como decisión de performance, no como diseño base.

Estas dos preguntas parten "redundancia" en las **tres** clases que la palabra confundía:

| Tipo | Qué es | Frontera A | Frontera B | Veredicto |
|---|---|---|---|---|
| **1. Copia derivable del presente, sin dueño** | `total` guardado como columna suelta que "debería" igualar `sum(líneas)` | fuente NO cambia tras el evento | sin dueño | **Redundancia patológica** → normaliza (bórrala) |
| **2. Snapshot de un hecho as-of** | `order_line.unit_price` | fuente SÍ cambia tras el evento | — | **No es redundancia** → consérvala (EXP-06/07) |
| **3. Copia derivada con dueño mecánico** | `order.total` como columna generada o vista materializada con `CHECK sum(líneas)==total` | fuente NO cambia | CON dueño | **Redundancia gobernada** → legítima como decisión de rendimiento |

El discriminador entre patológica (1) y snapshot (2) es la frontera A; el discriminador entre patológica (1) y gobernada (3) es la frontera B. La palabra "redundancia" sola no ve ninguna de las dos fronteras — por eso hay que reformularla en Paso 0.

**El detector mecánico de la clase 1 es el test de anomalías (oráculo semi-honesto, y es un test diferencial de EXP-05):** ¿existe un update que, para mantener el invariante, obliga a escribir en dos lugares a la vez? Si sí, esos dos lugares guardan el mismo hecho sin dueño = redundancia patológica. Es exactamente la forma de EXP-05: dos estimaciones de la misma cosa que *deben concordar* y nada garantiza que concuerden. El fix es o quitar una (normalizar) o darle a la coincidencia un dueño mecánico (constraint) — que es hacerla clase 3.

### Paso 4 — Materialización y falsificación: el caso concreto (y el choque de dos reglas propias)

Tomo la línea de EXP-06/08 —órdenes, líneas, productos, clientes— porque el refutador más barato de un método es correrlo (EXP-06) y porque quiero ver chocar dos reglas de esta skill sobre el mismo campo.

**Primer intento — el esquema que produce el reflejo "sin redundancia" (H0/H1), y su bug.**

```sql
-- INTENTO INGENUO (máximamente normalizado)
CREATE TABLE product (
    id           bigint PRIMARY KEY,
    name         text NOT NULL,
    price_cents  int  NOT NULL          -- precio vigente
);
CREATE TABLE "order" (
    id           bigint PRIMARY KEY,
    customer_id  bigint NOT NULL REFERENCES customer(id),
    placed_at    timestamptz NOT NULL
);
CREATE TABLE order_line (
    order_id     bigint NOT NULL REFERENCES "order"(id),
    product_id   bigint NOT NULL REFERENCES product(id),
    qty          int NOT NULL CHECK (qty > 0),
    PRIMARY KEY (order_id, product_id)
    -- ¡sin unit_price! "sería redundante con product.price_cents"
);
```

Este esquema está en BCNF y "sin redundancia" según H0. Y tiene un bug de corrección.

*Falsificación con ejemplo trabajado de fuente independiente del código (EXP-08):* el 1 de marzo el cliente compra 2 unidades de un producto a $10.00 → el total de esa orden **es** $20.00, es un hecho histórico, un asiento. El 1 de junio el negocio sube el precio a $12.00 (`UPDATE product SET price_cents=1200`). Ahora el total de la orden de marzo, calculado como `sum(qty * product.price_cents)`, devuelve **$24.00**. Una orden del pasado cambió de monto sin que nadie la tocara. Eso viola dos invariantes de esta skill: **inmutabilidad del pasado** (EXP-06) y **corrección as-of** (EXP-07) — se está leyendo el precio *latest* donde el dominio quiere el precio *as-of* el evento. El "esquema sin redundancia" es incorrecto, y lo es *precisamente por* haber eliminado la supuesta redundancia.

*Diagnóstico (no probar otro esquema al azar — localizar el supuesto que falló, EXP-01):* el supuesto roto es que `order_line.unit_price` y `product.price_cents` son **el mismo hecho**. No lo son. Tienen **dependencias funcionales distintas**: `product_id → price_cents_vigente` frente a `(order_id, product_id) → precio_al_que_se_compró`. Coincidieron en un número el 1 de marzo y divergieron el 1 de junio. La normalización los fusionó porque BCNF mira un instante y en ese instante son iguales — la ceguera temporal de H0, hecha bug. La reparación no es "añadir una columna redundante", es reconocer que **había dos hechos y el esquema solo modelaba uno**:

```sql
CREATE TABLE order_line (
    order_id       bigint NOT NULL REFERENCES "order"(id),
    product_id     bigint NOT NULL REFERENCES product(id),
    qty            int NOT NULL CHECK (qty > 0),
    unit_price_cents int NOT NULL,        -- SNAPSHOT as-of: hecho distinto de product.price_cents
    PRIMARY KEY (order_id, product_id)
);
```

`unit_price_cents` **no es redundancia** (clase 2): su determinante es la línea, no el producto vigente. El esquema "con la columna" está *más* normalizado que el de H0, no menos, porque separa dos hechos que H0 había colapsado.

**Segundo campo — `order.total`, y aquí chocan dos reglas de esta skill sobre el mismo dato** (el patrón EXP-06/07/08: la falsificación más productiva es entre dos reglas propias). ¿Debe existir la columna `order.total_cents`?

- Regla **"sin redundancia / fuente de verdad única"** (EXP-06) → NO: `total = sum(line.qty * line.unit_price)`; las líneas son snapshots inmutables (append-only), así que la fuente *no* puede cambiar tras el evento (frontera A = No) → es derivable del estado presente → no la almacenes.
- Regla **"conservación con dueño mecánico"** (EXP-08) + lectura barata (EXP-06) → SÍ: el total se lee en cada listado de órdenes, en reportes, en el estado de cuenta; recalcular `sum` en cada lectura es caro, y el invariante `total == sum(líneas)` es exactamente la conservación de EXP-08 que quiero custodiar mecánicamente.

Las dos reglas dan **órdenes opuestas sobre el mismo campo** — el no-determinismo que hace fallar la transferencia (EXP-06): un modelo ejecutando la skill decidiría según cuál lea primero.

*Diagnóstico del choque (localiza el supuesto, no elijas la regla que grita más fuerte):* el supuesto roto es que "guardar el total" sea una única decisión binaria. No lo es. Se parte por la **frontera B**. La regla de EXP-06 prohíbe la copia *sin dueño* (clase 1: `total_cents int` a secas, que se desincroniza al primer line editado sin recomputar). La regla de EXP-08 *autoriza* la copia *con dueño* (clase 3). Ninguna de las dos gana; la frontera B las adjudica, igual que en EXP-08 el invariante de conservación adjudicó redondeo-una-vez vs. snapshot-de-línea. La forma correcta es la clase 3, y el motor la regala declarativamente:

```sql
-- Opción 3a: columna generada — el motor es el dueño, imposible desincronizar
ALTER TABLE order_line
    ADD COLUMN line_total_cents int GENERATED ALWAYS AS (qty * unit_price_cents) STORED;

-- Opción 3b: total materializado con el invariante de conservación como CHECK/trigger
--   total_cents se mantiene por trigger sobre order_line; el CHECK es el dueño mecánico:
--   CONSTRAINT total_conserva CHECK (total_cents = (SELECT sum(line_total_cents)
--                                                    FROM order_line WHERE order_id = id))
--   (materializado sólo si el perfil de lectura lo justifica; si no, es una VIEW)
```

`line_total_cents` como columna generada es redundancia clase 3 **gratis**: derivable, pero con el motor de dueño, imposible de violar. El `total` a nivel orden es clase 3 *condicional*: se materializa solo si el perfil de lectura lo pide (decisión de rendimiento medida, EXP-06: exige el número, no "es lento"), y siempre con el dueño de conservación de EXP-08. Si el perfil no lo pide, se queda como `VIEW` — derivación pura, cero redundancia. **La misma columna es bug (clase 1) o decisión legítima (clase 3) según tenga o no dueño; nunca es "redundancia" a secas.**

**Tercer campo — columnas nullable como tabla faltante escondida.** Reviso `"order"` y encuentro la tentación de añadir `gift_message text`, `gift_wrap_color text`, `gift_from text` — null para las órdenes que no son regalo. ¿Redundancia? No exactamente, pero es su prima: **redundancia de estructura**. El detector: *¿estas columnas se van a NULL en grupos correlacionados por tipo de fila?* Un `shipped_at timestamptz` que es null mientras la orden no se ha enviado es una **sola** columna opcional legítima (atributo de una entidad en un estado del ciclo). Pero tres columnas que son *todas* null juntas exactamente cuando la orden no es regalo, y *todas* no-null juntas cuando lo es, codifican un **subtipo oculto**: cada fila no-regalo repite implícitamente "no soy un regalo" en tres celdas. Regla de frontera: **columnas que van a null en grupos correlacionados por tipo de fila = extrae una tabla** (`gift_detail(order_id PK/FK, message, wrap_color, from_name)`); una columna independientemente opcional = déjala. El invariante "si hay una hay las tres" no era expresable como constraint simple en la tabla ancha — y por la asimetría del Paso 1, *una columna cuyo invariante no cabe en una constraint es señal de entidad mal modelada*. La tabla extraída sí lo expresa (`NOT NULL` en las tres + el PK/FK como presencia).

**Cuarto campo — la dirección de envío, y la frontera as-of como operador maestro.** `customer` tiene `address`. ¿La orden referencia `customer.address` o guarda su propia `shipping_address`? Frontera A otra vez: la dirección vigente del cliente **puede cambiar** después del evento de envío (el cliente se muda). La dirección *a la que se envió esta orden* es un hecho as-of. Son dos hechos → dos hogares: `customer.current_address` y `order.shipping_address_snapshot`. La dirección es la recurrencia más limpia del patrón: cada vez que la respuesta a la frontera A cambia de "No" a "Sí" a lo largo del ciclo de vida de un valor, ese valor **se parte en dos hechos** y gana su propia columna/tabla. La frontera as-of no es una regla que aplico de vez en cuando: es el **operador que genera las tablas correctas** del esquema.

### Paso 5 — Síntesis

Diseñar un esquema "sin redundancia" es, en una frase: **darle a cada *hecho* exactamente un hogar, donde un hecho se individúa por su dependencia funcional y por su identidad as-of; eliminar solo la copia derivable-del-presente-sin-dueño; y gobernar con un dueño declarativo toda copia que se conserve por rendimiento.** El desglose:

1. Reformula "sin redundancia" (quitar copias) a "un hecho, un hogar" (identidad correcta). "Redundancia" confunde tres cosas —copia patológica, snapshot as-of, copia gobernada— y el diseño es separarlas.
2. Por cada valor, **frontera A (EXP-06/07):** ¿la fuente cambia tras el evento? Sí → snapshot, no es redundancia, consérvalo (determinante = el evento). No → estado presente, derívalo.
3. Por cada copia derivable que quieras conservar, **frontera B (EXP-06/08):** ¿tiene dueño mecánico declarativo? Sin dueño → patológica, normaliza. Con dueño (columna generada, vista materializada con `CHECK`/trigger de conservación) → gobernada, legítima como decisión de rendimiento.
4. El detector mecánico de la copia patológica es el **test de anomalías** (¿un update obliga a escribir en dos lugares para mantener un invariante?) — un test diferencial de EXP-05 y el oráculo semi-honesto de la capa sintáctica del esquema.
5. **Cada invariante del dominio debe caer sobre una constraint declarativa** (FK, UNIQUE, CHECK, NOT NULL, generated, exclusion) — el esquema es el dominio donde el "dueño mecánico" de EXP-06 es más barato. Una columna cuyo invariante no cabe en una constraint es señal de entidad mal modelada (típicamente nulls correlacionados = subtipo/tabla faltante).
6. La identidad de entidad y de clave es **oráculo ausente** (dominio, no teoría); la normalización es **oráculo semi-honesto** (mecánico) pero **ciego a la identidad temporal** — por eso se corre *después* de la frontera A, nunca en su lugar.

**Meta-hallazgo del experimento:** la frontera de EXP-06 (*¿la fuente puede cambiar tras el evento?*) no era una regla de la capa de aplicación — es el **operador generador de tablas** de la capa de esquema, un nivel por debajo de donde se descubrió. Cada vez que la respuesta a esa frontera cambia a lo largo del ciclo de vida de un valor, el valor se parte en dos hechos y gana su hogar. Y la tipología del oráculo (EXP-07/08) se refina otra vez: **dentro del diseño de esquema, la normalización es la capa con oráculo semi-honesto (FD/anomalías, mecánico) pero temporalmente ciega, y la identidad de los hechos es la capa con oráculo ausente** — misma partición sintáctico/semántico de EXP-08, subida del archivo de código al modelo de datos. "Sin redundancia" resultó ser, como "detecta" y "maximiza el Sharpe", una consigna que hay que reformular antes de que sea segura de ejecutar.

## Patrones de razonamiento observados

1. **Reformulación de la consigna-trampa, 4ª instancia sistemática.** Tras "detecta" (EXP-08), "maximiza el Sharpe"/"hazla operable" (EXP-07), aquí "sin redundancia" se desactiva antes de tocar el esquema. El reflejo "sospecha del objetivo que suena unívoco" ya es un patrón confirmado: la consigna esconde una reformulación que cambia el método completo.
2. **La frontera de EXP-06 asciende de regla a operador generador.** El movimiento clave fue reconocer que *¿la fuente puede cambiar tras el evento?* no se aplica caso por caso sino que **genera las tablas**: cada flip de la respuesta parte un valor en dos hechos. La regla de aplicación de EXP-06 resultó ser un principio de esquema un nivel más abajo.
3. **Partición de un concepto confuso en tres por dos preguntas de frontera.** "Redundancia" se parte en patológica / snapshot / gobernada con las fronteras A (temporal) y B (dueño). Es el mismo movimiento que EXP-08 hizo con "oráculo" (honesto/ausente/adversarial) y EXP-02 con "fallo" (clases A–G): un sustantivo monolítico se resuelve en una tipología accionable.
4. **Descarte por materialización con falsificación numérica.** El esquema H0 "sin redundancia" se descarta escribiéndolo en DDL real y corriendo un ejemplo trabajado ($20→$24 al cambiar el precio) de fuente independiente del código (EXP-08), no argumentando en abstracto (EXP-03/06). El bug se exhibe, no se postula.
5. **Choque entre dos reglas propias → adjudicación por frontera, 4ª instancia.** Tras EXP-06 (fuente-única vs. inmutabilidad → snapshot), EXP-07 (más-historia vs. no-lookahead → as-of) y EXP-08 (redondeo-una-vez vs. snapshot-de-línea → conservación), aquí "sin redundancia" vs. "conservación con dueño" chocan sobre `order.total` y los adjudica la frontera B (¿tiene dueño?). El patrón "el invariante/pregunta superior adjudica el choque de dos reglas menores sobre el mismo campo" es ya un reflejo confirmado.
6. **Aprovechar la asimetría del dominio a favor, no solo para localizar lo que falta.** Por primera vez la asimetría estructural (EXP-04) señala una **ventaja** del dominio nuevo, no una carencia: el motor regala dueños mecánicos declarativos, así que el principio caro de EXP-06 ("todo invariante, un dueño mecánico") es aquí el más barato de cumplir. La asimetría reorganiza el método hacia "mapea cada invariante a una constraint".
7. **La columna sin constraint posible como señal de entidad mal modelada.** Corolario operativo de la asimetría: si un invariante no cabe en una constraint declarativa (nulls correlacionados, dependencia entre columnas), la entidad mezcla dos hechos → extrae tabla. Detección de modelado defectuoso por un disparador observable, no por gusto.

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

- Cuando la tarea sea "diseña un esquema sin redundancia" (o "normaliza esto"), no lo trates como "elimina toda copia": reformúlalo a "dale a cada *hecho* un solo hogar, donde un hecho se individúa por su dependencia funcional y por su identidad as-of" — "sin redundancia" literal borra los snapshots históricos y produce bugs de corrección (EXP-06).
- Cuando evalúes si una columna es redundante, aplica primero la frontera temporal (EXP-06/07): ¿la fuente de ese valor puede cambiar después del evento que lo consume? Si sí, es un snapshot as-of (un hecho con determinante propio, p. ej. `order_line.unit_price`, `order.shipping_address`), **no** redundancia — consérvalo; si no, es estado presente, derívalo.
- Cuando dos columnas compartan el mismo valor hoy (precio de producto vs. precio de línea, dirección de cliente vs. dirección de envío), no las fusiones por parecer iguales: si tienen dependencias funcionales distintas son dos hechos, y guardarlos ambos es normalización correcta, no duplicación — coincidir en un instante no es ser el mismo hecho.
- Cuando decidas si guardar un valor derivable del estado presente (un `total`, un contador, un agregado), aplica la frontera de dueño (EXP-06/08): sin dueño mecánico es redundancia patológica (anomalía de update) — normalízala; con dueño declarativo (columna generada, vista materializada con `CHECK`/trigger de conservación `suma(partes)==total`) es una copia gobernada, legítima solo como decisión de rendimiento medida, no como diseño base.
- Cuando sospeches redundancia patológica, corre el test de anomalías: ¿existe un update que, para mantener un invariante, obliga a escribir en dos lugares a la vez? Si sí, esos dos lugares guardan el mismo hecho sin dueño (test diferencial, EXP-05) — quita uno (normaliza) o dale un dueño mecánico (constraint).
- Cuando modeles cualquier entidad, mapea cada invariante del dominio a una constraint declarativa (FK, UNIQUE, CHECK, NOT NULL, columna generada, exclusion) — el motor es el dueño mecánico más barato que existe (EXP-06); un invariante custodiado por convención de aplicación no está custodiado.
- Cuando un invariante no quepa en una constraint declarativa, trátalo como señal de entidad mal modelada, no como límite del motor: casi siempre la fila mezcla dos hechos o dos entidades — reescribe el modelo hasta que el invariante sea expresable.
- Cuando veas varias columnas nullable que se van a null en grupos correlacionados por tipo de fila (todas presentes o todas ausentes juntas), extrae una tabla para ese subtipo: los nulls correlacionados codifican un subtipo oculto y repiten estructura; una sola columna independientemente opcional (p. ej. `shipped_at` mientras no se envía) se queda.
- Cuando dudes entre surrogate y natural key, no lo resuelvas por reflejo: responde primero la identidad de la entidad (¿qué hace que dos filas sean la misma cosa del mundo? — oráculo ausente, dominio), y deriva la clave de esa respuesta; la elección de clave es consecuencia de la identidad, no sustituto de definirla.
- Cuando normalices, recuerda que la teoría de formas normales es ciega a la identidad temporal (opera sobre dependencias funcionales en un instante): úsala como oráculo de la sub-pregunta sintáctica (¿anomalía de update?) **después** de resolver la frontera as-of, nunca en su lugar — BCNF no distingue un snapshot de un duplicado.
- Cuando consideres denormalizar por rendimiento, exige el número que lo justifica (perfil de lectura real, EXP-06: "es lento" no es un dato) y adjunta el dueño mecánico que reconcilia la copia con su fuente — denormalizar sin dueño es la anomalía de update de manual, denormalizar con dueño es una decisión de rendimiento gobernada.

## Impacto en la skill

- Nueva sección "Diseño de esquemas sin redundancia (EXP-09)" en INSTRUCCIONES APRENDIDAS con las 11 instrucciones extraídas.
- Paso 2 (Clasificación y descomposición) gana el caso de diseño de esquema: sub-dominio de arquitectura (EXP-06, ítem #1 de irreversibilidad) donde la asimetría es **a favor** — el motor regala dueños mecánicos declarativos; método = mapea cada invariante a una constraint, y "sin redundancia" se reformula a "un hecho, un hogar".
- PRINCIPIOS INVARIANTES: se refina "Fuente de verdad única" con la **taxonomía de redundancia en tres clases** (patológica / snapshot as-of / gobernada con dueño) discriminadas por la frontera A (temporal, EXP-06/07) y la frontera B (dueño, EXP-06/08); y se nombra la frontera as-of como **operador generador de tablas**.
- Tipología del oráculo (EXP-07/08): nuevo refinamiento — dentro del esquema, la normalización es capa con **oráculo semi-honesto pero temporalmente ciego** (FD/anomalías, mecánico) y la identidad de entidad es **oráculo ausente** (dominio); misma partición sintáctico/semántico de EXP-08 subida al modelo de datos.
- DETECTOR DE RESULTADOS SOSPECHOSOS: nuevas señales — esquema "perfectamente sin redundancia" que borró snapshots históricos (bug as-of, no logro); columna nullable en grupos correlacionados (subtipo/tabla faltante); columna cuyo invariante no cabe en constraint (entidad mal modelada); `total`/agregado guardado sin dueño mecánico (anomalía de update).
- Paso 4 (Falsificación): el refutador de un esquema es un ejemplo trabajado que cambia la fuente en el tiempo (subir el precio del producto y ver mutar una orden histórica), de fuente independiente del código (EXP-08).
