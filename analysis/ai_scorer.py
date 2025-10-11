"""
AI 評分系統
根據個人檔案特徵為對象評分，預測配對可能性
"""

from typing import Dict, List, Optional
import pickle
import os

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

from profile_analyzer import ProfileAnalyzer


class AIScorer:
    """AI 評分系統類別"""

    def __init__(self, model_path: Optional[str] = None):
        """
        初始化 AI 評分系統
        
        Args:
            model_path: 已訓練模型的路徑
        """
        self.analyzer = ProfileAnalyzer()
        self.model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
        if model_path and os.path.exists(model_path):
            self.load_model(model_path)
        else:
            # 使用預設的規則基礎評分
            self.use_rule_based = True

    def extract_features(self, profile_data: Dict) -> np.ndarray:
        """
        從個人檔案提取特徵向量
        
        Args:
            profile_data: 個人檔案資料
            
        Returns:
            特徵向量
        """
        analysis = self.analyzer.analyze_profile(profile_data)
        
        features = []
        
        # 1. 年齡特徵
        features.append(analysis.get('age', 0))
        
        # 2. 距離特徵
        features.append(analysis.get('distance', 0))
        
        # 3. 簡介長度
        features.append(analysis.get('bio_length', 0))
        
        # 4. 照片數量
        features.append(analysis.get('photo_count', 0))
        
        # 5. 情感分數
        sentiment = analysis.get('sentiment', {})
        features.append(sentiment.get('polarity', 0))
        features.append(sentiment.get('subjectivity', 0))
        
        # 6. 興趣數量
        features.append(len(analysis.get('interests', [])))
        
        # 7. Emoji 使用
        features.append(len(analysis.get('emojis', [])))
        
        # 8. 關鍵字多樣性
        features.append(len(analysis.get('keywords', [])))
        
        return np.array(features).reshape(1, -1)

    def rule_based_score(self, profile_data: Dict) -> float:
        """
        基於規則的評分系統
        
        Args:
            profile_data: 個人檔案資料
            
        Returns:
            評分 (0-100)
        """
        score = 50.0  # 基礎分數
        
        analysis = self.analyzer.analyze_profile(profile_data)
        
        # 年齡偏好 (假設偏好 24-32 歲)
        age = analysis.get('age', 0)
        if 24 <= age <= 32:
            score += 10
        elif 20 <= age <= 35:
            score += 5
        
        # 距離偏好 (越近越好，但不要太近)
        distance = analysis.get('distance', 0)
        if 2 <= distance <= 10:
            score += 10
        elif distance <= 20:
            score += 5
        elif distance > 50:
            score -= 10
        
        # 簡介品質
        bio_length = analysis.get('bio_length', 0)
        if 50 <= bio_length <= 300:
            score += 10
        elif 20 <= bio_length <= 500:
            score += 5
        elif bio_length == 0:
            score -= 15
        
        # 照片數量
        photo_count = analysis.get('photo_count', 0)
        if photo_count >= 4:
            score += 10
        elif photo_count >= 2:
            score += 5
        elif photo_count <= 1:
            score -= 10
        
        # 情感分析
        sentiment = analysis.get('sentiment', {})
        polarity = sentiment.get('polarity', 0)
        if polarity > 0.2:  # 正面情緒
            score += 10
        elif polarity < -0.2:  # 負面情緒
            score -= 5
        
        # 興趣豐富度
        interests_count = len(analysis.get('interests', []))
        if interests_count >= 3:
            score += 10
        elif interests_count >= 1:
            score += 5
        
        # Emoji 使用適度性
        emoji_count = len(analysis.get('emojis', []))
        if 1 <= emoji_count <= 5:
            score += 5
        elif emoji_count > 10:
            score -= 5
        
        # 確保分數在 0-100 範圍內
        return max(0, min(100, score))

    def predict_score(self, profile_data: Dict) -> Dict:
        """
        預測評分
        
        Args:
            profile_data: 個人檔案資料
            
        Returns:
            包含分數和理由的字典
        """
        # 提取特徵
        features = self.extract_features(profile_data)
        
        # 計算分數
        if self.model is not None and not self.use_rule_based:
            # 使用機器學習模型
            features_scaled = self.scaler.transform(features)
            probability = self.model.predict_proba(features_scaled)[0][1]
            score = probability * 100
            method = 'ml_model'
        else:
            # 使用規則基礎評分
            score = self.rule_based_score(profile_data)
            method = 'rule_based'
        
        # 生成決策理由
        reason = self._generate_decision_reason(profile_data, score)
        
        return {
            'score': round(score, 2),
            'method': method,
            'reason': reason,
            'recommendation': 'right' if score >= 60 else 'left'
        }

    def _generate_decision_reason(self, profile_data: Dict, score: float) -> str:
        """
        生成決策理由
        
        Args:
            profile_data: 個人檔案資料
            score: 評分
            
        Returns:
            決策理由文字
        """
        analysis = self.analyzer.analyze_profile(profile_data)
        reasons = []
        
        # 正面因素
        if analysis.get('photo_count', 0) >= 4:
            reasons.append("照片數量充足")
        
        if 50 <= analysis.get('bio_length', 0) <= 300:
            reasons.append("簡介詳細適中")
        
        interests = analysis.get('interests', [])
        if len(interests) >= 3:
            reasons.append(f"興趣廣泛 ({', '.join(interests[:3])})")
        
        sentiment = analysis.get('sentiment', {})
        if sentiment.get('polarity', 0) > 0.2:
            reasons.append("態度積極正面")
        
        distance = analysis.get('distance', 0)
        if distance <= 10:
            reasons.append(f"距離適中 ({distance}km)")
        
        # 負面因素
        if analysis.get('bio_length', 0) == 0:
            reasons.append("缺少個人簡介")
        
        if analysis.get('photo_count', 0) <= 1:
            reasons.append("照片數量不足")
        
        if not reasons:
            return f"綜合評分 {score:.0f} 分"
        
        return "; ".join(reasons)

    def train_model(self, training_data: List[Dict], labels: List[int]):
        """
        訓練機器學習模型
        
        Args:
            training_data: 訓練資料列表
            labels: 標籤列表 (1=配對成功, 0=未配對)
        """
        # 提取特徵
        X = np.vstack([self.extract_features(data) for data in training_data])
        y = np.array(labels)
        
        # 標準化特徵
        X_scaled = self.scaler.fit_transform(X)
        
        # 訓練模型
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_scaled, y)
        
        self.use_rule_based = False
        
        # 計算準確率
        accuracy = self.model.score(X_scaled, y)
        print(f"模型訓練完成，準確率: {accuracy * 100:.2f}%")

    def save_model(self, model_path: str):
        """
        儲存模型
        
        Args:
            model_path: 模型儲存路徑
        """
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'feature_names': self.feature_names
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"模型已儲存至 {model_path}")

    def load_model(self, model_path: str):
        """
        載入模型
        
        Args:
            model_path: 模型路徑
        """
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.feature_names = model_data.get('feature_names', [])
        self.use_rule_based = False
        
        print(f"模型已從 {model_path} 載入")


# 使用範例
if __name__ == '__main__':
    scorer = AIScorer()

    # 測試個人檔案
    test_profile = {
        'name': 'Alice',
        'age': 26,
        'bio': 'Love traveling, photography, and good coffee. Adventure seeker and dog lover.',
        'distance': 5,
        'photos': ['url1', 'url2', 'url3', 'url4']
    }

    # 預測評分
    result = scorer.predict_score(test_profile)
    
    print("AI 評分結果:")
    print(f"分數: {result['score']}")
    print(f"方法: {result['method']}")
    print(f"建議: {result['recommendation']}")
    print(f"理由: {result['reason']}")

