# CI/CD 設定指南

本專案支援多種 CI/CD 平台，包括 GitHub Actions 和 Travis CI。

## GitHub Actions

GitHub Actions 設定檔位於 `.github/workflows/ci.yml`

### 功能
- ✅ Go 後端測試（格式檢查、靜態分析、單元測試）
- ✅ Python 自動化測試（flake8、pytest）
- ✅ 資料庫遷移檢查
- ✅ 安全漏洞掃描（Trivy）
- ✅ 覆蓋率報告上傳（Codecov）

### 觸發條件
- Push 到 `main` 或 `develop` 分支
- Pull Request 到 `main` 或 `develop` 分支

### 使用方式
GitHub Actions 會自動執行，無需額外設定。

---

## Travis CI

Travis CI 設定檔位於 `.travis.yml`

### 功能
- ✅ Go 1.21 環境設置
- ✅ Python 3.11 環境設置
- ✅ PostgreSQL 15 資料庫
- ✅ Go 測試與建置
- ✅ Python 測試
- ✅ 資料庫遷移測試
- ✅ 覆蓋率報告

### 啟用 Travis CI

1. 訪問 [travis-ci.com](https://travis-ci.com)
2. 使用 GitHub 帳號登入
3. 啟用此儲存庫
4. Push 代碼觸發建置

### 環境變數設定

Travis CI 會自動設定以下變數：
```yaml
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=smart_dating_optimizer_test
```

### 建置狀態徽章

在 `README.md` 中加入：
```markdown
[![Build Status](https://travis-ci.com/yourusername/The-Smart-Dating-Optimizer.svg?branch=main)](https://travis-ci.com/yourusername/The-Smart-Dating-Optimizer)
```

---

## CircleCI（可選）

如需使用 CircleCI，可創建 `.circleci/config.yml`：

```yaml
version: 2.1

orbs:
  go: circleci/go@1.7
  python: circleci/python@2.0

jobs:
  test-go:
    docker:
      - image: cimg/go:1.21
      - image: cimg/postgres:15
        environment:
          POSTGRES_DB: smart_dating_optimizer_test
          POSTGRES_PASSWORD: postgres
    steps:
      - checkout
      - go/load-cache
      - go/mod-download
      - run: go test -v -race -coverprofile=coverage.out ./...
      - go/save-cache

  test-python:
    docker:
      - image: cimg/python:3.11
    steps:
      - checkout
      - python/install-packages:
          pkg-manager: pip
      - run: pip install -r requirements.txt
      - run: pytest --cov=automations --cov=analysis

workflows:
  test:
    jobs:
      - test-go
      - test-python
```

---

## 本地測試 CI 流程

### 模擬 GitHub Actions（使用 act）

```bash
# 安裝 act
# macOS
brew install act

# Windows
choco install act-cli

# 執行 workflow
act -j go-backend
act -j python-automation
```

### 模擬 Travis CI（使用 Docker）

```bash
# 拉取 Travis CI Docker 映像
docker pull travisci/ci-garnet:packer-1.4.5

# 執行建置
docker run -it -v $(pwd):/project travisci/ci-garnet:packer-1.4.5 \
  /bin/bash -c "cd /project && bash .travis.yml"
```

---

## 測試覆蓋率

### Codecov 設定

1. 訪問 [codecov.io](https://codecov.io)
2. 使用 GitHub 登入
3. 啟用此儲存庫
4. 取得 Token（如需私有儲存庫）

### 覆蓋率徽章

在 `README.md` 中加入：
```markdown
[![codecov](https://codecov.io/gh/yourusername/The-Smart-Dating-Optimizer/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/The-Smart-Dating-Optimizer)
```

---

## 持續部署（CD）

### 自動部署到 Heroku

在 `.travis.yml` 加入：

```yaml
deploy:
  provider: heroku
  api_key:
    secure: YOUR_ENCRYPTED_API_KEY
  app: your-app-name
  on:
    branch: main
```

### 自動部署到 AWS

使用 GitHub Actions：

```yaml
- name: Deploy to AWS
  uses: aws-actions/configure-aws-credentials@v1
  with:
    aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
    aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
    aws-region: ap-northeast-1
```

### 自動部署到 Docker Hub

```yaml
- name: Build and push Docker image
  uses: docker/build-push-action@v2
  with:
    push: true
    tags: yourusername/smart-dating-optimizer:latest
```

---

## 常見問題排解

### 問題 1: 測試超時

**解決方案**:
```yaml
# Travis CI
script:
  - travis_wait 30 go test ./...

# GitHub Actions
- name: Run tests
  timeout-minutes: 30
  run: go test ./...
```

### 問題 2: 資料庫連線失敗

**解決方案**:
```yaml
before_script:
  - sleep 10  # 等待資料庫啟動
  - psql -c "SELECT 1" -U postgres  # 測試連線
```

### 問題 3: 快取失效

**解決方案**:
```yaml
cache:
  directories:
    - $HOME/.cache/go-build
    - $HOME/go/pkg/mod
  key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
```

---

## 最佳實踐

1. **並行測試**: 將不同語言的測試並行執行
2. **快取依賴**: 快取 Go modules 和 Python packages
3. **失敗快速**: 先執行快速測試，再執行耗時測試
4. **分支保護**: 要求 CI 通過才能合併 PR
5. **定期更新**: 定期更新 CI 環境和依賴版本

---

## 監控與通知

### Slack 通知

Travis CI:
```yaml
notifications:
  slack:
    rooms:
      - your-team:TOKEN#ci-notifications
```

GitHub Actions:
```yaml
- name: Slack Notification
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

### Email 通知

```yaml
notifications:
  email:
    recipients:
      - dev@example.com
    on_success: change
    on_failure: always
```

---

## 效能優化

### 1. 使用快取

```yaml
cache:
  directories:
    - node_modules
    - .next/cache
```

### 2. 矩陣建置

```yaml
strategy:
  matrix:
    go-version: [1.20, 1.21]
    python-version: [3.10, 3.11]
```

### 3. 條件執行

```yaml
jobs:
  test:
    if: contains(github.event.head_commit.message, '[test]')
```

---

## 相關資源

- [GitHub Actions 文件](https://docs.github.com/en/actions)
- [Travis CI 文件](https://docs.travis-ci.com/)
- [CircleCI 文件](https://circleci.com/docs/)
- [Codecov 文件](https://docs.codecov.com/)

