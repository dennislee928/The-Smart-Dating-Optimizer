import { useEffect, useState } from 'react';
import type { NextPage } from 'next';

const Home: NextPage = () => {
  const [apiStatus, setApiStatus] = useState<string>('checking...');

  useEffect(() => {
    // 檢查 API 健康狀態
    fetch('/api/health')
      .then((res) => res.json())
      .then((data) => {
        setApiStatus(data.status === 'ok' ? 'connected' : 'disconnected');
      })
      .catch(() => {
        setApiStatus('disconnected');
      });
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-50">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            智慧社交改善器
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            Smart Dating Optimizer Dashboard
          </p>

          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <div className="flex items-center justify-center mb-6">
              <div
                className={`w-3 h-3 rounded-full mr-2 ${
                  apiStatus === 'connected' ? 'bg-green-500' : 'bg-red-500'
                }`}
              />
              <span className="text-gray-700">
                API Status: <span className="font-semibold">{apiStatus}</span>
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="p-6 bg-pink-50 rounded-lg">
                <h3 className="text-2xl font-bold text-pink-600 mb-2">0</h3>
                <p className="text-gray-600">總配對數</p>
              </div>
              <div className="p-6 bg-purple-50 rounded-lg">
                <h3 className="text-2xl font-bold text-purple-600 mb-2">0%</h3>
                <p className="text-gray-600">配對率</p>
              </div>
              <div className="p-6 bg-blue-50 rounded-lg">
                <h3 className="text-2xl font-bold text-blue-600 mb-2">0</h3>
                <p className="text-gray-600">活躍測試</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              快速開始
            </h2>
            <div className="text-left space-y-4">
              <div className="flex items-start">
                <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-pink-100 text-pink-600 font-semibold mr-3">
                  1
                </span>
                <div>
                  <h3 className="font-semibold text-gray-900">連接帳號</h3>
                  <p className="text-gray-600">
                    連接你的 Tinder 或其他社交軟體帳號
                  </p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-purple-100 text-purple-600 font-semibold mr-3">
                  2
                </span>
                <div>
                  <h3 className="font-semibold text-gray-900">建立檔案</h3>
                  <p className="text-gray-600">設定多個個人檔案進行 A/B 測試</p>
                </div>
              </div>
              <div className="flex items-start">
                <span className="inline-flex items-center justify-center w-8 h-8 rounded-full bg-blue-100 text-blue-600 font-semibold mr-3">
                  3
                </span>
                <div>
                  <h3 className="font-semibold text-gray-900">開始分析</h3>
                  <p className="text-gray-600">
                    查看數據分析與 AI 建議，優化你的配對策略
                  </p>
                </div>
              </div>
            </div>
          </div>

          <div className="mt-8 text-gray-500 text-sm">
            <p>正在開發中... 🚧</p>
            <p className="mt-2">
              完整功能請參閱{' '}
              <a
                href="/api/docs"
                className="text-pink-600 hover:underline"
                target="_blank"
                rel="noopener noreferrer"
              >
                API 文件
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;

