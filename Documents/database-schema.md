# 資料庫架構設計 (Database Schema Design)

## ERD 概述

本專案使用 PostgreSQL (Supabase) 作為主要資料庫，設計遵循正規化原則，支援 A/B 測試、配對分析與智慧滑卡功能。

## 核心資料表

### 1. users (使用者表)
儲存系統使用者的基本資訊。

```sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);
```

### 2. dating_accounts (社交帳號表)
儲存使用者連接的社交軟體帳號資訊。

```sql
CREATE TABLE dating_accounts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL, -- 'tinder', 'hearting', etc.
    account_id VARCHAR(255), -- platform specific account id
    session_token TEXT, -- encrypted session token
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, platform)
);
```

### 3. profiles (個人檔案表)
儲存使用者在社交軟體上的個人檔案配置。

```sql
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_name VARCHAR(100) NOT NULL, -- e.g., 'Profile A', 'Profile B'
    bio TEXT,
    photos JSONB, -- array of photo URLs
    age INT,
    gender VARCHAR(20),
    interests JSONB, -- array of interests
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);
```

### 4. ab_tests (A/B 測試表)
儲存 A/B 測試實驗的設定與狀態。

```sql
CREATE TABLE ab_tests (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    test_name VARCHAR(100) NOT NULL,
    profile_a_id BIGINT NOT NULL REFERENCES profiles(id),
    profile_b_id BIGINT NOT NULL REFERENCES profiles(id),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'completed', 'paused'
    swipes_per_profile INT DEFAULT 100,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 5. swipe_records (滑卡記錄表)
記錄每次滑卡操作的詳細資訊。

```sql
CREATE TABLE swipe_records (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_id BIGINT REFERENCES profiles(id),
    ab_test_id BIGINT REFERENCES ab_tests(id),
    target_name VARCHAR(100),
    target_age INT,
    target_bio TEXT,
    target_photos JSONB,
    target_distance INT, -- in km
    swipe_direction VARCHAR(10) NOT NULL, -- 'left', 'right', 'super'
    is_match BOOLEAN DEFAULT FALSE,
    ai_score DECIMAL(5,2), -- AI evaluation score
    decision_reason TEXT, -- why AI made this decision
    swiped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_swipe_records_account ON swipe_records(dating_account_id);
CREATE INDEX idx_swipe_records_profile ON swipe_records(profile_id);
CREATE INDEX idx_swipe_records_test ON swipe_records(ab_test_id);
CREATE INDEX idx_swipe_records_direction ON swipe_records(swipe_direction);
```

### 6. matches (配對表)
儲存成功配對的記錄。

```sql
CREATE TABLE matches (
    id BIGSERIAL PRIMARY KEY,
    swipe_record_id BIGINT NOT NULL REFERENCES swipe_records(id),
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_id BIGINT REFERENCES profiles(id),
    match_name VARCHAR(100),
    match_profile_data JSONB,
    matched_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    first_message_sent BOOLEAN DEFAULT FALSE,
    first_message_received BOOLEAN DEFAULT FALSE,
    conversation_started BOOLEAN DEFAULT FALSE,
    unmatched_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_matches_account ON matches(dating_account_id);
CREATE INDEX idx_matches_profile ON matches(profile_id);
CREATE INDEX idx_matches_matched_at ON matches(matched_at);
```

### 7. messages (訊息表)
儲存配對後的對話訊息。

```sql
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    match_id BIGINT NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    sender VARCHAR(20) NOT NULL, -- 'user', 'match'
    content TEXT NOT NULL,
    sentiment_score DECIMAL(5,2), -- sentiment analysis result
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_match ON messages(match_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);
```

### 8. analytics_snapshots (分析快照表)
儲存定期的統計分析快照，用於儀表板顯示。

```sql
CREATE TABLE analytics_snapshots (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_id BIGINT REFERENCES profiles(id),
    ab_test_id BIGINT REFERENCES ab_tests(id),
    snapshot_date DATE NOT NULL,
    total_swipes INT DEFAULT 0,
    right_swipes INT DEFAULT 0,
    left_swipes INT DEFAULT 0,
    matches_count INT DEFAULT 0,
    match_rate DECIMAL(5,2), -- percentage
    message_response_rate DECIMAL(5,2), -- percentage
    avg_ai_score DECIMAL(5,2),
    metadata JSONB, -- additional metrics
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(dating_account_id, profile_id, snapshot_date)
);

CREATE INDEX idx_analytics_account ON analytics_snapshots(dating_account_id);
CREATE INDEX idx_analytics_date ON analytics_snapshots(snapshot_date);
```

### 9. ai_models (AI 模型配置表)
儲存機器學習模型的配置與版本資訊。

```sql
CREATE TABLE ai_models (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL, -- 'scoring', 'preference', 'nlp'
    model_version VARCHAR(20) NOT NULL,
    model_path TEXT, -- file path or S3 URL
    parameters JSONB,
    accuracy_score DECIMAL(5,2),
    is_active BOOLEAN DEFAULT FALSE,
    trained_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### 10. automation_logs (自動化日誌表)
記錄自動化腳本的執行日誌。

```sql
CREATE TABLE automation_logs (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL, -- 'swipe', 'profile_update', 'message'
    status VARCHAR(20) NOT NULL, -- 'success', 'failed', 'warning'
    error_message TEXT,
    metadata JSONB,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_automation_logs_account ON automation_logs(dating_account_id);
CREATE INDEX idx_automation_logs_executed ON automation_logs(executed_at);
```

## 資料關聯圖

```
users (1) --> (*) dating_accounts
dating_accounts (1) --> (*) profiles
dating_accounts (1) --> (*) ab_tests
dating_accounts (1) --> (*) swipe_records
dating_accounts (1) --> (*) matches
dating_accounts (1) --> (*) ai_models
dating_accounts (1) --> (*) analytics_snapshots

profiles (1) --> (*) ab_tests (as profile_a or profile_b)
profiles (1) --> (*) swipe_records
profiles (1) --> (*) matches

ab_tests (1) --> (*) swipe_records

swipe_records (1) --> (0..1) matches

matches (1) --> (*) messages
```

## 索引策略

1. 主鍵使用 BIGSERIAL 自增 ID
2. 外鍵欄位建立索引以加速 JOIN 查詢
3. 常用查詢條件欄位建立索引（時間戳記、狀態等）
4. JSONB 欄位視需求建立 GIN 索引

## 資料保留政策

- 使用 `deleted_at` 欄位實現軟刪除
- 敏感資料（session_token）需加密儲存
- 日誌資料定期歸檔（超過 90 天）
- 測試資料與生產資料完全分離

## 遷移策略

- 使用 goose 或 golang-migrate 管理資料庫遷移
- 每次 schema 變更必須建立新的 migration 檔案
- Migration 檔案命名格式：`YYYYMMDDHHMMSS_description.sql`
- 禁止修改已執行的 migration 檔案

