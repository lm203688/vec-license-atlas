# vec-license-atlas

**三层许可图谱：虚拟细胞 / 虚拟胚胎系统里，代码、权重、数据各自能做什么。**
A three-layer license atlas for virtual-cell / virtual-embryo work — code, weights and data, annotated separately, each row backed by the actual license text.

> 这份表不是法律意见。它是**核对过的线索**：每一行都给出证据地址和核查日期，你可以用 `tools/build.py --check` 自己重跑一遍。
> Not legal advice. Every row carries an evidence URL and a check date; re-run the checks yourself with `tools/build.py --check`.

---

**永久标识 / Permanent DOI:** [10.5281/zenodo.24274064](https://doi.org/10.5281/zenodo.24274064)
![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24274064.svg)
版本 DOI 指向 v1.0.0；概念 DOI [10.5281/zenodo.24274063](https://doi.org/10.5281/zenodo.24274063) 自动指向全部版本。
The version DOI above identifies v1.0.0; the concept DOI [10.5281/zenodo.24274063](https://doi.org/10.5281/zenodo.24274063) always resolves to the latest version.

Archived copy: https://zenodo.org/records/24274064 (Zenodo, filed 2026-11-16)


---

## 为什么需要它

在这个领域里，「某个模型是 MIT」这句话通常是错的。真实情况有三种：

1. **代码是宽松许可，权重是另一套**。`ArcInstitute/state`：代码 CC BY-NC-SA 4.0，权重是另一份 `State Model Non-Commercial License`，**输出**还要额外受 Acceptable Use Policy 约束。三层、三套条款。
2. **仓库根本没有 LICENSE 文件，所以默认"保留所有权利"**。`A4Bio/CellVQ`、`guomics-lab/PTV-1` 都属这一类。没有 LICENSE ≠ 可以随便用。
3. **轻度 copyleft 被当成 MIT 传**。`bm2-lab/scPerturBench` 是 **GPL-3.0**，不是 MIT。改动它再分发，你的衍生作品也要开源。

一个人花三小时能做完的核对，一百个人就要各花三小时。这份表就是那三小时的合并版。

---

## 60 秒用法

```bash
# 1. 我能不能把某个模型用在商业产品上？（看权重层，不是代码层）
python tools/licctl.py --layer weights --status no

# 2. 哪些仓库压根没有许可文件（默认不能用）？
python tools/licctl.py --no-license

# 3. 哪些是 copyleft，分发衍生作品要开源？
python tools/licctl.py --copyleft

# 4. 查一个具体项目
python tools/licctl.py --search state

# 5. 导出机读结果给自己的脚本用
python tools/licctl.py --json > my_audit.json
```

零依赖，只用 Python 标准库。数据在 [`data/atlas.csv`](data/atlas.csv)（人读）和 `data/atlas.json`（机读，由 `tools/build.py` 生成）。

---

## 本表纠正的 7 个常见说法

| 常见说法 | 核对后的结论 | 证据 |
|---|---|---|
| scPerturBench 是 MIT | **GPL-3.0**，copyleft，分发衍生作品须开源 | `bm2-lab/scPerturBench/LICENSE`，GitHub license API 判为 GPL-3.0 |
| OpenFold3 许可"见仓库" | **Apache-2.0** | `aqlaboratory/openfold/LICENSE` |
| Protenix 许可"见仓库" | **Apache-2.0** | `bytedance/Protenix/LICENSE` |
| RF3 权重另算 | **BSD-3-Clause，且 LICENSE 明文覆盖模型权重**（"covers both the source code and model weights"） | `RosettaCommons/foundry/LICENSE.md` |
| CellVQ 开源可商用 | **仓库无 LICENSE 文件**，默认保留所有权利 | GitHub license API 对该仓库返回 404 |
| PTV-1 代码开源 | **仓库无 LICENSE 文件**；数据矩阵另受 PTDS 学术非商业条款约束 | 同上 + PTV-1 README |
| cz-benchmarks 许可不明 | **MIT**（LICENSE.md 是外包装文字，API 因格式判为 NOASSERTION） | `chanzuckerberg/cz-benchmarks/LICENSE.md` |

还有一条是**对我自己上一版表的纠错**：scFoundation 的权重我上一版写成"非商业研究"。核对原文后只能说——README 明示「任何对 Model Weights 的使用或利用均受独立的 Model License 约束」，但**该条款文本不在仓库里**。所以正确结论是"权重层存在独立条款、内容未公开在此仓库"，而不是我上一版那句笃定的话。

---

## 三层分别怎么看

| 层 | 你会踩的坑 | 本表字段 |
|---|---|---|
| **代码** | 宽松 vs copyleft；无 LICENSE 文件 = 不能用 | `code_license` / `copyleft` / `commercial_code` |
| **权重** | 代码 MIT 不代表权重 MIT；权重常是"非商业研究"或自定义条款 | `weights_license` / `commercial_weights` |
| **数据** | 训练数据条款会传导到产出；赛事数据另有发表审批 | `data_license` |

`commercial_*` 三态：`yes` / `no` / `unknown`。**`unknown` 是需要你亲自去问的情况，不要当 `yes` 用。**

---

## 赛事数据红线

见 [`docs/data-redlines.md`](docs/data-redlines.md)。核心一句原文（Virtual Embryo Challenge Terms §14）：

> 数据集仅用于研究与教育目的；数据集尚未发表，**任何在论文或公开演示中的使用，须事先获得 Dr. Neil Chi 与数据生成团队批准**；发表时须同时致谢 Dr. Qingquan Zhang 与 Dr. Neil Chi。

---

## 验证方法（可复现）

```bash
python tools/build.py --check
```

它会校验：项目名唯一、许可证取值在允许集合内、每行都有证据 URL 与核查日期、`copyleft` 与 GPL 类许可一致、非商业许可不得标为 `commercial=yes`。
`--online` 会额外对每行的证据 URL 发起 HEAD 请求（需要联网）。

数据来源分三类，表里 `method` 字段标注：
- `github_license_api` — 由 GitHub 自身的许可识别给出 SPDX，最硬；
- `license_text` / `readme_statement` — 直接读仓库里的 LICENSE / README 原文；
- `terms_page` — 官网条款原句；
- `reported` — 二手来源（如 HF 模型卡），**本轮未能直连复核**，`confidence=reported`。

---

## 目录

```
data/atlas.csv        27 行三层许可表（人读）
data/atlas.json       同上，机读，含 method / confidence
tools/licctl.py       查询 CLI，零依赖
tools/build.py        CSV→JSON 构建 + 一致性校验（--check / --online）
docs/data-redlines.md 赛事数据红线与三个判决示例
tests/test_atlas.py   表结构不变量测试
```

## 许可

代码 MIT，表数据 CC0（见 `LICENSE` 与 `data/README.md`）。欢迎 PR 补行或纠错——请附证据 URL 与日期。
