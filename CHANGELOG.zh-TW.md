# 版本變更紀錄

正式發行版本以 GitHub Releases 為準。`main` 可能包含尚未發布的修改；這份檔案與英文 `CHANGELOG.md` 應同步維護。

## Unreleased

### 研究品質

- 修正監管風險推論與 Prompt Injection 防護，強化來源可信度判斷。
- 增加評分信心度與 **Not Assessed（未評估）**，避免將未知事項硬填分數。
- 更正台灣當舖法定年利率的錯誤比較基準，區分不同金融費率與實際資金成本。
- 將數字稽核改為可從報告實際內容取值，再驗算承重主張。

### 安全性與驗證

- 圖表提示與圖例的動態文字改為安全文字節點，並加入惡意 HTML 標籤的 Chromium 測試。
- 建立研究回歸情境與人工評估 Rubric；尚未實際執行的 AI 研究測試會標示為 NOT RUN。

### 開源文件

- 採用 MIT 授權，補齊英文與台灣繁中 README、貢獻與安全性政策、GitHub 範本。

## v0.2.0 — 2026-10-08

既有正式版本：[v0.2.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.2.0)。後續尚未發布的修改不得誤列成當時已發行內容。

歷史版本：[v0.1.2](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.2)、[v0.1.1](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.1)、[v0.1.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.0)。
