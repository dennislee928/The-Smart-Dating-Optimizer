package dto

// CreateDatingAccountRequest 建立社交帳號請求
type CreateDatingAccountRequest struct {
	Platform     string `json:"platform" binding:"required,oneof=tinder hearting"`
	AccountID    string `json:"account_id"`
	SessionToken string `json:"session_token"`
}

// UpdateDatingAccountRequest 更新社交帳號請求
type UpdateDatingAccountRequest struct {
	SessionToken string `json:"session_token"`
	IsActive     *bool  `json:"is_active"`
}

// SyncDatingAccountRequest 同步社交帳號資料請求
type SyncDatingAccountRequest struct {
	DatingAccountID int64 `json:"dating_account_id" binding:"required"`
}

