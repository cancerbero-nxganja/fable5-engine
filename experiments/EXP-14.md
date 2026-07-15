# EXP-14 — Agregar ejemplos concretos extraídos de los experimentos anteriores

**Fecha:** 2026-07-15 16:13 UTC
**Modelo usado:** claude-fable-5
**Run número:** 14
**Fase:** FASE 3 (Destilación a la skill)

## Pregunta / Prompt enviado a Fable 5

> Agrega a la skill ejemplos concretos extraídos de los experimentos anteriores. Muestra tu razonamiento real: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la forma final. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Reformulación: "agregar ejemplos" es consigna-trampa

Antes de tocar nada corro el detector de consigna-trampa (EXP-13) sobre la propia consigna, porque "agregar ejemplos" tiene exactamente la forma sospechosa: nombra una acción de superficie (añadir ilustraciones) donde la propiedad que importa vive un nivel abajo. ¿Cuál es la propiedad real?

La respuesta ya estaba en la skill, escrita por EXP-03 para otro contexto: *"cuando una especificación en prosa admita dos lecturas, ciérrala con un ejemplo concreto entrada→salida en vez de con más prosa — toda prosa de especificación deja semántica de frontera abierta; un par literal la cierra."* La skill **es** una especificación en prosa (unas ~100 instrucciones "Cuando X, haz Y") transferida a un modelo que no comparte mis internals. Cada instrucción admite lecturas divergentes. Por lo tanto la propiedad real de EXP-14 no es "decorar con ejemplos" sino **cerrar la semántica de frontera de las instrucciones — el ejemplo es el oráculo de la instrucción**, igual que el par entrada→salida es el oráculo de una tarea de código delegada.

Esto conecta con el criterio de éxito #2 del roadmap ("ejemplos reales extraídos de experimentos, no hipotéticos"): la palabra decisiva es *reales*. Un ejemplo hipotético lo inventa la misma fuente que escribió la instrucción — comparte su supuesto, es una segunda cuenta y no una segunda vista (EXP-05). Un caso real ejecutado en un experimento es una observación independiente: ahí la instrucción ya corrió contra el mundo y se puede citar qué devolvió.

### Paso 1 — Qué transfiere un ejemplo (y qué no): el error tiene que estar dentro

Segunda pregunta antes de diseñar: ¿qué hace que un ejemplo transfiera procedimiento y no solo apariencia? Reviso los casos que los experimentos produjeron y encuentro una asimetría nítida:

- El caso de EXP-01 no es "la suma vale 3/8". Es: *la primera conclusión fue 1/4, se sentía correcta, y dos términos sumados a mano la mataron antes de declararla*. El valor pedagógico está en el error refutado, no en la respuesta.
- El caso de EXP-05 no es "la respuesta es 23". Es el gap de 159 entre la vía fluida (182) y la exacta (23), invisible desde dentro de la primera.
- El caso de EXP-09 no es el esquema final. Es el esquema BCNF "perfecto" cuyo total de marzo muta a $24.00 cuando el precio sube en junio.

Generalización: **un ejemplo sin el error incluido muestra qué es el éxito; un ejemplo con la lectura ingenua ejecutada y refutada muestra qué previene la instrucción** — y eso es lo único que discrimina entre las dos lecturas de la prosa. El criterio de admisión al banco queda fijado: solo casos con la forma *situación → lectura ingenua y su output → refutación → output correcto*, con los números reales del experimento.

### Paso 2 — Hipótesis de colocación, consideradas y descartadas

**H1 — Apéndice "EJEMPLOS" al final, uno por experimento.** Descartada por materialización contra la evidencia de EXP-02: la zona de fallo de "recuperación enterrada" — un modelo ejecutando la instrucción del Paso 4 no va a saltar a un apéndice desconectado; la probabilidad de que el ejemplo se use depende del acoplamiento disparador→ejemplo. Un apéndice plano es un catálogo sin índice: exactamente la forma que EXP-06 descartó ("el catálogo no cierra ningún gap").

**H2 — Un ejemplo inline después de cada instrucción (~100 instrucciones).** Descartada por la economía de EXP-12: la skill mide ~103KB; ejemplificar cada instrucción la duplicaría o triplicaría, y el 43× medido enseña que el sobre-uso de contexto **fabrica** la zona de fallo de recuperación enterrada que pretendía prevenir. Además viola el triage de EXP-11 aplicado hacia adentro: la mayoría de las instrucciones tienen lectura única o barata de equivocar — un ejemplo ahí es contexto muerto que ninguna decisión consume.

**H3 — Reescribir las instrucciones para que "contengan" sus ejemplos.** Descartada al materializarla: las instrucciones ya contienen alusiones comprimidas ("182 vs 23", "43×", "P=0.82"). El problema es que la alusión solo funciona para quien ya conoce el caso — que es exactamente quien no necesita la skill. Inflar cada alusión a caso completo es H2 con otro nombre.

**H4 (elegida) — Banco de casos canónicos indexado por la clave de citación existente.** La observación que la desbloquea: la skill ya tiene un sistema de citación uniforme — prácticamente toda instrucción termina en `(EXP-XX)` o `[CALC-N, EXP-XX]`. Ese tag ya es un puntero; solo le falta un destino resoluble. Un banco de casos **keyed por EXP-ID** convierte cada cita existente en un índice sin editar ni una instrucción: el modelo que lee "verifica que g(n)=f(n+1)… (EXP-01)" resuelve a CASO EXP-01 y ve la traza real 1/4→refutación→3/8. Es la forma de EXP-13 ("indexar y nombrar, no borrar ni acretar") aplicada a la pedagogía, y respeta "un hecho, un hogar" (EXP-09): el caso completo vive una vez; las alusiones son punteros.

### Paso 3 — Selección: triage de casos por divergencia × costo

No todos los experimentos aportan un caso admisible. Criterios: (a) real y verbatim del archivo del experimento, (b) con el error ejecutado dentro, (c) cierra una frontera de lectura de instrucciones muy citadas. Seleccionados 11 (10 IDs, EXP-08 aporta dos porque sus dos casos cierran fronteras distintas):

| Caso | Error incluido | Frontera que cierra |
|---|---|---|
| EXP-01 | suma=1/4 declarable, refutada con 0.3>0.25 | "refuta ANTES de concluir"; contraejemplo=diagnóstico |
| EXP-04 | afirmación estadística como opinión | clase A disfrazada: P=0.82→1.0 medida en 30s |
| EXP-05 | 182 confiado vs 23 exacto (gap 159) | no hay señal monofuente; detección diferencial |
| EXP-06 | dos reglas propias en órdenes opuestas | "derivable" es propiedad temporal; snapshot≠duplicación |
| EXP-07 | RSI computado y ejecutado al mismo close | as-of por tiempo de conocimiento; deflación mejor-de-N |
| EXP-08 | $70 vs $30 (signo); $98.00 vs $97.20 (orden) | el valor esperado viene de fuente externa al código |
| EXP-08b | $1.60 vs $1.61 según reparto | conservación adjudica el choque redondeo/snapshot |
| EXP-09 | orden de marzo que pasa de $20.00 a $24.00 | "sin redundancia" literal = bug; frontera as-of genera tablas |
| EXP-10 | p<0.05 leído como 5% cuando el real es 18% | la propiedad vive en el procedimiento, se simula |
| EXP-11 | "está claro" → 864 lecturas, 16.8% de acierto | el ejemplo caminado, no la relectura, encuentra la omisión |
| EXP-12 | archivo entero (43×) y orden natural (1.97×) | la optimalidad es de la economía de la afirmación |

Excluidos y por qué: EXP-02 (su output es la taxonomía A–G misma, ya estructural en la skill; su "caso" son las clases, no una traza con error único), EXP-03 (su payload es la plantilla de delegación, ya presente como plantilla; su evidencia de firma-confabulada quedó absorbida en clase C), EXP-13 (su caso es la propia reescritura de la skill — autorreferente, sin entrada→salida citable). Criterio: el banco no es un resumen de los experimentos, es el cierre de fronteras de lectura.

### Paso 4 — Falsificación del propio diseño

1. **¿El banco es un "catálogo" del tipo que EXP-06 descartó?** No — lo descartado era el catálogo de conocimiento que el otro modelo ya tiene (SOLID, CAP). Estas trazas el otro modelo *no* las tiene, y cada una viene acoplada a un procedimiento por la clave de citación. Test de transferibilidad por caso: ¿un modelo sin mis internals puede ejecutar la jugada tras leer la traza? Caminado con CASO EXP-09: la traza da el esquema literal, el UPDATE literal y el output mutado — el modelo puede re-ejecutar el refutador sobre cualquier esquema nuevo ("sube el precio después del evento y mira si el pasado muta"). Pasa.
2. **¿Redundancia con las alusiones inline existentes?** Es exactamente la clase 3 de EXP-09 (copia gobernada): la alusión es el puntero, el banco es el hogar, y la convención de índice (declarada en el NÚCLEO) es el dueño mecánico de la relación. No se editó ninguna instrucción — cero churn, cero riesgo de romper lo que ya funciona.
3. **¿Tamaño?** +10.4KB sobre 103KB (~10%), contra el 2-3× de H2. Once casos ≤ 15 líneas cada uno. El triage dejó fuera lo que no cierra fronteras.
4. **Deriva de alcance releída contra la consigna literal:** "agregar ejemplos concretos extraídos de los experimentos anteriores" — se agregaron (banco nuevo), concretos (números y código literales), extraídos de los experimentos (verbatim de experiments/EXP-XX.md, ninguno inventado). Sin borrar nada (eso es EXP-16). Cumple.

### Conclusión

EXP-14 ejecutado como instancia de la propia skill: la consigna se reformuló (ejemplos = oráculos de las instrucciones), el diseño se eligió por materialización y descarte (apéndice, inline exhaustivo, inflado de alusiones → banco indexado por la clave de citación existente), el criterio de admisión quedó fijado por la evidencia (solo casos con el error ejecutado dentro), y el resultado se falsificó contra el test de transferibilidad y la economía de contexto antes de escribirse.

## Patrones de razonamiento observados

1. **La consigna del roadmap también pasa por el detector de consigna-trampa** — quinta instancia medida ("agregar ejemplos" → cerrar semántica de frontera), confirmando que el operador es transversal incluso sobre las meta-tareas del propio loop.
2. **El ejemplo que transfiere es el que contiene el error refutado** — el par entrada→salida de EXP-03 se refina: para transferir *procedimiento de detección*, el par debe ser (lectura ingenua ejecutada → refutación → corrección), no (entrada → salida correcta).
3. **Indexar por la clave de citación existente** — la infraestructura de punteros ya estaba en la skill (las citas EXP-XX); el diseño barato no crea un sistema nuevo, resuelve el que existe. Cero ediciones sobre las instrucciones = cero riesgo de regresión.
4. **Triage de ejemplos = triage de preguntas de EXP-11 hacia adentro** — solo gana ejemplo la instrucción cuyas lecturas divergen en decisiones caras; ejemplificar lectura única es contexto muerto.
5. **"Un hecho, un hogar" aplicado a pedagogía** — alusión comprimida como puntero, caso completo con hogar único; la relación alusión↔caso tiene dueño declarado (la convención de índice en el NÚCLEO).

## Instrucciones extraídas (formato "Cuando [condición], [acción concreta].")

- Cuando transfieras una instrucción procedimental, adjunta el caso real con el error incluido (situación → lectura ingenua y su output → refutación → output correcto): el ejemplo sin el fallo no discrimina entre las dos lecturas de la prosa.
- Cuando un cuerpo de instrucciones cite casos por alusión comprimida, dale a cada caso un hogar único y completo y convierte las alusiones en punteros — la alusión solo funciona para quien ya conoce el caso, que es quien no necesita la skill.
- Cuando decidas dónde colocar ejemplos en un artefacto de transferencia, indexa el banco por la clave de citación que el texto ya usa: ni apéndice desconectado (recuperación enterrada) ni inline exhaustivo (43× de contexto).
- Cuando selecciones qué ejemplos incluir, haz triage por divergencia de lecturas × costo de la lectura equivocada; un ejemplo para una instrucción de lectura única es contexto muerto.

## Impacto en la skill

- v1.13 → v1.14.
- Nueva sección de primera clase **"CASOS CANÓNICOS — banco de ejemplos reales (EXP-14)"** antes de `# TAREA`: 11 casos verbatim de los experimentos, formato fijo con el error incluido, indexados por EXP-ID.
- **Convención de índice** declarada en el NÚCLEO DESTILADO: toda cita `(EXP-XX)` resuelve al banco.
- Nuevo bloque **"Ejemplos como cierre de semántica (EXP-14)"** en INSTRUCCIONES APRENDIDAS con las 4 instrucciones anteriores.
- Header actualizado (run 14, próximo EXP-15). Frontmatter intacto (verificado contra HEAD byte a byte). Criterio de éxito #2 del roadmap ("ejemplos reales, no hipotéticos") queda cubierto.
