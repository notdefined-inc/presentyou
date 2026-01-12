# Style Guide & Layout Rules

## 1. Layouts
Prefer these built-in layouts:
- **`cover`**: For the first slide. Bold text, full background.
- **`intro`**: For section headers.
- **`two-cols`**: For comparing concepts (e.g. "Old vs New").
- **`default`**: For standard bullet points.

## 2. Typography
- Use `###` for sub-headings on slides.
- Keep bullet points short (1 line ideal).
- Use `**bold**` for key terms.

## 3. Colors
- Use Tailwind classes in `frontmatter.class` (e.g., `text-white bg-black`).
- Avoid hardcoded hex codes in Markdown; use utility classes.

## 4. Images
- Store images in `public/images/`.
- Reference them via `/images/filename.png` in frontmatter.
- Use `assets` in JSON to deliver image content (base64).
