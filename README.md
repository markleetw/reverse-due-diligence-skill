# Reverse Due Diligence Skill

給求職者使用的 AI Agent Skill。  
在投履歷、面試或接受 offer 前，用公開資料反向調查公司與職缺。

## 它會幫你做什麼

- 判斷公司財務、營運與結構性風險
- 拆解職缺的實際權責、KPI、資源與決策空間
- 產出「值不值得去」的判斷與面試提問清單

## 安裝

到 [Releases](https://github.com/markleetw/reverse-due-diligence-skill/releases) 下載最新的 `reverse-due-diligence.zip`。

**ChatGPT**

`外掛程式 → 外掛程式目錄 → 技能 → 建立 → 從電腦上傳`

**Claude**

`自訂 → 技能 → + → 建立技能 → 上傳技能`

完整步驟請看 [安裝說明](docs/install.md)。

## 使用

直接告訴 AI 公司、職缺，以及你想做的決定：

```text
/rdd 台積電 資深工程師
/rdd 某某公司 Head of Product，幫我判斷值不值得接
```

如果有 JD、offer、獵頭訊息或內部人士說法，也可以一起提供。

---

開發與維護資訊請看 [Development](docs/development.md)。
