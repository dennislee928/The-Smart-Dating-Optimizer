package model

import (
	"time"

	"gorm.io/gorm"
)

// DatingAccount 社交帳號模型
type DatingAccount struct {
	ID           int64          `gorm:"primaryKey;autoIncrement"`
	UserID       int64          `gorm:"not null;index:idx_dating_accounts_user"`
	Platform     string         `gorm:"type:varchar(50);not null;index:idx_dating_accounts_platform"`
	AccountID    string         `gorm:"type:varchar(255)"`
	SessionToken string         `gorm:"type:text"` // 應加密儲存
	IsActive     bool           `gorm:"default:true"`
	LastSyncAt   *time.Time     `gorm:"type:timestamp with time zone"`
	CreatedAt    time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt    time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	DeletedAt    gorm.DeletedAt `gorm:"type:timestamp with time zone;index"`

	// Relations
	User               User                 `gorm:"foreignKey:UserID"`
	Profiles           []Profile            `gorm:"foreignKey:DatingAccountID"`
	ABTests            []ABTest             `gorm:"foreignKey:DatingAccountID"`
	SwipeRecords       []SwipeRecord        `gorm:"foreignKey:DatingAccountID"`
	Matches            []Match              `gorm:"foreignKey:DatingAccountID"`
	AIModels           []AIModel            `gorm:"foreignKey:DatingAccountID"`
	AnalyticsSnapshots []AnalyticsSnapshot  `gorm:"foreignKey:DatingAccountID"`
	AutomationLogs     []AutomationLog      `gorm:"foreignKey:DatingAccountID"`
}

// TableName 指定表名
func (DatingAccount) TableName() string {
	return "dating_accounts"
}

