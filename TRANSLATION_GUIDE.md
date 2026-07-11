# Translation Guide — Hacking the Xbox 日本語訳

See `CLAUDE.md` for operational rules. This guide covers substance.

## Project scope

Japanese translation of:

> *Hacking the Xbox: An Introduction to Reverse Engineering*  
> Author: Andrew "bunnie" Huang  
> Copyright © 2003 by Xenatera LLC  
> Publisher: No Starch Press, San Francisco, CA  
> Original license: Creative Commons Attribution-NonCommercial-ShareAlike 1.0 (CC BY-NC-SA 1.0)  
> Free edition release: https://nostarch.com/xboxfree

The Japanese translation is also released under **CC BY-NC-SA 1.0**.

## Attribution requirements (mandatory in every chapter file)

Every `docs/ja/*.md` file must include the following visible footer `<small>` block:

```html
<small>
*原著*: *Hacking the Xbox: An Introduction to Reverse Engineering* © 2003 Xenatera LLC<br>
*著者*: Andrew "bunnie" Huang | *出版*: No Starch Press<br>
*本翻訳*: ニコ技深圳コミュニティ / 高須正和による日本語訳 — CC BY-NC-SA 1.0<br>
*翻訳・レビュー*: ニコ技深圳コミュニティ / 高須正和（@tks） — https://takasumasakazu.net<br>
*注記*: 本翻訳は、原著の Creative Commons ライセンス条件に従って公開する翻訳コントリビューションであり、著者 bunnie からも歓迎のコメントをいただいています。出版社による公式日本語版ではありません。
</small>
```

Never use the phrases "公式日本語版", "公認翻訳", or "正規翻訳".  
Do not describe the translation as "非公式日本語訳". Use "ニコ技深圳コミュニティ / 高須正和による日本語訳" in attribution credits and chapter footers. For the homepage hero title, use "日本語訳" only.

## Translation priorities

These four priorities override every specific rule below. Apply them in order when they conflict.

**1. Japanese reader clarity comes first.**  
Translate so a technically curious Japanese reader can understand the point without decoding English-shaped prose. If a literal technical term is obscure, explain the function first and add the formal term only if useful.

**2. Preserve bunnie's voice.**  
The target voice should feel like the Japanese edition of *The Hardware Hacker*: direct, practical, hands-on, hacker-oriented, essay-like, lightly conversational, and not academic. Use 「僕」 for bunnie's first-person narration. Prefer concrete verbs and short declarative sentences.

**3. Technical accuracy still matters.**  
Do not simplify by changing meaning. Preserve all technical facts, part numbers, signal names, figure/table references, commands, and source order.

**4. Translate meaning and function, not English syntax.**  
Rebuild sentences in natural Japanese. Do not carry over English noun chains, vague pronouns, hedges, or passive abstractions when they obscure the point.

## Voice target

The Japanese should sound like a working hacker explaining what he learned, not a textbook author summarizing a chapter.

- Use 「だ／だった」 prose where natural.
- Use practical verbs: いじる、つつく、たどる、探る、飛ばす、つながる、保つ、抑える。
- Replace textbook/report phrases:

| Avoid | Prefer |
|-------|--------|
| 「〜と考えることができる」 | 「〜だ」（assert directly） |
| 「〜に慰めを見出せる」 | 「〜ものだ」/「〜は救いだ」 |
| 「断続的な信頼性の問題」 | 「たまにしか再現しない不安定動作や間欠不良」 |
| 「〜に基づいて機能を推測する」 | 「〜を見て機能を推測する」 |
| 「〜することも助けになる」 | 「〜してみるといい」 |
| 「最も起きやすい問題は〜だ」 | 「〜が起きやすい」 |
| 「〜を最小化する」 | 「〜を抑える」 |
| 「エンジニアリング人材のプール」 | 「エンジニアの人材基盤」/「技術者の層」 |
| 「地下社会」（hackers） | 「アンダーグラウンドなコミュニティ」 |

## Reader-first terminology policy

Use standard Japanese electronics terms. If a term is too specialized for general readers, explain the function first, then give the term.

**First mention pattern:** Japanese explanation + formal Japanese term + English term (if useful)  
**After first mention:** natural Japanese term, no parentheses.

Do not overload sentences with parentheses. Prefer "what it does" over "what the English noun phrase literally says". Add 「つまり」 or apposition only when genuinely helpful. If a longer translator note is needed, leave a `<!-- TODO: -->` comment; do not insert long explanations into the main text.

| English | Preferred Japanese | Avoid |
|---------|-------------------|-------|
| printed circuit board / circuit board | プリント基板 / 基板 | 回路基板 (acceptable; prefer 基板 for short references) |
| trace / copper trace | 配線 / 配線パターン | 銅のトレース; 「トレース」 as standalone noun for conductors |
| netlist | 部品同士の接続関係（ネットリスト） | 回路図のネットリスト (unless CAD structure itself is the topic) |
| soldermask | はんだレジスト（soldermask）first use; then はんだレジスト | ソルダーマスク as primary term |
| pad / land | ランド / パッド | 開口部 (too abstract) |
| via | ビア (layer-connecting holes only) | do not use ビア for solder pads |
| resistor pack / RP | 抵抗アレイ（resistor pack） | 抵抗器パック |
| patterned copper | 銅箔の配線パターン | パターン銅 |
| fiberglass impregnated with epoxy | エポキシ樹脂を含ませたガラス繊維シート | エポキシを含浸させたガラス繊維 |
| thin polymer coating | 薄い樹脂膜 | ポリマーがコーティングされている |
| plating | めっき | メッキ |
| parasitics | 寄生成分 | パラサイティクス |
| decoupling capacitor | デカップリングコンデンサ | — |
| power plane | 電源プレーン | — |
| black art | 職人芸 | ブラックアート |
| intermittent reliability problem | たまにしか再現しない不安定動作や間欠不良 | 断続的な信頼性の問題 |
| signal tracing (following a path) | 信号の追跡 / 信号をたどる | — |

Good: 「その配線パターンには、部品同士の接続関係、つまりネットリストがそのまま刻み込まれている。」  
Good: 「部品をはんだ付けするためのランドやパッドだけは、はんだレジストがかからないようになっていて、銅のパターンが露出している。」

## Translation style

### Core rules
- **Faithful**: Translate every paragraph. Do not summarize, condense, or skip content.
- **Complete**: Do not omit paragraphs, sentences, footnotes, sidebars, or captions.
- **No invented text**: If source text is unclear or garbled from PDF extraction, mark with `<!-- TODO: verify: [description] -->`. Do not fabricate.
- **Preserve order**: Keep all paragraphs in original order. Do not reorganize.
- **Consult glossary.tsv** before translating technical terms. Add missing terms before translating.
- **Katakana** for established loanwords (ハッカー, ソルダー, フラックス, etc.). Kanji compounds for native-equivalent terms where natural.

### What to preserve verbatim
- Code, assembly listings, pseudocode, shell commands
- Hexadecimal values (e.g., `0xDEADBEEF`)
- Part numbers and order numbers (e.g., `MCM order number 22-3495`)
- URLs
- Figure numbers and table numbers (e.g., `Figure 1-1`, `Table 2-1`)
- Product names, company names, brand names (e.g., Xbox, Weller WTCPT, Kester 24-6337-8802)
- US Code citations (e.g., `17 U.S.C § 1201(f)`)
- Footnote numbers (preserve as superscripts)

### Sentence construction

**Rebuild sentences; do not mirror English syntax.** When a literal translation produces stacked relative clauses, unclear pronouns, or abstract noun chains, break or rephrase.

- Split long English sentences at natural pauses. "and / but / since / while / hence" chains → separate Japanese sentences.
- **"not because A, but because B"** → 「Aだからではない。Bだからこそ……」
- **Resolve ambiguous pronouns** from context. 「その」 alone is not enough if the referent is unclear; use the explicit noun.
- **Replace abstract noun endings with cause/effect.** Prefer 「XするとYが起きやすい」 over 「最も起きやすい問題はYだ」.
- **Avoid repeated adjacent subjects/locations.** Use 「手始めに」「次に」 or omit repeated context.
- **"secret" in security contexts** → 「秘密情報」「秘密鍵」or 「保護情報」 — never just 「秘密」.

Good (cause/effect):  
「飛ばしたコンデンサを交換せずにそのまま使うと、たまにしか再現しない不安定動作や間欠不良が起きやすい。」

Good (repeated subject removed):  
「Xboxのマザーボード上で、いくつかの信号をたどってみよう。手始めに、セクター8Cにある40ピンIDEコネクタJ8C1を見る。」

Good (security / secret):  
「安価なハードウェアクライアントに委ねられる秘密情報の重要度には、おのずと上限がある。安く大量に配布される機器を完全に守ることは難しい。だからこそ、その内部に置く秘密鍵や保護情報も、「破られたとしても許容できる範囲」に抑えるべきなのだ。」

### First-person pronoun
Use **「僕」** (not 「私」) for bunnie's first-person narration throughout.
- "I hack because..." → 「僕がハックするのは……」
- "my work / my research" → 「僕の仕事」 / 「僕の研究」

### Callout boxes

Source "sidebar" → heading uses **「コラム」** or **「囲み記事」**. Do **not** use 「サイドバー」 — in VitePress this sounds like site navigation.

```markdown
> **📦 コラム：なぜ基板の配線はあちこちで蛇行しているのか？**
>
> 翻訳テキスト...
```

"Note", "Tip", "Caution" callouts:
```markdown
> [!NOTE]
> 翻訳テキスト

> [!TIP]
> 翻訳テキスト

> [!WARNING]
> 翻訳テキスト
```

### YAML frontmatter

Any frontmatter value containing a colon must be quoted or written as a block scalar:
```yaml
details: >-
  翻訳・レビューはニコ技深圳コミュニティ / 高須正和（@tks）によるものです。
```
Applies to `details`, `tagline`, `description`, and any other frontmatter string field.

## Figure and caption handling

- Preserve every figure number exactly as printed: **Figure 1-1**, **Figure 2-3**, etc.
- Translate captions into Japanese below the image tag.
- Format:
  ```markdown
  ![Figure 1-1: A selection of security bits.](/images/page-034-img-01.png)
  **図1-1**: セキュリティビットの一覧。左から右へ：任天堂4.5mm、セキュリティトルクス、...
  ```
- If the image file has not yet been extracted:
  ```markdown
  <!-- TODO: insert Figure 1-1 — source: PDF page 34 -->
  ```
- Do not guess which image file corresponds to which figure. Only link images confirmed in `source/extract/figures-manifest.json`.

## Footnote handling

**Do NOT use Markdown footnote syntax** (`[^n]` / `[^n]:`). VitePress does not support it natively.

**Inline reference:**
```markdown
本文テキスト<sup>1</sup>続きのテキスト
```

**Footnote section:** add `## 注` after the last paragraph, before the `<small>` attribution footer:
```markdown
## 注

1. 原注テキスト（英語原文: "original English text"）
```

Rules: preserve original numbering; translate body text where possible; keep URLs verbatim; no HTML back-link anchors.

## LLM translation checklist

Before marking any section complete, verify all 15 items:

1. Japanese reader can understand the point without decoding English syntax.
2. bunnie's voice feels direct, practical, hacker-like, and essay-like.
3. 「僕」 is used for first-person narration.
4. No paragraphs, sentences, or footnotes are omitted.
5. No text is invented; unclear source is marked with a TODO comment.
6. Unclear pronouns and demonstratives are resolved to explicit nouns.
7. Technical terms follow the reader-first terminology table.
8. English terms are added only when useful, not for every technical noun.
9. No unnecessary katakana jargon (パラサイティクス, ブラックアート, etc.).
10. No stiff phrases such as 「〜と考えることができる」 when direct assertion is better.
11. No repeated adjacent subjects or locations in consecutive sentences.
12. Circuit behavior is explained by function or cause/effect, not abstract noun stacks.
13. PCB terms follow the terminology table (soldermask → はんだレジスト; trace → 配線).
14. Source "sidebar" headings are translated as 「コラム」 or 「囲み記事」, not 「サイドバー」.
15. Links, YAML, figures, and footnotes are valid; no mojibake or "\ufffd".
