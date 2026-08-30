# Prompt templates

## Shared identity block

```text
Use Image 1 as the sole identity reference for the same [adult person / pet / fictional character].
Identity invariants: [face or fur features, age impression, hair, color palette, signature accessories, source outfit unless replaced].
Keep the subject immediately recognizable. Do not change age, gender presentation, species, fur markings, or signature costume.

Visual direction: [photographic low-fi cutout / illustrated / chibi / pixel], friendly absurd internet-reaction humor, intensity [1-5]/5, readable pose, clean die-cut silhouette.
```

## Quick grid

Append:

```text
Create exactly [count] distinct stickers in a strict [rows]x[columns] grid on one square canvas.

Expressions in exact order:
1. [ID] — [visual prompt]
...

One complete subject per cell. Wide empty gaps. No overlap or elements crossing cells. No captions unless explicitly listed. Use a plain neutral preview background; never paint a checkerboard. No duplicate reactions, extra subjects, cropped head, identity drift, watermark, or illegible text.
```

## Independent production sticker

Append:

```text
Generate only [ID] — [visual prompt] as one centered sticker on a square genuinely transparent RGBA canvas. Do not include a grid, other reactions, caption, scenery, drop shadow, or background. Keep generous transparent padding around the complete silhouette.
```

Add captions later with `scripts/build_pack.py` unless the user explicitly prefers model-rendered lettering.

## Intensity guide

- `1/5`: subtle facial change, almost no effect marks.
- `2/5`: clear reaction, restrained pose.
- `3/5`: default meme exaggeration and one readable gesture.
- `4/5`: large gesture, strong distortion, comic effect marks.
- `5/5`: absurd internet-reaction energy while identity remains recognizable.
