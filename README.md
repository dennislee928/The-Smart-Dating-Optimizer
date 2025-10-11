# 智慧社交改善器 (The Smart Dating Optimizer)

一個旨在透過數據分析與智慧自動化來提升社交軟體（Tinder, 心交等）配對與互動表現的工具。本專案整合了個人檔案 A/B 測試、配對對象分析以及可自訂策略的智慧滑卡功能。

## 核心功能 (Core Features)

- **📊 個人檔案 A/B 測試:** 自動輪換多組照片與自我介紹，並產出數據報告，分析各版本的配對成功率與訊息率。
- **🧠 AI 戀愛助理:** 分析你右滑的對象以及成功配對者的檔案特徵（關鍵字、照片風格），幫助你理解自己的偏好與市場吸引力。
- **🤖 智慧滑卡機器人:** 根據你自訂的規則或 AI 學習模型，自動化執行滑卡操作，只對高潛力對象按下喜歡，節省你的時間。
- **📈 表現儀表板:** 視覺化呈現你的配對數據、訊息回覆率等關鍵績效指標 (KPI)。

## 技術棧 (Tech Stack)

### 後端
- **語言:** Go 1.21+
- **框架:** Gin (HTTP Web Framework)
- **ORM:** GORM
- **資料庫:** PostgreSQL 15+ (Supabase)
- **認證:** JWT

### 自動化
- **語言:** Python 3.11+
- **瀏覽器自動化:** Playwright, Selenium
- **數據分析:** Pandas, NumPy
- **NLP:** NLTK, TextBlob
- **機器學習:** Scikit-learn

### CI/CD
- **GitHub Actions:** 自動化測試與部署
- **Docker:** 容器化部署
- **Kubernetes:** 生產環境編排 (可選)

## 快速開始 (Quick Start)

### 前置需求

- Go 1.21+
- Python 3.11+
- PostgreSQL 15+ (或使用 Docker)
- Git

### 安裝步驟

1. **克隆專案**
```bash
git clone https://github.com/yourusername/The-Smart-Dating-Optimizer.git
cd The-Smart-Dating-Optimizer
```

2. **設定環境變數**
```bash
cp config.env.template .env
# 編輯 .env 並填入必要資訊
```

3. **啟動資料庫 (使用 Docker)**
```bash
make docker-up
```

4. **安裝依賴**
```bash
# Go 依賴
make setup-go

# Python 依賴
make setup-python
```

5. **執行資料庫遷移**
```bash
make migrate-up
```

6. **啟動 API 伺服器**
```bash
make run-api
```

API 將在 `http://localhost:8080` 運行

7. **執行自動化腳本**
```bash
# 自動滑卡（10 次）
python main.py auto --count 10

# 生成統計報告
python main.py analyze

# AI 評分
python main.py aiscore
```

## 專案結構 (Project Structure)

```plaintext
smart-dating-optimizer/
├── automations/              # Python 自動化腳本
│   ├── tinder_bot.py        # Tinder 機器人
│   └── database_client.py   # 資料庫客戶端
├── analysis/                 # 數據分析模組
│   ├── profile_analyzer.py  # 個人檔案分析器
│   ├── ab_test_manager.py   # A/B 測試管理器
│   ├── stats_generator.py   # 統計報告生成器
│   └── ai_scorer.py         # AI 評分系統
├── cmd/                      # Go 應用程式入口
│   └── server/
│       └── main.go          # API 伺服器主程式
├── internal/                 # Go 內部套件
│   ├── model/               # GORM 資料模型
│   ├── dto/                 # 請求資料傳輸物件
│   ├── vo/                  # 回應值物件
│   ├── handler/             # HTTP 處理器
│   ├── service/             # 業務邏輯層
│   ├── repository/          # 資料存取層
│   ├── config/              # 設定管理
│   └── database/            # 資料庫連線
├── configs/                  # 設定檔
│   ├── profile_a.json       # 個人檔案 A
│   ├── profile_b.json       # 個人檔案 B
│   └── ab_test_config.json  # A/B 測試設定
├── database/                 # 資料庫相關
│   └── migrations/          # SQL 遷移檔案
├── Documents/                # 專案文檔
│   ├── database-schema.md
│   ├── API-Documentation.md
│   ├── Development-Guide.md
│   └── Deployment-Guide.md
├── .github/
│   └── workflows/
│       └── ci.yml           # CI/CD 流程
├── main.py                   # Python 主程式入口
├── go.mod                    # Go 模組定義
├── requirements.txt          # Python 依賴
├── Makefile                  # 建置指令
├── docker-compose.yml        # Docker 設定
└── README.md                 # 本文件
```

## 使用指南

### 1. 自動化滑卡

```bash
# 基本用法
python main.py auto --count 20

# 指定策略
python main.py auto --count 50 --strategy all_right

# 無頭模式
python main.py auto --count 100 --headless
```

### 2. A/B 測試

```bash
# 執行 A/B 測試
python main.py abtest --config configs/ab_test_config.json
```

### 3. 數據分析

```bash
# 生成統計報告
python main.py analyze --account-id 1

# 匯出 JSON
python main.py analyze --output reports/stats.json
```

### 4. AI 評分

```bash
# 使用預設規則評分
python main.py aiscore

# 使用訓練好的模型
python main.py aiscore --model models/scorer.pkl
```

### 5. API 使用

詳細 API 文件請參閱 [API Documentation](./Documents/API-Documentation.md)

Swagger UI: `http://localhost:8080/swagger/index.html`

## 開發指南

完整的開發指南請參閱 [Development Guide](./Documents/Development-Guide.md)

### 常用指令

```bash
# 執行測試
make test

# 格式化代碼
make fmt

# 生成 Swagger 文件
make swagger

# 清理建置產物
make clean
```

## 部署

詳細部署指南請參閱 [Deployment Guide](./Documents/Deployment-Guide.md)

### Docker 部署

```bash
# 啟動所有服務
docker-compose up -d

# 查看日誌
docker-compose logs -f api

# 停止服務
docker-compose down
```

## 文檔

- [資料庫架構設計](./Documents/database-schema.md)
- [API 文件](./Documents/API-Documentation.md)
- [開發指南](./Documents/Development-Guide.md)
- [部署指南](./Documents/Deployment-Guide.md)
- [開發藍圖](./dev_phase.md)

## 專案狀態

- ✅ Phase 1: 核心自動化引擎 (MVP)
- ✅ Phase 2: A/B 測試系統
- ✅ Phase 3: AI 戀愛助理
- ✅ Phase 4: 智慧滑卡系統
- 🚧 Phase 5: 前端儀表板 (開發中)

## 貢獻

歡迎貢獻！請參閱開發指南中的貢獻章節。

1. Fork 專案
2. 創建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 創建 Pull Request

## 授權

本專案採用 MIT 授權 - 詳見 LICENSE 檔案

## 免責聲明

本專案僅供教育和研究目的。使用自動化工具可能違反某些平台的服務條款。請謹慎使用並自行承擔風險。

## 聯絡方式

- 專案連結: [https://github.com/yourusername/The-Smart-Dating-Optimizer](https://github.com/yourusername/The-Smart-Dating-Optimizer)
- Issue Tracker: [GitHub Issues](https://github.com/yourusername/The-Smart-Dating-Optimizer/issues)
