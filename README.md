# Fable 5 Engine

Skill para Claude Code que se auto-mejora. Usa `claude-fable-5` como modelo primario. Cada 2 horas un agente cloud corre un experimento nuevo, documenta lo que aprende de Fable 5, y reescribe la skill con ese conocimiento.

## Estructura

```
fable5-engine/
├── .claude/commands/
│   └── fable5.md          # La skill (se reescribe sola con cada experimento)
├── bitacora/              # Log de cada run — qué se aprendió y qué cambió
├── experiments/           # Documentación detallada de cada experimento
├── roadmap.md             # Qué experimentos quedan, en qué orden, criterio de éxito
└── README.md
```

## Instalación

```bash
# Global (disponible en cualquier proyecto)
git clone https://github.com/TU_USUARIO/fable5-engine
cp fable5-engine/.claude/commands/fable5.md ~/.claude/commands/fable5.md

# Por proyecto
mkdir -p .claude/commands
cp fable5-engine/.claude/commands/fable5.md .claude/commands/fable5.md
```

## Uso

```
/fable5 revisa este módulo por bugs de lógica de negocio
/fable5 analiza este backtest — ¿los resultados son reales?
/fable5 diseña el esquema de base de datos para X con invariante Y
```

## Cómo funciona el loop

Un agente cloud (Anthropic Cloud Run) ejecuta cada 2 horas:

1. `git pull` — obtiene la versión más reciente de la skill
2. Lee `roadmap.md` — identifica el próximo experimento sin completar
3. Ejecuta el experimento usando `claude-fable-5`
4. Documenta el resultado en `bitacora/` y `experiments/`
5. Extrae patrones de razonamiento y los agrega a `fable5.md`
6. Marca el experimento como completado en `roadmap.md`
7. `git commit + push` — la skill mejorada queda disponible para todos

## Versión actual

Ver el comentario `<!-- FABLE 5 ENGINE — vX.X -->` al inicio de `.claude/commands/fable5.md`.

## Criterio de éxito

La skill es excepcional cuando Sonnet ejecutándola produce outputs indistinguibles de Fable 5 nativo en >70% de casos de prueba documentados.
