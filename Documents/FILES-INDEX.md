# 專案檔案索引

本文件提供專案中所有重要檔案的快速索引和說明。

## 📁 根目錄檔案

| 檔案 | 說明 |
|------|------|
| `README.md` | 專案主要說明文件 |
| `dev_phase.md` | 開發階段規劃 |
| `main.py` | Python 主程式入口 |
| `go.mod` | Go 模組定義 |
| `requirements.txt` | Python 依賴清單 |
| `Makefile` | 建置與開發指令 |
| `docker-compose.yml` | Docker 服務編排 |
| `Dockerfile.api` | API 服務 Docker 映像 |
| `.gitignore` | Git 忽略規則 |
| `LICENSE` | MIT 授權條款 |
| `config.env.template` | 環境變數範本 |

## 📂 automations/ - Python 自動化腳本

| 檔案 | 行數 | 說明 |
|------|------|------|
| `tinder_bot.py` | ~400 | Tinder 自動化機器人 |
| `database_client.py` | ~200 | 資料庫客戶端 |

**功能**:
- 瀏覽器自動化（Playwright）
- 自動滑卡
- 個人檔案資料抓取
- 配對檢測
- 資料儲存

## 📂 analysis/ - 數據分析模組

| 檔案 | 行數 | 說明 |
|------|------|------|
| `profile_analyzer.py` | ~250 | 個人檔案 NLP 分析 |
| `ab_test_manager.py` | ~180 | A/B 測試管理器 |
| `stats_generator.py` | ~220 | 統計報告生成器 |
| `ai_scorer.py` | ~300 | AI 評分系統 |

**功能**:
- 關鍵字提取（NLTK）
- 情感分析（TextBlob）
- 興趣偵測
- A/B 測試結果分析
- 統計報告生成
- AI 評分與推薦

## 📂 cmd/server/ - Go 應用程式入口

| 檔案 | 行數 | 說明 |
|------|------|------|
| `main.go` | ~150 | API 伺服器主程式 |

**功能**:
- API 路由設定
- 中介層配置
- 依賴注入
- 健康檢查

## 📂 internal/ - Go 內部套件

### internal/model/ - GORM 資料模型

| 檔案 | 說明 |
|------|------|
| `user.go` | 使用者模型 |
| `dating_account.go` | 社交帳號模型 |
| `profile.go` | 個人檔案模型（含 JSONB 型別） |
| `ab_test.go` | A/B 測試模型 |
| `swipe_record.go` | 滑卡記錄模型 |
| `match.go` | 配對模型 |
| `message.go` | 訊息模型 |
| `analytics_snapshot.go` | 分析快照模型 |
| `ai_model.go` | AI 模型配置 |
| `automation_log.go` | 自動化日誌模型 |

**共 10 個模型，總計 ~800 行**

### internal/dto/ - 請求資料傳輸物件

| 檔案 | 說明 |
|------|------|
| `user_dto.go` | 使用者相關 DTO |
| `dating_account_dto.go` | 社交帳號 DTO |
| `profile_dto.go` | 個人檔案 DTO |
| `ab_test_dto.go` | A/B 測試 DTO |
| `swipe_dto.go` | 滑卡記錄 DTO |

**共 5 個檔案，總計 ~300 行**

### internal/vo/ - 回應值物件

| 檔案 | 說明 |
|------|------|
| `user_vo.go` | 使用者回應 VO |
| `dating_account_vo.go` | 社交帳號 VO |
| `profile_vo.go` | 個人檔案 VO |
| `ab_test_vo.go` | A/B 測試結果 VO |
| `swipe_vo.go` | 滑卡記錄 VO |
| `analytics_vo.go` | 分析統計 VO |
| `common_vo.go` | 通用回應結構 |

**共 7 個檔案，總計 ~400 行**

### internal/repository/ - 資料存取層

| 檔案 | 行數 | 說明 |
|------|------|------|
| `user_repository.go` | ~80 | 使用者資料操作 |
| `swipe_repository.go` | ~150 | 滑卡記錄操作 |

### internal/service/ - 業務邏輯層

| 檔案 | 行數 | 說明 |
|------|------|------|
| `user_service.go` | ~150 | 使用者業務邏輯 |

### internal/handler/ - HTTP 處理器

| 檔案 | 行數 | 說明 |
|------|------|------|
| `user_handler.go` | ~150 | 使用者 API 處理器 |

### internal/config/ - 設定管理

| 檔案 | 行數 | 說明 |
|------|------|------|
| `config.go` | ~80 | 應用程式設定載入 |

### internal/database/ - 資料庫連線

| 檔案 | 行數 | 說明 |
|------|------|------|
| `database.go` | ~80 | 資料庫初始化與遷移 |

## 📂 configs/ - 設定檔

| 檔案 | 說明 |
|------|------|
| `profile_a.json` | 個人檔案 A 範本 |
| `profile_b.json` | 個人檔案 B 範本 |
| `ab_test_config.json` | A/B 測試設定範本 |

## 📂 database/migrations/ - 資料庫遷移

| 檔案 | 行數 | 說明 |
|------|------|------|
| `20251011000001_init_schema.up.sql` | ~200 | 初始 schema 建立 |
| `20251011000001_init_schema.down.sql` | ~15 | Schema 回滾 |

**資料表**: users, dating_accounts, profiles, ab_tests, swipe_records, matches, messages, analytics_snapshots, ai_models, automation_logs

## 📂 Documents/ - 專案文檔

| 檔案 | 行數 | 說明 |
|------|------|------|
| `database-schema.md` | ~350 | 資料庫架構設計 |
| `API-Documentation.md` | ~400 | 完整 API 文件 |
| `Development-Guide.md` | ~600 | 開發指南 |
| `Deployment-Guide.md` | ~600 | 部署指南 |
| `PROJECT-SUMMARY.md` | ~500 | 專案實作總結 |
| `QUICK-START-GUIDE.md` | ~200 | 5 分鐘快速開始 |
| `FILES-INDEX.md` | ~200 | 本檔案索引 |

**共 7 個文檔，總計 ~2,850 行**

## 📂 .github/workflows/ - CI/CD

| 檔案 | 行數 | 說明 |
|------|------|------|
| `ci.yml` | ~150 | GitHub Actions CI 流程 |

**包含**: Go 測試、Python 測試、Migration 檢查、安全掃描

## 📊 統計總結

### 程式碼統計

| 類別 | 檔案數 | 總行數 |
|------|--------|--------|
| **Go 程式碼** | 30 | ~3,000 |
| **Python 程式碼** | 7 | ~2,500 |
| **SQL** | 2 | ~400 |
| **設定檔** | 6 | ~500 |
| **文檔** | 8 | ~3,000 |
| **總計** | 53 | **~9,400** |

### Go 套件結構

```
internal/
├── model/       (10 檔案, ~800 行)
├── dto/         (5 檔案, ~300 行)
├── vo/          (7 檔案, ~400 行)
├── repository/  (2 檔案, ~230 行)
├── service/     (1 檔案, ~150 行)
├── handler/     (1 檔案, ~150 行)
├── config/      (1 檔案, ~80 行)
└── database/    (1 檔案, ~80 行)
```

### Python 模組結構

```
automations/     (2 檔案, ~600 行)
analysis/        (4 檔案, ~950 行)
main.py          (1 檔案, ~200 行)
```

## 🔍 快速查找

### 尋找特定功能

| 功能 | 相關檔案 |
|------|----------|
| **自動化滑卡** | `automations/tinder_bot.py` |
| **AI 評分** | `analysis/ai_scorer.py` |
| **A/B 測試** | `analysis/ab_test_manager.py` |
| **統計分析** | `analysis/stats_generator.py` |
| **NLP 分析** | `analysis/profile_analyzer.py` |
| **使用者註冊/登入** | `internal/handler/user_handler.go`, `internal/service/user_service.go` |
| **資料庫模型** | `internal/model/*.go` |
| **API 端點** | `cmd/server/main.go`, `internal/handler/*.go` |

### 尋找設定

| 設定類型 | 檔案位置 |
|----------|----------|
| **環境變數** | `config.env.template` |
| **資料庫 Schema** | `database/migrations/*.sql` |
| **Docker 設定** | `docker-compose.yml`, `Dockerfile.api` |
| **CI/CD 設定** | `.github/workflows/ci.yml` |
| **個人檔案範本** | `configs/profile_*.json` |
| **A/B 測試設定** | `configs/ab_test_config.json` |

### 尋找文檔

| 主題 | 文件 |
|------|------|
| **快速開始** | `Documents/QUICK-START-GUIDE.md` |
| **API 參考** | `Documents/API-Documentation.md` |
| **開發指南** | `Documents/Development-Guide.md` |
| **部署指南** | `Documents/Deployment-Guide.md` |
| **資料庫設計** | `Documents/database-schema.md` |
| **專案總結** | `Documents/PROJECT-SUMMARY.md` |
| **開發階段** | `dev_phase.md` |

## 📝 檔案命名規範

### Go 檔案
- **Model**: `{entity}.go` (例如: `user.go`)
- **DTO**: `{entity}_dto.go`
- **VO**: `{entity}_vo.go`
- **Repository**: `{entity}_repository.go`
- **Service**: `{entity}_service.go`
- **Handler**: `{entity}_handler.go`

### Python 檔案
- **模組**: `{module_name}.py` (snake_case)
- **類別**: PascalCase
- **函式**: snake_case

### SQL 檔案
- **Migration**: `YYYYMMDDHHMMSS_description.{up|down}.sql`

### 設定檔
- **JSON**: `{name}_config.json` 或 `{name}.json`
- **YAML**: `{name}.yml` 或 `{name}.yaml`
- **環境變數**: `.env`, `config.env.template`

## 🔗 相關連結

- [專案 README](../README.md)
- [開發藍圖](../dev_phase.md)
- [LICENSE](../LICENSE)

---

**更新日期**: 2025-10-11  
**版本**: 1.0.0

