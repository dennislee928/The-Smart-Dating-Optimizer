"""
A/B 測試管理器
管理個人檔案 A/B 測試的執行與結果分析
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

from database_client import DatabaseClient


class ABTestManager:
    """A/B 測試管理器類別"""

    def __init__(self, db_client: DatabaseClient):
        """
        初始化 A/B 測試管理器
        
        Args:
            db_client: 資料庫客戶端實例
        """
        self.db_client = db_client

    def load_test_config(self, config_path: str) -> Dict:
        """
        載入 A/B 測試設定
        
        Args:
            config_path: 設定檔路徑
            
        Returns:
            測試設定字典
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def load_profile_config(self, config_path: str) -> Dict:
        """
        載入個人檔案設定
        
        Args:
            config_path: 設定檔路徑
            
        Returns:
            個人檔案設定字典
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def calculate_match_rate(self, swipe_records: List[Dict]) -> float:
        """
        計算配對率
        
        Args:
            swipe_records: 滑卡記錄列表
            
        Returns:
            配對率（百分比）
        """
        if not swipe_records:
            return 0.0

        right_swipes = [r for r in swipe_records if r.get('swipe_direction') == 'right']
        matches = [r for r in right_swipes if r.get('is_match', False)]

        if not right_swipes:
            return 0.0

        return (len(matches) / len(right_swipes)) * 100

    def analyze_test_results(
        self,
        profile_a_records: List[Dict],
        profile_b_records: List[Dict]
    ) -> Dict:
        """
        分析 A/B 測試結果
        
        Args:
            profile_a_records: Profile A 的滑卡記錄
            profile_b_records: Profile B 的滑卡記錄
            
        Returns:
            分析結果
        """
        # Profile A 統計
        profile_a_right = [r for r in profile_a_records if r.get('swipe_direction') == 'right']
        profile_a_left = [r for r in profile_a_records if r.get('swipe_direction') == 'left']
        profile_a_matches = [r for r in profile_a_right if r.get('is_match', False)]

        # Profile B 統計
        profile_b_right = [r for r in profile_b_records if r.get('swipe_direction') == 'right']
        profile_b_left = [r for r in profile_b_records if r.get('swipe_direction') == 'left']
        profile_b_matches = [r for r in profile_b_right if r.get('is_match', False)]

        # 計算配對率
        profile_a_match_rate = self.calculate_match_rate(profile_a_records)
        profile_b_match_rate = self.calculate_match_rate(profile_b_records)

        # 決定勝者
        if profile_a_match_rate > profile_b_match_rate * 1.1:  # 需要有 10% 以上的差距
            winner = 'profile_a'
            confidence = 'high' if profile_a_match_rate > profile_b_match_rate * 1.2 else 'medium'
        elif profile_b_match_rate > profile_a_match_rate * 1.1:
            winner = 'profile_b'
            confidence = 'high' if profile_b_match_rate > profile_a_match_rate * 1.2 else 'medium'
        else:
            winner = 'tie'
            confidence = 'low'

        return {
            'profile_a': {
                'total_swipes': len(profile_a_records),
                'right_swipes': len(profile_a_right),
                'left_swipes': len(profile_a_left),
                'matches': len(profile_a_matches),
                'match_rate': profile_a_match_rate
            },
            'profile_b': {
                'total_swipes': len(profile_b_records),
                'right_swipes': len(profile_b_right),
                'left_swipes': len(profile_b_left),
                'matches': len(profile_b_matches),
                'match_rate': profile_b_match_rate
            },
            'winner': winner,
            'confidence': confidence,
            'recommendation': self._generate_recommendation(winner, profile_a_match_rate, profile_b_match_rate)
        }

    def _generate_recommendation(self, winner: str, rate_a: float, rate_b: float) -> str:
        """
        生成建議
        
        Args:
            winner: 勝者
            rate_a: Profile A 配對率
            rate_b: Profile B 配對率
            
        Returns:
            建議文字
        """
        if winner == 'profile_a':
            improvement = ((rate_a - rate_b) / rate_b * 100) if rate_b > 0 else 100
            return f"建議使用 Profile A，配對率高出 {improvement:.1f}%"
        elif winner == 'profile_b':
            improvement = ((rate_b - rate_a) / rate_a * 100) if rate_a > 0 else 100
            return f"建議使用 Profile B，配對率高出 {improvement:.1f}%"
        else:
            return "兩個檔案表現相近，建議繼續測試或混合使用"

    def generate_report(self, test_results: Dict) -> str:
        """
        生成測試報告
        
        Args:
            test_results: 測試結果
            
        Returns:
            格式化的報告文字
        """
        report = []
        report.append("=" * 60)
        report.append("A/B 測試報告")
        report.append("=" * 60)
        report.append("")

        # Profile A 結果
        report.append("Profile A 表現:")
        report.append(f"  總滑卡數: {test_results['profile_a']['total_swipes']}")
        report.append(f"  右滑數: {test_results['profile_a']['right_swipes']}")
        report.append(f"  配對數: {test_results['profile_a']['matches']}")
        report.append(f"  配對率: {test_results['profile_a']['match_rate']:.2f}%")
        report.append("")

        # Profile B 結果
        report.append("Profile B 表現:")
        report.append(f"  總滑卡數: {test_results['profile_b']['total_swipes']}")
        report.append(f"  右滑數: {test_results['profile_b']['right_swipes']}")
        report.append(f"  配對數: {test_results['profile_b']['matches']}")
        report.append(f"  配對率: {test_results['profile_b']['match_rate']:.2f}%")
        report.append("")

        # 結論
        report.append("測試結論:")
        report.append(f"  勝者: {test_results['winner'].upper()}")
        report.append(f"  信心水準: {test_results['confidence'].upper()}")
        report.append(f"  建議: {test_results['recommendation']}")
        report.append("")
        report.append("=" * 60)

        return "\n".join(report)


# 使用範例
if __name__ == '__main__':
    # 建立測試管理器
    db_client = DatabaseClient()
    manager = ABTestManager(db_client)

    # 模擬測試資料
    profile_a_data = [
        {'swipe_direction': 'right', 'is_match': True},
        {'swipe_direction': 'right', 'is_match': False},
        {'swipe_direction': 'right', 'is_match': True},
        {'swipe_direction': 'left', 'is_match': False},
        {'swipe_direction': 'right', 'is_match': False},
    ]

    profile_b_data = [
        {'swipe_direction': 'right', 'is_match': False},
        {'swipe_direction': 'right', 'is_match': True},
        {'swipe_direction': 'left', 'is_match': False},
        {'swipe_direction': 'right', 'is_match': False},
        {'swipe_direction': 'right', 'is_match': False},
    ]

    # 分析結果
    results = manager.analyze_test_results(profile_a_data, profile_b_data)
    
    # 生成報告
    report = manager.generate_report(results)
    print(report)

