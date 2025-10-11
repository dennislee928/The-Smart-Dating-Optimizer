"""
資料庫客戶端
用於 Python 自動化腳本與 PostgreSQL 資料庫互動
"""

import os
from datetime import datetime
from typing import Dict, List, Optional

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Text, DECIMAL, BigInteger, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

Base = declarative_base()


class SwipeRecord(Base):
    """滑卡記錄 ORM 模型"""
    __tablename__ = 'swipe_records'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dating_account_id = Column(BigInteger, nullable=False)
    profile_id = Column(BigInteger)
    ab_test_id = Column(BigInteger)
    target_name = Column(String(100))
    target_age = Column(Integer)
    target_bio = Column(Text)
    target_photos = Column(JSON)
    target_distance = Column(Integer)
    swipe_direction = Column(String(10), nullable=False)
    is_match = Column(Boolean, default=False)
    ai_score = Column(DECIMAL(5, 2))
    decision_reason = Column(Text)
    swiped_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)


class AutomationLog(Base):
    """自動化日誌 ORM 模型"""
    __tablename__ = 'automation_logs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    dating_account_id = Column(BigInteger, nullable=False)
    action_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    metadata = Column(JSON)
    executed_at = Column(DateTime, default=datetime.utcnow)


class DatabaseClient:
    """資料庫客戶端類別"""

    def __init__(self):
        """初始化資料庫連線"""
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = os.getenv('DB_PORT', '5432')
        db_user = os.getenv('DB_USER', 'postgres')
        db_password = os.getenv('DB_PASSWORD', '')
        db_name = os.getenv('DB_NAME', 'smart_dating_optimizer')

        connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        self.engine = create_engine(connection_string, echo=False)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """取得資料庫 session"""
        return self.SessionLocal()

    def save_swipe_record(
        self,
        dating_account_id: int,
        profile_data: Dict,
        swipe_direction: str,
        is_match: bool = False,
        profile_id: Optional[int] = None,
        ab_test_id: Optional[int] = None,
        ai_score: Optional[float] = None,
        decision_reason: Optional[str] = None
    ) -> bool:
        """
        儲存滑卡記錄
        
        Args:
            dating_account_id: 社交帳號 ID
            profile_data: 個人檔案資料
            swipe_direction: 滑卡方向 ('left', 'right', 'super')
            is_match: 是否配對成功
            profile_id: 使用的個人檔案 ID
            ab_test_id: A/B 測試 ID
            ai_score: AI 評分
            decision_reason: 決策原因
            
        Returns:
            是否成功儲存
        """
        session = self.get_session()
        
        try:
            record = SwipeRecord(
                dating_account_id=dating_account_id,
                profile_id=profile_id,
                ab_test_id=ab_test_id,
                target_name=profile_data.get('name', ''),
                target_age=profile_data.get('age', 0),
                target_bio=profile_data.get('bio', ''),
                target_photos=profile_data.get('photos', []),
                target_distance=profile_data.get('distance', 0),
                swipe_direction=swipe_direction,
                is_match=is_match,
                ai_score=ai_score,
                decision_reason=decision_reason,
                swiped_at=datetime.fromisoformat(profile_data.get('timestamp', datetime.now().isoformat()))
            )
            
            session.add(record)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"儲存滑卡記錄失敗: {str(e)}")
            return False
            
        finally:
            session.close()

    def save_automation_log(
        self,
        dating_account_id: int,
        action_type: str,
        status: str,
        error_message: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        儲存自動化日誌
        
        Args:
            dating_account_id: 社交帳號 ID
            action_type: 動作類型
            status: 狀態 ('success', 'failed', 'warning')
            error_message: 錯誤訊息
            metadata: 額外資訊
            
        Returns:
            是否成功儲存
        """
        session = self.get_session()
        
        try:
            log = AutomationLog(
                dating_account_id=dating_account_id,
                action_type=action_type,
                status=status,
                error_message=error_message,
                metadata=metadata or {}
            )
            
            session.add(log)
            session.commit()
            return True
            
        except Exception as e:
            session.rollback()
            print(f"儲存自動化日誌失敗: {str(e)}")
            return False
            
        finally:
            session.close()

    def batch_save_swipe_records(self, records: List[Dict], dating_account_id: int) -> int:
        """
        批次儲存滑卡記錄
        
        Args:
            records: 滑卡記錄列表
            dating_account_id: 社交帳號 ID
            
        Returns:
            成功儲存的記錄數
        """
        session = self.get_session()
        success_count = 0
        
        try:
            for record_data in records:
                record = SwipeRecord(
                    dating_account_id=dating_account_id,
                    target_name=record_data.get('name', ''),
                    target_age=record_data.get('age', 0),
                    target_bio=record_data.get('bio', ''),
                    target_photos=record_data.get('photos', []),
                    target_distance=record_data.get('distance', 0),
                    swipe_direction=record_data.get('swipe_direction', 'left'),
                    is_match=record_data.get('is_match', False),
                    swiped_at=datetime.fromisoformat(record_data.get('timestamp', datetime.now().isoformat()))
                )
                session.add(record)
                success_count += 1
                
            session.commit()
            
        except Exception as e:
            session.rollback()
            print(f"批次儲存失敗: {str(e)}")
            
        finally:
            session.close()
            
        return success_count


# 使用範例
if __name__ == '__main__':
    # 建立資料庫客戶端
    db_client = DatabaseClient()
    
    # 測試儲存滑卡記錄
    test_profile = {
        'name': 'Test User',
        'age': 25,
        'bio': 'Test bio',
        'distance': 5,
        'photos': ['url1', 'url2'],
        'timestamp': datetime.now().isoformat()
    }
    
    success = db_client.save_swipe_record(
        dating_account_id=1,
        profile_data=test_profile,
        swipe_direction='right',
        is_match=False
    )
    
    print(f"儲存測試記錄: {'成功' if success else '失敗'}")

