from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.db_manager import db_manager
from services.utils import get_stage_title

case_bp = Blueprint('case', __name__)

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
    return render_template('cases/details.html', case=case, get_stage_title=get_stage_title)

@case_bp.route('/api/cases/new', methods=['POST'])
def create_case():
    """إنشاء قضية جديدة"""
    data = request.json
    case_id = db_manager.create_case(
        title=data['title'],
        description=data['description'],
        parties=data['parties']
    )
    return jsonify({
        "status": "success",
        "case_id": case_id
    }) 