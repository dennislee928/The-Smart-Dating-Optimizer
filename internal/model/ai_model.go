package model

import (
	"time"

	"gorm.io/gorm"
)

// AIModel AI 模型配置模型
type AIModel struct {
	ID              int64      `gorm:"primaryKey;autoIncrement"`
	DatingAccountID int64      `gorm:"not null;index:idx_ai_models_account"`
	ModelName       string     `gorm:"type:varchar(100);not null"`
	ModelType       string     `gorm:"type:varchar(50);not null"` // 'scoring', 'preference', 'nlp'
	ModelVersion    string     `gorm:"type:varchar(20);not null"`
	ModelPath       string     `gorm:"type:text"`
	Parameters      JSONB      `gorm:"type:jsonb"`
	AccuracyScore   *float64   `gorm:"type:decimal(5,2)"`
	IsActive        bool       `gorm:"default:false;index:idx_ai_models_active"`
	TrainedAt       *time.Time `gorm:"type:timestamp with time zone"`
	CreatedAt       time.Time  `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt       time.Time  `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`

	// Relations
	DatingAccount DatingAccount `gorm:"foreignKey:DatingAccountID"`
}

// TableName 指定表名
func (AIModel) TableName() string {
	return "ai_models"
}
