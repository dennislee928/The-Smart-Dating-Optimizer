# 快速開始指南

這是一份 5 分鐘快速開始指南，讓你快速運行 Smart Dating Optimizer。

## 前置需求檢查

確保你已安裝以下工具：

```bash
# 檢查 Go 版本
go version  # 需要 1.21+

# 檢查 Python 版本
python --version  # 需要 3.11+

# 檢查 Docker
docker --version
docker-compose --version
```

如果缺少任何工具，請先安裝：
- [Go 安裝](https://golang.org/dl/)
- [Python 安裝](https://www.python.org/downloads/)
- [Docker 安裝](https://docs.docker.com/get-docker/)

## 一鍵啟動（使用 Docker）

### 步驟 1: 克隆專案

```bash
git clone https://github.com/yourusername/The-Smart-Dating-Optimizer.git
cd The-Smart-Dating-Optimizer
```

### 步驟 2: 設定環境變數

```bash
# 複製範本
cp config.env.template .env

# 使用預設值（開發環境）
# 或編輯 .env 檔案自訂設定
```

### 步驟 3: 啟動所有服務

```bash
# 一鍵啟動資料庫和 API
make docker-up
```

等待約 30 秒讓服務完全啟動。

### 步驟 4: 驗證安裝

```bash
# 檢查健康狀態
curl http://localhost:8080/health
```

應該看到：
```json
{
  "status": "ok",
  "message": "Smart Dating Optimizer API is running"
}
```

### 步驟 5: 安裝 Python 依賴

```bash
# 建立虛擬環境（建議）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate     # Windows

# 安裝依賴
pip install -r requirements.txt

# 安裝 Playwright 瀏覽器
playwright install
```

## 快速測試

### 1. 測試 API

```bash
# 註冊新使用者
curl -X POST http://localhost:8080/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "username": "testuser"
  }'
```

### 2. 測試 Python 自動化

```bash
# AI 評分測試
python main.py aiscore
```

### 3. 測試統計分析

```bash
# 生成統計報告
python main.py analyze
```

## 訪問服務

- **API 端點**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/swagger/index.html
- **pgAdmin**: http://localhost:5050
  - Email: `admin@example.com`
  - Password: `admin`

## 常見問題

### 問題 1: 無法連接資料庫

**解決方案**:
```bash
# 重啟 Docker 服務
make docker-down
make docker-up

# 檢查容器狀態
docker-compose ps
```

### 問題 2: Go 模組錯誤

**解決方案**:
```bash
go mod download
go mod tidy
```

### 問題 3: Python 套件衝突

**解決方案**:
```bash
# 使用虛擬環境
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 問題 4: Port 被占用

**解決方案**:
```bash
# 修改 .env 中的 SERVER_PORT
# 或停止占用該 port 的服務
```

## 下一步

### 開始使用

1. **查看 API 文件**
   ```
   http://localhost:8080/swagger/index.html
   ```

2. **執行自動化滑卡**
   ```bash
   python main.py auto --count 10
   ```

3. **設置 A/B 測試**
   - 編輯 `configs/profile_a.json` 和 `configs/profile_b.json`
   - 執行: `python main.py abtest`

### 深入學習

- 📖 [開發指南](./Development-Guide.md) - 學習如何開發新功能
- 🚀 [部署指南](./Deployment-Guide.md) - 學習如何部署到生產環境
- 📊 [API 文件](./API-Documentation.md) - 完整的 API 參考

## 停止服務

```bash
# 停止所有 Docker 服務
make docker-down

# 或手動停止
docker-compose down
```

## 完全清理

如果你想完全移除所有資料：

```bash
# 停止並刪除所有容器和資料
docker-compose down -v

# 清理建置產物
make clean
```

## 取得幫助

- 查看 [README](../README.md)
- 閱讀 [專案總結](./PROJECT-SUMMARY.md)
- 提交 [GitHub Issue](https://github.com/yourusername/The-Smart-Dating-Optimizer/issues)

---

**恭喜！** 你已經成功設置了 Smart Dating Optimizer。現在可以開始探索各種功能了。 🎉

