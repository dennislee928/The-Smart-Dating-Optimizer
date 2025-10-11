package model

import (
	"time"

	"gorm.io/gorm"
)

// User 使用者模型
type User struct {
	ID           int64          `gorm:"primaryKey;autoIncrement"`
	Email        string         `gorm:"type:varchar(255);uniqueIndex;not null"`
	PasswordHash string         `gorm:"type:varchar(255);not null"`
	Username     string         `gorm:"type:varchar(100);uniqueIndex;not null"`
	CreatedAt    time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	UpdatedAt    time.Time      `gorm:"type:timestamp with time zone;default:CURRENT_TIMESTAMP"`
	DeletedAt    gorm.DeletedAt `gorm:"type:timestamp with time zone;index"`

	// Relations
	DatingAccounts []DatingAccount `gorm:"foreignKey:UserID"`
}

// TableName 指定表名
func (User) TableName() string {
	return "users"
}

