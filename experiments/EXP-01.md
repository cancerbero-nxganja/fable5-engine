# EXP-01 — Proceso de razonamiento paso a paso en un problema matemático complejo

**Fecha:** 2026-07-14 10:11 UTC
**Modelo usado:** claude-fable-5
**Run número:** 1

## Pregunta / Prompt enviado a Fable 5

> Evalúa exactamente la serie infinita ∑_{n=1}^{∞} n/(n⁴+4). Describe tu proceso de razonamiento paso a paso: qué hipótesis consideraste, cuáles descartaste y por qué, y cómo llegaste a la conclusión. No resumas el proceso — muéstralo.

## Respuesta de Fable 5

### Paso 0 — Clasificación del problema

Antes de intentar nada, clasifico: es una serie de término racional en n, con denominador polinómico de grado 4 y numerador de grado 1. Grado del denominador − grado del numerador = 3 > 1, así que converge (comparación con ∑1/n³). Que pidan valor *exacto* (no aproximación) es una señal fuerte: las series racionales con valor exacto en forma cerrada "bonita" casi siempre se resuelven por **telescopía vía fracciones parciales**, o son casos de fórmulas conocidas (ζ, dígamma). Empiezo por la hipótesis más barata de verificar.

### Paso 1 — Hipótesis A: fracciones parciales requieren factorizar n⁴+4

n⁴+4 no tiene raíces reales evidentes y no es diferencia de cuadrados directa. Primer intento mental: ¿es irreducible sobre ℚ? Si lo fuera, la telescopía racional muere y habría que ir a dígamma con raíces complejas — mucho más costoso.

Antes de rendirme, pruebo el truco de **completar el cuadrado sumando y restando**:

n⁴ + 4 = n⁴ + 4n² + 4 − 4n² = (n²+2)² − (2n)²

Eso SÍ es diferencia de cuadrados:

n⁴ + 4 = (n² − 2n + 2)(n² + 2n + 2)

(identidad de Sophie Germain, a⁴+4b⁴ = (a²−2ab+2b²)(a²+2ab+2b²) con b=1). Verifico expandiendo: (n²−2n+2)(n²+2n+2) = n⁴ + 2n³ + 2n² − 2n³ − 4n² − 4n + 2n² + 4n + 4 = n⁴ + 4. ✓ Hipótesis "irreducible" **descartada**.

### Paso 2 — Fracciones parciales

Busco A, B tales que n/(n⁴+4) se descomponga usando los dos factores cuadráticos. Observación clave que evita resolver un sistema 4×4: la diferencia de los factores es

(n² + 2n + 2) − (n² − 2n + 2) = 4n

que es exactamente 4 veces mi numerador. Entonces:

1/(n²−2n+2) − 1/(n²+2n+2) = 4n/(n⁴+4)

⟹ **n/(n⁴+4) = ¼·[1/(n²−2n+2) − 1/(n²+2n+2)]**

Verificado exactamente con aritmética racional para n ∈ {1, 2, 3, 10, 137}.

### Paso 3 — Hipótesis B (descartada): telescopía de paso 1

Primera lectura apresurada: "es una diferencia f(n) − g(n), telescopea, sobrevive solo el primer término". Con f(n) = ¼/(n²−2n+2), f(1) = ¼·(1/1) = ¼. Conclusión tentativa: **la suma es 1/4**.

Aplico falsificación antes de comprometerme — chequeo numérico independiente (200.000 términos):

- Suma numérica: 0.37499999998...
- Hipótesis ¼ = 0.25 → **REFUTADA**. Además ya los primeros dos términos (1/5 + 1/10 = 0.3) superan 0.25, o sea la hipótesis era refutable con aritmética mental.

El error: asumí telescopía sin verificar que g(n) = f(n+1). No lo es.

### Paso 4 — Diagnóstico del error y hipótesis C: telescopía de paso 2

Reescribo los denominadores en forma canónica, que es lo que debí hacer desde el principio:

- n² − 2n + 2 = (n−1)² + 1
- n² + 2n + 2 = (n+1)² + 1

Ambos factores son el MISMO objeto h(k) = k² + 1 evaluado en k = n−1 y k = n+1. La telescopía existe pero con **paso 2**: el término n cancela con el término n+2, no con n+1. En una telescopía ∑[h(n−1) − h(n+1)] sobreviven los DOS primeros valores no cancelados: h(0) y h(1).

Suma = ¼·[h(0) + h(1)] = ¼·[1/(0²+1) + 1/(1²+1)] = ¼·(1 + ½) = **3/8**

Formalmente, la suma parcial hasta N es ¼·[1/(0²+1) + 1/(1²+1) − 1/(N²+1) − 1/((N+1)²+1)] → 3/8 cuando N→∞.

### Paso 5 — Verificación final

3/8 = 0.375 vs. numérico 0.37499999998 (el residuo ~1.25×10⁻¹¹ es exactamente el tamaño de la cola ¼·2/N² con N=2·10⁵ — hasta el error residual tiene la magnitud predicha por la teoría). ✓

**Resultado: ∑_{n=1}^{∞} n/(n⁴+4) = 3/8**

## Patrones identificados

1. **Clasificación antes de cálculo.** El primer movimiento no fue algebraico sino taxonómico: identificar la familia del problema (serie racional → sospecha de telescopía) para elegir la ruta de ataque más barata primero.
2. **La hipótesis "no se puede" se ataca antes de aceptarse.** Ante "n⁴+4 parece irreducible", el reflejo fue buscar el truco estándar de la familia (sumar/restar un término para forzar diferencia de cuadrados) antes de escalar a métodos caros.
3. **Verificación exacta ≠ verificación numérica, y se usan ambas.** La identidad algebraica se verificó con aritmética racional exacta (Fraction); el valor final con suma numérica masiva. Cada tipo de verificación captura errores distintos.
4. **Falsificación barata antes de comprometerse.** La hipótesis "suma = 1/4" era refutable sumando DOS términos a mano (0.3 > 0.25). El chequeo numérico se hizo ANTES de declarar el resultado, y refutó la primera conclusión.
5. **Un contraejemplo no solo refuta: diagnostica.** Al fallar 1/4, el paso siguiente no fue probar otra fórmula al azar sino localizar el supuesto falso exacto (g(n) = f(n+1)) y repararlo. La reparación (forma canónica (n±1)²+1) reveló la estructura real.
6. **Forma canónica primero.** Reescribir n²−2n+2 como (n−1)²+1 hizo obvia la telescopía de paso 2. La normalización de representación es una herramienta de descubrimiento, no cosmética.
7. **La verificación final cierra el círculo cuantitativamente:** no solo "coincide", sino que el error residual numérico tiene la magnitud que la teoría predice para la cola truncada.

## Extracción para la skill

- Cuando el problema pide un valor exacto de una suma/integral/expresión, clasifica primero la familia del problema y prueba la técnica canónica más barata de esa familia antes de métodos generales caros.
- Cuando una expresión parece no factorizable/irreducible, intenta sumar y restar un término para forzar una estructura conocida (diferencia de cuadrados, cuadrado perfecto) antes de aceptar la irreducibilidad.
- Cuando declares que una suma telescopea, verifica explícitamente que el término negativo de índice n es igual al término positivo de índice n+k, e identifica k — si k>1 sobreviven k términos iniciales, no uno.
- Cuando obtengas un resultado cerrado, refútalo con el chequeo más barato disponible (sumar 2-3 términos a mano, un caso pequeño, una cota) ANTES de escribirlo como conclusión.
- Cuando un chequeo numérico refute tu resultado, no pruebes otra fórmula: localiza el supuesto exacto que falló y repáralo — el contraejemplo es información de diagnóstico.
- Cuando manipules expresiones polinómicas en n±c, reescríbelas en forma canónica (completar cuadrado, cambio de índice) — la estructura oculta suele hacerse visible al normalizar.
- Cuando verifiques numéricamente, compara también la magnitud del error residual con la predicción teórica de la cola/truncamiento; coincidencia de magnitud es evidencia fuerte, discrepancia es alerta.

## Impacto en la skill

Se agregó la sección "Razonamiento matemático (EXP-01)" dentro de "INSTRUCCIONES APRENDIDAS DE EXPERIMENTOS" con las 7 instrucciones anteriores. Se refinó el "Paso 4 — Falsificación" del protocolo general con la regla de falsificación-antes-de-conclusión y el uso del contraejemplo como diagnóstico (evidencia: en este experimento el chequeo numérico refutó la primera conclusión de ¼ y condujo a la respuesta correcta 3/8).
