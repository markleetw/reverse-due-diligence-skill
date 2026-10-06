# Reverse Due Diligence Skill

給求職者使用的 AI Agent Skill：在投履歷、進入面試流程或接受 offer 前，用公開資料反向調查雇主。

RDD（Reverse Due Diligence，反向盡職調查）的目標不是做一份漂亮的公司簡介，而是把公開資訊轉成**可以拿來做職涯決策的判斷**：公司體質如何、這個角色到底有多少實權，以及面試現場該問什麼。

## 這個 Skill 會回答什麼

1. **這家公司會不會有事？**
   財務體質、現金流、營收結構、股權、低潮期、監管與結構性風險。

2. **這個角色有沒有實權與資源？**
   權責邊界、KPI、匯報線、預算與 headcount 彈性，以及產品／業務／財務誰真正掌握決策權。

3. **面試現場該問什麼？**
   面試題不是通用題庫，而是從調查結果反推出來，並附上「為什麼問」與「什麼答案是紅旗」。

## 運作流程

```text
確認公司／角色／決策問題
        ↓
釘住法律實體與公司事實骨架
        ↓
平行蒐集財務、股權、營收、組織、文化、敘事
        ↓
深挖商業模式與結構性風險
        ↓
證據分級、交叉驗證、不確定性標註
        ↓
收斂成職涯判斷
        ↓
產生面試提問清單
        ↓
輸出 HTML 報告
        ↓
Deterministic audit
```

## 安裝

請直接從 [Releases](https://github.com/markleetw/reverse-due-diligence-skill/releases) 下載最新版本。

- **Claude**：建議下載 `reverse-due-diligence.zip`
- **ChatGPT**：建議下載 `reverse-due-diligence.zip`；Release 同時提供內容相同的 `.skill` 檔

完整安裝步驟請看 [`docs/install.md`](docs/install.md)。

> ChatGPT Skills 目前只開放給符合資格的 Business、Enterprise、Healthcare 與 Edu 工作區，且仍受工作區設定影響。如果你的 ChatGPT 看不到「外掛程式 > 技能」，通常代表目前方案／工作區尚未提供，或管理員尚未開啟相關權限。

## 使用方式

常見輸入：

```text
/rdd 台積電 資深工程師
/rdd 星圖科技 Head of Product
/rdd 某某公司 資深 PM 想知道值不值得接
```

Skill 最理想的輸入有三項：

- **公司**：公司名、品牌名或股票代號
- **角色**：應徵職缺或預計加入的角色
- **決策問題**：要不要投、要不要繼續面、要不要接 offer、怎麼談薪等

如果有 JD、offer、獵頭訊息或內部人士說法，也可以一起提供；Skill 會依證據強度分開處理，不會把口述資訊直接當成事實。

## Repo 結構

```text
.
├── README.md
├── SKILL.md                         # Orchestrator：決定何時啟動、下一步做什麼
├── docs/
│   └── install.md                   # Claude / ChatGPT 安裝方式
├── references/
│   ├── analysis-playbook.md         # 分析方法、證據紀律、QA heuristics
│   ├── report-template.md           # 報告資訊架構
│   ├── taiwan-sources.md            # 台灣資料來源
│   └── global-sources.md            # 海外／外商資料來源
├── templates/
│   └── report-shell.html            # 自包含 HTML 報告樣板與圖表函式
├── scripts/
│   ├── audit.py                     # 通用 deterministic audit
│   ├── package.py                   # 建立 release package
│   └── check_repo.py                # Repo 一致性與 smoke test
├── examples/
│   └── audit-spec.example.json
└── .github/workflows/
    ├── ci.yml
    └── release.yml
```

### 各層責任

- **`SKILL.md`**：只負責「什麼情況啟動」與「工作流程怎麼走」。
- **`references/`**：分析方法與證據規則的單一事實來源。
- **`templates/`**：可重複使用的輸出樣板。
- **`scripts/`**：適合 deterministic 處理的事情，例如殘留掃描、算術驗證、打包與 repo 檢查。
- **`docs/`**：給人看的使用與安裝說明。

## 報告稽核

`scripts/audit.py` 是通用稽核引擎，不包含任何特定公司的數字。每次研究會另外產生一份 audit spec：

```bash
python3 scripts/audit.py report.html audit-spec.json
```

audit spec 可以定義：

- 不應再出現的舊值／舊主張
- 必須存在的 canonical values
- 已解決但不應再被寫成「查不到」的主張
- 算術恆等式與結構性約束

這套 audit 檢查的是**報告內部是否自洽**，不是替代原始來源查證。

## 開發與維護原則

1. **同一條規則只維護一份。**
   詳細 evidence / QA 規則放在 playbook，不要再複製到 `SKILL.md`。

2. **Reusable file 不放特定公司 state。**
   特定公司的數字、舊值與檢查條件屬於單次研究產物，不應硬編碼在通用 script 或 template。

3. **Deterministic 的問題用程式檢查。**
   算術、舊值殘留、路徑、package contents、reproducible build 不靠 LLM 重讀。

4. **案例用來教方法，不用來暗示真實公司。**
   playbook 內的案例以明確標示的虛構公司為主，數字只供教學。

## 打包與 Release

Git repo 是 source of truth；可安裝的 Skill 是 release artifact，不回寫進 repo。

本機打包：

```bash
python scripts/package.py --output dist/reverse-due-diligence.skill
```

正式發布有兩種方式：

```bash
# 方式一：更新 VERSION 後 push 到 main
echo 0.1.0 > VERSION
git add VERSION
git commit -m "release: v0.1.0"
git push

# 方式二：直接建立 tag
git tag v0.1.0
git push origin v0.1.0
```

`VERSION` 變更時，Publish workflow 會先跑 repo checks，再自動建立對應的 `vX.Y.Z` tag；正式 Release 仍以 tag 為版本識別。

當 `v*` tag 被建立後，GitHub Actions 會：

1. 跑完整 CI
2. 建立 reproducible package
3. 產出 `.skill` 與 `.zip`
4. 產生 SHA-256 checksum
5. 建立／更新對應的 GitHub Release
6. 把安裝指引與版本變更寫入 Release page

同一份 source tree 重複打包，產物必須 byte-for-byte 一致。
