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
        return sorted(self.cases, key=lambda x: x['date'], reverse=True)
    
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
            'status': 'قيد الانتظار',
            'analyses': [],
            'current_stage': 1,
            'completion_percentage': 0,
            'last_update': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.cases.append(case)
        self.statistics['total_cases'] += 1
        self.statistics['pending_analyses'] += 1
        return case_id
    
    def add_analysis(self, case_id, stage, result):
        """إضافة تحليل لقضية"""
        case = self.get_case(case_id)
        if case:
            # إضافة التحليل
            analysis = {
                'stage': stage,
                'result': result,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            case['analyses'].append(analysis)
            
            # تحديث المرحلة الحالية
            case['current_stage'] = stage + 1
            
            # حساب نسبة الإكمال
            total_stages = 12  # عدد المراحل الكلي
            case['completion_percentage'] = int((len(case['analyses']) / total_stages) * 100)
            
            # تحديث الحالة
            if stage == 1:  # بداية التحليل
                case['status'] = 'قيد التحليل'
            elif stage == total_stages:  # اكتمال التحليل
                case['status'] = 'مكتملة'
                self.statistics['completed_analyses'] += 1
                self.statistics['pending_analyses'] -= 1
            
            # تحديث وقت آخر تعديل
            case['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            return True
        return False
    
    def get_case_status(self, case_id):
        """الحصول على حالة القضية"""
        case = self.get_case(case_id)
        if case:
            return {
                'status': case['status'],
                'current_stage': case['current_stage'],
                'completion_percentage': case['completion_percentage'],
                'last_update': case['last_update']
            }
        return None

db_manager = DatabaseManager() 