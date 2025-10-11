package repository

import (
	"github.com/pclee/smart-dating-optimizer/internal/model"
	"gorm.io/gorm"
)

// UserRepository 使用者資料庫操作介面
type UserRepository interface {
	Create(user *model.User) error
	FindByID(id int64) (*model.User, error)
	FindByEmail(email string) (*model.User, error)
	FindByUsername(username string) (*model.User, error)
	Update(user *model.User) error
	Delete(id int64) error
}

type userRepository struct {
	db *gorm.DB
}

// NewUserRepository 建立使用者 repository
func NewUserRepository(db *gorm.DB) UserRepository {
	return &userRepository{db: db}
}

func (r *userRepository) Create(user *model.User) error {
	return r.db.Create(user).Error
}

func (r *userRepository) FindByID(id int64) (*model.User, error) {
	var user model.User
	err := r.db.First(&user, id).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) FindByEmail(email string) (*model.User, error) {
	var user model.User
	err := r.db.Where("email = ?", email).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) FindByUsername(username string) (*model.User, error) {
	var user model.User
	err := r.db.Where("username = ?", username).First(&user).Error
	if err != nil {
		return nil, err
	}
	return &user, nil
}

func (r *userRepository) Update(user *model.User) error {
	return r.db.Save(user).Error
}

func (r *userRepository) Delete(id int64) error {
	return r.db.Delete(&model.User{}, id).Error
}

