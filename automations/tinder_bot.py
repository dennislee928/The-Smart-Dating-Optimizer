"""
Tinder 自動化機器人
使用 Playwright 實現自動登入與滑卡功能
"""

import asyncio
import logging
import os
from datetime import datetime
from typing import Dict, List, Optional

from playwright.async_api import async_playwright, Page, Browser

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TinderBot:
    """Tinder 自動化機器人類別"""

    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.base_url = "https://tinder.com"
        
    async def init_browser(self):
        """初始化瀏覽器"""
        playwright = await async_playwright().start()
        self.browser = await playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await self.browser.new_context(
            viewport={'width': 1280, 'height': 720},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        )
        self.page = await context.new_page()
        logger.info("瀏覽器初始化完成")
        
    async def close_browser(self):
        """關閉瀏覽器"""
        if self.browser:
            await self.browser.close()
            logger.info("瀏覽器已關閉")
            
    async def navigate_to_tinder(self):
        """導航至 Tinder 網站"""
        await self.page.goto(self.base_url)
        logger.info(f"已導航至 {self.base_url}")
        await asyncio.sleep(2)
        
    async def login_with_phone(self, phone_number: str):
        """
        使用手機號碼登入
        
        Args:
            phone_number: 手機號碼
        """
        try:
            # 點擊登入按鈕
            login_button = await self.page.wait_for_selector('text="Log in"', timeout=5000)
            await login_button.click()
            logger.info("已點擊登入按鈕")
            await asyncio.sleep(1)
            
            # 選擇手機號碼登入
            phone_login = await self.page.wait_for_selector('text="Log in with phone number"', timeout=5000)
            await phone_login.click()
            logger.info("選擇手機號碼登入")
            await asyncio.sleep(1)
            
            # 輸入手機號碼
            phone_input = await self.page.wait_for_selector('input[type="tel"]', timeout=5000)
            await phone_input.fill(phone_number)
            logger.info(f"已輸入手機號碼: {phone_number}")
            
            # 點擊繼續
            continue_button = await self.page.wait_for_selector('button:has-text("Continue")', timeout=5000)
            await continue_button.click()
            logger.info("等待驗證碼...")
            
            # TODO: 實現驗證碼輸入邏輯
            # 這裡需要人工介入或整合驗證碼服務
            
        except Exception as e:
            logger.error(f"登入失敗: {str(e)}")
            raise
            
    async def wait_for_main_page(self):
        """等待主頁面載入完成"""
        try:
            await self.page.wait_for_selector('[aria-label="Like"]', timeout=30000)
            logger.info("主頁面載入完成")
            return True
        except Exception as e:
            logger.error(f"主頁面載入失敗: {str(e)}")
            return False
            
    async def get_current_profile_data(self) -> Dict:
        """
        取得當前顯示的個人檔案資料
        
        Returns:
            包含姓名、年齡、簡介等資訊的字典
        """
        profile_data = {
            'name': '',
            'age': 0,
            'bio': '',
            'distance': 0,
            'photos': [],
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # 取得姓名和年齡
            name_age_selector = 'span[itemprop="name"], span[itemprop="age"]'
            name_age_elements = await self.page.query_selector_all(name_age_selector)
            
            if len(name_age_elements) >= 2:
                profile_data['name'] = await name_age_elements[0].inner_text()
                age_text = await name_age_elements[1].inner_text()
                profile_data['age'] = int(age_text)
                
            # 取得簡介
            bio_selector = 'div[class*="Bdrs"]'
            bio_element = await self.page.query_selector(bio_selector)
            if bio_element:
                profile_data['bio'] = await bio_element.inner_text()
                
            # 取得距離資訊
            distance_selector = 'div:has-text("kilometer")'
            distance_element = await self.page.query_selector(distance_selector)
            if distance_element:
                distance_text = await distance_element.inner_text()
                profile_data['distance'] = int(''.join(filter(str.isdigit, distance_text)))
                
            logger.info(f"已取得個人檔案: {profile_data['name']}, {profile_data['age']}")
            
        except Exception as e:
            logger.error(f"取得個人檔案資料失敗: {str(e)}")
            
        return profile_data
        
    async def swipe_left(self):
        """向左滑（不喜歡）"""
        try:
            dislike_button = await self.page.wait_for_selector('[aria-label="Nope"]', timeout=5000)
            await dislike_button.click()
            logger.info("已執行左滑（不喜歡）")
            await asyncio.sleep(1)
            return True
        except Exception as e:
            logger.error(f"左滑失敗: {str(e)}")
            return False
            
    async def swipe_right(self):
        """向右滑（喜歡）"""
        try:
            like_button = await self.page.wait_for_selector('[aria-label="Like"]', timeout=5000)
            await like_button.click()
            logger.info("已執行右滑（喜歡）")
            await asyncio.sleep(1)
            
            # 檢查是否配對成功
            is_match = await self.check_for_match()
            return is_match
        except Exception as e:
            logger.error(f"右滑失敗: {str(e)}")
            return False
            
    async def super_like(self):
        """超級喜歡"""
        try:
            super_like_button = await self.page.wait_for_selector('[aria-label="Super Like"]', timeout=5000)
            await super_like_button.click()
            logger.info("已執行超級喜歡")
            await asyncio.sleep(1)
            
            # 檢查是否配對成功
            is_match = await self.check_for_match()
            return is_match
        except Exception as e:
            logger.error(f"超級喜歡失敗: {str(e)}")
            return False
            
    async def check_for_match(self) -> bool:
        """檢查是否出現配對畫面"""
        try:
            match_text = await self.page.query_selector('text="It\'s a Match!"', timeout=2000)
            if match_text:
                logger.info("配對成功！")
                # 關閉配對彈窗
                close_button = await self.page.query_selector('[aria-label="Close"]')
                if close_button:
                    await close_button.click()
                    await asyncio.sleep(1)
                return True
        except:
            pass
        return False
        
    async def auto_swipe(self, count: int, strategy: str = 'random') -> List[Dict]:
        """
        自動滑卡
        
        Args:
            count: 滑卡次數
            strategy: 策略 ('random', 'all_right', 'all_left')
            
        Returns:
            滑卡記錄列表
        """
        records = []
        
        for i in range(count):
            try:
                # 取得當前個人檔案資料
                profile_data = await self.get_current_profile_data()
                
                # 根據策略執行滑卡
                is_match = False
                if strategy == 'all_right':
                    is_match = await self.swipe_right()
                    direction = 'right'
                elif strategy == 'all_left':
                    await self.swipe_left()
                    direction = 'left'
                else:  # random
                    import random
                    if random.random() > 0.5:
                        is_match = await self.swipe_right()
                        direction = 'right'
                    else:
                        await self.swipe_left()
                        direction = 'left'
                        
                # 記錄滑卡資訊
                record = {
                    **profile_data,
                    'swipe_direction': direction,
                    'is_match': is_match
                }
                records.append(record)
                
                logger.info(f"進度: {i+1}/{count} - {profile_data['name']} - {direction}")
                
                # 隨機延遲，模擬人類行為
                import random
                await asyncio.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"第 {i+1} 次滑卡失敗: {str(e)}")
                continue
                
        logger.info(f"自動滑卡完成，共 {len(records)} 筆記錄")
        return records


async def main():
    """主程式"""
    # 讀取環境變數
    headless = os.getenv('HEADLESS_MODE', 'false').lower() == 'true'
    
    # 建立機器人實例
    bot = TinderBot(headless=headless)
    
    try:
        # 初始化瀏覽器
        await bot.init_browser()
        
        # 導航至 Tinder
        await bot.navigate_to_tinder()
        
        # TODO: 實現登入邏輯
        # await bot.login_with_phone('+886912345678')
        
        # TODO: 等待手動登入或實現自動登入
        logger.info("請手動登入 Tinder，登入完成後程式將繼續...")
        input("登入完成後請按 Enter 繼續...")
        
        # 等待主頁面載入
        if await bot.wait_for_main_page():
            # 執行自動滑卡
            records = await bot.auto_swipe(count=10, strategy='random')
            
            # 輸出記錄
            logger.info(f"滑卡記錄: {records}")
            
            # TODO: 將記錄儲存至資料庫
            
    except Exception as e:
        logger.error(f"程式執行錯誤: {str(e)}")
        
    finally:
        # 關閉瀏覽器
        await bot.close_browser()


if __name__ == '__main__':
    asyncio.run(main())

