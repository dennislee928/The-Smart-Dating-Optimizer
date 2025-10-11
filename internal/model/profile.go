package model

import (
	"database/sql/driver"
	"encoding/json"
	"time"

	"gorm.io/gorm"
)

// JSONB 自訂型別用於 PostgreSQL JSONB
type JSONB map[string]interface{}

// Value 實現 driver.Valuer 介面
func (j JSONB) Value() (driver.Value, error) {
	if j == nil {
		return nil, nil
	}
	return json.Marshal(j)
}

// Scan 實現 sql.Scanner 介面
func (j *JSONB) Scan(value interface{}) error {
	if value == nil {
		*j = nil
		return nil
	}
	bytes, ok := value.([]byte)
	if !ok {
		return nil
	}
	return json.Unmarshal(bytes, j)
}

// Profile 個人檔案模型
type Profile struct {
	ID              int64          `gorm:"primaryKey;autoIncrement"`
	DatingAccountID int64          `gorm:"not null;index:idx_profiles_account"`
	ProfileName     string         `gorm:"type:varchar(100);not null"`
	Bio             string         `gorm:"type:text"`
	Photos          JSONB          `gorm:"type:jsonb"` // array of photo URLs
	Age             int            `gorm:"type:integer"`
	Gender          string         `gorm:"type:varchar(20)"`
	Interests       JSONB          `gorm:"type:jsonb"` // array of interests
	IsActive        bool           `gorm:"default:false;index:idx_profiles_active"`
	CreatedAt       time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt       time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	DeletedAt       gorm.DeletedAt `gorm:"type:timestamp with time zone;index"`

	// Relations
	DatingAccount      DatingAccount       `gorm:"foreignKey:DatingAccountID"`
	SwipeRecords       []SwipeRecord       `gorm:"foreignKey:ProfileID"`
	Matches            []Match             `gorm:"foreignKey:ProfileID"`
	AnalyticsSnapshots []AnalyticsSnapshot `gorm:"foreignKey:ProfileID"`
}

// TableName 指定表名
func (Profile) TableName() string {
	return "profiles"
}
