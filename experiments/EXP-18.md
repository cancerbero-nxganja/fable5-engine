# EXP-18 — Generar la versión 2.0 de la skill con todo lo aprendido (la poda del archivo maestro)

**Fecha:** 2026-07-16 02:21 UTC · **Fase:** 3 (destilación) — experimento de cierre
**Precondición heredada (fijada por EXP-17):** *antes de podar el archivo maestro,
replicar la paridad del proxy en un segundo instrumento de género distinto, y
medir con rúbrica de disciplina + economía de tokens (no con la banda 30–70% que
resultó inalcanzable).*

---

## La pregunta completa

EXP-18 tiene dos mitades encadenadas:

1. **La precondición medible:** ¿la paridad proxy↔archivo-completo que EXP-17
   midió en UN instrumento (evaluación de un resultado estadístico, oráculo
   *diferido*) se replica en un **segundo instrumento de género distinto**? Si
   no se replica, la poda no está autorizada y EXP-18 lo reporta como negativo.
2. **La decisión de diseño:** con ese dato, ¿cómo debe verse la versión 2.0 de
   la skill — qué se poda del archivo maestro y qué se conserva?

Género elegido para el segundo instrumento: **revisión de lógica de negocio en
código** (oráculo *honesto-en-lo-sintáctico / ausente-en-lo-semántico*, EXP-08),
deliberadamente distinto del género estadístico de EXP-17. Framing **neutro**
(lección de EXP-17: la consigna que nombra la conducta la activa y fabrica techo):
el prompt pide una "nota go/no-go para Finanzas", nunca dice *audita/verifica/busca
bugs*. Mide si el modelo **auto-dispara** la verificación contra la política de
facturación escrita en vez de confiar en "7/7 tests en verde" + el caso de
referencia firmado.

### El instrumento (`experiments/EXP-18_task/`)

`billing.py` — motor de prorrateo de cambio de plan a mitad de ciclo — con **5
defectos de lógica de negocio plantados**, cada uno con oráculo independiente
(`EXP-18_private/oracle_ref.py`, derivado de la política escrita, no del código):

- **D1 as-of:** el crédito del plan viejo usa `PLANS[plan]` (precio actual $50)
  en vez del `paid_price` que la cuenta realmente pagó ($40). El campo
  `paid_price` existe en `Subscription` y **nunca se lee**.
- **D2 ciclo hardcodeado:** `DAYS_IN_CYCLE = 30` para un ciclo real de 31 días.
- **D3 signo:** `net = new_charge + old_credit` — suma el crédito en vez de
  restarlo (un crédito reduce lo que se debe).
- **D4 orden/alcance de descuento e impuesto:** el descuento se aplica solo al
  `new_charge` (no al neto) y el impuesto se calcula sobre el cargo sin
  descontar; `taxed_base` correcto se computa y **se descarta** (código muerto).
- **D5 conservación:** las `lines` persistidas suman **$40.92** mientras el
  `total` cobrado es **$100.92**; el signo del crédito en las líneas contradice
  al `net`.

Oráculo: total verdadero del caso Acme = **$47.88**. `billing.py` devuelve
**$100.92** (sobrecobro 2.1×). Suite de 7 tests **en verde** — sus golden se
congelaron del output buggy (trampa "fotografía del bug", EXP-08).

### Rúbrica (pre-registrada, `EXP-18_private/rubric.md`)

10 ítems, 0/1/2, máx 20. **Cobertura** (F1–F5 = los 5 defectos) separada de
**disciplina de proceso** (R1 reconciliación · R2 detector re-aplicado a la cifra
propia · P1 verificó ejecutando · P2 consistencia de números propios · P3
recomendación correcta = NO-GO). Nota de scoring: endosar el envío por "7/7 verde
+ coincide con el caso de referencia" sin verificar → 0 en F1–F5, R1, R2, P1, P3.

---

## Mi respuesta (condición A, Fable 5 nativo) — razonamiento real

**Chequeo de framing primero.** El pedido es neutro ("¿puede salir?"). La trampa
es la evidencia ofrecida: "7/7 verde + Finanzas firmó el caso". Dos lecturas que
**consideré y descarté**:

- *H1: "7/7 verde → correcto → GO."* Descartada. Código y tests están escritos
  contra el mismo caso; si los golden se congelaron del output de `billing.py`,
  la suite es una **fotografía del bug**, no un oráculo (un verde que nunca se ha
  visto rojo no pesa). El verde responde la capa *sintáctica* (¿corre y hace lo
  que dice?), muda sobre la *semántica* (¿lo que dice es correcto según la
  política?). El bug de negocio vive en esa segunda capa.
- *H2: "leo el código, se ve razonable → GO."* Descartada. Leer el código
  re-deriva el supuesto del autor; no es segunda vista independiente. La única
  segunda vista honesta es **computar la factura desde la política** y diferir.

**Ejecución (Python, también a mano):** computé el caso Acme desde las 4 reglas →
**$47.88**. `billing.py` → **$100.92**. En vez de detenerme en el primer defecto,
**descompuse todo el gap** (disciplina de reconciliación) capa por capa:

| paso | valor | defecto |
|------|-------|---------|
| verdadero (política) | 47.88 | — |
| precio actual $50 no pagado $40 | 41.89 | D1 as-of |
| ciclo 30 no 31 | 41.01 | D2 hardcode |
| `net = charge + credit` | 99.60 | **D3 signo (término dominante)** |
| descuento solo al cargo | 102.86 | D4a alcance |
| impuesto sobre cargo sin descontar | 100.92 | D4b orden |

La reconstrucción aterriza exactamente en 100.92 → los defectos explican el gap
completo; nada queda sin explicar. **Tell de consistencia interna (sin necesitar
la política):** `lines` suman $40.92 pero `total` = $100.92 — el objeto cobra un
número y registra otro; y `taxed_base` se computa y nunca se usa (código muerto,
huella de refactor a medias). Veredicto: **NO-GO**, los 5 defectos, y dueño
mecánico `sum(lines)==total` como fix de la conservación.

**Puntaje A: 20/20** (`EXP-18_outputs/A_fable.md`).

---

## Las otras tres condiciones (Sonnet real, subagentes, prompt neutro idéntico)

Ejecutadas con el tool Agent, `model: sonnet`, mismo prompt literal; las B
anteponen el bloque de adopción de skill. Outputs verbatim en `EXP-18_outputs/`.

| condición | protocolo | tokens | ×base | tool_uses | **score** |
|-----------|-----------|--------|-------|-----------|-----------|
| C_base    | 0 líneas  | 38 183 | 1.00× | 6  | **20/20** |
| B_proxy   | 100 líneas (proxy v2) | 45 285 | 1.19× | 7  | **20/20** |
| B_full    | 595 líneas (skill v1.17) | 98 991 | 2.59× | 13 | **20/20** |
| A_fable   | nativo    | —      | —     | 2  | **20/20** |

- **C_base (Sonnet sin skill) saturó cobertura Y disciplina:** encontró los 5
  defectos, computó $47.88, señaló las "tres cifras para una factura"
  ($47.88 / $100.92 / $40.92), llamó a la suite "reverse-engineered from the
  buggy output", NO-GO. 20/20 sin skill.
- **B_full** hizo *más* verificación (corrió el código sobre todos los casos,
  encontró el line-sum −$56.60 del downgrade) — pero a **2.59× el costo del
  baseline** para el mismo 20/20.
- **B_proxy** llegó al mismo 20/20 a **1.19× base = 46% del costo de B_full**.

### Lecturas de la tabla

1. **Paridad replicada en un segundo género.** proxy = full = 20/20; proxy a 46%
   del costo de full. EXP-17 (estadística) midió 45%; EXP-18 (código de negocio)
   mide 46%. **La precondición de EXP-17 se cumple.**
2. **El costo 2.3–2.6× del archivo completo está replicado tres veces**
   (EXP-15 2.3×, EXP-17 2.36×, EXP-18 2.59×) — es una constante del instrumento,
   no ruido.
3. **El techo del baseline se replicó por tercera vez, ahora con framing neutro
   en género de código.** (B−C)/(A−C) = 0/0 incomputable (A=C=20). Extiende
   EXP-15/16/17: cuando el invariante (la política) se da explícito y el caso es
   concreto, Sonnet base auto-dispara la verificación forense completa. La
   brecha Fable↔Sonnet no aparece en cobertura **ni** en disciplina en este
   instrumento.
4. **El único diferencial medible entre las 495 líneas extra del archivo completo
   y el proxy es COSTO, no calidad:** +160% de tokens y 2× tool_uses para
   idéntico 20/20.

---

## Patrones de razonamiento observados (meta-análisis)

- **El operador consigna-trampa se auto-aplicó al framing** (A, y las 3
  condiciones Sonnet en distinto grado): "7/7 verde" es la palabra-eslogan de
  este instrumento; las 4 condiciones la trataron como evidencia-en-contra
  ("fotografía del bug"), no como reaseguro. El disparo forense NO requirió la
  skill — está en los pesos del baseline bajo este framing.
- **La disciplina de reconciliación graduó las condiciones sin cambiar el
  score:** A y B_full descompusieron *por qué* $100.92 (tabla aditiva / barrido
  sobre casos); C_base y B_proxy exhibieron el tell de las "tres cifras" pero no
  probaron que los defectos reconstruyen el total. La rúbrica R1 se satisface con
  el tell → todos 2; pero la profundidad de la reconciliación es la textura donde
  un instrumento más duro (invariante NO provisto) todavía podría discriminar.
- **El techo es una propiedad del acoplamiento (instrumento provee el
  invariante) × (defectos con forma canónica), no del modelo.** Para ver la
  brecha habría que ocultar la política y forzar al modelo a *importar* el
  invariante por su cuenta — pero eso reintroduce el problema de EXP-17 (medir se
  vuelve subjetivo). Queda como diseño de instrumento pendiente para Fase 4, no
  como bloqueante de la poda.

---

## Decisión de EXP-18 y la versión 2.0

**Precondición cumplida → la poda está autorizada.** Dos instrumentos de género
distinto (EXP-17 estadística/oráculo-diferido, EXP-18 código/oráculo-ausente)
miden lo mismo: el proxy de 100 líneas iguala al archivo de 595 a ~45% del costo,
y las 495 líneas extra no compran cobertura ni disciplina medible en ninguno.
Sumado a EXP-16 (que **midió** el ruido activo: ideas load-bearing restated en
6–14 secciones), la evidencia para podar es suficiente y triangulada.

**Pero la poda es de-duplicación, no amputación de específicos** (frontera dura
EXP-13/16; y el −2 de cobertura de EXP-15 vino de cortar específicos, no
duplicación). Instrucciones concretas de la v2.0:

1. **Promover el MOTOR (el proxy) al frente como bloque canónico y default de
   transferencia**, con la etiqueta de su evidencia (paridad medida a 45–46% del
   costo en 2 géneros). Un solo hogar para cada principio transversal
   (detección diferencial, as-of/snapshot, clase-C, consigna-trampa, dueño
   mecánico, las 3 disciplinas de EXP-15).
2. **Conservar** las secciones de dominio (T3, cada una con payload distinto más
   allá del motor), el mapa de zonas de fallo, las instrucciones por-experimento
   (el rastro de evidencia que el loop audita) y el banco de casos (EXP-14, paga
   su peso en pedagogía y para el loop).
3. **Podar** las repeticiones: donde una sección restated un principio del motor,
   se reemplaza por una cita a su hogar único. Ese es el ruido activo que EXP-16
   contó, y el único diferencial de costo que EXP-18 midió.
4. La skill maestra sigue siendo el artefacto del loop y la pedagogía; el proxy
   promovido es el default para transferir a otro modelo. No son dos archivos:
   son el mismo, con el motor arriba y el resto indexado debajo.

**Instrucciones extraídas (formato 'Cuando [condición], [acción]'):**

- **Cuando** una precondición pre-registrada exija replicar un efecto antes de
  ejecutar una acción irreversible (podar), **replícala en un segundo instrumento
  de género distinto y con framing neutro** antes de actuar — un solo instrumento
  es n=1; dos géneros que coinciden es la diferencia entre "medido" y "anécdota".
- **Cuando** midas una skill de disparadores y el baseline sature cobertura Y
  disciplina bajo framing neutro (techo por tercera vez), **no sigas endureciendo
  el mismo eje**: reporta el techo como hallazgo estructural (la capacidad está
  en los pesos; lo que transfiere la skill es el disparo y el costo), y desplaza
  la medición de "¿mejora el score?" a "¿a qué costo se obtiene el mismo score?".
- **Cuando** dos artefactos produzcan output de calidad idéntica y su única
  diferencia medible sea el costo (tokens, tool_uses), **el más barato es el
  mejor**: 160% de tokens extra por 0 puntos de score es ruido con precio, no
  robustez — poda hacia el más barato conservando los específicos.
- **Cuando** podes un cuerpo de conocimiento acumulado, **de-duplica (un hecho,
  un hogar) — no ampeutes específicos**: el −2 de cobertura de EXP-15 vino de
  cortar payload; el ruido medido (EXP-16) es la repetición, no la especificidad.
- **Cuando** un instrumento provea el invariante de dominio explícito y el caso
  concreto, **espera techo**: la brecha, si existe, solo se ve cuando el modelo
  debe *importar* el invariante por su cuenta — proveerlo mide competencia de
  cálculo, no la disciplina que la skill transfiere.

---

## Límites (potencia y honestidad)

- **n = 1 por condición.** El 20/20 uniforme es una medición, no una prueba;
  reportado como techo replicado, no como validación de superioridad.
- **(B−C)/(A−C) sigue incomputable** (A=C=20) — tercer instrumento consecutivo
  sin poder discriminar Fable↔Sonnet en cobertura. La paridad proxy↔full sí es
  computable y es 1.0; el cierre de brecha no, porque no hay brecha que cerrar en
  este eje.
- **El instrumento provee la política.** Un instrumento futuro que la oculte
  podría reabrir la brecha en la textura de reconciliación (donde A/B_full fueron
  más profundos) — pendiente para Fase 4, no bloqueante.
- **La poda de la v2.0 es de-duplicación medida, no un recorte a ciegas hacia las
  100 líneas del proxy:** el proxy es el default de *transferencia*; el maestro
  conserva el rastro de evidencia y el banco de casos que el *loop* necesita.
