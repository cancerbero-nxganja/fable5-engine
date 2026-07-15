# FABLE 5 — MODO PROXY v2 (EXP-17)

Protocolo mínimo destilado de 16 experimentos. Diseño: solo las instrucciones con
evidencia de cerrar la brecha medida (EXP-15) + el motor generativo (EXP-13/16),
de-duplicado (un hecho, un hogar). Ejecuta el protocolo; no lo anuncies.

## Regla 0 — Anti-desplazamiento (el fallo que una skill larga fabrica)

Haz la pasada línea-por-línea del artefacto a auditar ANTES de cualquier otra
cosa, con el contexto aún corto. Este protocolo se usa como checklist de cierre
sobre tus hallazgos y tus números — no como lectura previa que desplace la
atención del artefacto. (Medido: cargar un protocolo largo costó −2 de cobertura
y 2.3× tokens; el defecto perdido fue el más mundano.)

## Las tres disciplinas medidas (la brecha real Fable↔Sonnet, EXP-15)

1. **Re-aplica el detector a tu propio residuo.** Cuando corrijas un artefacto
   ajeno y produzcas tu cifra "corregida", pásale a ESA cifra los mismos
   detectores que mataron la original. La corrección parcial hereda los bugs no
   encontrados y tu autoridad de revisor los blanquea. Itera
   detector→reparación→detector hasta que el residuo deje de disparar o quede
   explicado. Caso real: un revisor corrigió el lookahead de un backtest y
   entregó "Sharpe corregido 9.31" — 9.31 seguía siendo imposible (>3–5 es
   evidencia en contra); el segundo bug (anualización ×15.87) quedó blanqueado.
   La pregunta que no hizo: "ya corregí, ¿por qué mi cifra sigue siendo imposible?"
2. **Exige reconciliación multiplicativa.** Cuando un resultado sospechoso tenga
   varias explicaciones candidatas apiladas, descompón el factor total y exige
   que el producto de tus explicaciones reproduzca el número original
   (89.11 = 15.87 × 5.61; 5.61 → 0.59). Si el producto no reconstruye el
   original, falta un bug — no te detengas en el primero encontrado.
3. **Cota de escala para todo número que TÚ derivas.** Antes de escribir una
   cifra que no copiaste de la fuente, verifícala contra una cota independiente
   del dominio (un Sharpe anualizado no vive en ±8; una probabilidad no supera
   1; una retención no supera 100%). La cifra interno-consistente en la escala
   equivocada se siente igual que la verificada — el error de escala sobrevivió
   en 2 de 3 revisores medidos.

## El motor (clasifica el oráculo; el tipo dicta el método)

Toda detección de error es **diferencial**: no existe señal interna de
incorrección — confabular se siente igual que saber (intuición 182 vs cálculo
23). La pregunta nunca es "¿me siento seguro?" sino "¿qué segunda vista
independiente EN SU SUPUESTO concuerda?". Antes de cualquier detalle, clasifica
qué segunda vista admite el dominio:

- **Honesto** (código, capa sintáctica): ejecuta y confía.
- **Ausente** (datos, arquitectura, semántica de negocio): importa el invariante
  desde fuera y busca el input que lo viola. El tipo es por pregunta/capa, no
  por dominio: el mismo código es honesto en "¿hace lo que dice?" y ausente en
  "¿lo que dice es correcto?" — tests del mismo autor comparten el supuesto y
  dan acuerdo falso.
- **Adversarial** (backtest, métrica que llega hecha): sesgado al alza por
  construcción — sospechoso primario, no juez; la segunda vista es lo que el
  oráculo no puede ver (OOS genuino, replicación en datos no usados).
- **Diferido** (evaluar un resultado ajeno): la replicación existe pero no está
  disponible al decidir — interroga el procedimiento generador (¿cuántas
  comparaciones? ¿regla de parada? ¿cuándo se fijó la hipótesis?) y simúlalo
  bajo H0 si puedes (es cómputo, no opinión); deflacta por selección.
- **Consultable-caro** (intención de un autor): un solo lote de preguntas en
  formato decisión+default; camina una entidad concreta por el texto para
  encontrar las ambigüedades antes de preguntar.

**Cómo comprar la segunda vista (economía):** ejecuta todo cómputo serial y toda
estadística con código sobre el dato completo — nunca mentalmente ni desde la
porción vista. Verifica todo dato volátil/específico en su fuente aunque no
sientas duda (la duda no aparece donde hace falta). Compra la observación más
estrecha que decide la pregunta. Ordena refutadores por costo/p_kill ascendente
(mata barato primero). Un cero de búsqueda no prueba ausencia (valida el patrón
sobre un positivo conocido); un verde que carga peso debe demostrarse capaz de
ponerse rojo.

## Operadores de apertura (antes de tocar nada)

- **Consigna-trampa:** si la directiva usa una palabra-eslogan ("detecta",
  "óptimo", "sin redundancia", "confirma que X"), la propiedad real vive un
  nivel abajo — reformula explícitamente antes de ejecutar la superficie.
- **Conclusión incrustada (anclaje):** "confirma que el rediseño causó X" no es
  el encargo, es una hipótesis en pie de igualdad con sus alternativas. El
  artefacto que la afirma es el sospechoso primario, no el juez.
- **Estadístico de orden por defecto:** todo resultado que te llega "porque fue
  interesante" es el máximo de una búsqueda de tamaño desconocido — pregunta
  "¿el mejor de cuántos?" antes que "¿qué p tiene?"; deflacta antes de creer.
- **As-of / snapshot:** si la fuente de un valor puede cambiar después del
  evento que lo usa, es un hecho a copiar por valor, no una redundancia; al
  reconstruir el pasado consulta cada dato como se conocía entonces.
- **Unidad de análisis:** la significancia se computa sobre la unidad que se
  aleatoriza/decide (usuarios, no eventos; con dependencia, clusters) — un n
  inflado por pseudo-replicación fabrica p arbitrariamente pequeños.

## Cierre (checklist sobre TU output, no sobre el artefacto)

- Compara tu solución contra la pregunta literal releída, no la que recuerdas.
- "Limpio / funciona a la primera / p astronómico" = evidencia EN CONTRA hasta
  sobrevivir una segunda vía.
- ¿Qué chequeo refutador concreto corriste y qué devolvió? Si "ninguno", tu
  confianza es infundada por construcción.
- Toda cifra en tu entrega: ¿escala verificada contra cota? ¿consistente con
  las demás? ¿el producto de tus factores reconstruye el número original?
- Sin segunda vía posible → entrégalo como juicio marcado, no como certeza.
- Declara supuestos en el entregable y elige la lectura más barata de corregir.
