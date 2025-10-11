# API 文件

## 概述

Smart Dating Optimizer API 提供完整的 RESTful API，用於管理社交帳號、個人檔案、滑卡記錄和 A/B 測試。

## 基礎資訊

- **Base URL**: `http://localhost:8080/api/v1`
- **認證方式**: JWT Bearer Token
- **Content-Type**: `application/json`

## 認證 API

### 註冊新使用者

```http
POST /api/v1/auth/register
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "username": "john_doe"
}
```

**Response (201):**
```json
{
  "success": true,
  "message": "註冊成功",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "username": "john_doe",
    "created_at": "2025-10-11T10:00:00Z",
    "updated_at": "2025-10-11T10:00:00Z"
  }
}
```

### 使用者登入

```http
POST /api/v1/auth/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "success": true,
  "message": "登入成功",
  "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_at": "2025-10-18T10:00:00Z",
    "user": {
      "id": 1,
      "email": "user@example.com",
      "username": "john_doe"
    }
  }
}
```

## 社交帳號 API

### 建立社交帳號

```http
POST /api/v1/dating-accounts
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "platform": "tinder",
  "account_id": "tinder_user_123",
  "session_token": "encrypted_session_token"
}
```

### 取得社交帳號列表

```http
GET /api/v1/dating-accounts
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "accounts": [
      {
        "id": 1,
        "user_id": 1,
        "platform": "tinder",
        "account_id": "tinder_user_123",
        "is_active": true,
        "last_sync_at": "2025-10-11T10:00:00Z",
        "created_at": "2025-10-10T10:00:00Z",
        "updated_at": "2025-10-11T10:00:00Z"
      }
    ],
    "total": 1
  }
}
```

## 個人檔案 API

### 建立個人檔案

```http
POST /api/v1/profiles
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "dating_account_id": 1,
  "profile_name": "Profile A",
  "bio": "Adventure seeker | Love hiking",
  "photos": ["url1", "url2", "url3"],
  "age": 28,
  "gender": "male",
  "interests": ["Hiking", "Photography", "Coffee"]
}
```

### 取得個人檔案列表

```http
GET /api/v1/profiles?dating_account_id=1
Authorization: Bearer <token>
```

### 啟用個人檔案

```http
POST /api/v1/profiles/{id}/activate
Authorization: Bearer <token>
```

## A/B 測試 API

### 建立 A/B 測試

```http
POST /api/v1/ab-tests
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "dating_account_id": 1,
  "test_name": "Outdoor vs Urban",
  "profile_a_id": 1,
  "profile_b_id": 2,
  "start_date": "2025-10-11T00:00:00Z",
  "swipes_per_profile": 100
}
```

### 取得 A/B 測試結果

```http
GET /api/v1/ab-tests/{id}/results
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "ab_test_id": 1,
    "test_name": "Outdoor vs Urban",
    "status": "completed",
    "profile_a_stats": {
      "profile_id": 1,
      "profile_name": "Profile A",
      "total_swipes": 100,
      "right_swipes": 60,
      "matches_count": 12,
      "match_rate": 20.0
    },
    "profile_b_stats": {
      "profile_id": 2,
      "profile_name": "Profile B",
      "total_swipes": 100,
      "right_swipes": 55,
      "matches_count": 8,
      "match_rate": 14.5
    },
    "winner": "profile_a",
    "recommendation": "建議使用 Profile A，配對率高出 37.9%"
  }
}
```

## 滑卡記錄 API

### 記錄滑卡

```http
POST /api/v1/swipes
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "dating_account_id": 1,
  "profile_id": 1,
  "target_name": "Alice",
  "target_age": 26,
  "target_bio": "Love traveling...",
  "target_photos": ["url1", "url2"],
  "target_distance": 5,
  "swipe_direction": "right",
  "is_match": true,
  "ai_score": 85.5,
  "decision_reason": "High compatibility score"
}
```

### 取得滑卡歷史

```http
GET /api/v1/swipes?dating_account_id=1&page=1&page_size=20
Authorization: Bearer <token>
```

### 取得滑卡統計

```http
GET /api/v1/swipes/stats?dating_account_id=1
Authorization: Bearer <token>
```

## 分析儀表板 API

### 取得儀表板統計

```http
GET /api/v1/analytics/dashboard?dating_account_id=1
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "success": true,
  "data": {
    "total_swipes": 500,
    "total_matches": 85,
    "match_rate": 17.0,
    "message_response_rate": 65.5,
    "active_profiles": 2,
    "active_ab_tests": 1,
    "recent_swipes": [...],
    "top_performing_profile": {...},
    "weekly_trend": [...]
  }
}
```

### 取得表現趨勢

```http
GET /api/v1/analytics/trend?dating_account_id=1&start_date=2025-10-01&end_date=2025-10-11
Authorization: Bearer <token>
```

## 錯誤回應格式

所有錯誤回應遵循以下格式：

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "錯誤訊息",
    "details": "詳細資訊（可選）"
  }
}
```

### 常見錯誤代碼

- `VALIDATION_ERROR`: 請求資料驗證失敗
- `UNAUTHORIZED`: 未授權，需要登入
- `FORBIDDEN`: 禁止存取
- `NOT_FOUND`: 資源不存在
- `INTERNAL_ERROR`: 伺服器內部錯誤

## 分頁

支援分頁的 API 端點使用以下查詢參數：

- `page`: 頁碼（預設：1）
- `page_size`: 每頁數量（預設：20，最大：100）

分頁回應包含以下資訊：

```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total": 500,
    "total_pages": 25
  }
}
```

## 速率限制

- 每個 IP 每分鐘最多 60 次請求
- 超過限制將返回 `429 Too Many Requests`

## Swagger 文件

完整的互動式 API 文件可在以下位置訪問：

```
http://localhost:8080/swagger/index.html
```

