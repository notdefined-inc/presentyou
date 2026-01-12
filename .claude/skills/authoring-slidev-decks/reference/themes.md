# Design Themes & Color Palettes

Curated themes for beautiful Slidev presentations. Use these in your `frontmatter.class` or custom CSS.

---

## 1. Cream & Blue (Professional)

A calm, professional palette perfect for business and educational presentations.

| Element | Color | CSS/Tailwind |
|---------|-------|--------------|
| Background | Cream `#F5F5DC` | `bg-[#F5F5DC]` |
| Text | Navy `#0047AB` | `text-[#0047AB]` |
| Accent | Royal Blue `#4169E1` | `text-[#4169E1]` |
| Highlight | Light Blue `#87CEEB` | `bg-[#87CEEB]` |

**Frontmatter example:**
```yaml
class: text-[#0047AB] bg-[#F5F5DC]
```

---

## 2. Dark Mode (Developer)

Modern, eye-friendly theme for technical presentations.

| Element | Color | CSS/Tailwind |
|---------|-------|--------------|
| Background | Slate `#1E293B` | `bg-slate-800` |
| Text | White | `text-white` |
| Accent | Cyan `#22D3EE` | `text-cyan-400` |
| Code BG | Dark `#0F172A` | `bg-slate-900` |

**Frontmatter example:**
```yaml
class: text-white bg-slate-800
```

---

## 3. Vibrant Gradient (Creative)

Bold, energetic theme for creative and startup presentations.

| Element | Color | CSS/Tailwind |
|---------|-------|--------------|
| Background | Purple-Pink Gradient | `bg-gradient-to-r from-purple-600 to-pink-500` |
| Text | White | `text-white` |
| Accent | Yellow `#FBBF24` | `text-yellow-400` |

**Frontmatter example:**
```yaml
class: text-white bg-gradient-to-r from-purple-600 to-pink-500
```

---

## 4. Minimal Light

Clean, distraction-free theme for documentation.

| Element | Color | CSS/Tailwind |
|---------|-------|--------------|
| Background | White | `bg-white` |
| Text | Gray `#374151` | `text-gray-700` |
| Accent | Blue `#3B82F6` | `text-blue-500` |

---

## Typography Recommendations

- **Headers**: Use Inter, Outfit, or Roboto for modern feel
- **Body**: Keep font-size at least 18px for readability
- **Bullet points**: Max 6 per slide, 1 line each

## Layout Best Practices

| Layout | Use Case |
|--------|----------|
| `cover` | Title slides, section breaks |
| `center` | Key quotes, important statements |
| `two-cols` | Comparisons, code vs output |
| `default` | Standard content slides |
| `image-right` | Content with visual support |
