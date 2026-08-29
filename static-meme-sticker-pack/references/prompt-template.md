# Prompt template

Use only the fields relevant to the request.

```text
Use case: identity-preserve
Asset type: static custom meme sticker pack
Input image: Image 1 is the sole identity reference.

Create a static meme sticker pack of the same [adult person / pet / character]. Preserve [identity invariants from the reference].

Style: [photo cutout / illustrated / chibi / pixel], exaggerated internet-reaction expressions, awkward readable poses, clean die-cut edges, friendly absurd humor.

Expressions in exact order:
1. [expression ID] — [visual prompt]
...

Layout: exactly [count] distinct stickers in a strict [rows]x[columns] grid on a square canvas. One complete subject per cell. Wide empty gaps. No overlap or elements crossing cell boundaries.

Background: [genuinely transparent RGBA for production / plain neutral preview background]. Never depict a checkerboard.

Constraints: same recognizable subject in every sticker; every expression and pose clearly different; no captions unless requested; no duplicated reactions; no extra subjects; no cropped head; no identity drift; no watermark.
```

For independent PNG production, replace the layout paragraph with:

```text
Generate only expression [ID] as one centered sticker on a square transparent RGBA canvas. Do not include a grid, other reactions, or a background.
```
