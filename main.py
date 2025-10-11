#!/usr/bin/env python3
"""
Smart Dating Optimizer - 主程式入口
智慧社交改善器
"""

import argparse
import asyncio
import sys
import os
from pathlib import Path

# 將專案路徑加入 Python path
sys.path.append(str(Path(__file__).parent))
sys.path.append(str(Path(__file__).parent / 'automations'))
sys.path.append(str(Path(__file__).parent / 'analysis'))

from automations.tinder_bot import TinderBot
from automations.database_client import DatabaseClient
from analysis.profile_analyzer import ProfileAnalyzer
from analysis.ab_test_manager import ABTestManager
from analysis.stats_generator import StatsGenerator
from analysis.ai_scorer import AIScorer


def print_banner():
    """印出專案 Banner"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          Smart Dating Optimizer                          ║
    ║          智慧社交改善器                                    ║
    ║                                                           ║
    ║          提升你的社交軟體配對表現                           ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


async def run_automation(args):
    """執行自動化滑卡"""
    print("\n[自動化模式] 啟動 Tinder 機器人...")
    
    bot = TinderBot(headless=args.headless)
    db_client = DatabaseClient()
    
    try:
        await bot.init_browser()
        await bot.navigate_to_tinder()
        
        print("\n請手動登入 Tinder...")
        input("登入完成後按 Enter 繼續...")
        
        if await bot.wait_for_main_page():
            print(f"\n開始自動滑卡，共 {args.count} 次...")
            records = await bot.auto_swipe(
                count=args.count,
                strategy=args.strategy
            )
            
            # 儲存至資料庫
            if args.account_id:
                saved_count = db_client.batch_save_swipe_records(
                    records,
                    dating_account_id=args.account_id
                )
                print(f"\n已儲存 {saved_count} 筆記錄至資料庫")
            
            print("\n自動化完成！")
        
    except Exception as e:
        print(f"\n錯誤: {str(e)}")
    
    finally:
        await bot.close_browser()


def run_analysis(args):
    """執行數據分析"""
    print("\n[分析模式] 生成統計報告...")
    
    # TODO: 從資料庫讀取記錄
    # 這裡使用模擬資料作為範例
    test_records = []
    
    generator = StatsGenerator()
    report = generator.generate_comprehensive_report(test_records)
    generator.print_text_report(report)
    
    if args.output:
        generator.export_to_json(report, args.output)
        print(f"\n報告已匯出至 {args.output}")


def run_ab_test(args):
    """執行 A/B 測試"""
    print("\n[A/B 測試模式] 開始測試...")
    
    db_client = DatabaseClient()
    manager = ABTestManager(db_client)
    
    # 載入測試設定
    test_config = manager.load_test_config(args.config)
    print(f"\n測試名稱: {test_config.get('test_name')}")
    print(f"測試時長: {test_config.get('duration_days')} 天")
    print(f"每個檔案滑卡數: {test_config.get('swipes_per_profile')}")
    
    # TODO: 實現完整的 A/B 測試流程
    print("\nA/B 測試功能開發中...")


def run_ai_score(args):
    """執行 AI 評分"""
    print("\n[AI 評分模式] 初始化評分系統...")
    
    scorer = AIScorer()
    
    # 測試範例檔案
    test_profile = {
        'name': 'Test User',
        'age': 26,
        'bio': 'Love hiking, photography, and good coffee. Adventure seeker!',
        'distance': 5,
        'photos': ['url1', 'url2', 'url3', 'url4']
    }
    
    result = scorer.predict_score(test_profile)
    
    print("\nAI 評分結果:")
    print(f"  分數: {result['score']:.2f}")
    print(f"  建議: {result['recommendation'].upper()}")
    print(f"  理由: {result['reason']}")


def main():
    """主函式"""
    print_banner()
    
    parser = argparse.ArgumentParser(
        description='Smart Dating Optimizer - 智慧社交改善器'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用指令')
    
    # 自動化指令
    auto_parser = subparsers.add_parser('auto', help='執行自動化滑卡')
    auto_parser.add_argument('--count', type=int, default=10, help='滑卡次數')
    auto_parser.add_argument('--strategy', choices=['random', 'all_right', 'all_left'], 
                           default='random', help='滑卡策略')
    auto_parser.add_argument('--headless', action='store_true', help='無頭模式')
    auto_parser.add_argument('--account-id', type=int, help='社交帳號 ID')
    
    # 分析指令
    analysis_parser = subparsers.add_parser('analyze', help='生成統計分析報告')
    analysis_parser.add_argument('--output', help='輸出檔案路徑 (JSON)')
    analysis_parser.add_argument('--account-id', type=int, help='社交帳號 ID')
    
    # A/B 測試指令
    abtest_parser = subparsers.add_parser('abtest', help='執行 A/B 測試')
    abtest_parser.add_argument('--config', default='configs/ab_test_config.json',
                             help='測試設定檔路徑')
    
    # AI 評分指令
    ai_parser = subparsers.add_parser('aiscore', help='使用 AI 評分系統')
    ai_parser.add_argument('--model', help='模型檔案路徑')
    
    args = parser.parse_args()
    
    # 執行對應指令
    if args.command == 'auto':
        asyncio.run(run_automation(args))
    elif args.command == 'analyze':
        run_analysis(args)
    elif args.command == 'abtest':
        run_ab_test(args)
    elif args.command == 'aiscore':
        run_ai_score(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()

