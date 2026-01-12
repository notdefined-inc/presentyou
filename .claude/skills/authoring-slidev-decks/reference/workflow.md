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
  python tools/validate.py --stdin --schema patch <<'JSON'
  { ... }
  JSON
  ```

## 3. Apply Changes
**Goal**: Update the filesystem deterministically.
- Use `tools/apply_patch.py` for single slides.
- Use `tools/render_deck.py` for full deck synchronizing.

## 4. Audit & Review
**Goal**: Ensure the generated slides match the `deck.json` source of truth.
- Run `python tools/audit.py` to check for drift.
- If drift is found, ask the user if they want to sync to `deck.json` or update `deck.json` from current slides.

## 5. Export
**Goal**: Produce the final artifacts.
- PPTX: `python tools/export.py --format pptx`
- PDF: `python tools/export.py --format pdf`
