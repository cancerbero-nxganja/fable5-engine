# EXP-08 — Cómo Fable 5 detecta bugs en código con lógica de negocio incorrecta

**Fecha:** 2026-07-15 00:13 UTC
**Modelo usado:** claude-fable-5
**Run número:** 8 (FASE 2 — Patrones de razonamiento)

## Pregunta / Prompt enviado a Fable 5

> Muéstrame cómo detectas un bug en código donde la *lógica de negocio* es incorrecta —no un crash, no un error de tipos, no un test que falla, sino código que corre limpio y da un resultado plausible pero equivocado según las reglas del dominio. Toma un caso concreto y muestra tu proceso real de razonamiento: qué hipótesis sobre el método de detección consideraste, cuáles descartaste y por qué, y cómo llegas a decidir que algo está mal. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica

La pregunta trae una palabra que hay que desactivar antes de tocar nada: **"detectas"**. Sugiere que hay un acto perceptivo — leo el código, *veo* que está mal. Por EXP-05 eso es exactamente la trampa: no existe una señal interna monofuente de incorrección, y "mirar más fuerte" el código no la produce. Reformulo el método pedido de *"cómo percibes el bug"* a *"qué segunda vista independiente exhibes contra la cual el código puede discrepar"*. Un bug de lógica de negocio no se ve; se **exhibe como desacuerdo** entre el código y una regla del dominio establecida por fuera del código. Si no tengo esa regla externa, no tengo detector — tengo una opinión sobre código que ya entendí.

Y hay una segunda reformulación, más importante, que define todo el experimento. El enunciado la nombra sin saber que es la clave: *"corre limpio... no un test que falla"*. En EXP-03 clasifiqué código como el dominio con **oráculo honesto**: el runtime ejecuta y no miente, así que el criterio de done es ejecutable y los fallos son autocorregibles dentro del turno. Pero el enunciado describe precisamente el caso donde ese oráculo **se queda callado**. El compilador aprueba, los tipos cuadran, los tests pasan, el output es plausible — y sin embargo es incorrecto. Entonces la pregunta real de EXP-08 es: *¿qué método uso cuando el oráculo que hizo de código el dominio fácil desaparece?* Eso es el Paso 1.

### Paso 1 — La asimetría estructural: el oráculo honesto es de alcance limitado

Aplico el método de EXP-04/06/07: comparo el dominio nuevo contra el vecino resuelto más cercano y localizo qué falta. El vecino aquí no es otro dominio — es **el mismo dominio, código (EXP-03), pero en otra capa**. Comparo las dos capas de una pieza de código:

| | Capa sintáctica/ejecución | Capa semántica/dominio |
|---|---|---|
| ¿Qué pregunta responde el oráculo? | "¿el código hace lo que dice?" | "¿lo que el código dice es lo correcto?" |
| ¿Hay oráculo? | **Sí — el runtime, honesto** (EXP-03) | **No existe** |
| Qué detecta correr el código | crashes, tipos, tests, comportamiento vs. intención declarada | nada — corre limpio *por construcción* del bug |
| Qué clase de bug vive aquí | implementación (código ≠ su propia intención) | **lógica de negocio (la intención del código ≠ la verdad del dominio)** |
| Antídoto | ejecutar y confiar | reconstruir el invariante por fuera y buscar el desacuerdo |

La conclusión reordena todo: **la clasificación "código = oráculo honesto" de EXP-03 no era del dominio, era de la capa.** El runtime es honesto sobre *lo que el código hace* y absolutamente mudo sobre *lo que el dominio requiere*. Un bug de lógica de negocio es, con precisión, el bug que vive **en el hueco entre esas dos capas**: código que hace fielmente lo que su autor quiso, donde lo que el autor quiso está mal según una regla que el runtime no conoce. Por eso correr el código nunca lo atrapa — el oráculo honesto está mirando la capa equivocada.

Esto refina la tipología del oráculo de EXP-07. No era "código honesto, datos/arquitectura ausente, trading adversarial" como etiquetas **por dominio**. El tipo de oráculo es **por pregunta, no por dominio**: la misma pieza de código tiene oráculo honesto para la pregunta sintáctica y oráculo *ausente* para la pregunta semántica. Y una vez visto así, el método está determinado por EXP-07: cuando el oráculo está ausente, no ejecutas y confías — **sustituyes por el protocolo adversarial** (el de datos/arquitectura). Es decir: para cazar un bug de lógica de negocio, uso el método de EXP-04/06 *dentro* de un archivo de código. Reconstruyo los invariantes del dominio por fuera del código y busco el input donde el código los viola. El detector no es leer mejor; es importar la regla.

### Paso 2 — Por qué correr el código y leer el código no alcanzan (descarte de los métodos ingenuos)

Antes de proponer el método, descarto los cuatro reflejos que la palabra "detectar" activa, porque cada descarte define por contraste lo que sí funciona.

**H0 — "Traza el código con cuidado, sigue el flujo, entiéndelo."**
*Descartada como detector primario, y es una inversión.* Trazar verifica que el código hace lo que dice — sigue la intención del autor, re-ejecuta su modelo mental. Un bug de lógica de negocio es código que hace *exactamente* lo que dice, y lo que dice está mal. Puedo trazar una función que aplica el descuento después del impuesto con precisión perfecta y concluir "sí, aplica descuento sobre el total con impuesto" sin notar nada — porque la traza no tiene referencia a la regla del dominio contra la cual comparar. Trazar detecta *código ≠ intención declarada del código*; el bug de negocio es *intención del código ≠ verdad del dominio*. Trazar más fuerte me hunde más en el modelo mental del autor, que es de donde salió el bug.

**H1 — "Corre los tests, o escribe más tests."**
*Descartada como suficiente — y aquí está el hallazgo operativo del experimento.* Un test es un oráculo **solo si codifica la regla del dominio de forma independiente del código.** El caso típico: el test lo escribió el mismo autor, a la vez que el código, desde la misma lectura del spec. El bug ("descuento después de impuesto") y su test (`assert total == 98.00`) nacieron del mismo malentendido. Corren juntos y **concuerdan** — pero es el falso acuerdo de EXP-05: dos vías que comparten el supuesto falso (la lectura del autor) no son independientes en su supuesto, solo en su cálculo. "Todos los tests pasan" **no es evidencia de corrección lógica**; es evidencia de consistencia entre dos artefactos del mismo autor. Corolario que sí es detector: para cualquier test que custodia una regla de negocio, pregunta *¿de dónde salió el valor esperado?* Si salió del output actual del código ("lo corrí, dio 98.00, lo congelé como golden"), el test es una **fotografía del bug**, no un oráculo. El valor esperado tiene que venir de una fuente independiente del código: un ejemplo trabajado que dio el negocio, una fórmula regulatoria, una identidad contable, un cálculo a mano desde primeros principios.

**H2 — "Busca code smells, complejidad, hotspots."**
*Descartada — no hay correlación.* Los bugs de lógica de negocio viven tanto en código limpio como en código enredado. `balance += refundAmount` es una línea limpia, legible, con buen nombre — y con el signo invertido. Las heurísticas de complejidad encuentran bugs de implementación (donde la enredadera esconde el error), no bugs de dominio (donde el error *es* la regla, escrita claramente). Peor: la limpieza es engañosa en la otra dirección (H4 abajo).

**H3 — "Confía en el sistema de tipos."**
*Descartada como detector, retenida como prevención.* El bug canónico de negocio es **type-correct**: el reembolso es un `Money`, el balance es un `Money`, `+` chequea tipos perfectamente. Los tipos atrapan errores de categoría (sumar `Money` a `Date`), no errores de dirección o de regla. El valor real de los tipos aquí no es detectar — es **prevenir**, subiendo el invariante al tipo (un `Refund` que solo sabe decrementar, un `Money` sin operador `double`), lo cual convierte H3 en el método de EXP-06 (dueño mecánico del invariante). Pero "los tipos pasan" no detecta el bug; *diseñar los tipos para que el bug sea irrepresentable* lo previene. Son cosas distintas y adyacentes.

Los cuatro descartes convergen en un punto: **todos operan dentro del código o de sus derivados (tests del autor, tipos del autor).** Ninguno importa una verdad de afuera. Y el bug de lógica de negocio es, por definición (Paso 1), invisible desde adentro. El detector tiene que cruzar la frontera del código.

### Paso 3 — El método: reconstruir el oráculo ausente y buscar el desacuerdo

Si el oráculo honesto está mudo en la capa semántica (Paso 1), lo sustituyo por el protocolo adversarial de EXP-04/06, instanciado en código:

**(1) Recupera el conjunto de invariantes del dominio — por fuera del código.** Antes de leer la implementación *para juzgarla*, enumero qué debe ser siempre verdad en este dominio, sacándolo del dominio (docs, la persona de negocio, la regulación, la ecuación del libro mayor), **nunca leyendo lo que el código hace** — porque leer el código para extraer la regla es re-derivar el bug. Es el "enumera invariantes y dale a cada uno un dueño mecánico" de EXP-06, usado ahora como detector, no solo como diseño. Los invariantes de negocio caen en un catálogo recurrente, y ese catálogo *es* el mapa de dónde buscar:

- **Conservación / balance:** las partes suman el todo después de la operación (splits de pago, asignación de impuesto, reembolsos parciales); dinero que entra = dinero que sale; el doble asiento cuadra.
- **Dirección / signo:** cada crédito/débito, incremento/decremento se mueve en el sentido correcto (reembolso decrementa el balance, cargo lo incrementa).
- **Orden no conmutativo:** descuento vs. impuesto, fee antes/después de conversión de divisa, redondear antes/después de sumar. El runtime no sabe que estos no conmutan.
- **Fronteras e inclusividad:** período de facturación `[inicio, fin)` — ¿se cobra dos veces el último día? ¿`edad >= 18` o `> 18`? Off-by-one en unidades *de negocio* (días, centavos, asientos), no de array.
- **Monotonía / máquina de estados:** el log de auditoría es append-only, el estado de una orden no retrocede (`shipped → pending` prohibido), los timestamps no decrecen.
- **Autoridad / alcance:** toda mutación y lectura está acotada a su tenant/dueño — el query filtra por `tenant_id`, no solo por `id` (el IDOR es un bug de lógica de negocio que el sistema de tipos adora dejar pasar).
- **Concurrencia sobre invariantes compartidos:** inventario ≥ 0, balance ≥ 0 se cumplen mono-hilo y se rompen con dos requests entrelazados; check-then-act sin lock/constraint.
- **Tiempo y as-of (EXP-07):** proración, interés, día bisiesto, frontera de día dependiente de timezone; y computar el valor de *hoy* donde la regla quiere el valor *conocido en el instante del evento*.
- **Redondeo y representación de dinero:** floats para dinero; redondear cada línea vs. el total; half-up vs. banquero; el centavo que aparece o se esfuma.

**(2) Por cada invariante, formula la pregunta diferencial (EXP-05):** ¿existe un segundo enunciado independiente de esta regla contra el cual el código pueda discrepar? El bug **es** ese desacuerdo. Si el único enunciado de la regla es el código mismo, no hay oráculo y no hay detección posible — hay que importar la regla de afuera. Así que la detección es literalmente: exhibir el invariante, y buscar el input que hace que el código lo viole.

**(3) Ataca por las costuras donde las reglas de dominio se concentran** (la lista de arriba es la lista de costuras). En cada una, el movimiento es el mismo: nombrar la regla del dominio, luego buscar el input que la rompe.

**(4) El refutador más barato (invariante EXP-01/03/04/05): un ejemplo trabajado concreto del dominio, entrada→salida, calculado independientemente, corrido contra el código.** Para un bug de lógica, el refutador **no** es otra lectura del código (comparte el supuesto) ni un test cuyo golden salió del código (misma cosa): es un número cuyo resultado esperado saqué del negocio/spec/primeros principios. "Ítem de $100, 10% de descuento, 8% de impuesto → esperado $97.20 si el descuento va primero — ¿el código devuelve $97.20 o $98.00?" Un solo número mata el bug de orden al instante, y es la segunda vista independiente que el runtime no puede dar.

### Paso 4 — Materialización y falsificación: el mini-caso donde chocan dos de mis reglas

El output limpio es sospechoso (EXP-05) y el refutador más barato de un método es correrlo contra un caso concreto (EXP-06). Tomo una función de checkout real:

```python
def order_total(lines, discount_pct, tax_pct):
    subtotal = sum(l.price for l in lines)
    tax = round(subtotal * tax_pct, 2)
    discounted = subtotal + tax - round(subtotal * discount_pct, 2)
    return discounted

def apply_refund(balance, refund):
    return balance + refund
```

**Costura de signo (el más barato, el que más mata).** Invariante del dominio: *un reembolso reduce lo que el cliente debe*. Refutador: balance $50, reembolso $20 → esperado $30. El código da $70. `balance + refund` tiene el signo invertido; el runtime lo suma feliz porque ambos son `Money` y `+` chequea tipos. **Bug confirmado por desacuerdo con el invariante de dirección, no por leer el código** — de hecho la línea se lee perfectamente bien.

**Costura de orden no conmutativo.** Invariante: *el descuento se aplica sobre la base imponible, antes del impuesto* (regla fiscal típica; el negocio la fija, no yo). El código calcula `subtotal + tax − descuento`: aplica el impuesto sobre el subtotal **sin** descontar. Refutador con número del dominio: subtotal $100, descuento 10%, impuesto 8% → esperado = impuesto sobre $90 = $7.20, total $97.20. El código da $100 + $8.00 − $10.00 = $98.00. Desacuerdo de $0.80. El bug es el *orden*, y trazar el código no lo delata porque el código hace consistentemente lo que dice — solo que "lo que dice" contradice la regla fiscal que vive fuera del archivo.

**Y aquí aparece el choque que busco** (el patrón EXP-06/07: la falsificación más productiva es entre dos de mis propias reglas sobre el mismo dato). Al arreglar el redondeo colisionan dos invariantes de esta skill:

- Regla **"redondea una sola vez en la frontera"** (disciplina de redondeo de dinero) → calcula el total exacto y redondea al final, una vez.
- Regla **"cada línea es un hecho registrado, un snapshot inmutable"** (EXP-06, snapshot ≠ duplicación) → cada línea de la factura persiste su propio monto, y esos montos son registros que después deben cuadrar.

Para una factura con líneas de $10.005 y $10.005, 8% de impuesto: redondear-una-vez sobre el total ($20.01 → impuesto $1.6008 → $1.60) da un número; redondear por línea ($10.005 → $10.01 cada una, impuesto $0.80 + $0.80 = $1.60... o según el reparto, $1.61) da otro. Las dos reglas dan **órdenes opuestas sobre el mismo campo**: ¿redondeo por línea (para que cada hecho persistido sea un centavo válido) o sobre el total (para no acumular error)? Un modelo ejecutando la skill decidiría según cuál lea primero — el no-determinismo que hace fallar la transferencia (EXP-06).

**Diagnóstico del contraejemplo (no probar otra regla — localizar el supuesto que falló, EXP-01):** el supuesto roto es que redondeo y snapshot gobiernan la *misma* cantidad. No. Gobiernan cantidades distintas unidas por un tercer invariante. El invariante de **conservación** es el árbitro: *la suma de los montos de línea persistidos debe igualar el total cobrado*. Eso fuerza el método: redondea **una vez** para fijar el total (regla de frontera), y luego **asigna** ese total redondeado de vuelta a las líneas por reparto de mayor-residuo (largest-remainder), de modo que los centavos de las líneas reconcilien con el total. Ninguna de las dos reglas ganó; el invariante de conservación las adjudicó. Es exactamente la forma de EXP-06 ("derivable es propiedad temporal") y EXP-07 ("as-of: el valor es función de cuándo preguntas"): una regla de frontera nacida del choque de dos reglas internas sobre el mismo campo. La llamo **conservación con reconciliación de redondeo**, y su dueño mecánico es el chequeo `sum(lines) == total` en el punto de persistencia.

**Costura de autoridad y estado (chequeo rápido, misma jugada):** si `apply_refund` no verifica que la orden esté en un estado reembolsable ni que el `refund ≤ paid`, permite reembolsar una orden ya reembolsada o más de lo cobrado — violación de conservación (dinero que sale > dinero que entró) y de máquina de estados. El detector es el mismo: nombrar el invariante ("no se reembolsa más de lo pagado", "refunded es terminal"), buscar el input que lo rompe.

### Paso 5 — Síntesis

Detectar un bug de lógica de negocio es, en una frase: **importar el invariante que el runtime no conoce y buscar el input donde el código y el invariante discrepan.** El oráculo honesto de EXP-03 es de alcance limitado — honesto sobre lo que el código hace, mudo sobre lo que el dominio requiere — y el bug de negocio vive justo en ese hueco. Por eso:

1. Reformula "detecta el bug" (percibir) a "exhibe la segunda vista independiente" (diferencial, EXP-05). Leer y correr el código no son segundas vistas: comparten el supuesto del autor.
2. Reconstruye los invariantes del dominio **por fuera del código** (conservación, signo, orden no conmutativo, frontera, estado, autoridad, concurrencia, as-of, redondeo) — leerlos del código re-deriva el bug.
3. Ataca por esas costuras; en cada una nombra la regla del dominio y busca el input que la viola.
4. El refutador más barato es un ejemplo trabajado con resultado esperado **de fuente independiente del código** (negocio, regulación, identidad contable, cálculo a mano). Un test cuyo golden salió del código es una fotografía del bug, no un oráculo.
5. El fix durable de todo invariante violado es darle un **dueño mecánico** (constraint, tipo, transacción, política append-only), no una convención (EXP-06).

**Meta-hallazgo del experimento:** el tipo de oráculo no es **por dominio** sino **por pregunta / por capa**. EXP-07 clasificó dominios (código honesto, datos/arquitectura ausente, trading adversarial); EXP-08 muestra que la misma pieza de código tiene oráculo honesto para la pregunta sintáctica y oráculo *ausente* para la pregunta semántica. Los bugs de lógica de negocio son exactamente los que habitan esa brecha, y por eso el método correcto para cazarlos dentro de un archivo de código es el método de *dominio-sin-oráculo* (protocolo adversarial de EXP-04/06), no el método de *código-con-oráculo* (ejecutar y confiar) de EXP-03. La tipología del oráculo se refina de una etiqueta de dominio a una clasificación (dominio × capa de la pregunta).

## Patrones de razonamiento observados

1. **Localización del oráculo por capa, no por dominio.** El movimiento clave fue no aceptar la etiqueta heredada "código = oráculo honesto" (EXP-03) y preguntar *¿honesto respecto de qué pregunta?* — separando la capa sintáctica (oráculo presente) de la semántica (oráculo ausente). El bug se define entonces como el habitante de la brecha entre capas. Es el método de asimetría estructural (EXP-04/06/07) aplicado por primera vez **dentro de un mismo dominio**, entre dos capas de la misma pieza.
2. **Inversión del reflejo "detectar = percibir".** Igual que EXP-07 invirtió "maximizar el Sharpe", aquí Fable 5 invierte "leer el código con más cuidado": leer más fuerte hunde más en el modelo mental del autor, que es la fuente del bug. La detección no es perceptiva sino diferencial — exhibir una regla externa.
3. **Falso acuerdo código↔test como instancia software de EXP-05.** El "todos los tests pasan" se diagnostica como dos vías que comparten el supuesto del autor (no independientes en el supuesto), reproduciendo el fallo exacto de EXP-05. De ahí sale una regla operativa nítida: preguntar de dónde salió el valor esperado del test.
4. **Descarte por materialización de los cuatro métodos ingenuos.** Trazar, testear, smells, tipos — cada uno se descarta mostrando el caso concreto donde falla, no argumentando en abstracto (EXP-03/06). El patrón común de los cuatro (todos operan dentro del código o de sus derivados) es lo que revela el requisito: cruzar la frontera del código.
5. **Choque entre reglas propias → regla de frontera, 3ª instancia sistemática.** Tras EXP-06 (fuente-única vs. inmutabilidad → snapshot temporal) y EXP-07 (más-historia vs. no-lookahead → as-of), aquí redondeo-una-vez vs. snapshot-de-línea chocan sobre el monto de una línea, y el diagnóstico produce **conservación con reconciliación de redondeo** (reparto por mayor-residuo). El patrón "el invariante superior adjudica el choque de dos reglas menores" ya es reflejo confirmado.
6. **Detección y prevención convergen en el dueño mecánico (EXP-06).** El método no termina en "encontré el bug": el cierre es asignar al invariante violado un custodio mecánico para que no reaparezca por erosión de convención — unificando el detector de EXP-08 con el principio de diseño de EXP-06.

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

- Cuando busques un bug de lógica de negocio (código que corre limpio, tipa bien y pasa tests pero da un resultado equivocado según el dominio), no lo trates como perceptivo: reconstruye el invariante del dominio por fuera del código y busca el input donde el código y el invariante discrepan — leer o correr el código no son segundas vistas, comparten el supuesto del autor.
- Cuando quieras extraer la regla del dominio contra la cual juzgar el código, sácala de una fuente externa (docs, la persona de negocio, regulación, identidad contable), nunca leyendo lo que el código hace — extraer la regla del código re-deriva el bug.
- Cuando revises código de negocio, recorre las costuras donde las reglas se concentran y el runtime es mudo: conservación (partes suman el todo), signo/dirección (crédito vs. débito), orden no conmutativo (descuento vs. impuesto, redondeo vs. suma), frontera/off-by-one en unidades de negocio (días, centavos, asientos), máquina de estados (no retroceder), autoridad/alcance (filtrar por tenant, no solo por id), concurrencia sobre invariantes compartidos, as-of temporal, y redondeo de dinero.
- Cuando "todos los tests pasan" se ofrezca como evidencia de corrección lógica, no lo aceptes: si el código y el test los escribió el mismo autor desde la misma lectura del spec, son dos vías que comparten el supuesto falso y dan acuerdo falso (EXP-05) — pregunta de dónde salió el valor esperado de cada test.
- Cuando un test custodie una regla de negocio, verifica el origen de su valor esperado: si salió del output actual del código ("lo corrí y congelé el golden"), es una fotografía del bug, no un oráculo — el valor esperado debe venir de una fuente independiente del código.
- Cuando quieras confirmar o refutar un bug de lógica, construye un ejemplo trabajado concreto entrada→salida con el resultado esperado calculado de forma independiente del código (negocio, regulación, cálculo a mano) y córrelo — un solo número del dominio mata un bug de orden o de signo al instante.
- Cuando encuentres una regla de negocio implementada en una sola línea limpia sin manejo de redondeo, frontera ni signo, trátalo como evidencia EN CONTRA (EXP-05, "demasiado limpio"): las reglas de dominio reales son asimétricas y tienen esquinas; una implementación sin fricción suele significar que se saltó una esquina, no que no existía.
- Cuando manejes dinero en líneas persistidas más un total, aplica conservación con reconciliación de redondeo: redondea una sola vez para fijar el total y luego asigna ese total a las líneas por reparto de mayor-residuo, con el chequeo `suma(líneas) == total` como dueño mecánico — así se reconcilian la regla "redondea una vez en la frontera" y la regla "cada línea es un hecho registrado" (snapshot, EXP-06).
- Cuando confirmes un bug de lógica de negocio, no cierres con el fix puntual: asigna al invariante violado un dueño mecánico (constraint, tipo, transacción, política append-only) para que no reaparezca por erosión de convención (EXP-06) — detección y prevención terminan en el mismo lugar.
- Cuando la petición o el ticket incrusten la regla de negocio ("aplica el descuento al total final"), evalúa la regla contra el dominio antes de implementarla: seguir el ticket fielmente reproduce el error del negocio con competencia (clase F, EXP-02) — el revisor juzga la regla, no solo la conformidad del código con el ticket.
- Cuando abras cualquier pieza de código para juzgar su corrección, separa la pregunta sintáctica (¿hace lo que dice? → oráculo honesto, ejecútalo) de la semántica (¿lo que dice es correcto? → oráculo ausente, protocolo adversarial): el tipo de oráculo es por pregunta, no por dominio, y los bugs de negocio viven en la capa semántica.

## Impacto en la skill

- Nueva sección "Detección de bugs de lógica de negocio (EXP-08)" en INSTRUCCIONES APRENDIDAS con las instrucciones extraídas.
- Paso 2 (Clasificación y descomposición) gana el refinamiento de la **tipología del oráculo de EXP-07: es por pregunta/capa, no por dominio**. El código tiene oráculo honesto para la capa sintáctica y ausente para la semántica; los bugs de negocio viven en la brecha y se cazan con el método de dominio-sin-oráculo (protocolo adversarial) dentro del archivo de código.
- Nuevo principio de frontera en PRINCIPIOS INVARIANTES: **Conservación con reconciliación de redondeo** (redondea una vez en la frontera; asigna a los hechos persistidos por mayor-residuo; `suma(partes) == todo` como dueño mecánico), hermana de snapshot≠duplicación (EXP-06) y corrección as-of (EXP-07).
- Detector de resultados sospechosos gana señales de lógica de negocio: "todos los tests pasan" como posible falso acuerdo código↔test del mismo autor; regla de negocio en una línea limpia sin redondeo/frontera/signo como "demasiado limpio"; el test "¿de dónde salió el valor esperado?".
- Paso 4 (Falsificación) gana el refutador de lógica de negocio: un ejemplo trabajado con resultado esperado de fuente independiente del código — nunca otra lectura del código ni un test cuyo golden salió del código.
- Mapa de zonas de fallo: se anota que la lógica de negocio es la sub-región del código donde el oráculo honesto (clase C tiene solución barata vía runtime) enmudece, porque el runtime es honesto sobre sintaxis y mudo sobre semántica.
