# 部署指南

## 部署架構

### 生產環境架構

```
┌─────────────┐
│   Cloudflare│
│     CDN     │
└──────┬──────┘
       │
┌──────▼──────┐
│   NGINX     │
│   反向代理  │
└──────┬──────┘
       │
┌──────▼──────────────────────────┐
│        Kubernetes Cluster       │
│  ┌─────────┐    ┌─────────┐   │
│  │  API    │    │  API    │   │
│  │  Pod 1  │    │  Pod 2  │   │
│  └─────────┘    └─────────┘   │
└─────────────────┬───────────────┘
                  │
         ┌────────▼────────┐
         │   PostgreSQL    │
         │   (Supabase)    │
         └─────────────────┘
```

## Docker 部署

### 1. 建置 Docker 映像

```bash
# 建置 API 映像
docker build -f Dockerfile.api -t smart-dating-optimizer-api:latest .
```

### 2. 使用 Docker Compose

啟動所有服務：
```bash
docker-compose up -d
```

停止服務：
```bash
docker-compose down
```

查看日誌：
```bash
docker-compose logs -f api
```

### 3. 環境變數設定

建立 `.env` 檔案：
```env
# 資料庫設定
DB_HOST=postgres
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_NAME=smart_dating_optimizer
DB_SSLMODE=require

# JWT 設定
JWT_SECRET=your_production_jwt_secret_key
JWT_EXPIRATION_HOURS=168

# 伺服器設定
SERVER_PORT=8080
GIN_MODE=release

# CORS
CORS_ALLOWED_ORIGINS=https://yourdomain.com
```

## Kubernetes 部署

### 1. 建立命名空間

```bash
kubectl create namespace smart-dating-optimizer
```

### 2. 設定 Secrets

```bash
kubectl create secret generic app-secrets \
  --from-literal=db-password=your_db_password \
  --from-literal=jwt-secret=your_jwt_secret \
  -n smart-dating-optimizer
```

### 3. 部署 PostgreSQL (或使用 Supabase)

```yaml
# postgres-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: postgres
  namespace: smart-dating-optimizer
spec:
  replicas: 1
  selector:
    matchLabels:
      app: postgres
  template:
    metadata:
      labels:
        app: postgres
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: db-password
        - name: POSTGRES_DB
          value: smart_dating_optimizer
        ports:
        - containerPort: 5432
        volumeMounts:
        - name: postgres-storage
          mountPath: /var/lib/postgresql/data
      volumes:
      - name: postgres-storage
        persistentVolumeClaim:
          claimName: postgres-pvc
```

### 4. 部署 API

```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: smart-dating-optimizer
spec:
  replicas: 3
  selector:
    matchLabels:
      app: api
  template:
    metadata:
      labels:
        app: api
    spec:
      containers:
      - name: api
        image: your-registry/smart-dating-optimizer-api:latest
        env:
        - name: DB_HOST
          value: postgres
        - name: DB_PASSWORD
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: db-password
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: jwt-secret
        - name: GIN_MODE
          value: release
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
```

### 5. 建立 Service

```yaml
# api-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api-service
  namespace: smart-dating-optimizer
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: api
```

### 6. 部署 Ingress

```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: api-ingress
  namespace: smart-dating-optimizer
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - api.yourdomain.com
    secretName: api-tls
  rules:
  - host: api.yourdomain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: api-service
            port:
              number: 80
```

### 7. 應用設定

```bash
kubectl apply -f postgres-deployment.yaml
kubectl apply -f api-deployment.yaml
kubectl apply -f api-service.yaml
kubectl apply -f ingress.yaml
```

## 使用 Supabase

### 1. 建立 Supabase 專案

1. 訪問 [supabase.com](https://supabase.com)
2. 建立新專案
3. 取得連線資訊

### 2. 執行 Migrations

```bash
# 使用 Supabase CLI
supabase db push

# 或直接執行 SQL
psql $SUPABASE_DB_URL -f database/migrations/20251011000001_init_schema.up.sql
```

### 3. 更新環境變數

```env
DB_HOST=db.your-project.supabase.co
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_supabase_password
DB_NAME=postgres
DB_SSLMODE=require
```

## 監控與日誌

### 1. 設定 Prometheus

```yaml
# prometheus-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: prometheus-config
  namespace: smart-dating-optimizer
data:
  prometheus.yml: |
    global:
      scrape_interval: 15s
    scrape_configs:
    - job_name: 'api'
      kubernetes_sd_configs:
      - role: pod
        namespaces:
          names:
          - smart-dating-optimizer
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_label_app]
        regex: api
        action: keep
```

### 2. 設定 Grafana

1. 安裝 Grafana
2. 連接到 Prometheus
3. 匯入預設儀表板

### 3. 日誌聚合 (ELK Stack)

```yaml
# filebeat-config.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: filebeat-config
  namespace: smart-dating-optimizer
data:
  filebeat.yml: |
    filebeat.inputs:
    - type: container
      paths:
        - /var/log/containers/*.log
    output.elasticsearch:
      hosts: ['${ELASTICSEARCH_HOST}']
```

## 備份策略

### 1. 資料庫備份

```bash
# 每日備份腳本
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="backup_$DATE.sql.gz"

pg_dump $DATABASE_URL | gzip > $BACKUP_DIR/$FILENAME

# 上傳至 S3
aws s3 cp $BACKUP_DIR/$FILENAME s3://your-bucket/backups/

# 保留最近 30 天的備份
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete
```

### 2. 自動化備份 (Kubernetes CronJob)

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: database-backup
  namespace: smart-dating-optimizer
spec:
  schedule: "0 2 * * *"  # 每天凌晨 2 點
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: postgres:15-alpine
            command:
            - /bin/sh
            - -c
            - pg_dump $DATABASE_URL | gzip > /backup/backup_$(date +%Y%m%d).sql.gz
          restartPolicy: OnFailure
```

## 效能調校

### 1. PostgreSQL 優化

```sql
-- 設定連線池大小
ALTER SYSTEM SET max_connections = 200;

-- 設定共享緩衝區
ALTER SYSTEM SET shared_buffers = '256MB';

-- 設定工作記憶體
ALTER SYSTEM SET work_mem = '16MB';

-- 啟用查詢計劃快取
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
```

### 2. API 優化

- 啟用 Gzip 壓縮
- 設定適當的快取標頭
- 使用 Redis 快取熱門查詢
- 實現連線池

### 3. 水平擴展

```bash
# 增加 API Pod 數量
kubectl scale deployment api --replicas=5 -n smart-dating-optimizer
```

## 安全加固

### 1. 網路安全

- 使用 HTTPS (Let's Encrypt)
- 啟用 HSTS
- 設定 CSP 標頭
- 實現速率限制

### 2. 應用程式安全

- 定期更新依賴
- 掃描漏洞 (Trivy)
- 最小權限原則
- 加密敏感資料

### 3. 資料庫安全

- 使用 SSL 連線
- 限制 IP 白名單
- 定期審計存取日誌
- 加密備份

## 災難復原

### 1. 復原計劃

- RPO (復原點目標): 1 小時
- RTO (復原時間目標): 4 小時

### 2. 復原步驟

1. 評估損壞程度
2. 啟動備援系統
3. 從最近的備份還原
4. 驗證資料完整性
5. 切換流量到新系統
6. 監控系統穩定性

## 健康檢查

### API 健康檢查端點

```
GET /health
```

回應：
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "2025-10-11T10:00:00Z"
}
```

## 故障排除

### 常見問題

1. **Pod 無法啟動**
   ```bash
   kubectl describe pod <pod-name> -n smart-dating-optimizer
   kubectl logs <pod-name> -n smart-dating-optimizer
   ```

2. **資料庫連線失敗**
   - 檢查 Service DNS 解析
   - 驗證 Secrets 設定
   - 確認網路策略

3. **效能問題**
   - 查看資源使用率
   - 分析慢查詢
   - 檢查日誌錯誤

## 更新部署

### 滾動更新

```bash
# 更新映像
kubectl set image deployment/api api=your-registry/api:v2.0.0 -n smart-dating-optimizer

# 查看更新狀態
kubectl rollout status deployment/api -n smart-dating-optimizer

# 回滾 (如需要)
kubectl rollout undo deployment/api -n smart-dating-optimizer
```

## 成本優化

1. 使用 Spot Instances
2. 自動擴展 (HPA)
3. 資源請求優化
4. 使用 CDN
5. 壓縮資產

