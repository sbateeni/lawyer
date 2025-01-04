import json
from datetime import datetime

class DatabaseManager:
    def __init__(self):
        self.cases = []
        self.statistics = {
            'total_cases': 0,
            'completed_analyses': 0,
            'pending_analyses': 0
        }
    
    def get_statistics(self):
        """الحصول على الإحصائيات"""
        return self.statistics
    
    def get_cases(self):
        """الحصول على قائمة القضايا"""
        return self.cases
    
    def get_case(self, case_id):
        """الحصول على تفاصيل قضية محددة"""
        for case in self.cases:
            if case.get('id') == case_id:
                return case
        return None
    
    def create_case(self, title, description, parties):
        """إنشاء قضية جديدة"""
        case_id = len(self.cases) + 1
        case = {
            'id': case_id,
            'title': title,
            'description': description,
            'parties': parties,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'جديدة',
            'analyses': [],
            'current_stage': 1
        }
        self.cases.append(case)
        self.statistics['total_cases'] += 1
        self.statistics['pending_analyses'] += 1
        return case_id
    
    def add_analysis(self, case_id, stage, result):
        """إضافة تحليل لقضية"""
        case = self.get_case(case_id)
        if case:
            analysis = {
                'stage': stage,
                'result': result,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            case['analyses'].append(analysis)
            case['current_stage'] = stage + 1
            
            if stage == 14:  # اكتمال جميع المراحل
                case['status'] = 'مكتملة'
                self.statistics['completed_analyses'] += 1
                self.statistics['pending_analyses'] -= 1
            
            return True
        return False

db_manager = DatabaseManager() 