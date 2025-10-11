"""
個人檔案分析器
分析配對對象的特徵與偏好
"""

import re
from collections import Counter
from typing import Dict, List, Tuple

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# 下載必要的 NLTK 資料
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class ProfileAnalyzer:
    """個人檔案分析器類別"""

    def __init__(self):
        """初始化分析器"""
        self.stop_words = set(stopwords.words('english'))

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        從文字中提取關鍵字
        
        Args:
            text: 待分析文字
            top_n: 返回前 N 個關鍵字
            
        Returns:
            關鍵字列表，格式為 [(keyword, count), ...]
        """
        if not text:
            return []

        # 轉換為小寫並分詞
        words = word_tokenize(text.lower())

        # 過濾停用詞和標點符號
        filtered_words = [
            word for word in words 
            if word.isalnum() and word not in self.stop_words and len(word) > 2
        ]

        # 統計詞頻
        word_freq = Counter(filtered_words)
        
        return word_freq.most_common(top_n)

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        分析文字情感
        
        Args:
            text: 待分析文字
            
        Returns:
            情感分析結果，包含 polarity（極性）和 subjectivity（主觀性）
        """
        if not text:
            return {'polarity': 0.0, 'subjectivity': 0.0}

        blob = TextBlob(text)
        
        return {
            'polarity': blob.sentiment.polarity,  # -1 (negative) to 1 (positive)
            'subjectivity': blob.sentiment.subjectivity  # 0 (objective) to 1 (subjective)
        }

    def detect_interests(self, bio: str) -> List[str]:
        """
        從簡介中偵測興趣
        
        Args:
            bio: 個人簡介
            
        Returns:
            興趣列表
        """
        # 常見興趣關鍵字
        interest_keywords = {
            'sports': ['gym', 'fitness', 'yoga', 'running', 'swimming', 'sports', 'workout'],
            'music': ['music', 'concert', 'guitar', 'piano', 'singing', 'band'],
            'food': ['foodie', 'cooking', 'chef', 'food', 'wine', 'coffee', 'restaurant'],
            'travel': ['travel', 'adventure', 'explore', 'wanderlust', 'hiking', 'backpacking'],
            'arts': ['art', 'painting', 'drawing', 'photography', 'design', 'creative'],
            'reading': ['books', 'reading', 'literature', 'novel', 'writer'],
            'technology': ['tech', 'coding', 'programming', 'developer', 'engineer', 'startup'],
            'pets': ['dog', 'cat', 'pet', 'puppy', 'kitten', 'animal'],
            'movies': ['movie', 'film', 'cinema', 'netflix', 'series', 'tv'],
            'nature': ['nature', 'outdoors', 'camping', 'beach', 'mountains', 'forest']
        }

        detected_interests = []
        bio_lower = bio.lower()

        for category, keywords in interest_keywords.items():
            if any(keyword in bio_lower for keyword in keywords):
                detected_interests.append(category)

        return detected_interests

    def extract_emojis(self, text: str) -> List[str]:
        """
        提取文字中的 emoji
        
        Args:
            text: 待分析文字
            
        Returns:
            emoji 列表
        """
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)

        return emoji_pattern.findall(text)

    def analyze_profile(self, profile_data: Dict) -> Dict:
        """
        全面分析個人檔案
        
        Args:
            profile_data: 個人檔案資料
            
        Returns:
            分析結果
        """
        bio = profile_data.get('bio', '')
        
        analysis = {
            'name': profile_data.get('name', ''),
            'age': profile_data.get('age', 0),
            'distance': profile_data.get('distance', 0),
            'bio_length': len(bio),
            'keywords': self.extract_keywords(bio),
            'sentiment': self.analyze_sentiment(bio),
            'interests': self.detect_interests(bio),
            'emojis': self.extract_emojis(bio),
            'photo_count': len(profile_data.get('photos', []))
        }

        return analysis

    def analyze_batch(self, profiles: List[Dict]) -> Dict:
        """
        批次分析多個個人檔案
        
        Args:
            profiles: 個人檔案列表
            
        Returns:
            批次分析結果
        """
        all_keywords = []
        all_interests = []
        all_sentiments = []
        avg_age = 0
        avg_distance = 0

        for profile in profiles:
            analysis = self.analyze_profile(profile)
            all_keywords.extend([kw for kw, _ in analysis['keywords']])
            all_interests.extend(analysis['interests'])
            all_sentiments.append(analysis['sentiment']['polarity'])
            avg_age += analysis['age']
            avg_distance += analysis['distance']

        profile_count = len(profiles)

        return {
            'total_profiles': profile_count,
            'avg_age': avg_age / profile_count if profile_count > 0 else 0,
            'avg_distance': avg_distance / profile_count if profile_count > 0 else 0,
            'top_keywords': Counter(all_keywords).most_common(20),
            'top_interests': Counter(all_interests).most_common(10),
            'avg_sentiment': sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
        }


# 使用範例
if __name__ == '__main__':
    analyzer = ProfileAnalyzer()

    # 測試個人檔案
    test_profile = {
        'name': 'John',
        'age': 28,
        'bio': 'Love hiking, photography, and good coffee. Dog lover and adventure seeker.',
        'distance': 5,
        'photos': ['url1', 'url2', 'url3']
    }

    result = analyzer.analyze_profile(test_profile)
    
    print("個人檔案分析結果:")
    print(f"姓名: {result['name']}")
    print(f"年齡: {result['age']}")
    print(f"關鍵字: {result['keywords']}")
    print(f"興趣: {result['interests']}")
    print(f"情感分數: {result['sentiment']}")

