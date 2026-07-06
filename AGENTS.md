# Project Workspace Instructions

本 project 是工作區，不是正式 shared skills repo。

## 正式 Skill 來源

正式 shared skills repo：

```text
%USERPROFILE%\.agents\skills
```

正式 shared skills 必須回到 shared skills repo 維護。project-local active skills 必須由該 project 的 `overview.md`、`AGENTS.md` 與 `skills\overview.md` 明確記錄。

## Project Init 入口

初始化或檢查 project workspace 時，正式共用入口是 shared skills repo 的 bootstrap script：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.agents\skills\scripts\bootstrap\init-codex-project.ps1" -ProjectPath "<project path>"
```

預設 dry-run；只有加上 `-Apply` 才會寫入 project `AGENTS.md`、`AGENTS.workspace-rules-template.md`、`_codex` 或初始化報告。路徑必須使用 `%USERPROFILE%` 或 `$env:USERPROFILE`，不得硬寫 `C:\Users\<name>`。

## AI 產物位置

```text
_codex
```

建議結構：

```text
_codex\inbox
_codex\work
_codex\deliverables
_codex\archive
_codex\tmp
_codex\assets
_codex\logs
_codex\reports
_codex\drafts\skills
```

- `_codex\work\YYYYMMDD-topic` 放每次任務的草稿、檢查紀錄、腳本與 README。
- `_codex\deliverables` 只放已確認可交付給使用者的最終輸出。
- `_codex\tmp` 只放可重建的暫存檔。
- `_codex\reports` 放不隸屬單一 session 的 project-level AI 報告。
- skill 草稿只能放 `_codex\drafts\skills`。

## 禁止事項

- project 內不得建立 `.agents\skills` 作為正式 skill 來源。
- 不得把 `_codex\drafts\skills` 內的內容視為正式 skill。
- 不得把 `_codex` 內的草稿視為正式 shared skill。
- 不得自動刪除不確定檔案。
- 不得自動 commit / push。
- 不得建立 symlink 作為預設整理方式。

## Folder README First Rule

When adding, moving, organizing, or editing files inside a folder:

- First check whether the target folder or its parent folders contain `README.md`, `readme.md`, `00.README.md`, `AGENTS.md`, or similar local guidance.
- Read the most relevant local guidance before deciding where files belong or how they should be changed.
- Treat README guidance as context, not blind authority: compare it with the actual folder structure and the current user request.
- If the README defines intake, naming, current/legacy/reference, archive, version-history, or safety rules, follow those rules unless the user explicitly overrides them.
- After adding or reorganizing files, update the relevant README when the directory structure, current entry point, version history, or usage guidance has changed.
- If the correct location is unclear, report candidate locations and reasoning before moving files.

## Windows / OneDrive Encoding Rule

When organizing or editing OneDrive folders that contain BAT/PS1/TXT/MD files with Chinese text:

- Prefer a saved Python organizer for multi-step moves, README generation, or validation.
- Do not use long Windows PowerShell 5 here-strings or opaque inline commands to write Chinese text.
- Write machine-readable JSON/hooks as UTF-8 no BOM; use UTF-8 BOM only for human README/Markdown that needs Windows compatibility, and mark that exception.
- Preserve legacy BAT/TXT/EXE bytes; do not transcode old scripts unless explicitly requested.
- Do not repeat sensitive values such as `PWD=` or `-pw` in README, reports, or chat replies.
- Put Codex-created organizer scripts and reports under `_codex/work/YYYYMMDD-topic/` by default; use `_codex/reports/` only for project-level AI reports that are not session-specific.

## 發現 SKILL.md

發現 `SKILL.md` 時，只列報告分類，不自動刪除或搬移。

報告欄位至少包含：

| 欄位            | 說明                                                                                                                        |
| --------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Path            | 檔案或資料夾路徑                                                                                                            |
| Type            | File / Directory                                                                                                            |
| Marker          | `SKILL.md` 或疑似 skills directory                                                                                          |
| Classification  | ActiveProjectLocalSkill / DraftSkill / LegacyAiWorkResidue / ArchivedMigrationSkill / BackupSkill / ResidualSkill / Unknown |
| SuggestedAction | 保留 / 待確認 / 搬移候選 / 歸檔候選 / 刪除候選                                                                              |
| RiskLevel       | Low / Medium / High                                                                                                         |
| Notes           | 判斷理由                                                                                                                    |

## 文件輸出

若產生架構、流程或規則，必須輸出 Markdown；涉及流程時使用 Mermaid。
