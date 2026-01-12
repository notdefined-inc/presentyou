# Workflow: From Brainstorm to Export

## 1. Brainstorm & Outline
**Goal**: Agree on the content structure before generating any code.
- Discuss topic, audience, and tone.
- Propose a 5-8 slide outline.
- **Do NOT** write any files in this phase.

## 2. Build (JSON-Only)
**Goal**: Generate the deck content in a strictly validated format.
- Output `DeckSpec` (for fresh decks) or `SlidePatch` (for edits).
- **Format**: JSON only. No explanation text outside the JSON block if possible.
- **Validation**:
  ```bash
  python .claude/skills/authoring-slidev-decks/scripts/validate.py --stdin --schema patch <<'JSON'
  { ... }
  JSON
  ```

## 3. Apply Changes
**Goal**: Update the filesystem deterministically.
- Use `.claude/skills/authoring-slidev-decks/scripts/apply_patch.py` for single slides.
- Use `.claude/skills/authoring-slidev-decks/scripts/render_deck.py` for full deck synchronizing.

## 4. Audit & Review
**Goal**: Ensure the generated slides have no broken references and stay in sync.
- Run `python .claude/skills/authoring-slidev-decks/scripts/audit.py --project <path>` to check structure and (if present) compare `deck.json` vs `slides.md` ordering.

## 5. Export
**Goal**: Produce the final artifacts.
- PPTX: `python .claude/skills/authoring-slidev-decks/scripts/export.py --project <path> --format pptx`
- PDF: `python .claude/skills/authoring-slidev-decks/scripts/export.py --project <path> --format pdf`
