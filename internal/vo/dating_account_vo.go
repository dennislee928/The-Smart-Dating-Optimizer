package vo

import "time"

// DatingAccountVO 社交帳號回應
type DatingAccountVO struct {
	ID         int64      `json:"id"`
	UserID     int64      `json:"user_id"`
	Platform   string     `json:"platform"`
	AccountID  string     `json:"account_id,omitempty"`
	IsActive   bool       `json:"is_active"`
	LastSyncAt *time.Time `json:"last_sync_at,omitempty"`
	CreatedAt  time.Time  `json:"created_at"`
	UpdatedAt  time.Time  `json:"updated_at"`
}

// DatingAccountListResponse 社交帳號列表回應
type DatingAccountListResponse struct {
	Accounts []DatingAccountVO `json:"accounts"`
	Total    int64             `json:"total"`
}

