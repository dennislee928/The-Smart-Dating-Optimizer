package dto

import "time"

// CreateABTestRequest 建立 A/B 測試請求
type CreateABTestRequest struct {
	DatingAccountID  int64     `json:"dating_account_id" binding:"required"`
	TestName         string    `json:"test_name" binding:"required,max=100"`
	ProfileAID       int64     `json:"profile_a_id" binding:"required"`
	ProfileBID       int64     `json:"profile_b_id" binding:"required"`
	StartDate        time.Time `json:"start_date" binding:"required"`
	SwipesPerProfile int       `json:"swipes_per_profile" binding:"required,min=10,max=1000"`
}

// UpdateABTestRequest 更新 A/B 測試請求
type UpdateABTestRequest struct {
	Status  string     `json:"status" binding:"omitempty,oneof=active completed paused"`
	EndDate *time.Time `json:"end_date"`
}

// GetABTestResultRequest 取得 A/B 測試結果請求
type GetABTestResultRequest struct {
	ABTestID int64 `json:"ab_test_id" binding:"required"`
}
