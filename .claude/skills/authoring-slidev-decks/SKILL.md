---
name: claude-skills-presentation-you
description: Orchestrates creation of Slidev presentation decks using deterministic JSON-driven workflows and repo tools. Use when the user asks to (1) Generate, create, or build slides/presentations/decks, (2) Edit, update, or modify existing slides, (3) Export presentations to PPTX/PDF formats, (4) Work with Slidev files (slides.md, deck.json, slide patches), (5) Apply slide layouts or themes, or (6) Mentions presentation authoring, slide generation, deck building, or Slidev.
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./.claude/skills/authoring-slidev-decks/scripts/security-check.sh \"$TOOL_INPUT\""
---

# Authoring Slidev Decks (Deterministic)

## Overview
Produce Slidev decks via a strict JSON-driven workflow:
- Generate ONLY JSON matching the repo schema
- Modify filesystem ONLY via deterministic scripts
- Render and export slides via scripts/CLI, never by direct file editing

## Getting Started

### Initialize a New Project

```bash
python .claude/skills/authoring-slidev-decks/scripts/init_slidev_project.py ./my-presentation --name "My Deck"
# Optional: Add --install to run 'npm install' automatically
cd my-presentation
npm install # if not installed via --install
npm run dev
```

### Brainstorm First! (MANDATORY)

**You MUST NOT generate slides without a plan.**
Before building, have a brainstorm conversation:
1. **Topic**: What's this presentation about?
2. **Audience**: Who will watch it?
3. **Tone**: Professional, technical, or creative?
4. **Theme**: See [themes.md](reference/themes.md) for color palettes
5. **Structure**: 5-8 slides with clear flow

See [brainstorm.md](reference/brainstorm.md) for the full guided workflow.

## Hard Rules
1. Never directly write or edit `slides.md` or `slides/*.md`
2. In build steps, output JSON ONLY (DeckSpec or SlidePatch)
3. Always validate JSON with `validate.py` before applying
4. Always provide `--project` flag to specify target directory
5. Apply changes ONLY using `apply_patch.py` or `render_deck.py`

## Styling & Components

### Tailwind / UnoCSS
Slidev supports Tailwind/UnoCSS out of the box. **Use it extensively.**
- Gradients: `bg-gradient-to-r from-blue-500 to-purple-600`
- Typography: `font-bold text-transparent bg-clip-text`
- Layouts: `grid grid-cols-2 gap-4 items-center`

### Custom Components
We ship with built-in Vue components in `components/`. Use them!

**FeatureCard**:
```html
<FeatureCard color-class="text-blue-500">
  <template #icon><ph-star-fill /></template> <!-- Requires icon pack -->
  <template #title>Amazing Feature</template>
  Description goes here.
</FeatureCard>
```

**StatBox**:
```html
<StatBox value="99%" label="Uptime" />
```

**StepList**:
```html
<StepList :steps="[{title: 'Step 1', desc: 'Do this'}, {title: 'Step 2', desc: 'Then this'}]" />
```

## Operating Modes

### Brainstorm Mode
- Discuss topic, audience, tone, and styling
- **Explicitly ask about Tailwind/UnoCSS preferences**
- Reference [brainstorm.md](reference/brainstorm.md)
- **Never write slide files in this mode**

### Build Mode (JSON-only)
Output one of:
- `DeckSpec` JSON (full deck)
- `SlidePatch` JSON (single slide)

The runner will:
- Validate JSON
- Apply patch or render deck to the **user's project**
- Audit for consistency
- Export to PPTX/PDF if requested

## Tool Commands

All tools require specifying the target project with `--project`:

**Initialize deck:**
```bash
python .claude/skills/authoring-slidev-decks/scripts/init_slidev_project.py ./my-deck --name "My Presentation" --install
```

**Validate JSON:**
```bash
python .claude/skills/authoring-slidev-decks/scripts/validate.py patch.json
```

**Apply slide patch:**
```bash
python .claude/skills/authoring-slidev-decks/scripts/apply_patch.py patch.json --project ./my-deck
```

**Render full deck:**
```bash
python .claude/skills/authoring-slidev-decks/scripts/render_deck.py deck.json --project ./my-deck
```

**Read deck state:**
```bash
python .claude/skills/authoring-slidev-decks/scripts/list_slides.py --project ./my-deck
python .claude/skills/authoring-slidev-decks/scripts/read_slide.py --no 3 --project ./my-deck
```

**Export:**
```bash
cd my-deck && npm run export
```

## Additional Resources

- **Workflow details**: [workflow.md](reference/workflow.md) - Step-by-step process
- **Schema contracts**: [schemas.md](reference/schemas.md) - DeckSpec and SlidePatch structure
- **Style guide**: [style-guide.md](reference/style-guide.md) - Layout and typography
- **Brainstorm guide**: [brainstorm.md](reference/brainstorm.md) - Guided outline creation
- **Themes**: [themes.md](reference/themes.md) - Curated color palettes
