package service

import (
	"errors"
	"time"

	"github.com/pclee/smart-dating-optimizer/internal/dto"
	"github.com/pclee/smart-dating-optimizer/internal/model"
	"github.com/pclee/smart-dating-optimizer/internal/repository"
	"github.com/pclee/smart-dating-optimizer/internal/vo"
	"golang.org/x/crypto/bcrypt"
)

// UserService 使用者服務介面
type UserService interface {
	Register(req *dto.RegisterUserRequest) (*vo.UserVO, error)
	Login(req *dto.LoginRequest) (*vo.LoginResponse, error)
	GetUserByID(id int64) (*vo.UserVO, error)
	UpdateUser(id int64, req *dto.UpdateUserRequest) (*vo.UserVO, error)
	DeleteUser(id int64) error
}

type userService struct {
	userRepo repository.UserRepository
}

// NewUserService 建立使用者服務
func NewUserService(userRepo repository.UserRepository) UserService {
	return &userService{
		userRepo: userRepo,
	}
}

func (s *userService) Register(req *dto.RegisterUserRequest) (*vo.UserVO, error) {
	// 檢查 email 是否已存在
	existingUser, _ := s.userRepo.FindByEmail(req.Email)
	if existingUser != nil {
		return nil, errors.New("email 已被註冊")
	}

	// 檢查 username 是否已存在
	existingUser, _ = s.userRepo.FindByUsername(req.Username)
	if existingUser != nil {
		return nil, errors.New("使用者名稱已被使用")
	}

	// 加密密碼
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, err
	}

	// 建立使用者
	user := &model.User{
		Email:        req.Email,
		PasswordHash: string(hashedPassword),
		Username:     req.Username,
	}

	if err := s.userRepo.Create(user); err != nil {
		return nil, err
	}

	return &vo.UserVO{
		ID:        user.ID,
		Email:     user.Email,
		Username:  user.Username,
		CreatedAt: user.CreatedAt,
		UpdatedAt: user.UpdatedAt,
	}, nil
}

func (s *userService) Login(req *dto.LoginRequest) (*vo.LoginResponse, error) {
	// 查找使用者
	user, err := s.userRepo.FindByEmail(req.Email)
	if err != nil {
		return nil, errors.New("email 或密碼錯誤")
	}

	// 驗證密碼
	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password)); err != nil {
		return nil, errors.New("email 或密碼錯誤")
	}

	// TODO: 生成 JWT token
	token := "placeholder_jwt_token"
	expiresAt := time.Now().Add(168 * time.Hour)

	return &vo.LoginResponse{
		Token:     token,
		ExpiresAt: expiresAt,
		User: vo.UserVO{
			ID:        user.ID,
			Email:     user.Email,
			Username:  user.Username,
			CreatedAt: user.CreatedAt,
			UpdatedAt: user.UpdatedAt,
		},
	}, nil
}

func (s *userService) GetUserByID(id int64) (*vo.UserVO, error) {
	user, err := s.userRepo.FindByID(id)
	if err != nil {
		return nil, errors.New("找不到使用者")
	}

	return &vo.UserVO{
		ID:        user.ID,
		Email:     user.Email,
		Username:  user.Username,
		CreatedAt: user.CreatedAt,
		UpdatedAt: user.UpdatedAt,
	}, nil
}

func (s *userService) UpdateUser(id int64, req *dto.UpdateUserRequest) (*vo.UserVO, error) {
	user, err := s.userRepo.FindByID(id)
	if err != nil {
		return nil, errors.New("找不到使用者")
	}

	// 更新欄位
	if req.Username != "" {
		user.Username = req.Username
	}

	if req.Password != "" {
		hashedPassword, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
		if err != nil {
			return nil, err
		}
		user.PasswordHash = string(hashedPassword)
	}

	if err := s.userRepo.Update(user); err != nil {
		return nil, err
	}

	return &vo.UserVO{
		ID:        user.ID,
		Email:     user.Email,
		Username:  user.Username,
		CreatedAt: user.CreatedAt,
		UpdatedAt: user.UpdatedAt,
	}, nil
}

func (s *userService) DeleteUser(id int64) error {
	return s.userRepo.Delete(id)
}

