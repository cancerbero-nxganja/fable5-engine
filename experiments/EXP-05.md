# EXP-05 — Heurísticas internas para detectar cuando una solución es incorrecta

**Fecha:** 2026-07-14 18:10 UTC
**Modelo usado:** claude-fable-5
**Run número:** 5

## Pregunta / Prompt enviado a Fable 5

> Describe tus heurísticas internas para detectar cuando una solución es incorrecta. Muestra tu proceso real de razonamiento: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación epistémica

La pregunta pide "heurísticas **internas**". Tomada literal, es una pregunta de **clase D** (introspección del propio mecanismo, EXP-02): me pide reportar qué proceso interno ejecuto cuando "siento" que algo está mal. No tengo acceso fiable a ese mecanismo, y peor: la trampa de este experimento es que la respuesta ingenua —"tengo una sensación de duda y la sigo"— es exactamente la heurística que EXP-02 clase C ya demostró **no fiable**. Confabular un dato se siente igual que recordarlo; una solución incorrecta puede sentirse tan cierta como una correcta.

Reformulo a la versión respondible: **¿qué propiedades observables de una solución candidata predicen que es incorrecta, con independencia de cuán confiado me sienta al producirla?** El cambio de "internas" a "observables" no es cosmético — es el hallazgo central del experimento, y lo justifico en el Paso 1.

### Paso 1 — El descarte que define el experimento: la confianza no es un detector de error

Antes de listar heurísticas, tengo que matar la candidata obvia, porque si sobrevive, todo lo demás es decoración.

**Hipótesis 0 — "Mi heurística primaria es una señal interna de duda: cuando algo está mal, lo noto, y verifico eso."**

*Descartada, y es el descarte más importante de todo el run.* La evidencia acumulada la contradice de frente:
- EXP-02, clase C: la ausencia de sensación de duda no protege contra la confabulación. Los datos que invento se sienten idénticos a los que recuerdo.
- EXP-01: mi primera respuesta (suma = 1/4) se sentía correcta y elegante. No disparó duda. La mató un cálculo a mano, no una sensación.
- El detector de la skill ya lo dice sin sacar la conclusión: "código que funciona a la primera → sospechoso". Es decir, la *fluidez* correlaciona con el error tanto como con el acierto.

El corolario es incómodo pero es el eje del experimento: **si me apoyo en la duda para detectar errores, solo atrapo los errores que ya iba a atrapar de todas formas.** Los errores peligrosos —los que llegan a la respuesta— son precisamente los que *no* dispararon duda. Una heurística de detección que depende de sentir que algo va mal es ciega exactamente donde más la necesito.

Esto obliga a reorientar toda la pregunta: las heurísticas útiles no pueden ser introspectivas ("¿me siento seguro?"). Tienen que ser **estructurales**: propiedades de la solución o de la tarea que predicen error aunque la confianza sea máxima.

### Paso 2 — Segundo descarte: la lista de firmas de error no es la heurística

**Hipótesis 1 — "La heurística es un catálogo de señales de alarma conocidas: Sharpe > 5 → datos sintéticos; test que siempre pasa → no testea nada; métrica que salta en fecha redonda → cambio de definición."**

*Descartada como principio organizador, conservada como ejemplos.* Ese catálogo ya vive en el DETECTOR de la skill y es útil, pero no es una *heurística* — es una lista de instancias. No generaliza al error que no está en la lista, y el error que más me preocupa es justamente el que no anticipé. Un catálogo de síntomas no es un diagnóstico. Necesito el mecanismo que *genera* esas señales, para reconocer la señal número 50 que nadie escribió. Así que la pregunta se afila una vez más: **¿qué tienen en común "Sharpe > 5", "funciona a la primera", "número redondo", "test verde siempre" y "1/4"?** Todas son casos particulares de *algo*. Encontrar ese algo es el experimento.

### Paso 3 — La síntesis: el error es invisible desde un solo punto de vista

Puse las señales fiables que conozco en una fila y busqué la estructura común (materializar antes de argumentar — EXP-03):

| Señal de error | Qué se compara contra qué |
|---|---|
| Chequeo refutador barato (EXP-01) | valor de entrada ↔ valor recomputado |
| Doble vía independiente (EXP-01) | método analítico ↔ evaluación numérica |
| Escalera de artefactos (EXP-04) | "es señal del mundo" ↔ "es error de mi pipeline/datos" |
| Regla dura de clase C (EXP-02) | lo que "recuerdo" ↔ la fuente real |
| Oráculo ejecutable (EXP-03) | comportamiento producido ↔ ejemplo entrada→salida |
| "Demasiado limpio" (detector) | este resultado ↔ la tasa base de resultados así de limpios |
| Respuesta ↔ pregunta (scope) | lo que resolví ↔ lo que se pidió |

El patrón es único y lo confirmé con una demostración ejecutable (abajo): **cada señal fiable de error es un DESACUERDO entre dos estimaciones independientes de la misma cosa.** No hay ni una sola que sea monofuente. Y hay una razón por la que no puede haberla: una fuente única no puede detectar su propio error, porque el error ya está incorporado en lo que produce. Mi confianza es parte de esa fuente única — por eso no detecta nada. **El error solo se hace visible en el GAP entre dos vistas independientes del mismo objeto.**

Esto reescribe "heurística interna" como un oxímoron útil: no existe una señal interna monofuente de incorrección. Toda detección de error es **diferencial**. Lo que yo experimentaba como "intuición de que algo está mal" es, cuando es fiable, el momento en que dos representaciones que tenía en paralelo no cuadran; cuando es sensación pura sin segunda vista, no es fiable.

**Verificación ejecutable del principio** (clase A: no afirmo sin ejecutar). Tomé un caso donde la intuición fluida da una respuesta confiada y redonda, y una segunda vía la refuta — el problema del cumpleaños:

```
Vía 1 (intuición redonda, monofuente): 182   ("la mitad de 365")
Vía 2 (cálculo exacto): n mínimo con P>=0.5 = 23
P(colisión) con la respuesta intuitiva: 1.000000
GAP entre las dos vías: 159 personas
```

La Vía 1 no dispara duda —se siente obvia y es limpia (365/2)—. Lo que la delata no es una sensación sino el desacuerdo con la Vía 2, más el hecho de ser un número redondo derivado de un solo paso. El gap de 159 es enorme y aun así invisible desde dentro de la Vía 1. Este es el experimento en miniatura: **la fluidez alta y el resultado limpio son los dos disfraces del error, y ninguno se detecta sin una segunda vía.**

### Paso 4 — De principio a heurísticas operables

El principio diferencial genera las heurísticas concretas, cada una como "¿contra qué segunda vista comparo esta clase de afirmación?":

**H1 — Desajuste confianza↔clase de fallo (el disparador primario).** No verifico "cuando dudo"; verifico cuando la tarea cae en una clase de fallo predecible (A–G del mapa) *aunque no dude*. La señal no es la duda: es la coincidencia de fluidez alta con una tarea de clase A/B/C. Esa coincidencia es el reemplazo estructural de la duda. *(Deriva de matar la Hipótesis 0.)*

**H2 — Resultado demasiado limpio ↔ tasa base.** Número redondo, fórmula elegante, "funciona a la primera", taxonomía que particiona perfecto, migración sin efectos. Comparo el resultado contra "¿con qué frecuencia un problema real sale así de limpio?". Casi nunca. La limpieza es evidencia *contra* la corrección hasta que sobrevive una segunda vía. *(EXP-02/03/04: mis propios outputs limpios se sometieron al detector; el cumpleaños lo confirma.)*

**H3 — Respuesta ↔ pregunta (deriva de alcance).** El modo de error más silencioso: resuelvo competentemente una versión ligeramente distinta de lo que se pidió. Segunda vista: releer la pregunta literal y verificar que mi salida responde *esa* y no la vecina más fácil. *(Conecta con EXP-03: "resolver el problema equivocado con excelencia".)*

**H4 — Doble vía obligatoria para lo que carga peso.** Para la afirmación de la que depende toda la respuesta, genero una segunda estimación por un camino independiente y busco el gap. Cuál es la segunda vía depende del tipo: recomputar a mano (matemática), ejecutar contra un ejemplo (código), la escalera de artefactos (datos), la fuente real (dato de clase C). *(EXP-01 dual-path, generalizado.)*

**H5 — La refutación saltada se siente igual que la refutación pasada.** Esta es sutil y crítica. Desde dentro, "no intenté romperlo" y "lo intenté romper y aguantó" producen la misma sensación de confianza. Por eso no puedo confiar en el recuerdo de haber verificado; tengo que rastrear si *ejecuté* el chequeo, no si *siento* que está bien. La heurística operable: antes de emitir, la pregunta no es "¿estoy seguro?" sino "¿qué chequeo refutador concreto corrí, y qué devolvió?". Si la respuesta es "ninguno", la confianza es infundada por construcción. *(Corolario directo de matar la Hipótesis 0.)*

### Paso 5 — Falsificación de la propia síntesis

El principio "toda detección de error es diferencial" es limpio → sospechoso por su propio detector (H2). Busco el caso que no encaje:

- **¿Y si no hay segunda vía disponible?** (Juicio de diseño, gusto, una afirmación sin oráculo ni fuente.) Contraejemplo real: "esta API es más elegante que aquella". No hay recomputación posible. *Refinamiento local, no reescritura:* cuando falta la segunda vía, el principio no se rompe, se degrada a su forma honesta — **bajar la confianza reportada al nivel de "sin segunda vía disponible"** y marcarlo como juicio, no como hecho. La ausencia de vía diferencial no autoriza confianza alta; la prohíbe. El principio sobrevive porque predice exactamente esto: sin gap medible, no hay derecho a certeza.
- **¿Y el costo?** Generar una segunda vía para *cada* afirmación es caro e imposible. Por eso H1 es el disparador: la doble vía (H4) se gasta solo donde la clase de fallo o el peso de la afirmación lo justifican. El detector es un **router de triage**, no un "verifica todo". Sin este refinamiento, el principio sería correcto e inaplicable. *(Misma degradación por valor marginal que EXP-03/04.)*
- **¿Y si las dos vías comparten el mismo error?** Contraejemplo: recomputo con el mismo supuesto falso y ambas coinciden — falso acuerdo. Frontera porosa documentada: la segunda vía solo vale si es **independiente en su supuesto**, no solo en su cálculo. La independencia real es la que captura el error; dos vías correlacionadas dan una falsa sensación de verificación (es el mismo peligro que un test que "siempre pasa" porque testea lo que el código ya asume).

La síntesis sobrevive con dos refinamientos: (a) sin segunda vía → prohibición de confianza alta, no permiso; (b) el detector es triage disparado por clase de fallo/peso, no verificación universal.

### Conclusión

No tengo una heurística interna de incorrección, y creer que la tengo es el error de calibración más peligroso que puedo cometer, porque la sensación de certeza acompaña por igual al acierto y a la confabulación. Lo que tengo —y lo que la skill debe codificar— es un **principio diferencial**: una solución es sospechosa de incorrecta en la medida en que no puedo exhibir una **segunda estimación independiente** que concuerde con ella. Todas las señales concretas (chequeo refutador, doble vía, escalera de artefactos, regla de clase C, "demasiado limpio", deriva de alcance) son instancias de buscar el gap entre dos vistas. Las heurísticas operables son: verificar por desajuste confianza↔clase-de-fallo (no por duda), tratar la limpieza como evidencia en contra, comparar respuesta contra pregunta, exigir doble vía independiente en lo que carga peso, y —lo más importante— rastrear **si corrí el refutador**, no si me siento seguro, porque la refutación saltada y la refutación pasada son indistinguibles desde dentro. Donde no hay segunda vía posible, la conclusión correcta no es confiar: es reportar el juicio como juicio.

## Patrones de razonamiento observados

1. **El descarte central es introspectivo-negativo.** El experimento avanza matando la respuesta ingenua ("sigo mi duda") con evidencia dura de runs previos (clase C, el 1/4 de EXP-01). Reconocer que la propia confianza es la fuente no fiable es el movimiento que desbloquea todo lo demás.
2. **Búsqueda de invariante sobre casos conocidos.** En vez de listar más señales de alarma, puso las señales fiables en una tabla y buscó qué comparten. El resultado —"todas son un desacuerdo entre dos vistas"— es una compresión, no una enumeración. Mismo movimiento que EXP-02 (clases de fallo) y EXP-04 (asimetría estructural del dominio).
3. **Verificación ejecutable de la tesis introspectiva.** La afirmación "la fluidez disfraza el error" no se dejó como retórica: se instanció en el problema del cumpleaños con código (intuición redonda 182 vs. exacto 23), obedeciendo la regla de clase A incluso para una tesis sobre uno mismo.
4. **Falsificación que refina, no reescribe.** El caso "no hay segunda vía" no tumbó el principio: lo forzó a su forma honesta (sin gap medible → prohibición de confianza alta). El patrón contraejemplo → refinamiento local → frontera documentada es invariante en EXP-01/02/03/04/05.
5. **Meta-honestidad como resultado, no como disclaimer.** La respuesta a "describe tu heurística interna" es "no tengo una, y esa es la respuesta útil". Reformular clase D hacia lo observable produjo un hallazgo más fuerte que cualquier fabricación de mecanismo.
6. **Distinción entre saltar y pasar un chequeo.** El insight de que "no verifiqué" y "verifiqué y aguantó" son indistinguibles desde dentro convierte la verificación de una sensación en un hecho rastreable (¿qué corrí, qué devolvió?). Es la traducción operable de la meta-honestidad.

## Extracción para la skill

Instrucciones en formato accionable, con evidencia real de EXP-05:

- Cuando vayas a emitir una solución, no preguntes "¿me siento seguro?" sino "¿qué segunda vista independiente concuerda con esto?" — la confianza es parte de la fuente única que produjo la solución y no puede detectar su propio error (EXP-05: intuición del cumpleaños 182 vs. exacto 23, gap invisible desde dentro).
- Cuando produzcas una afirmación que carga el peso de la respuesta, genera una segunda estimación por un camino independiente en su supuesto (no solo en su cálculo) y busca el desacuerdo; dos vías que comparten el supuesto falso dan un falso acuerdo.
- Cuando la tarea caiga en una clase de fallo predecible (A–G) verifica aunque NO sientas duda — el disparador es el desajuste confianza↔clase-de-fallo, no la sensación de duda, porque la confabulación y el acierto se sienten idénticos (EXP-02 clase C, confirmado en EXP-05).
- Cuando un resultado sea limpio, redondo, elegante o "funcione a la primera", trátalo como evidencia EN CONTRA de la corrección hasta que sobreviva una segunda vía — comparar contra la tasa base: los problemas reales casi nunca salen así de limpios.
- Cuando termines una solución, compárala contra la pregunta literal releída, no contra la pregunta que recuerdas — el error más silencioso es resolver con excelencia una versión ligeramente distinta de lo que se pidió.
- Cuando estés por confiar en que "ya verifiqué", rastrea qué chequeo refutador concreto corriste y qué devolvió; si la respuesta es "ninguno", la confianza es infundada por construcción — saltar el refutador y pasar el refutador son indistinguibles desde dentro.
- Cuando no exista una segunda vía posible (juicio de diseño, gusto, afirmación sin oráculo ni fuente), no eleves la confianza: repórtalo como juicio marcado, porque la ausencia de vía diferencial prohíbe la certeza, no la autoriza.

## Impacto en la skill

Se elevó el DETECTOR DE RESULTADOS SOSPECHOSOS de "lista de casos" a **principio diferencial**: toda detección de error es la búsqueda de un desacuerdo entre dos estimaciones independientes; no existe señal interna monofuente de incorrección. Se agregó la sección "Heurísticas de detección de error (EXP-05)" en INSTRUCCIONES APRENDIDAS con las siete instrucciones extraídas. Se reforzó el Paso 4 del protocolo con la distinción saltar↔pasar el refutador (rastrear qué se ejecutó, no qué se siente) y con el disparador confianza↔clase-de-fallo como reemplazo estructural de la duda. Se añadió a CALIBRACIÓN la regla "sin segunda vía → prohibición de confianza alta, no permiso". Los casos sueltos del detector (Sharpe > 5, funciona a la primera, número redondo) quedan re-enmarcados como instancias del principio diferencial, no como reglas independientes.
