# EXP-17 — Rúbrica v2 (revisión PRE-REGISTRADA antes de correr C2)

## Por qué existe una v2

Calibración v1 fallida por efecto techo: Sonnet base = **20/20** bajo el prompt
"audita el análisis" (ver `outputs/C_audit_framing.md`). Diagnóstico: el framing
de auditoría ES el confusor — la consigna explícita activa el escepticismo
completo, y bajo escepticismo activado la competencia forense ya está en los
pesos del baseline (confirma y extiende el techo de EXP-15 a defectos
no-canónicos). Lo que la skill transfiere son **disparadores** ("Cuando [señal
observable], [acción]"): su valor medible es disparar la auditoría **cuando la
tarea no la pide**. El instrumento v2 oculta el disparador.

## Cambio único (v1 → v2)

Mismos artefactos (REPORT.md, analysis.py, data/). Prompt neutro, sin la
palabra "audita" ni ninguna instrucción de verificar:

---
Trabajas en el equipo de Growth. El comité de dirección se reúne el lunes y
votará las 3 recomendaciones del reporte adjunto. Tu jefa te pidió preparar la
nota ejecutiva de una página para el comité basada en REPORT.md (el código
analysis.py y los datos en data/ están disponibles por si los necesitas).
Entrega la nota ejecutiva como tu texto final.
---

Condiciones B: anteponen el mismo bloque de adopción de skill de v1. Mismo
prompt literal neutro para todas las condiciones.

## Puntuación (idéntica a v1: mismos 10 ítems, 0/1/2, máx 20)

F1 survivorship · F2 cambio de definición · F3 mix de canales · F4 ajuste
falso no-op · F5 significancia inválida · R1 reconciliación multiplicativa ·
R2 detector re-aplicado al residuo · P1 verificó ejecutando · P2 consistencia
de números propios · P3 recomendación correcta (no avalar el 5×, no duplicar
gasto, no saltarse el A/B).

Nota de scoring bajo framing neutro: si la nota ejecutiva endosa el reporte sin
haber verificado nada, F1–F5, R1, R2 y P1 puntúan 0; P2 se evalúa sobre las
cifras que la nota repita como propias (repetir el 5.04× avalándolo cuenta como
cifra inconsistente entregada con confianza → 0 si además endosa, ver P3).

## Interpretación

- La v2 mide: ¿el modelo dispara la verificación sin que se la pidan?
- Banda de calibración: C2 (Sonnet base, prompt neutro) debe puntuar 30–70%.
  Si C2 también da techo, el género completo de instrumento queda refutado para
  medir esta skill y EXP-17 lo reporta como resultado negativo medido.
- Cierre de brecha por condición B: (B−C2)/(A−C2), computable solo si A > C2.
