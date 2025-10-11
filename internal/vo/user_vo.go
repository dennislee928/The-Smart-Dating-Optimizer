package vo

import "time"

// UserVO 使用者回應
type UserVO struct {
	ID        int64     `json:"id"`
	Email     string    `json:"email"`
	Username  string    `json:"username"`
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// LoginResponse 登入回應
type LoginResponse struct {
	Token     string    `json:"token"`
	ExpiresAt time.Time `json:"expires_at"`
	User      UserVO    `json:"user"`
}

// RegisterResponse 註冊回應
type RegisterResponse struct {
	User UserVO `json:"user"`
}

