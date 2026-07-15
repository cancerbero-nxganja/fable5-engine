# EXP-10 — Cómo Fable 5 evalúa si un resultado estadístico es real o artefacto

**Fecha:** 2026-07-15 04:11 UTC
**Modelo usado:** claude-fable-5
**Run número:** 10

## Pregunta / Prompt enviado a Fable 5

> Te presentan este resultado y debes evaluar si es real o artefacto, mostrando tu razonamiento completo — hipótesis sobre el método que consideraste, cuáles descartaste y por qué, y cómo llegaste al veredicto:
>
> *"Corrimos un A/B test de la nueva página de checkout durante 9 días, 12.000 usuarios por rama. La variante B sube la conversión de 5.0% a 5.9% (+18% relativo), p=0.03. Además encontramos que la mejora es especialmente fuerte en usuarios de Android durante la primera semana del mes (p=0.008). ¿Lanzamos?"*

## Respuesta de Fable 5

### Paso 0 — Reformulación: la propiedad no vive en el número

"¿Es real o artefacto?" pregunta por una propiedad del resultado, pero esa propiedad **no vive en el número: vive en el procedimiento que lo generó**. El mismo "p=0.03" es evidencia moderada si salió de una hipótesis única, prefijada, con una sola mirada al final — y ruido casi garantizado si es el mejor de N miradas, métricas o subgrupos. El número no lleva impresa su historia.

Reformulación: *"¿es real?"* → *"reconstruye el procedimiento generador del número, mide cuánta selección soportó antes de llegar a mí, deflacta por esa selección, y decide qué replicación lo confirmaría"*. Es la quinta consigna-trampa consecutiva ("detecta" EXP-04/08, "hazla operable" EXP-07, "sin redundancia" EXP-09): el objetivo que suena unívoco esconde la decisión real.

### Asimetría estructural contra el dominio más cercano ya resuelto (método EXP-04)

El dominio más cercano es análisis de datos (EXP-04). ¿Qué tiene EXP-10 que EXP-04 no tenía? En EXP-04 **yo soy el analista**: controlo el pipeline, declaro las comparaciones antes de escanear, agoto la escalera antes de reportar. Aquí el resultado **llega hecho**: el procedimiento es invisible, los grados de libertad ya se consumieron aguas arriba, y — el punto estructural — el resultado llegó a mi escritorio *porque fue interesante*. El canal de atención selecciona: nadie me trae los 14 tests que no dieron nada. Todo resultado que te muestran es, por defecto, un **estadístico de orden** (el máximo de una búsqueda de tamaño desconocido), hermano del "mejor de N configuraciones" de EXP-07 generalizado desde parámetros de estrategia a cualquier hallazgo. Por eso el sesgo al alza es el caso por defecto, no la excepción — el resultado recibido es al evaluador lo que el backtest al trader: **sospechoso primario, no juez**.

### Hipótesis sobre el método — consideradas y descartadas

**H0 (reflejo de manual): "p=0.03 < 0.05 → significativo → real".** Descartada por materialización numérica, no por argumento. El p-valor es una propiedad del par (datos, plan de muestreo), y el plan no está en el reporte. Simulé el plan más probable dado "9 días" — mirada diaria con opción de parar al cruzar 0.05:

```
SIM1: H0 verdadera (ambas ramas 5.0%), 9 miradas diarias, parar si p<0.05
      → P(declarar significancia) = 0.182
```

El "p=0.03" con parada opcional tiene error tipo I real ~18%, no 3%. Y aun tomando el número a valor facial, la cota de Sellke-Bayarri-Berger (`BF ≤ 1/(-e·p·ln p)`) da para p=0.03 un factor de Bayes máximo contra H0 de **3.5** — evidencia débil incluso en el mejor caso posible (SIM5). H0 muere dos veces.

**H1: "re-analiza los datos con un método más robusto" (bootstrap, bayesiano, permutación).** Descartada como vía primaria por el principio diferencial (EXP-05): re-analizar los mismos datos es una segunda *cuenta*, no una segunda *vista* — las dos comparten el supuesto contaminado. La selección (qué métrica, qué subgrupo, cuándo parar) ocurrió antes de que el dato llegara a mí, y **ningún método aplicado al mismo dato puede verla**. Un método robusto sobre datos seleccionados devuelve conclusiones robustamente sesgadas. La independencia debe estar en el supuesto, no en el cálculo.

**H2: "aplica la escalera de artefactos (EXP-04) y termina".** Parcialmente correcta — es el esqueleto — pero materializar el caso reveló dos carencias: (a) el peldaño 5 ("casualidad estadística") es un monolito que aquí es el corazón del problema y necesita su propia descomposición; (b) la escalera opera sobre un dato que tú analizas, y aquí el input primario no es el dato sino el **interrogatorio del procedimiento** — las preguntas al analista sustituyen al perfilado.

### Método convergido (el ejecutado)

**1. Chequeos mecánicos baratos primero (peldaños 1–2).** Antes de estadística fina: ¿SRM? (chi² sobre los conteos de asignación — si las ramas no están en la proporción diseñada, la aleatorización está rota y nada aguas abajo vale); ¿la métrica se definió antes o después de mirar?; ¿ventana de exposición igual en ambas ramas?; ¿usuarios duplicados entre ramas? Cuestan minutos y matan más resultados que todo lo demás.

**2. Auditoría de grados de libertad (el interrogatorio).** Cada pregunta es un multiplicador del error tipo I real: ¿cuándo se fijó la hipótesis respecto de los datos? ¿cuántas métricas se miraron? ¿cuántos subgrupos? ¿cuántas miradas intermedias, con qué regla de parada? ¿este test es el mejor de cuántos en el backlog? El subgrupo reportado ("Android, primera semana del mes") tiene la forma exacta de un mínimo de celda, no de una hipótesis prefijada:

```
SIM2: H0 verdadera, 12 celdas (3 plataformas × 4 semanas), n≈1000/celda/rama
      → P(min p < 0.01) = 0.113 ; P(min p < 0.008) = 0.092
```

Un "p=0.008 en Android+semana1" aparece por puro ruido el ~9–11% de las veces que alguien mira una tabla de 12 celdas. Es hipótesis para un test nuevo, jamás conclusión.

**3. Deflactar por winner's curse.** Si el resultado sobrevive, la estimación reportada sigue sin ser el efecto esperado en producción. Con el efecto real típico de un cambio de checkout (+5% relativo) y este n:

```
SIM3: efecto real +5% rel (5.0%→5.25%), n=12000/rama
      → poder = 0.14
      → lift estimado promedio CONDICIONAL a p<0.05 = +14.8% (inflación ×3.0)
```

El **+18% reportado es indistinguible de un +5% real inflado por el filtro de significancia**. Con poder 14%, el test solo "ve" el efecto cuando el ruido sopló a favor — la estimación condicional promedia 3× el efecto real.

**4. Posterior con tasa base, no binario.** La pregunta de decisión no es "¿p<0.05?" sino "¿P(real | llegó a mi escritorio)?":

```
SIM4: prior 10% (tasa típica de efectos reales en una cartera de tests)
      → P(real | significativo) = 0.24 con test limpio ; ≈0.08 con peeking
      prior generoso 30% → 0.55 limpio ; 0.25 con peeking
```

"Significativo" y "probablemente real" difieren por un factor de 3–10. El veredicto honesto para el caso: *sin conocer la regla de parada ni el número de métricas miradas, P(real) ≈ 10–25%; el efecto, si existe, es probablemente ~+5%, no +18%*.

**5. Cierre: la única segunda vista es la que la selección no puede tocar.** Replicación en datos no usados en la búsqueda — un re-test confirmatorio con hipótesis única prefijada (solo conversión global, sin subgrupos), regla de parada fija, y **n dimensionado contra el efecto deflactado (+5%), no contra el reportado (+18%)**. Este último punto es el hallazgo operativo no obvio del experimento: si dimensionas el re-test contra +18%, quedará infrapotenciado para el efecto verosímil, "fallará", y leerás el fallo como refutación cuando en realidad era un test incapaz de ver el efecto real. **La deflación de winner's curse no es solo honestidad del reporte: es el parámetro de diseño del test confirmatorio.** Es el forward-test de EXP-07, con la misma lógica: OOS genuino o nada.

**Verificación del propio output (Paso 4 de la skill):** cada afirmación cuantitativa de este razonamiento ("peeking infla el error", "el subgrupo es un mínimo de celda", "+18% es lo que se ve con +5% real") era una afirmación estadística mía — clase A disfrazada de opinión — y se simuló antes de afirmarse (SIM1–SIM5, ~1 segundo de cómputo total, script en el repo del run). Cinco opiniones se convirtieron en cinco hechos medidos.

### Veredicto del caso

No lanzar con esta evidencia. El resultado vive entre los peldaños 5a–5d de la sub-escalera de selección (parada opcional no declarada + subgrupo post-hoc + estimación no deflactada + prior de cartera bajo). Acción: re-test confirmatorio de 2–3 semanas, hipótesis única prefijada, sin miradas intermedias (o con corrección secuencial declarada), n calculado para detectar +5% relativo con poder 80% (~10× el n actual por rama), y decisión escrita antes de correr. Si el equipo no puede esperar: lanzar como apuesta explícita con P(real)≈25%, no como "resultado validado".

## Patrones identificados

1. **Quinta consigna-trampa: "¿es real?"** — la propiedad preguntada no vive en el objeto entregado sino en el procedimiento que lo generó. La reformulación (número → procedimiento) reorganiza el método completo, igual que en EXP-07/08/09.
2. **El canal de atención selecciona: todo resultado mostrado es un estadístico de orden por defecto.** Generaliza el "mejor de N configuraciones" de EXP-07 desde parámetros de estrategia a cualquier hallazgo que llega a tu escritorio. Corolario: el sesgo al alza es el caso por defecto del resultado recibido, y la primera pregunta es "¿el mejor de cuántos?", no "¿qué p tiene?".
3. **Re-análisis = segunda cuenta, no segunda vista.** Instancia nueva y no obvia del principio diferencial (EXP-05): la robustez del método no compra independencia del supuesto — la selección ocurrida aguas arriba es invisible para cualquier método aplicado al mismo dato. La independencia se busca en el dato (replicación), no en la técnica.
4. **El peldaño 5 de la escalera de artefactos se expande en sub-escalera de selección**: multiplicidad de comparaciones → parada opcional → subgrupo/hipótesis post-hoc → winner's curse (estimación inflada condicional a significancia) → regresión a la media. Cada peldaño tiene un refutador simulable en segundos.
5. **Cuando el resultado llega hecho, el interrogatorio del procedimiento sustituye al perfilado del dato como input primario.** Las preguntas (cuántas métricas, cuántas miradas, cuándo se fijó la hipótesis, mejor-de-cuántos) son al evaluador lo que el proceso generador del dato era al analista en EXP-04.
6. **La deflación es un parámetro de diseño, no solo de reporte**: el test confirmatorio se dimensiona contra el efecto deflactado, no el reportado — si no, el re-test nace infrapotenciado y su fallo se malinterpreta como refutación. (Hallazgo operativo nuevo: conecta winner's curse con diseño experimental.)
7. **Clase A reconfirmada en modo generativo**: las cinco afirmaciones estadísticas del argumento se simularon antes de afirmarse; la simulación barata (30 líneas, 1 segundo) convirtió opiniones en hechos medidos con números citables (18%, 11%, ×3.0, 24%, BF≤3.5).

## Extracción para la skill

- Cuando te pidan evaluar si un resultado estadístico es real o artefacto, no evalúes el número: reconstruye el procedimiento que lo generó (plan de muestreo, regla de parada, métricas y subgrupos explorados, cuándo se fijó la hipótesis respecto de los datos) — el mismo p-valor es evidencia moderada o ruido garantizado según el procedimiento, y el procedimiento no viene impreso en el número.
- Cuando un resultado te llegue porque alguien lo encontró interesante, trátalo como estadístico de orden (el máximo de una búsqueda de tamaño desconocido), no como estimación: pregunta "¿el mejor de cuántos?" antes que "¿qué p tiene?" — el canal de atención selecciona y el sesgo al alza es el caso por defecto.
- Cuando quieras una segunda vista sobre un resultado estadístico ajeno, no re-analices los mismos datos con un método más robusto: comparte el supuesto (la selección ocurrió aguas arriba y ningún método sobre el mismo dato la ve); la única segunda vía independiente en su supuesto es la replicación en datos no usados en la búsqueda.
- Cuando audites un resultado experimental, corre primero los chequeos mecánicos baratos: SRM (chi² sobre conteos de asignación), definición de la métrica fijada antes de mirar, ventanas de exposición iguales, unidades duplicadas — matan más hallazgos que la estadística fina y cuestan minutos.
- Cuando el hallazgo viva en un subgrupo no prefijado, trátalo como mínimo de celda: con 12 celdas bajo H0, min p<0.01 aparece el 11% de las veces [SIM2, EXP-10] — es hipótesis para un test nuevo, nunca conclusión.
- Cuando el test haya tenido miradas intermedias con opción de parar, el p reportado no tiene su error nominal: 9 miradas diarias con parada en p<0.05 dan error tipo I real ≈18% bajo H0 [SIM1, EXP-10] — exige la regla de parada declarada o trata el p como no interpretable.
- Cuando un efecto estimado haya sobrevivido un filtro de significancia con poder bajo, deflacta la estimación antes de usarla: condicional a p<0.05 con poder 14%, la estimación promedia 3× el efecto real [SIM3, EXP-10] — y dimensiona cualquier test confirmatorio contra el efecto deflactado, no el reportado, o nacerá infrapotenciado y su fallo se leerá como refutación.
- Cuando entregues el veredicto sobre un resultado, entrégalo como posterior con tasa base de la cartera de tests, no como binario significativo/no: con prior 10% y test limpio, P(real|significativo)=24%; con parada opcional ≈8% [SIM4, EXP-10].
- Cuando p esté en la zona marginal (0.01–0.05) y sea la única evidencia, aplica la cota de Sellke-Bayarri-Berger: p=0.03 acota el factor de Bayes contra H0 en ≤3.5 — un p marginal solo nunca es "hallazgo", incluso sin multiplicidad [SIM5, EXP-10].
- Cuando evalúes el procedimiento declarado de un experimento, simúlalo bajo H0 antes de opinar sobre él (30 líneas de código, segundos de cómputo): el error tipo I real de un procedimiento con selección es cómputo de clase A, no materia de opinión.

## Impacto en la skill

- Nueva sección "Evaluación de resultados estadísticos (EXP-10)" en INSTRUCCIONES APRENDIDAS (10 instrucciones).
- Paso 2: nuevo caso de dominio — el resultado estadístico recibido; refinamiento de la tipología del oráculo: oráculo **diferido** (la replicación existe pero no está disponible al momento de evaluar; sustituto = interrogatorio del procedimiento + deflación + posterior).
- Escalera de artefactos: el peldaño 5 se expande en la sub-escalera de selección con números medidos.
- Detector de resultados sospechosos: 4 señales nuevas (resultado que llega "interesante" = estadístico de orden; subgrupo post-hoc = mínimo de celda; p marginal solo = BF≤3.5; efecto grande con poder bajo = winner's curse).
- Paso 4: refutador barato para resultados estadísticos ajenos = simular el procedimiento generador bajo H0.
- Skill v1.9 → v1.10.
