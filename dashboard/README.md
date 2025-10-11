# Smart Dating Optimizer Dashboard

Next.js + TypeScript 前端儀表板，用於視覺化顯示社交軟體配對數據與分析結果。

## 技術棧

- **框架**: Next.js 14
- **語言**: TypeScript
- **UI 庫**: Tailwind CSS
- **圖表**: Recharts
- **狀態管理**: Zustand
- **API 客戶端**: Axios

## 快速開始

### 安裝依賴

```bash
cd dashboard
npm install
```

### 開發模式

```bash
npm run dev
```

訪問 http://localhost:3000

### 生產建置

```bash
npm run build
npm start
```

## 專案結構

```
dashboard/
├── src/
│   ├── components/    # React 元件
│   ├── pages/         # Next.js 頁面
│   ├── services/      # API 服務
│   ├── types/         # TypeScript 型別定義
│   └── utils/         # 工具函式
├── public/            # 靜態資源
├── package.json
├── tsconfig.json
├── next.config.js
└── tailwind.config.js
```

## 環境變數

建立 `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8080/api/v1
```

## 主要功能（規劃）

### 儀表板首頁
- 總體統計概覽
- 配對率趨勢圖
- 最近滑卡記錄
- 活躍的 A/B 測試

### 個人檔案管理
- 檔案列表
- 新增/編輯檔案
- 啟用/停用檔案
- 檔案表現統計

### A/B 測試
- 測試列表
- 建立新測試
- 查看測試結果
- 比較分析圖表

### 數據分析
- 滑卡統計
- 配對分析
- 時間趨勢
- AI 評分分布

### 設定
- 使用者設定
- 社交帳號管理
- 通知設定

## 開發狀態

🚧 **目前狀態**: 基礎架構已建立，待實作功能

### 待完成項目

- [ ] 元件庫建立
- [ ] API 服務整合
- [ ] 頁面實作
- [ ] 圖表整合
- [ ] 響應式設計
- [ ] 深色模式
- [ ] 國際化 (i18n)

## API 整合

儀表板將整合以下 API 端點：

- `/auth/login` - 使用者登入
- `/dashboard/stats` - 儀表板統計
- `/profiles` - 個人檔案管理
- `/ab-tests` - A/B 測試管理
- `/swipes` - 滑卡記錄
- `/analytics` - 數據分析

## 型別生成

可從 Swagger 自動生成 TypeScript 型別：

```bash
# 使用 openapi-generator
npx openapi-generator-cli generate \
  -i http://localhost:8080/swagger/doc.json \
  -g typescript-axios \
  -o src/services/api
```

## 貢獻

歡迎貢獻前端功能！請參閱主專案的開發指南。

