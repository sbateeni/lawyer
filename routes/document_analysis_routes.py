from flask import Blueprint, request, jsonify
from services.document_analyzer import DocumentAnalyzer
import os
from werkzeug.utils import secure_filename

document_analysis_bp = Blueprint('document_analysis', __name__)
analyzer = DocumentAnalyzer()

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@document_analysis_bp.route('/api/analyze-document', methods=['POST'])
def analyze_document():
    """تحليل المستند المرفوع وإرجاع النتائج"""
    if 'file' not in request.files:
        return jsonify({'error': 'لم يتم إرفاق ملف'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'لم يتم اختيار ملف'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            analysis_results = analyzer.analyze_document(filepath)
            # حذف الملف بعد التحليل
            os.remove(filepath)
            return jsonify(analysis_results)
        except Exception as e:
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'نوع الملف غير مدعوم'}), 400

@document_analysis_bp.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    """إرجاع قائمة بأنواع الملفات المدعومة"""
    return jsonify({
        'formats': list(ALLOWED_EXTENSIONS),
        'max_file_size': '10MB'
    })
