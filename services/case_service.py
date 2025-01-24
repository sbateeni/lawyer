from services.db_manager import db_manager
from typing import Dict, Optional, List

class CaseService:
    def create_case(self, title: str, description: str, parties: List[str] = None) -> Optional[Dict]:
        """
        إنشاء قضية جديدة
        """
        try:
            if parties is None:
                parties = []
                
            case_id = db_manager.create_case(
                title=title,
                description=description,
                parties=parties
            )
            
            if case_id:
                return {
                    'id': case_id,
                    'title': title,
                    'description': description,
                    'parties': parties,
                    'status': 'pending'
                }
            return None
        except Exception as e:
            print(f"Error creating case: {str(e)}")
            raise e
            
    def get_case(self, case_id: int) -> Optional[Dict]:
        """
        استرجاع تفاصيل قضية
        """
        try:
            case = db_manager.get_case(case_id)
            if case:
                return {
                    'id': case['id'],
                    'title': case['title'],
                    'description': case['description'],
                    'status': case['status'],
                    'analyses': case.get('analyses', [])
                }
            return None
        except Exception as e:
            print(f"Error getting case: {str(e)}")
            raise e 