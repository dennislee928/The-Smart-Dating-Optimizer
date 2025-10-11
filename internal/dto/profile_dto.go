package dto

// CreateProfileRequest 建立個人檔案請求
type CreateProfileRequest struct {
	DatingAccountID int64                  `json:"dating_account_id" binding:"required"`
	ProfileName     string                 `json:"profile_name" binding:"required,max=100"`
	Bio             string                 `json:"bio"`
	Photos          []string               `json:"photos"`
	Age             int                    `json:"age" binding:"omitempty,min=18,max=100"`
	Gender          string                 `json:"gender" binding:"omitempty,oneof=male female other"`
	Interests       []string               `json:"interests"`
}

// UpdateProfileRequest 更新個人檔案請求
type UpdateProfileRequest struct {
	ProfileName string   `json:"profile_name" binding:"omitempty,max=100"`
	Bio         string   `json:"bio"`
	Photos      []string `json:"photos"`
	Age         int      `json:"age" binding:"omitempty,min=18,max=100"`
	Gender      string   `json:"gender" binding:"omitempty,oneof=male female other"`
	Interests   []string `json:"interests"`
	IsActive    *bool    `json:"is_active"`
}

// ActivateProfileRequest 啟用檔案請求
type ActivateProfileRequest struct {
	ProfileID int64 `json:"profile_id" binding:"required"`
}

