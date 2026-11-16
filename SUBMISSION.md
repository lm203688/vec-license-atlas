# 这份贡献是什么（提交用文案存档）

**标题**：vec-license-atlas — 虚拟细胞/胚胎生态的三层许可图谱（代码/权重/数据分开标注，27 项逐条核对）

**类别**：build（工具 + 数据集）

**公开链接**：https://github.com/lm203688/vec-license-atlas

## 一句话

在这个领域，「某模型是 MIT」这句话经常是错的：代码是宽松许可、权重是另一套、数据又是第三套，而核对成本被每个人重复支付——这份表把 27 个项目的三层许可逐条核对到原文，标出 7 个会让人踩坑的常见误判，并给出一张赛事数据的红线页。

## 它解决的具体问题

1. **代码/权重/数据三层不同**。`ArcInstitute/state`：代码 CC BY-NC-SA 4.0，权重与输出受 `State Model Non-Commercial License` + Acceptable Use Policy 约束——三层三套条款。
2. **仓库没有 LICENSE 文件 = 保留所有权利**。`A4Bio/CellVQ`、`guomics-lab/PTV-1` 属这一类，GitHub license API 均返回 404。传成"开源"会直接侵权。
3. **轻度 copyleft 被当成 MIT 传**。`bm2-lab/scPerturBench` 实为 **GPL-3.0**；改动再分发，衍生作品要开源。
4. **赛事数据不能替它发表**。Terms §14：数据集尚未发表，任何进论文或公开演示的使用须事先获 Dr. Neil Chi 与数据生成团队批准，发表须同时致谢 Dr. Qingquan Zhang 与 Dr. Neil Chi。

## 核对方法（可自己重跑）

- 代码层：GitHub 自身的 license 识别接口（`/repos/:owner/:repo/license`）给出 SPDX，比只看 README 徽章硬；
- 自定义条款：直接读 LICENSE / LICENSE.md / README 的版权段落原文并引用；
- 数据层：读官网条款原句；
- 无法直连复核的（HF 模型卡）显式标 `confidence=reported`，不冒充已核。

`python tools/build.py --check` 校验 27 行不变量（唯一性、取值集合、每行须有证据 URL 与日期、copyleft 与许可类型一致、非商业层不得标为可商用）；`--online` 额外 HEAD 每个证据 URL。

## 谁会用到

- 想用现成模型做产品、但不确定权重能不能商用的团队；
- 写评测、写教程、要把别人模型塞进 pipeline 的人；
- 准备把赛事数据结果写成论文、需要先判断"要不要先拿批准"的参赛者；
- 评审/导师，需要一张能追到原文的许可清单。

## 边界（写清楚，避免被读成过度承诺）

- **不是法律意见**，是核对过的线索；每行都给证据地址与日期，最终以对方 LICENSE 原文为准。
- 27 行覆盖的是本领域常见项目，不是全集；扩展靠 PR。
- 权重层的核查覆盖率低于代码层：很多项目仓库里只写"权重另见 Model License"，条款文本不在仓库内——本表如实标为 `unknown` 而不是猜一个。
- 需要联网的地方（HF 模型卡、证据 URL HEAD）在断网环境下会失败，这是设计上可接受的降级。

## 如何运行（写给下一个人）

```bash
git clone https://github.com/lm203688/vec-license-atlas
cd vec-license-atlas
python tools/build.py            # 重建 data/atlas.json 并校验
python tests/test_atlas.py       # 7 项不变量，纯标准库，无需 pytest
python tools/licctl.py --layer weights --status no
```

Python 3.9+，零第三方依赖。
