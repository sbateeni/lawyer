from flask import Blueprint, render_template, jsonify, request
from services.legal_library import LegalLibraryService

legal_library_bp = Blueprint('legal_library', __name__)
legal_service = LegalLibraryService()

@legal_library_bp.route('/legal-library')
def legal_library_page():
    """عرض صفحة المكتبة القانونية"""
    return render_template('legal_library.html')

@legal_library_bp.route('/api/legal-library/search', methods=['POST'])
async def search_legal():
    """البحث في القوانين"""
    query = request.json.get('query', '')
    results = await legal_service.search_legal_info(query)
    return jsonify({
        'status': 'success',
        'results': results
    })

@legal_library_bp.route('/api/legal-library/law/<int:law_id>')
async def get_law(law_id):
    """الحصول على تفاصيل قانون محدد"""
    details = await legal_service.get_law_details(law_id)
    return jsonify({
        'status': 'success',
        'law': details
    })

@legal_library_bp.route('/api/legal-library/updates')
async def get_updates():
    """الحصول على آخر التحديثات"""
    updates = await legal_service.get_latest_updates()
    return jsonify({
        'status': 'success',
        'updates': updates
    }) 