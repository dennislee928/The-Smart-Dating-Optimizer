# 開發指南

## 專案架構

```
smart-dating-optimizer/
├── automations/          # Python 自動化腳本
│   ├── tinder_bot.py    # Tinder 機器人
│   └── database_client.py
├── analysis/            # 數據分析模組
│   ├── profile_analyzer.py
│   ├── ab_test_manager.py
│   ├── stats_generator.py
│   └── ai_scorer.py
├── cmd/                 # Go 應用程式入口
│   └── server/
│       └── main.go
├── internal/            # Go 內部套件
│   ├── model/          # GORM 資料模型
│   ├── dto/            # 請求資料傳輸物件
│   ├── vo/             # 回應值物件
│   ├── handler/        # HTTP 處理器
│   ├── service/        # 業務邏輯層
│   ├── repository/     # 資料存取層
│   ├── config/         # 設定管理
│   └── database/       # 資料庫連線
├── configs/            # 設定檔
├── database/           # 資料庫相關
│   └── migrations/     # SQL 遷移檔案
├── dashboard/          # 前端儀表板（待開發）
└── Documents/          # 專案文檔
```

## 技術棧

### 後端
- **語言**: Go 1.21+
- **框架**: Gin (HTTP)
- **ORM**: GORM
- **資料庫**: PostgreSQL 15+
- **認證**: JWT

### 自動化
- **語言**: Python 3.11+
- **瀏覽器自動化**: Playwright
- **數據分析**: Pandas, NumPy
- **NLP**: NLTK, TextBlob
- **機器學習**: Scikit-learn

### 前端（規劃中）
- **框架**: Next.js 14+
- **語言**: TypeScript
- **UI 庫**: Tailwind CSS
- **狀態管理**: Zustand
- **API 客戶端**: 從 Swagger 自動生成

## 本地開發環境設置

### 1. 安裝依賴

#### Go 依賴
```bash
make setup-go
```

#### Python 依賴
```bash
make setup-python
```

### 2. 設定資料庫

使用 Docker Compose 啟動 PostgreSQL：
```bash
make docker-up
```

或手動安裝 PostgreSQL 並建立資料庫：
```bash
createdb smart_dating_optimizer
```

### 3. 執行 Migration

```bash
make migrate-up
```

### 4. 設定環境變數

複製範本檔案：
```bash
cp config.env.template .env
```

編輯 `.env` 並填入必要資訊。

### 5. 啟動開發伺服器

#### Go API 伺服器
```bash
make run-api
```

API 將在 `http://localhost:8080` 運行。

#### Python 自動化
```bash
python main.py auto --count 10
```

## 開發流程

### 1. 分支策略

- `main`: 生產環境分支
- `develop`: 開發分支
- `feature/*`: 功能分支
- `bugfix/*`: 錯誤修復分支

### 2. 提交流程

1. 從 `develop` 創建功能分支
2. 開發並提交變更
3. 執行測試：`make test`
4. 執行格式化：`make fmt`
5. 提交 Pull Request 至 `develop`
6. 通過 CI 檢查和代碼審查
7. 合併至 `develop`

### 3. 提交訊息規範

使用 Conventional Commits 格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**類型 (type):**
- `feat`: 新功能
- `fix`: 錯誤修復
- `docs`: 文檔變更
- `style`: 代碼格式（不影響功能）
- `refactor`: 重構
- `test`: 測試相關
- `chore`: 建置流程或輔助工具變更

**範例:**
```
feat(api): 新增 A/B 測試結果 API

實現取得 A/B 測試結果的 API 端點，包含統計分析和勝者判定。

Closes #123
```

## 測試

### 執行所有測試
```bash
make test
```

### 執行 Go 測試
```bash
make test-go
```

### 執行 Python 測試
```bash
make test-python
```

### 測試覆蓋率

測試完成後會生成覆蓋率報告：
- Go: `coverage.html`
- Python: `htmlcov/index.html`

## 代碼風格

### Go

遵循官方 Go 代碼風格：
- 使用 `gofmt` 格式化
- 使用 `go vet` 檢查
- 遵循 Effective Go 指南

### Python

遵循 PEP 8：
- 使用 `black` 格式化
- 使用 `isort` 排序 import
- 使用 `flake8` 檢查

## 資料庫遷移

### 創建新的 Migration

1. 在 `database/migrations/` 建立新檔案：
   - Up: `YYYYMMDDHHMMSS_description.up.sql`
   - Down: `YYYYMMDDHHMMSS_description.down.sql`

2. 在 Up 檔案中編寫 DDL
3. 在 Down 檔案中編寫回滾 DDL
4. 執行 migration：`make migrate-up`

**注意事項:**
- 禁止修改已執行的 migration 檔案
- 確保 down migration 可以正確回滾
- 在 staging 環境測試後再部署到生產

## API 開發

### 新增 API 端點流程

1. **定義 DTO/VO** (`internal/dto/`, `internal/vo/`)
   ```go
   type CreateResourceRequest struct {
       Name string `json:"name" binding:"required"`
   }
   ```

2. **更新 Model** (如需要) (`internal/model/`)

3. **實現 Repository** (`internal/repository/`)
   ```go
   func (r *repo) Create(resource *model.Resource) error
   ```

4. **實現 Service** (`internal/service/`)
   ```go
   func (s *service) Create(req *dto.CreateResourceRequest) (*vo.ResourceVO, error)
   ```

5. **實現 Handler** (`internal/handler/`)
   ```go
   func (h *handler) Create(c *gin.Context)
   ```

6. **註冊路由** (`cmd/server/main.go`)

7. **新增 Swagger 註解**

8. **編寫單元測試**

## Swagger 文件

### 生成 Swagger

```bash
make swagger
```

### 查看 Swagger UI

啟動 API 伺服器後訪問：
```
http://localhost:8080/swagger/index.html
```

### Swagger 註解範例

```go
// CreateResource 建立資源
// @Summary 建立新資源
// @Description 建立新的資源並返回資源資訊
// @Tags resources
// @Accept json
// @Produce json
// @Param request body dto.CreateResourceRequest true "建立請求"
// @Success 201 {object} vo.Response
// @Failure 400 {object} vo.Response
// @Router /api/v1/resources [post]
func (h *handler) CreateResource(c *gin.Context) {
    // Implementation
}
```

## 除錯技巧

### Go 除錯

使用 Delve 除錯器：
```bash
dlv debug cmd/server/main.go
```

### Python 除錯

使用 pdb：
```python
import pdb; pdb.set_trace()
```

### 資料庫查詢

使用 pgAdmin：
```
http://localhost:5050
```

或使用 psql：
```bash
psql -h localhost -U postgres -d smart_dating_optimizer
```

## 常見問題

### 資料庫連線失敗

檢查環境變數設定和 PostgreSQL 服務狀態：
```bash
docker-compose ps
```

### Import 錯誤

確保 Go module 路徑正確：
```bash
go mod tidy
```

### Python 套件衝突

使用虛擬環境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

## 效能優化

### 資料庫查詢優化

1. 使用適當的索引
2. 避免 N+1 查詢
3. 使用 `Preload` 預載關聯
4. 使用批次操作

### API 效能

1. 實現分頁
2. 使用快取 (Redis)
3. 壓縮回應
4. 使用 CDN（靜態資源）

## 安全最佳實踐

1. **永不提交敏感資料**
   - 使用 `.env` 儲存機密
   - 將 `.env` 加入 `.gitignore`

2. **密碼處理**
   - 使用 bcrypt 加密
   - 最小長度 8 字元

3. **SQL 注入防護**
   - 使用 ORM 參數化查詢
   - 驗證使用者輸入

4. **API 安全**
   - 實現速率限制
   - 使用 HTTPS
   - 驗證 JWT token

## 貢獻指南

歡迎貢獻！請遵循以下步驟：

1. Fork 專案
2. 創建功能分支
3. 提交變更
4. 推送到分支
5. 創建 Pull Request

請確保：
- 代碼通過所有測試
- 遵循代碼風格
- 更新相關文檔
- 提供清晰的提交訊息

