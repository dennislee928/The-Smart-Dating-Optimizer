-- Initial schema migration for Smart Dating Optimizer
-- Created: 2025-10-11

-- Enable necessary extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. users table
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_username ON users(username);

-- 2. dating_accounts table
CREATE TABLE dating_accounts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    platform VARCHAR(50) NOT NULL,
    account_id VARCHAR(255),
    session_token TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    last_sync_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(user_id, platform)
);

CREATE INDEX idx_dating_accounts_user ON dating_accounts(user_id);
CREATE INDEX idx_dating_accounts_platform ON dating_accounts(platform);

-- 3. profiles table
CREATE TABLE profiles (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_name VARCHAR(100) NOT NULL,
    bio TEXT,
    photos JSONB,
    age INT,
    gender VARCHAR(20),
    interests JSONB,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_profiles_account ON profiles(dating_account_id);
CREATE INDEX idx_profiles_active ON profiles(is_active);

-- 4. ab_tests table
CREATE TABLE ab_tests (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    test_name VARCHAR(100) NOT NULL,
    profile_a_id BIGINT NOT NULL REFERENCES profiles(id),
    profile_b_id BIGINT NOT NULL REFERENCES profiles(id),
    start_date TIMESTAMP WITH TIME ZONE NOT NULL,
    end_date TIMESTAMP WITH TIME ZONE,
    status VARCHAR(20) DEFAULT 'active',
    swipes_per_profile INT DEFAULT 100,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ab_tests_account ON ab_tests(dating_account_id);
CREATE INDEX idx_ab_tests_status ON ab_tests(status);

-- 5. swipe_records table
CREATE TABLE swipe_records (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    profile_id BIGINT REFERENCES profiles(id),
    ab_test_id BIGINT REFERENCES ab_tests(id),
    target_name VARCHAR(100),
    target_age INT,
    target_bio TEXT,
    target_photos JSONB,
    target_distance INT,
    swipe_direction VARCHAR(10) NOT NULL,
    is_match BOOLEAN DEFAULT FALSE,
    ai_score DECIMAL(5,2),
    decision_reason TEXT,
    swiped_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_swipe_records_account ON swipe_records(dating_account_id);
CREATE INDEX idx_swipe_records_profile ON swipe_records(profile_id);
CREATE INDEX idx_swipe_records_test ON swipe_records(ab_test_id);
CREATE INDEX idx_swipe_records_direction ON swipe_records(swipe_direction);
CREATE INDEX idx_swipe_records_swiped_at ON swipe_records(swiped_at);

-- 6. matches table
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
CREATE INDEX idx_matches_swipe_record ON matches(swipe_record_id);

-- 7. messages table
CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    match_id BIGINT NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    sender VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    sentiment_score DECIMAL(5,2),
    sent_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_match ON messages(match_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);

-- 8. analytics_snapshots table
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
    match_rate DECIMAL(5,2),
    message_response_rate DECIMAL(5,2),
    avg_ai_score DECIMAL(5,2),
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(dating_account_id, profile_id, snapshot_date)
);

CREATE INDEX idx_analytics_account ON analytics_snapshots(dating_account_id);
CREATE INDEX idx_analytics_date ON analytics_snapshots(snapshot_date);

-- 9. ai_models table
CREATE TABLE ai_models (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    model_version VARCHAR(20) NOT NULL,
    model_path TEXT,
    parameters JSONB,
    accuracy_score DECIMAL(5,2),
    is_active BOOLEAN DEFAULT FALSE,
    trained_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_models_account ON ai_models(dating_account_id);
CREATE INDEX idx_ai_models_active ON ai_models(is_active);

-- 10. automation_logs table
CREATE TABLE automation_logs (
    id BIGSERIAL PRIMARY KEY,
    dating_account_id BIGINT NOT NULL REFERENCES dating_accounts(id) ON DELETE CASCADE,
    action_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    error_message TEXT,
    metadata JSONB,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_automation_logs_account ON automation_logs(dating_account_id);
CREATE INDEX idx_automation_logs_executed ON automation_logs(executed_at);
CREATE INDEX idx_automation_logs_status ON automation_logs(status);

