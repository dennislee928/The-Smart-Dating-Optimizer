"""
統計報告生成器
生成各種統計報告與視覺化數據
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

import pandas as pd


class StatsGenerator:
    """統計報告生成器類別"""

    def __init__(self):
        """初始化統計生成器"""
        pass

    def records_to_dataframe(self, records: List[Dict]) -> pd.DataFrame:
        """
        將記錄轉換為 DataFrame
        
        Args:
            records: 滑卡記錄列表
            
        Returns:
            Pandas DataFrame
        """
        return pd.DataFrame(records)

    def generate_daily_stats(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        生成每日統計
        
        Args:
            df: 滑卡記錄 DataFrame
            
        Returns:
            每日統計 DataFrame
        """
        if 'swiped_at' not in df.columns:
            return pd.DataFrame()

        df['date'] = pd.to_datetime(df['swiped_at']).dt.date
        
        daily_stats = df.groupby('date').agg({
            'id': 'count',  # 總滑卡數
            'is_match': 'sum'  # 配對數
        }).rename(columns={
            'id': 'total_swipes',
            'is_match': 'matches'
        })

        daily_stats['match_rate'] = (daily_stats['matches'] / daily_stats['total_swipes'] * 100).round(2)
        
        return daily_stats

    def generate_time_distribution(self, df: pd.DataFrame) -> Dict:
        """
        生成時間分布統計
        
        Args:
            df: 滑卡記錄 DataFrame
            
        Returns:
            時間分布字典
        """
        if 'swiped_at' not in df.columns:
            return {}

        df['hour'] = pd.to_datetime(df['swiped_at']).dt.hour
        
        hourly_stats = df.groupby('hour').size().to_dict()
        
        return {
            'hourly_distribution': hourly_stats,
            'peak_hour': max(hourly_stats, key=hourly_stats.get) if hourly_stats else None
        }

    def generate_age_stats(self, df: pd.DataFrame) -> Dict:
        """
        生成年齡統計
        
        Args:
            df: 滑卡記錄 DataFrame
            
        Returns:
            年齡統計字典
        """
        if 'target_age' not in df.columns:
            return {}

        age_data = df[df['target_age'] > 0]['target_age']

        if age_data.empty:
            return {}

        return {
            'avg_age': round(age_data.mean(), 1),
            'min_age': int(age_data.min()),
            'max_age': int(age_data.max()),
            'median_age': int(age_data.median()),
            'age_distribution': age_data.value_counts().to_dict()
        }

    def generate_distance_stats(self, df: pd.DataFrame) -> Dict:
        """
        生成距離統計
        
        Args:
            df: 滑卡記錄 DataFrame
            
        Returns:
            距離統計字典
        """
        if 'target_distance' not in df.columns:
            return {}

        distance_data = df[df['target_distance'] > 0]['target_distance']

        if distance_data.empty:
            return {}

        return {
            'avg_distance': round(distance_data.mean(), 1),
            'min_distance': int(distance_data.min()),
            'max_distance': int(distance_data.max()),
            'median_distance': int(distance_data.median())
        }

    def generate_swipe_direction_stats(self, df: pd.DataFrame) -> Dict:
        """
        生成滑卡方向統計
        
        Args:
            df: 滑卡記錄 DataFrame
            
        Returns:
            滑卡方向統計字典
        """
        if 'swipe_direction' not in df.columns:
            return {}

        direction_counts = df['swipe_direction'].value_counts().to_dict()
        total = len(df)

        return {
            'counts': direction_counts,
            'percentages': {k: round(v / total * 100, 2) for k, v in direction_counts.items()},
            'right_swipe_rate': round(direction_counts.get('right', 0) / total * 100, 2) if total > 0 else 0
        }

    def generate_comprehensive_report(self, records: List[Dict]) -> Dict:
        """
        生成綜合統計報告
        
        Args:
            records: 滑卡記錄列表
            
        Returns:
            綜合統計報告字典
        """
        if not records:
            return {'error': '沒有記錄可供分析'}

        df = self.records_to_dataframe(records)

        report = {
            'summary': {
                'total_records': len(df),
                'date_range': {
                    'start': str(df['swiped_at'].min()) if 'swiped_at' in df.columns else None,
                    'end': str(df['swiped_at'].max()) if 'swiped_at' in df.columns else None
                }
            },
            'swipe_stats': self.generate_swipe_direction_stats(df),
            'age_stats': self.generate_age_stats(df),
            'distance_stats': self.generate_distance_stats(df),
            'time_stats': self.generate_time_distribution(df),
            'daily_stats': self.generate_daily_stats(df).to_dict() if not self.generate_daily_stats(df).empty else {}
        }

        return report

    def export_to_json(self, report: Dict, output_path: str):
        """
        匯出報告為 JSON
        
        Args:
            report: 報告字典
            output_path: 輸出檔案路徑
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

    def print_text_report(self, report: Dict):
        """
        印出文字格式報告
        
        Args:
            report: 報告字典
        """
        print("=" * 60)
        print("滑卡統計報告")
        print("=" * 60)
        print()

        if 'error' in report:
            print(f"錯誤: {report['error']}")
            return

        # 摘要
        print("摘要:")
        print(f"  總記錄數: {report['summary']['total_records']}")
        if report['summary']['date_range']['start']:
            print(f"  時間範圍: {report['summary']['date_range']['start']} ~ {report['summary']['date_range']['end']}")
        print()

        # 滑卡統計
        if report.get('swipe_stats'):
            print("滑卡統計:")
            for direction, count in report['swipe_stats'].get('counts', {}).items():
                percentage = report['swipe_stats']['percentages'].get(direction, 0)
                print(f"  {direction}: {count} ({percentage}%)")
            print()

        # 年齡統計
        if report.get('age_stats'):
            print("年齡統計:")
            print(f"  平均年齡: {report['age_stats'].get('avg_age', 0)}")
            print(f"  年齡範圍: {report['age_stats'].get('min_age', 0)} ~ {report['age_stats'].get('max_age', 0)}")
            print()

        # 距離統計
        if report.get('distance_stats'):
            print("距離統計:")
            print(f"  平均距離: {report['distance_stats'].get('avg_distance', 0)} km")
            print(f"  距離範圍: {report['distance_stats'].get('min_distance', 0)} ~ {report['distance_stats'].get('max_distance', 0)} km")
            print()

        print("=" * 60)


# 使用範例
if __name__ == '__main__':
    generator = StatsGenerator()

    # 模擬測試資料
    test_records = [
        {
            'id': 1,
            'target_age': 25,
            'target_distance': 5,
            'swipe_direction': 'right',
            'is_match': True,
            'swiped_at': '2025-10-11 10:00:00'
        },
        {
            'id': 2,
            'target_age': 28,
            'target_distance': 8,
            'swipe_direction': 'left',
            'is_match': False,
            'swiped_at': '2025-10-11 10:05:00'
        },
        {
            'id': 3,
            'target_age': 26,
            'target_distance': 3,
            'swipe_direction': 'right',
            'is_match': False,
            'swiped_at': '2025-10-11 11:00:00'
        }
    ]

    # 生成報告
    report = generator.generate_comprehensive_report(test_records)
    
    # 印出報告
    generator.print_text_report(report)
    
    # 匯出 JSON
    # generator.export_to_json(report, 'reports/stats_report.json')

