# 安裝 Reverse Due Diligence Skill

建議一律從 GitHub Release 下載，不要直接把 repo 整包下載後自行壓縮。Release 產物已經過 CI 驗證，且使用固定檔案順序、時間戳與權限做 reproducible build。

## Claude

依 Anthropic 目前的官方文件，自訂 Skill 以 **ZIP** 上傳。

1. 到本 repo 的 **Releases** 下載最新的 `reverse-due-diligence.zip`。
2. 確認 Claude 已啟用 Skill 所需功能：
   - Free / Pro / Max：到 **設定 > 功能**，確認已啟用程式碼執行與檔案建立。
   - Team / Enterprise：需由組織管理員在 **組織設定 > 外掛程式與技能 > 政策** 開啟相關能力。
3. 到 **自訂 > 技能**。
4. 點 **+** → **建立技能** → **上傳技能**。
5. 選擇剛下載的 `reverse-due-diligence.zip`。
6. 上傳後將 Skill 開啟。

之後可以直接輸入：

```text
/rdd 台積電 資深工程師
```

或用自然語言，例如：

```text
我正在面試某家公司 Head of Product，幫我做反向盡調。
```

Anthropic 官方說明：
https://support.claude.com/zh-TW/articles/12512180-%E5%9C%A8-claude-%E4%B8%AD%E4%BD%BF%E7%94%A8%E6%8A%80%E8%83%BD

## ChatGPT

依 OpenAI 目前的官方文件，ChatGPT Skills 提供給符合資格的 **Business、Enterprise、Healthcare、Edu** 工作區，並受工作區權限與產品開放狀態影響。

1. 到本 repo 的 **Releases** 下載最新的 `reverse-due-diligence.zip`。
2. 在 ChatGPT 左側邊欄進入 **外掛程式**。
3. 打開 **外掛程式目錄** → **技能**。
4. 點 **建立** → **從電腦上傳**。
5. 選擇 `reverse-due-diligence.zip`。
6. 等待 ChatGPT 完成安全掃描後即可使用。

Release 也會提供 `reverse-due-diligence.skill`。它和 ZIP 內容完全相同，主要方便保留 Skill artifact 的語意；若你的介面接受 `.skill`，也可以直接使用。若不確定，請優先上傳 ZIP。

如果你看不到「技能」分頁，通常是以下其中一種情況：

- 目前方案／工作區尚未開放 ChatGPT Skills
- 工作區管理員尚未啟用 Skill 建立或上傳權限
- 該功能尚未在你的產品介面提供

OpenAI 官方說明：
https://help.openai.com/en/articles/20001066-skills-in-chatgpt

OpenAI Agent Skills 格式說明：
https://developers.openai.com/api/docs/guides/tools-skills

## 驗證下載檔

每個 Release 會附上 `SHA256SUMS.txt`。

macOS / Linux：

```bash
shasum -a 256 reverse-due-diligence.zip
```

或：

```bash
sha256sum reverse-due-diligence.zip
```

比對結果是否與 `SHA256SUMS.txt` 一致。

## 安全提醒

Skill 可以包含指令、script 與其他資源。從任何第三方下載 Skill 前，都應先確認來源與內容。

這個 repo 的 source code 全部公開；Release package 只包含執行 RDD 所需的 runtime files，不包含 CI、開發測試檔或其他隱藏內容。
