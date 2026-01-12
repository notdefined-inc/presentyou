# Brainstorm Workflow

A guided process for creating amazing presentations. Follow these steps before building.

---

## Step 1: Understand the Topic

Ask these questions:
1. **What is the core message?** (One sentence summary)
2. **Who is the audience?** (Beginners, experts, stakeholders?)
3. **What's the goal?** (Inform, persuade, teach, inspire?)

---

## Step 2: Define the Tone

Choose one:
- **Professional** → Cream & Blue theme, formal language
- **Technical** → Dark Mode theme, code-heavy
- **Creative** → Vibrant Gradient theme, bold visuals
- **Minimal** → Light theme, distraction-free

---

## Step 3: Structure the Content

**Recommended 5-8 slide structure:**

| Slide | Purpose | Layout |
|-------|---------|--------|
| 1 | Title + Hook | `cover` |
| 2 | Problem/Context | `center` |
| 3-5 | Main Content | `default` or `two-cols` |
| 6 | Visual/Demo | `image-right` or component |
| 7 | Summary/Key Takeaways | `center` |
| 8 | Call to Action | `cover` |

---

## Step 4: Plan Visuals

For each slide, decide:
- [ ] Does it need an image? (Generate or stock)
- [ ] Does it need a diagram? (SVG or Mermaid)
- [ ] Does it need a Vue component? (Interactive demo)
- [ ] Does it need code? (Syntax highlighted block)

---

## Step 5: Review & Iterate

Before building:
- [ ] Is the slide count right? (5-10 is ideal)
- [ ] Is there visual variety? (Not all text slides)
- [ ] Does it flow logically? (Story arc)

---

## Example Brainstorm Output

```json
{
  "topic": "Introduction to Markdown",
  "audience": "Junior developers",
  "tone": "professional",
  "theme": "cream-blue",
  "slides": [
    {"no": 1, "title": "Markdown Magic", "layout": "cover", "visual": "background-image"},
    {"no": 2, "title": "What is Markdown?", "layout": "center", "visual": "svg-diagram"},
    {"no": 3, "title": "Basic Syntax", "layout": "two-cols", "visual": "code-example"},
    {"no": 4, "title": "Advanced Features", "layout": "default", "visual": "table"},
    {"no": 5, "title": "Try It Yourself", "layout": "center", "visual": "vue-component"}
  ]
}
```

Use this structure to guide deck generation!
