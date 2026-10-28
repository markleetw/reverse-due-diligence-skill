# 版本變更紀錄

正式發行版本以 GitHub Releases 為準。當前 `main` 可能有未發布修改；與英文 `CHANGELOG.md` 同步維護。正式 Release Notes 僅從有日期及版本號的章節產生。

## Unreleased

v1.0.0 發布後尚無新增變更。

## [1.0.0] - 2026-10-28

### 研究方法與安全

- 強化原始來源追溯、法律與監管風險推論、財務期間與分母檢查，區分公司體質與職位真正的決策權。
- 新增評分信心度與 **Not Assessed（未評估）**，強調條件式求職決策及 P0／P1／P2 面試問題。
- 更正台灣《當舖業法》第 11 條年利率上限為 30%，區分融資現金流的實際成本與個別法律是否適用。
- 強化 Prompt Injection 防護：外部網頁、職缺及附件只可作為不可信證據，不能指揮 AI 傳送求職者私人資料。

### 報告交付與驗證

- 加強決定性稽核：從交付的 HTML 擷取數值重算、檢查算術主張、完整文件結構及共用 Renderer 一致性。
- 將圖表提示與圖例的不可信字串安全地呈現為文字，增加 Chromium 的 XSS、深淺色、桌面及手機測試。
- 提供中英文完整虛構 Demo 與對應截圖，並對兩種語言加上 Renderer 一致性測試。
- 建立八情境研究評估規格；2026-10-28 已人工檢視五次代表性 Claude 實際研究，結果、未執行的項目與可重現性限制詳見 `evals/README.md`。此結果不能當成統計性模型品質基準。

### 封裝、發版與文件

- 提供可重現的九檔 Skill ZIP，包含 MIT 授權條款及內部 VERSION。
- 建立受保護分支的 PR／CI 閘門，分離只驗證、不發布的 RC 與需明確授權的正式 Release。
- 補齊中英文安裝說明、資料來源與保密限制、貢獻及安全性文件。

## v0.2.0 — 2026-10-08

既有正式版本：[v0.2.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.2.0)。後續尚未發布的修改不得誤列成當時已發行內容。

歷史版本：[v0.1.2](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.2)、[v0.1.1](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.1)、[v0.1.0](https://github.com/markleetw/reverse-due-diligence-skill/releases/tag/v0.1.0)。
