# 前端儀表板待辦事項

## 專案狀態

✅ **已完成**: 基礎架構與設定  
🚧 **進行中**: 元件開發  
📋 **待開發**: 頁面與功能

## 已完成項目

- ✅ Next.js 專案結構建立
- ✅ TypeScript 設定
- ✅ Tailwind CSS 設定
- ✅ API 型別定義
- ✅ API 客戶端基礎
- ✅ 專案文檔

## 待開發功能

### 1. 基礎元件 (Components)

#### 通用元件
- [ ] Button 元件
- [ ] Input 元件
- [ ] Card 元件
- [ ] Loading 元件
- [ ] Modal 元件
- [ ] Toast 通知元件
- [ ] Dropdown 元件
- [ ] Table 元件

#### 佈局元件
- [ ] Layout 主佈局
- [ ] Sidebar 側邊欄
- [ ] Header 頂部導航
- [ ] Footer 頁尾

#### 圖表元件
- [ ] LineChart 折線圖
- [ ] BarChart 柱狀圖
- [ ] PieChart 圓餅圖
- [ ] AreaChart 面積圖
- [ ] StatCard 統計卡片

### 2. 頁面開發 (Pages)

#### 認證頁面
- [ ] `/login` - 登入頁面
- [ ] `/register` - 註冊頁面
- [ ] `/forgot-password` - 忘記密碼

#### 主要頁面
- [ ] `/` - 儀表板首頁
- [ ] `/profiles` - 個人檔案管理
- [ ] `/profiles/[id]` - 檔案詳情
- [ ] `/profiles/new` - 新增檔案
- [ ] `/ab-tests` - A/B 測試列表
- [ ] `/ab-tests/[id]` - 測試詳情
- [ ] `/ab-tests/new` - 建立測試
- [ ] `/swipes` - 滑卡記錄
- [ ] `/analytics` - 數據分析
- [ ] `/settings` - 設定頁面

### 3. 狀態管理 (State Management)

- [ ] 使用者狀態 (Zustand store)
- [ ] 認證狀態
- [ ] 通知狀態
- [ ] 主題狀態（淺色/深色）

### 4. API 整合

#### 完整 API 方法
- [ ] 使用者相關 API
  - [x] 登入
  - [x] 註冊
  - [ ] 登出
  - [ ] 取得使用者資訊
  - [ ] 更新使用者資訊

- [ ] 社交帳號 API
  - [ ] 取得帳號列表
  - [ ] 建立帳號
  - [ ] 更新帳號
  - [ ] 刪除帳號

- [ ] 個人檔案 API
  - [ ] 取得檔案列表
  - [ ] 取得檔案詳情
  - [ ] 建立檔案
  - [ ] 更新檔案
  - [ ] 刪除檔案
  - [ ] 啟用檔案
  - [ ] 取得檔案統計

- [ ] A/B 測試 API
  - [ ] 取得測試列表
  - [ ] 取得測試詳情
  - [ ] 建立測試
  - [ ] 更新測試狀態
  - [ ] 取得測試結果

- [ ] 滑卡記錄 API
  - [ ] 取得滑卡列表
  - [ ] 取得滑卡統計
  - [ ] 取得滑卡詳情

- [ ] 分析 API
  - [x] 取得儀表板統計
  - [ ] 取得表現趨勢
  - [ ] 匯出報告

### 5. 功能特性

#### 核心功能
- [ ] 響應式設計（手機、平板、桌面）
- [ ] 深色模式支援
- [ ] 多語言支援 (i18n)
- [ ] 即時數據更新
- [ ] 資料快取策略

#### 使用者體驗
- [ ] 載入狀態處理
- [ ] 錯誤處理與顯示
- [ ] 表單驗證
- [ ] 友善的錯誤訊息
- [ ] 快捷鍵支援

#### 數據視覺化
- [ ] 配對率趨勢圖
- [ ] 滑卡統計圖表
- [ ] A/B 測試比較圖
- [ ] AI 評分分布圖
- [ ] 時間分布熱力圖

### 6. 優化與效能

- [ ] 圖片懶加載
- [ ] 代碼分割
- [ ] SSR/SSG 優化
- [ ] API 請求去抖動
- [ ] 分頁載入優化

### 7. 測試

- [ ] 單元測試（Jest）
- [ ] 元件測試（React Testing Library）
- [ ] E2E 測試（Playwright）
- [ ] API Mock 測試

### 8. 文檔

- [ ] 元件使用文檔
- [ ] Storybook 整合
- [ ] 開發者指南

## 優先順序

### 第一階段（MVP）
1. 基礎元件開發
2. 登入/註冊頁面
3. 儀表板首頁
4. API 客戶端完善

### 第二階段
1. 個人檔案管理
2. 滑卡記錄查看
3. 基本圖表整合

### 第三階段
1. A/B 測試功能
2. 數據分析頁面
3. 進階圖表

### 第四階段
1. 響應式優化
2. 深色模式
3. 效能優化

## 技術債務

- [ ] 無

## 已知問題

- [ ] 無

## 參考資源

### 設計靈感
- [Tailwind UI](https://tailwindui.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [DaisyUI](https://daisyui.com/)

### 圖表庫
- [Recharts](https://recharts.org/)
- [Chart.js](https://www.chartjs.org/)
- [Apache ECharts](https://echarts.apache.org/)

### 狀態管理
- [Zustand](https://github.com/pmndrs/zustand)
- [React Query](https://tanstack.com/query/)

## 貢獻指南

1. 選擇一個待辦事項
2. 建立功能分支
3. 開發與測試
4. 提交 Pull Request
5. 更新此文件

## 更新日誌

- **2025-10-11**: 建立前端專案基礎架構
- **待續**: 開始元件開發

---

**維護者**: Smart Dating Optimizer Team  
**最後更新**: 2025-10-11

