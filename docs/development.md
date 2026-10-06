# Development

這份文件給維護 repo 的人看。

## 結構

```text
.
├── SKILL.md
├── references/
│   ├── analysis-playbook.md
│   ├── report-template.md
│   ├── taiwan-sources.md
│   └── global-sources.md
├── templates/
│   └── report-shell.html
├── scripts/
│   ├── audit.py
│   ├── package.py
│   └── check_repo.py
└── .github/workflows/
    ├── ci.yml
    ├── publish.yml
    └── release.yml
```

- `SKILL.md`：流程控制，只放「何時啟動」與「下一步做什麼」
- `references/`：分析方法與證據規則的單一來源
- `templates/`：報告樣板
- `scripts/`：audit、package、repo checks

## 本機檢查

```bash
python scripts/check_repo.py
```

## Audit

```bash
python scripts/audit.py report.html audit-spec.json
```

audit spec 只放單次研究的舊值、canonical values 與算術檢查；不要把特定公司資料寫進通用 script。

## 發版

更新 `VERSION` 後 push 到 `main`：

```bash
echo 0.2.0 > VERSION
git add VERSION
git commit -m "release: v0.2.0"
git push
```

GitHub Actions 會自動驗證、建立 tag、打包 ZIP 並更新 GitHub Release。
