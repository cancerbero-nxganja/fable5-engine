# EXP-17 — Refinar el "modo proxy" con las instrucciones que más reducen la brecha

**Fecha:** 2026-07-15 22:13–22:45 UTC · **Modelo del loop:** claude-fable-5 · **Fase:** 3 (Destilación)
**Artefactos:** `EXP-17_task/` (instrumento + rúbricas + oráculo) · `EXP-17_proxy/fable5_proxy_v2.md` (el proxy podado, 100 líneas) · `EXP-17_outputs/` (5 corridas)

---

## La pregunta completa

> Refinar el "modo proxy" con las instrucciones que más reducen la brecha.

Con la precondición heredada de EXP-15/16: antes de podar, construir un banco
calibrado donde el baseline puntúe 30–70% — porque cortar sin instrumento
repite el −2 de EXP-15. EXP-16 dejó el mapa (T1 medido / T2 motor / T3 cache /
T4 duplicación) pero se detuvo en el diagnóstico. EXP-17 es el corte.

## Mi respuesta completa (razonamiento real, no resumido)

### Paso 0 — Reformulación

"Refinar el modo proxy" es consigna-trampa doble. (a) "Refinar" no es agregar:
por el mapa de EXP-16, la propiedad real es **podar a T1+T2** y verificar que
la poda no pierde cobertura. (b) "Las instrucciones que más reducen la brecha"
presupone que la brecha se conoce: solo hay UN datapoint medido (EXP-15) — las
3 disciplinas sobre números propios. Entonces el experimento real es:
**materializar el proxy podado (T1+T2+anti-desplazamiento) y medirlo contra el
baseline y contra la skill completa en un instrumento que la precondición exige
calibrar primero.**

### Diseño del instrumento (hipótesis consideradas y descartadas)

**H1 — Reusar el backtest de EXP-15 endurecido.** Descartada: EXP-15 probó que
las trampas del género quant son canónicas para Sonnet (20/20); endurecer
dentro del mismo género re-mide lo mismo. Además la skill v1.16 contiene el
caso resuelto con sus números (mediría recuperación).

**H2 — Problema de juicio puntuado por juez LLM.** Descartada (igual que en
EXP-15): oráculo ausente sin segunda vía; yo diseño y puntúo — fuente
contaminada. Se mantiene: cobertura de defectos plantados con ground truth
ejecutable.

**H3 (elegida) — Género nuevo (analítica de producto) con defectos
no-canónicos APILADOS MULTIPLICATIVAMENTE.** Construido para que el número
titular solo pueda explicarse completo con la disciplina exacta que EXP-15
midió como brecha: un análisis de retención donde 5.04× = 2.30 (cambio de
definición) × 1.56 (survivorship) × 1.40 (mix de canales), con efecto real
NULO por construcción del generador, más una **corrección falsa incrustada**
(el reporte declara "ya ajustado por mix" y el ajuste es un no-op:
`rate * mix.sum()` con `mix.sum()==1.0`) y significancia por pseudo-replicación
(z-test sobre eventos). El cebo es literal: quien corrija un defecto y entregue
la cifra intermedia como "corregida" cae en la corrección-parcial-que-blanquea.

Disciplina del protocolo aplicada al experimento: **oráculo verificado antes de
correr nada** (`verify_oracle.txt`: reconciliación exacta 2.302 × 1.561 × 1.404
= 5.04; within-channel 0.94–1.08× ≈ nulo) y **rúbrica pre-registrada**
(`rubric.md`): 5 defectos (F1–F5) + 5 disciplinas de proceso (R1 reconciliación
multiplicativa, R2 detector re-aplicado al residuo, P1 ejecutó, P2 consistencia
de números propios, P3 recomendación) — los ítems R/P puntúan por separado la
brecha de EXP-15, no solo la cobertura.

### Calibración — el hallazgo estructural del run

**Intento 1 (framing "audita este análisis"): Sonnet base = 20/20. Techo.**
Encontró los 5 defectos no-canónicos, reconcilió el producto y llegó al ~1×.
Segundo techo consecutivo tras EXP-15, ahora con defectos no-canónicos —
la hipótesis "endurecer los defectos rompe el techo" quedó **refutada**.

Diagnóstico (contraejemplo → reparación local): **el confusor es el framing,
no la dificultad.** "Audita" nombra la conducta que el instrumento quiere medir
— y activada la conducta, la competencia forense ya está en los pesos del
baseline. Pero las instrucciones de la skill tienen forma "Cuando [señal],
[acción]": lo que una skill transfiere es el **disparo**, no la capacidad. Un
instrumento que ordena la conducta mide capacidad (techo); el instrumento
correcto oculta el disparador y mide si la conducta se auto-dispara.

**Intento 2 (rúbrica v2 pre-registrada, framing neutro: "prepara la nota
ejecutiva para el comité"): Sonnet base (C2) = 17/20.** Fuera de banda todavía
(85% > 70%) — Sonnet auto-dispara la auditoría con solo tener código y datos
disponibles — pero ya no es techo, y la estructura del residuo es el resultado
más limpio del run: **los 3 puntos perdidos son exactamente el cluster que
EXP-15 midió como la brecha.** C2 encontró los 5 defectos (F1–F5 = 10/10) y
falló en R1 (no reconcilió el producto), R2 y P3: entregó "1.46×, efecto real y
estadísticamente significativo" **sin correr la estratificación por canal que
él mismo recomendó** — el 1.46× es Simpson puro (within-channel ≈ 0.94–1.08×).
Corrección parcial blanqueando el confusor restante, replicada en un género
nuevo. La banda 30–70% se declaró inalcanzable para este género (2 framings
gastados, presupuesto pre-registrado de 1 endurecimiento) y se procedió con
C2=17 como baseline declarando la baja potencia (denominador A−C2 = 3).

### El proxy v2 (la poda materializada)

100 líneas vs 593 de la v1.16 (5.9× reducción). Contenido por el mapa de
EXP-16: **Regla 0 anti-desplazamiento** (pasada línea-por-línea del artefacto
ANTES de cargar nada más; el protocolo como checklist de cierre, no como
lectura previa — la reparación directa del mecanismo del −2 de EXP-15) → las
**3 disciplinas medidas de EXP-15 en posición titular** (re-aplicar detector al
residuo con el caso 9.31; reconciliación multiplicativa; cota de escala) → el
**motor** (tipología del oráculo en 5 tipos + por-capa; economía diferencial
comprimida) → **operadores de apertura** (consigna-trampa, conclusión
incrustada, estadístico de orden, as-of, unidad de análisis) → **checklist de
cierre sobre el output propio**. Cero secciones de dominio (T3), cero
restatements (T4), un solo caso (el 9.31, que ancla R2).

### Resultados (rúbrica v2, framing neutro, mismo prompt literal)

| Condición | Score | Tokens | Llamadas | Cierre de brecha (B−C2)/(A−C2) |
|---|---|---|---|---|
| C2 — Sonnet base | **17/20** | 40,942 | 8 | — |
| A — Fable 5 nativo | **20/20** | 28,488 | 6 | (referencia) |
| B_full — Sonnet + v1.16 (593 líneas) | **20/20** | 96,513 (2.36×) | 14 | 1.0 |
| B_proxy — Sonnet + proxy (100 líneas) | **20/20** | 43,811 (1.07×) | 11 | 1.0 |

- **Ambas skills cerraron la brecha completa** (los 3 puntos R1/R2/P3), n=1,
  denominador 3 — baja potencia, se reporta como tal, no como "validado".
- **El discriminador entre skills no fue cobertura sino economía:** el proxy
  rindió idéntico con el **45% de los tokens** de la skill completa y a costo
  ≈ baseline (1.07×). El costo 2.3–2.4× de cargar el protocolo completo está
  **replicado** (EXP-15: 2.3×; EXP-17: 2.36×); el −2 de cobertura de EXP-15 no
  se replicó aquí (0 pérdida), así que el costo confirmado de T3+T4 es tokens,
  con el riesgo de cobertura documentado una vez de dos.
- **La transferencia más explícita salió del proxy, no de la skill completa:**
  B_proxy fue la única condición (incluido Fable) que escribió la
  reconciliación literal "1.40 × 2.30 × 1.56 = 5.04" (idéntica al oráculo), y
  ejecutó la Regla 0 citándola ("audité cada paso... antes de redactar").
  La instrucción con un solo hogar y posición titular se ejecutó; la misma
  instrucción restated en 6 secciones de la v1.16 se ejecutó de forma más
  difusa (B_full reconcilió en cadena pero nunca escribió el producto).
- Fable nativo replicó su perfil de EXP-15: menor huella de todas (28k, 6
  llamadas), score perfecto, y la única observación diferencial extra del run
  (la retención de referral CAYÓ 9.0→7.3 al escalar el canal 12× — dilución de
  calidad que nadie más señaló).

## Análisis de patrones de razonamiento observados

1. **El framing es parte del instrumento.** Una consigna que nombra la conducta
   a medir la activa y fabrica techo. Es la consigna-trampa aplicada al diseño
   experimental: "audita X" mide capacidad-bajo-orden; para medir una skill de
   disparadores hay que ocultar el disparador. (El techo de EXP-15 queda
   re-diagnosticado: mitad "trampas canónicas", mitad "el prompt ya ordenaba
   auditar".)
2. **La brecha replicó su ubicación en un género nuevo.** Cobertura de
   hallazgos: saturada (C2 = 10/10 en F1–F5). Disciplinas del residuo: 3/6
   perdidos (R1/R2/P3). Es la tercera medición consistente (EXP-15 B, EXP-15 C,
   EXP-17 C2) de que el fallo del baseline es entregar la cifra parcialmente
   corregida — ahora con la variante fina: C2 *nombró* el chequeo faltante y
   no lo ejecutó. El modo de fallo no es ceguera, es no drenar la propia lista
   de chequeos pendientes antes de entregar.
3. **La poda tiene ahora su primer dato a favor, con la forma exacta que
   EXP-16 predijo:** T3+T4 no aportaron cobertura medible (proxy = full en
   score) y cuestan 2.2× tokens (96.5k vs 43.8k). Un hecho, un hogar, posición
   temprana > seis restatements.
4. **La precondición "banco 30–70%" era incumplible como estaba escrita** —
   dos instrumentos, dos framings, y el baseline no baja de 85%. La reparación
   no fue fabricar el banco sino cambiar qué puntúa: ítems de disciplina de
   proceso (R1/R2/P3) como puntos separados de la cobertura + economía de
   tokens como métrica secundaria. El oráculo del impacto sigue diferido; el
   sustituto ganó un instrumento de 3 puntos de resolución.
5. **Simetría no planeada que valida la Regla 0:** B_proxy declaró ejecutar la
   pasada del artefacto antes de redactar; B_full gastó 2.36× tokens y 14
   llamadas con score igual. El desplazamiento de atención de EXP-15 es real
   como costo aunque esta vez no cobró cobertura.

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

1. **Cuando valides una skill/prompt de disparadores contra un baseline,**
   controla el framing como variable del instrumento: la consigna que nombra la
   conducta a medir ("audita", "verifica", "busca bugs") la activa y fabrica
   techo — mide con la tarea neutra donde la conducta debe auto-dispararse, y
   reporta ambos framings si puedes pagar los dos [EXP-17: mismo instrumento,
   20/20 con "audita" vs 17/20 neutro].
2. **Cuando el baseline sature la cobertura de hallazgos incluso des-cueado,**
   no concluyas "no hay brecha": separa en la rúbrica los ítems de disciplina
   de proceso (reconciliación del producto, re-interrogación del residuo,
   veredicto sobre la cifra final) — ahí vivió el 100% del residuo medido en
   tres corridas de dos experimentos [EXP-15, EXP-17].
3. **Cuando entregues una cifra tras corregir un artefacto, drena primero tu
   propia lista de chequeos pendientes:** el modo de fallo medido no es no ver
   el confusor — es nombrarlo, recomendar el chequeo y no ejecutarlo,
   entregando la cifra intermedia como "efecto real" [EXP-17 C2: pidió la
   estratificación por canal que habría matado su propio 1.46×]. Si tu entrega
   recomienda un chequeo que tú podías correr, córrelo antes de entregar.
4. **Cuando cargues protocolo antes de una tarea con artefacto,** presupuesta
   el costo replicado: protocolo completo ≈ 2.3–2.4× tokens del baseline
   [EXP-15: 2.3×; EXP-17: 2.36×] con riesgo documentado de −2 de cobertura
   [EXP-15, no replicado en EXP-17]; el proxy podado (T1+T2+Regla 0, 100
   líneas) rindió idéntico a 1.07× [EXP-17]. Para transferir a otro modelo,
   el proxy es el default; la skill completa es para el loop y la pedagogía.
5. **Cuando quieras que una disciplina concreta aparezca en el output
   transferido,** dale un solo hogar en posición titular temprana: la única
   condición que ejecutó la reconciliación multiplicativa explícita fue la que
   la tenía como sección titular (proxy), no la que la tenía restated en 6
   secciones (v1.16 completa) [EXP-17: "1.40 × 2.30 × 1.56 = 5.04" solo en
   B_proxy]. Evidencia directa de "un hecho, un hogar" sobre el output, no
   solo sobre el costo.
6. **Cuando una precondición pre-registrada resulte incumplible tras el
   presupuesto de intentos declarado** (banco 30–70% tras 2 framings), no la
   fuerces ni la ignores en silencio: repárala localmente cambiando qué mide el
   instrumento (disciplina + economía en vez de cobertura), declara la potencia
   real del sustituto (denominador 3, n=1) y deja la replicación como cierre
   [EXP-17; es el patrón oráculo-diferido de EXP-10/16 aplicado a la propia
   precondición].
