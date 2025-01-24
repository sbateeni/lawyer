from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.db_manager import db_manager
from services.utils import get_stage_title
from services.case_service import CaseService
from services.analysis_service import AnalysisService

case_bp = Blueprint('case', __name__)
case_service = CaseService()
analysis_service = AnalysisService()

@case_bp.route('/cases')
def cases():
    """عرض قائمة القضايا"""
    cases = db_manager.get_cases()
    return render_template('cases/list.html', cases=cases)

@case_bp.route('/case/new')
def new_case():
    """عرض نموذج إنشاء قضية جديدة"""
    return render_template('cases/new.html')

@case_bp.route('/case/<int:case_id>')
def case_details(case_id):
    """عرض تفاصيل القضية"""
    case = db_manager.get_case(case_id)
    if not case:
        return redirect(url_for('case.cases'))
    return render_template('cases/details.html', case=case, get_stage_title=get_stage_title)

@case_bp.route('/api/cases/new', methods=['POST'])
def create_case():
    """إنشاء قضية جديدة"""
    try:
        data = request.json
        case = case_service.create_case(
            title=data['title'],
            description=data['description'],
            parties=data.get('parties', [])
        )
        
        if case:
            return jsonify({
                "status": "success",
                "case": case
            })
        else:
            return jsonify({
                "status": "error",
                "error": "فشل في إنشاء القضية"
            }), 500
            
    except Exception as e:
        print(f"Error creating case: {str(e)}")
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@case_bp.route('/api/analyze', methods=['POST'])
def analyze_stage():
    try:
        data = request.get_json()
        case_id = data.get('case_id')
        stage = data.get('stage')
        model_type = data.get('model_type')
        text = data.get('text')
        
        if not all([case_id, stage, model_type, text]):
            return jsonify({
                'status': 'error',
                'error': 'جميع الحقول مطلوبة'
            }), 400
            
        # تحليل المرحلة باستخدام النموذج المناسب
        result = analysis_service.analyze_stage(
            case_id=case_id,
            stage=stage,
            model_type=model_type,
            text=text
        )
        
        return jsonify({
            'status': 'success',
            'result': result
        })
        
    except Exception as e:
        print(f"Error in analyze_stage: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500 