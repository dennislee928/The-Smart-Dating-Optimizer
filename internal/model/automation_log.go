package model

import (
	"time"
)

// AutomationLog 自動化日誌模型
type AutomationLog struct {
	ID              int64     `gorm:"primaryKey;autoIncrement"`
	DatingAccountID int64     `gorm:"not null;index:idx_automation_logs_account"`
	ActionType      string    `gorm:"type:varchar(50);not null"`                                  // 'swipe', 'profile_update', 'message'
	Status          string    `gorm:"type:varchar(20);not null;index:idx_automation_logs_status"` // 'success', 'failed', 'warning'
	ErrorMessage    string    `gorm:"type:text"`
	Metadata        JSONB     `gorm:"type:jsonb"`
	ExecutedAt      time.Time `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP;index:idx_automation_logs_executed"`

	// Relations
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
}

// TableName 指定表名
func (AutomationLog) TableName() string {
	return "automation_logs"
}
