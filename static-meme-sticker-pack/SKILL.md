---
name: static-meme-sticker-pack
description: Create static custom meme sticker packs from a person, pet, or character reference image. Use when the user wants 2x2, 3x3, larger sticker grids, independent transparent PNG stickers, randomized reaction sets, or a reusable photo-to-meme workflow. Do not use for animated GIF or video stickers.
---

# Static meme sticker pack

Create a varied static sticker set while keeping the referenced subject recognizable.

## Inputs

Require a usable reference image and infer reasonable defaults for everything else. Ask only when a missing choice materially changes the result.

- Subject reference: person, pet, or fictional character.
- Count/layout: default to 9 stickers in a 3x3 preview sheet. Support 4/2x2, 9/3x3, 16/4x4, or independent files.
- Style: default to photographic low-fi meme cutouts for photos and preserve the source medium for illustrations.
- Delivery: default to one preview sheet; use independent transparent PNG generation when the user wants production-ready stickers.

If the subject is a real person, treat them as an adult unless the user clearly identifies otherwise. Keep styling non-sexual and do not imply that possession of a photo grants publication or commercial rights.

## Choose expressions

Do not claim to choose randomly in prose. Run `scripts/pick_expressions.py` so the selection is reproducible and contains no duplicates:

```powershell
python scripts/pick_expressions.py --count 9 --theme mixed
```

Use `--seed <integer>` when the user wants the same set again. Available themes and expression details live in `references/expression-library.json`; read that file only when the user wants to browse, add, remove, or manually select reactions.

Prefer variety across emotional families. A nine-sticker set should not be nine versions of happiness, crying, or surprise. Preserve the selected expression IDs in the final prompt or order manifest.

## Generate

Read `references/prompt-template.md` before generating the first asset in a task. Fill the template with the selected expressions and reference-image invariants.

For a quick social-media preview, generate one strict grid sheet. For deliverable stickers, generate each expression separately, remove its background, normalize canvas size, and compose a preview sheet afterward. Never turn a painted checkerboard into the final background; require actual alpha transparency for production PNGs.

Maintain across every sticker:

- Same recognizable identity, face shape, hairstyle/fur pattern, age impression, and skin/fur color.
- One subject per sticker and one distinct reaction per cell.
- Complete head and relevant gesture inside the cell.
- Wide gaps, no overlap, no captions unless requested.

If one sticker fails, regenerate only that expression. Do not reroll an accepted pack.

## Deliver

Report the selected expression names and seed. For a production pack, provide independent PNGs plus a sheet preview. Do not create animation unless the user changes the request.
