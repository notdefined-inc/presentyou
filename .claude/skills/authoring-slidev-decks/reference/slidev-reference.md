# Slidev Reference (Local, Version-Accurate)

When you need an exhaustive, version-accurate list of Slidev options and built-ins, prefer reading the project's local `node_modules` sources instead of guessing.

## Fast Path (Token-Efficient)

Run the introspection script and use its output as the "source of truth":

```bash
python .claude/skills/authoring-slidev-decks/scripts/slidev_introspect.py --project ./my-deck --format json
```

## Authoritative Local Sources

- Config + frontmatter typings: `node_modules/@slidev/types/dist/index.d.mts`
  - `HeadmatterConfig` (presentation-level options)
  - `Frontmatter` (slide-level options)
  - `BuiltinLayouts`, `BuiltinSlideTransition`
- Built-in components/directives: `node_modules/@slidev/client/builtin/`
- Starter examples: `node_modules/@slidev/cli/template.md`

