from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


LIBRARY = Path(__file__).resolve().parents[1] / "references" / "expression-library.json"
CAPTIONS = Path(__file__).resolve().parents[1] / "references" / "caption-library.json"


def pick(items: list[dict], count: int, theme: str, seed: int | None) -> tuple[list[dict], int]:
    actual_seed = seed if seed is not None else random.SystemRandom().randrange(1, 2**63)
    rng = random.Random(actual_seed)
    candidates = [item for item in items if theme == "mixed" or theme in item["themes"]]
    if count > len(candidates):
        raise ValueError(f"theme {theme!r} only has {len(candidates)} expressions; requested {count}")

    by_family: dict[str, list[dict]] = {}
    for item in candidates:
        by_family.setdefault(item["family"], []).append(item)
    families = list(by_family)
    rng.shuffle(families)

    selected: list[dict] = []
    for family in families:
        if len(selected) == count:
            break
        selected.append(rng.choice(by_family[family]))

    remaining = [item for item in candidates if item["id"] not in {x["id"] for x in selected}]
    rng.shuffle(remaining)
    selected.extend(remaining[: count - len(selected)])
    rng.shuffle(selected)
    return selected, actual_seed


def attach_captions(selected: list[dict], rng: random.Random, mode: str) -> list[dict]:
    if mode == "none":
        return selected
    captions = json.loads(CAPTIONS.read_text(encoding="utf-8"))
    enriched = []
    for item in selected:
        copy = dict(item)
        options = captions.get(item["id"], [])
        copy["caption"] = rng.choice(options) if options else None
        enriched.append(copy)
    return enriched


def main() -> None:
    parser = argparse.ArgumentParser(description="Pick a diverse, reproducible static meme expression set")
    parser.add_argument("--count", type=int, default=9)
    parser.add_argument("--theme", default="mixed")
    parser.add_argument("--seed", type=int)
    parser.add_argument("--captions", choices=("none", "auto"), default="none")
    parser.add_argument("--format", choices=("json", "text"), default="json")
    args = parser.parse_args()

    items = json.loads(LIBRARY.read_text(encoding="utf-8"))
    themes = sorted({theme for item in items for theme in item["themes"]} | {"mixed"})
    if args.theme not in themes:
        parser.error(f"unknown theme {args.theme!r}; choose from: {', '.join(themes)}")
    selected, seed = pick(items, args.count, args.theme, args.seed)
    selected = attach_captions(selected, random.Random(seed ^ 0xC0DEC0DE), args.captions)
    payload = {"seed": seed, "theme": args.theme, "count": len(selected), "expressions": selected}
    if args.format == "json":
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"seed={seed} theme={args.theme}")
        for index, item in enumerate(selected, 1):
            caption = f" | caption={item['caption']}" if item.get("caption") else ""
            print(f"{index}. {item['id']} | {item['name_zh']} | {item['prompt']}{caption}")


if __name__ == "__main__":
    main()
