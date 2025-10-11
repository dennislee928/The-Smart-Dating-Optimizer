package dto

// RecordSwipeRequest 記錄滑卡請求
type RecordSwipeRequest struct {
	DatingAccountID int64                  `json:"dating_account_id" binding:"required"`
	ProfileID       *int64                 `json:"profile_id"`
	ABTestID        *int64                 `json:"ab_test_id"`
	TargetName      string                 `json:"target_name"`
	TargetAge       int                    `json:"target_age"`
	TargetBio       string                 `json:"target_bio"`
	TargetPhotos    []string               `json:"target_photos"`
	TargetDistance  int                    `json:"target_distance"`
	SwipeDirection  string                 `json:"swipe_direction" binding:"required,oneof=left right super"`
	IsMatch         bool                   `json:"is_match"`
	AIScore         *float64               `json:"ai_score"`
	DecisionReason  string                 `json:"decision_reason"`
}

// BatchRecordSwipeRequest 批次記錄滑卡請求
type BatchRecordSwipeRequest struct {
	Swipes []RecordSwipeRequest `json:"swipes" binding:"required,dive"`
}

// GetSwipeHistoryRequest 取得滑卡歷史請求
type GetSwipeHistoryRequest struct {
	DatingAccountID int64  `form:"dating_account_id" binding:"required"`
	ProfileID       *int64 `form:"profile_id"`
	ABTestID        *int64 `form:"ab_test_id"`
	StartDate       string `form:"start_date"`
	EndDate         string `form:"end_date"`
	Page            int    `form:"page" binding:"omitempty,min=1"`
	PageSize        int    `form:"page_size" binding:"omitempty,min=1,max=100"`
}

