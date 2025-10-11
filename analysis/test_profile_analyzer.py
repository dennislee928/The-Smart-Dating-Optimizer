"""
測試個人檔案分析器
"""

import unittest
from profile_analyzer import ProfileAnalyzer


class TestProfileAnalyzer(unittest.TestCase):
    """個人檔案分析器測試類別"""

    def setUp(self):
        """測試前設置"""
        self.analyzer = ProfileAnalyzer()

    def test_extract_keywords(self):
        """測試關鍵字提取"""
        text = "I love hiking, photography, and good coffee"
        keywords = self.analyzer.extract_keywords(text, top_n=3)
        
        self.assertIsInstance(keywords, list)
        self.assertGreater(len(keywords), 0)

    def test_analyze_sentiment(self):
        """測試情感分析"""
        positive_text = "I love life and adventure!"
        negative_text = "I hate boring days"
        
        positive_result = self.analyzer.analyze_sentiment(positive_text)
        negative_result = self.analyzer.analyze_sentiment(negative_text)
        
        self.assertIn('polarity', positive_result)
        self.assertIn('subjectivity', positive_result)
        self.assertGreater(positive_result['polarity'], negative_result['polarity'])

    def test_detect_interests(self):
        """測試興趣偵測"""
        bio = "Love hiking, photography, and playing guitar. Foodie and coffee lover."
        interests = self.analyzer.detect_interests(bio)
        
        self.assertIsInstance(interests, list)
        self.assertIn('travel', interests)
        self.assertIn('food', interests)
        self.assertIn('music', interests)

    def test_analyze_profile(self):
        """測試完整檔案分析"""
        test_profile = {
            'name': 'John',
            'age': 28,
            'bio': 'Love hiking, photography, and good coffee',
            'distance': 5,
            'photos': ['url1', 'url2', 'url3']
        }
        
        result = self.analyzer.analyze_profile(test_profile)
        
        self.assertIn('name', result)
        self.assertIn('keywords', result)
        self.assertIn('sentiment', result)
        self.assertIn('interests', result)
        self.assertEqual(result['name'], 'John')
        self.assertEqual(result['age'], 28)


if __name__ == '__main__':
    unittest.main()

