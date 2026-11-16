# data/ — 表数据的授权与口径

## 授权

`atlas.csv` 与 `atlas.json` 以 **CC0 1.0** 发布：随便复制、改写、商用、再分发，不必署名。这样做是故意的——一张许可表被越多项目引用，它的纠错就来得越快。

## 但要清楚：表里记录的许可不属于本仓库

每一行的 `code_license` / `weights_license` / `data_license` 是对**别人项目**的观察记录，不是本仓库对这些项目作出的授权。要不要用、怎么用，以对方仓库的 LICENSE 原文为准——本表给的是线索和入口。

## 口径

- `method` 字段说明这一行的结论是怎么得到的：
  - `github_license_api` —— GitHub 自身的许可识别给出的 SPDX（最硬）；
  - `license_text` / `readme_statement` —— 直接读仓库 LICENSE / README 原文；
  - `terms_page` —— 官网条款原句；
  - `reported` —— 二手来源，**本轮未直连复核**。
- `confidence`：`verified` / `mixed`（部分层已核，部分层未核）/ `reported`（整体未复核）。
- `commercial_code` / `commercial_weights` 三态：`yes` / `no` / `unknown`。**`unknown` 不等于可以，等于需要你去问。**
- `none-found`：该仓库没有 LICENSE 文件。按默认著作权规则，这等于保留所有权利，不能当作"开源"使用。

## 怎么纠错

提 PR 或在 issue 里贴：项目名、你认为正确的结论、**一句原文引用**、证据 URL、核查日期。只有结论没有原文的修改不会合并——这张表的价值全在"能指回原文"。
