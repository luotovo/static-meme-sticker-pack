---
name: static-meme-sticker-pack
description: Create static custom meme sticker packs from a person, pet, or character reference image. Use for 2x2, 3x3, or 4x4 sheets, randomized reaction sets, Chinese captions, independent transparent PNG stickers, and platform-ready exports. Do not use for animated GIF or video stickers.
---

# Static meme sticker pack

Create varied, recognizable static stickers from one reference subject. Infer safe defaults and ask only when a missing choice materially changes the result.

## Select a mode

- `quick`: one complete grid for ideation or social posting. Default when the user only asks for a grid.
- `standard`: generate independent stickers, check them, then compose a preview. Use for reusable PNGs.
- `pro`: standard mode plus captions, unified outline, platform preset, manifest, and stricter quality checks. Use for delivery.

Default to 9 stickers, `3x3`, `mixed`, intensity `3/5`, no captions, and the source visual medium. Keep real-person styling non-sexual and do not imply that possessing a photo grants publication or commercial rights.

## Choose expressions

Use the deterministic picker; never simulate randomness in prose:

```powershell
python scripts/pick_expressions.py --count 9 --theme mixed
```

Add `--captions auto` when captions are requested and `--seed <integer>` to reproduce a set. Supported themes are derived from the library and include `mixed`, `cute`, `cool`, `sarcastic`, `dramatic`, `love`, `celebration`, `work`, `chat`, `gaming`, and `festival`.

Read `references/expression-library.json` only when browsing or editing reactions. Read `references/caption-library.json` only when captions are involved. Preserve selected IDs, order, captions, and seed in the manifest or final report.

## Preserve identity

Extract a short invariant list before generation:

- person: face shape, age impression, hairstyle, hair color, skin tone, distinctive accessories;
- pet: species, breed impression, fur pattern, eye color, ear shape, distinctive markings;
- character: silhouette, palette, costume anchors, medium, and signature features.

Do not silently change age, gender presentation, species, fur pattern, or signature costume. Preserve the source outfit unless the user requests a replacement. One sticker contains exactly one subject.

## Generate

Read `references/prompt-template.md` before generating the first asset. Set expression intensity from `1/5` subtle to `5/5` absurdly exaggerated. Captions should normally be added after image generation so Chinese text stays legible.

For `quick`, generate one strict grid. For `standard` or `pro`, generate each selected expression as a separate square transparent RGBA image. If one fails, regenerate only that ID; do not reroll accepted work.

Check each result for:

- recognizable identity and one distinct reaction;
- no extra subject, duplicated limb, cropped head, or cell overlap;
- complete readable gesture with safe margins;
- correct caption and no generated gibberish;
- genuine alpha transparency rather than a painted checkerboard.

## Finish production packs

Run the post-processor only after independent PNGs exist:

```powershell
python scripts/build_pack.py --input-dir input --output-dir output --platform generic --strict-alpha
```

It normalizes canvases, adds a white die-cut outline, composes `preview.png`, writes `manifest.json`, and reports alpha/edge problems. Available presets: `generic`, `wechat`, `telegram`, `whatsapp`, and `discord`.

For captions, provide a JSON object that maps each input filename stem to final text:

```json
{"01-polite-smile": "好的呢", "02-clock-out": "下班！"}
```

Then pass `--captions captions.json`. Keep Chinese captions short, generally at most six characters, and do not cover the face.

## Deliver

For quick mode, return the sheet plus the selected expression list and seed. For production modes, return `stickers/`, `preview.png`, and `manifest.json`; summarize any quality warnings. Do not claim an image is transparent unless the alpha check passed. Do not create animation unless the user changes the request.
