# Static Meme Sticker Pack

一个用于生成静态定制表情包的 Agent Skill。

上传人物、宠物或虚拟角色参考图，Skill 会从 56 种反应中随机抽取不重复组合，生成 2×2、3×3、4×4 表情包或独立透明 PNG。随机结果带 seed，可以重复生成同一套表情。

## 效果示例

### 人物表情包

![人物静态表情包示例 1](assets/examples/person-sticker-pack-01.png)

![人物静态表情包示例 2](assets/examples/person-sticker-pack-02.png)

### 宠物表情包

![宠物静态表情包示例](assets/examples/pet-sticker-pack.png)

> 示例图片仅用于展示生成效果。使用真人、宠物、品牌或第三方角色参考图前，请确认自己拥有相应授权。

## 功能

- 内置 56 种静态表情，覆盖 14 个情绪家族
- 随机抽取且不重复，避免九张都是相似表情
- 支持 `2×2`、`3×3`、`4×4` 和独立贴纸
- 支持人物、宠物和虚拟角色参考图
- 尽量保持脸型、发型、肤色、毛色和角色辨识度
- 支持主题筛选和随机 seed 复现
- 支持快速整页预览与独立透明 PNG 生产模式
- 某一张失败时只返工该表情，不重做已确认内容

## 支持的主题

| 主题 | 适合场景 |
| --- | --- |
| `mixed` | 默认混合，情绪覆盖最丰富 |
| `cute` | 可爱、撒娇、害羞、呆萌 |
| `cool` | 墨镜、胜利、大佬感 |
| `sarcastic` | 侧眼、无语、礼貌鼓掌、扶额 |
| `dramatic` | 大哭、暴怒、震惊、逃跑 |
| `love` | 比心、飞吻、心动、心碎 |
| `celebration` | 彩纸、欢呼、派对、胜利 |
| `work` | 上班耗尽、咖啡续命、敬礼 |

## 安装

克隆仓库：

```bash
git clone https://github.com/luotovo/static-meme-sticker-pack.git
```

将仓库中的 `static-meme-sticker-pack` 文件夹复制到你的 Agent Skill 目录。

Codex 默认位置：

```text
$CODEX_HOME/skills/static-meme-sticker-pack
```

如果使用其他支持 `SKILL.md` 的 Agent，也可以直接导入整个 `static-meme-sticker-pack` 文件夹。

## 快速使用

上传参考图后发送：

```text
使用 static-meme-sticker-pack。
用这张参考图生成3×3静态表情包，
从mixed表情库随机抽取，不要重复。
```

也可以指定主题：

```text
使用 static-meme-sticker-pack。
用参考图生成2×2宠物表情包，
主题选择sarcastic，输出一张预览图。
```

如果需要正式贴纸文件：

```text
使用 static-meme-sticker-pack。
随机生成9种不重复表情，
每种表情分别输出独立透明PNG，
最后再合成一张3×3预览图。
```

## 随机抽取表情

Skill 使用脚本完成真实随机选择，而不是让模型口头模拟随机。

```bash
python static-meme-sticker-pack/scripts/pick_expressions.py \
  --count 9 \
  --theme mixed
```

输出会包含本次随机 seed 和完整表情顺序。

使用相同 seed 可以复现同一套组合：

```bash
python static-meme-sticker-pack/scripts/pick_expressions.py \
  --count 9 \
  --theme mixed \
  --seed 7756822817661310282
```

输出纯文本列表：

```bash
python static-meme-sticker-pack/scripts/pick_expressions.py \
  --count 9 \
  --theme cute \
  --format text
```

## 两种生成模式

### 快速预览

一次生成完整宫格，适合社交媒体发布和确认整体效果。速度较快，但单个表情不方便单独返工。

### 生产模式

逐张生成独立贴纸，再合成预览页。适合交付和长期使用：

- 单张失败可以单独重做
- 人物身份和表情更容易控制
- 可以获得真正透明的 PNG
- 后续可以继续制作 GIF、WebP 或平台贴纸包

## 表情库

完整表情定义位于：

```text
static-meme-sticker-pack/references/expression-library.json
```

每个表情包含：

- 唯一 ID
- 中文名称
- 情绪家族
- 可用主题
- 可视化动作提示词

你可以直接修改 JSON 增加自己的表情，只需确保 `id` 不重复。

## 目录结构

```text
static-meme-sticker-pack/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── expression-library.json
│   └── prompt-template.md
└── scripts/
    └── pick_expressions.py
```

## 使用提醒

- 生成模型无法保证每个宫格中的人物完全一致。
- 正式交付建议逐张生成，而不是只生成一张九宫格。
- 棋盘格图案不等于真实透明背景，生产 PNG 应检查 Alpha 通道。
- 使用真人照片前，请获得本人同意并确认肖像权与发布范围。
- 本 Skill 不自动授予照片、角色、Logo、服装或其他第三方素材的商业使用权。

## License

[MIT License](LICENSE)
