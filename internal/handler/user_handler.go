package handler

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
	"github.com/pclee/smart-dating-optimizer/internal/dto"
	"github.com/pclee/smart-dating-optimizer/internal/service"
	"github.com/pclee/smart-dating-optimizer/internal/vo"
)

// UserHandler 使用者處理器
type UserHandler struct {
	userService service.UserService
}

// NewUserHandler 建立使用者處理器
func NewUserHandler(userService service.UserService) *UserHandler {
	return &UserHandler{
		userService: userService,
	}
}

// Register 註冊使用者
// @Summary 註冊新使用者
// @Tags users
// @Accept json
// @Produce json
// @Param request body dto.RegisterUserRequest true "註冊請求"
// @Success 201 {object} vo.Response
// @Router /api/v1/auth/register [post]
func (h *UserHandler) Register(c *gin.Context) {
	var req dto.RegisterUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "VALIDATION_ERROR",
				Message: err.Error(),
			},
		})
		return
	}

	user, err := h.userService.Register(&req)
	if err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "REGISTER_FAILED",
				Message: err.Error(),
			},
		})
		return
	}

	c.JSON(http.StatusCreated, vo.Response{
		Success: true,
		Message: "註冊成功",
		Data:    user,
	})
}

// Login 使用者登入
// @Summary 使用者登入
// @Tags users
// @Accept json
// @Produce json
// @Param request body dto.LoginRequest true "登入請求"
// @Success 200 {object} vo.Response
// @Router /api/v1/auth/login [post]
func (h *UserHandler) Login(c *gin.Context) {
	var req dto.LoginRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "VALIDATION_ERROR",
				Message: err.Error(),
			},
		})
		return
	}

	loginResp, err := h.userService.Login(&req)
	if err != nil {
		c.JSON(http.StatusUnauthorized, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "LOGIN_FAILED",
				Message: err.Error(),
			},
		})
		return
	}

	c.JSON(http.StatusOK, vo.Response{
		Success: true,
		Message: "登入成功",
		Data:    loginResp,
	})
}

// GetUser 取得使用者資訊
// @Summary 取得使用者資訊
// @Tags users
// @Produce json
// @Param id path int true "使用者 ID"
// @Success 200 {object} vo.Response
// @Router /api/v1/users/{id} [get]
func (h *UserHandler) GetUser(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "INVALID_ID",
				Message: "無效的使用者 ID",
			},
		})
		return
	}

	user, err := h.userService.GetUserByID(id)
	if err != nil {
		c.JSON(http.StatusNotFound, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "USER_NOT_FOUND",
				Message: err.Error(),
			},
		})
		return
	}

	c.JSON(http.StatusOK, vo.Response{
		Success: true,
		Data:    user,
	})
}

// UpdateUser 更新使用者資訊
// @Summary 更新使用者資訊
// @Tags users
// @Accept json
// @Produce json
// @Param id path int true "使用者 ID"
// @Param request body dto.UpdateUserRequest true "更新請求"
// @Success 200 {object} vo.Response
// @Router /api/v1/users/{id} [put]
func (h *UserHandler) UpdateUser(c *gin.Context) {
	idStr := c.Param("id")
	id, err := strconv.ParseInt(idStr, 10, 64)
	if err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "INVALID_ID",
				Message: "無效的使用者 ID",
			},
		})
		return
	}

	var req dto.UpdateUserRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "VALIDATION_ERROR",
				Message: err.Error(),
			},
		})
		return
	}

	user, err := h.userService.UpdateUser(id, &req)
	if err != nil {
		c.JSON(http.StatusBadRequest, vo.Response{
			Success: false,
			Error: &vo.ErrorInfo{
				Code:    "UPDATE_FAILED",
				Message: err.Error(),
			},
		})
		return
	}

	c.JSON(http.StatusOK, vo.Response{
		Success: true,
		Message: "更新成功",
		Data:    user,
	})
}
