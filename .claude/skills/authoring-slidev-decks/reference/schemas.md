# Schema Contracts

## 1. SlidePatch
Used for updating a single slide.
- **`mode`**: Must be `"build"`.
- **`patch.no`**: Slide number (integer, 1-based).
- **`patch.content_md`**: The markdown content (including HTML/Vue).
- **`patch.frontmatter`**: Layout, classes, and background settings.
- **`patch.assets`**: Array of base64 or text assets to be written to disk.

## 2. DeckSpec
Used for defining the entire deck.
- **`deck.headmatter`**: Global config (theme, title, etc).
- **`deck.slides`**: Array of slide objects (same structure as patch).

## Validation
All JSON must pass:
```bash
python tools/validate.py --stdin --schema [patch|deck]
```
Unknown keys will cause validation failure.
