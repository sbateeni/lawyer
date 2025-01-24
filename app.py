import os
import sys
import traceback
import importlib

# إضافة مسار المشروع إلى sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
sys.path.insert(0, os.path.dirname(project_root))

print("Python Path:", sys.path)

try:
    # محاولة استيراد الوحدات بشكل مستقل للتشخيص
    print("Attempting to import modules...")
    
    print("Importing Flask...")
    from flask import Flask, render_template, request, jsonify
    
    print("Importing routes...")
    from routes.analysis_routes import analysis_bp
    from routes.document_analysis_routes import document_analysis_bp
    from routes.document_information_routes import document_information_bp
    from routes.legal_library_routes import legal_library_bp
    from routes.case_routes import case_bp
    from routes.verification_routes import verification_bp
    
    print("Importing chat routes...")
    from chat_builder.routes.chat_routes import chat_bp
    
    print("Importing dotenv...")
    from dotenv import load_dotenv

    print("Loading environment variables...")
    load_dotenv()

    print("Creating Flask app...")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max-limit

    print("Registering blueprints...")
    app.register_blueprint(analysis_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(document_analysis_bp)
    app.register_blueprint(document_information_bp)
    app.register_blueprint(legal_library_bp)
    app.register_blueprint(case_bp)
    app.register_blueprint(verification_bp)

    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/index')
    def index():
        return render_template('index.html')

    @app.route('/legal_documents')
    def legal_documents():
        return render_template('legal_documents.html')

    @app.route('/legal_articles')
    def legal_articles():
        return render_template('legal_articles.html')

    @app.route('/legal_articles/human_rights')
    def human_rights():
        return render_template('legal_articles/human_rights.html')

    @app.route('/legal_articles/arbitration')
    def arbitration():
        return render_template('legal_articles/arbitration.html')

    @app.route('/legal_articles/labor_law_changes')
    def labor_law_changes():
        return render_template('legal_articles/labor_law_changes.html')

    @app.route('/legal_articles/legal_responsibility_doctors')
    def legal_responsibility_doctors():
        return render_template('legal_articles/legal_responsibility_doctors.html')

    @app.route('/appointment_management')
    def appointment_management():
        return render_template('appointment_management.html')

    @app.route('/faq')
    def faq():
        return render_template('faq.html')

    @app.route('/lawyer_rating')
    def lawyer_rating():
        return render_template('lawyer_rating.html')

    @app.route('/law_information')
    def law_information():
        return render_template('law_information.html')

    @app.route('/contact')
    def contact():
        return render_template('contact.html')

    @app.route('/legal_resources')
    def legal_resources():
        return render_template('legal_resources.html')

    @app.route('/legal_models')
    def legal_models():
        return render_template('legal_models.html')

    @app.route('/legal_models/employment_contract')
    def employment_contract():
        return render_template('legal_models/employment_contract.html')

    @app.route('/legal_models/power_of_attorney')
    def power_of_attorney():
        return render_template('legal_models/power_of_attorney.html')

    @app.route('/legal_models/non_disclosure_agreement')
    def non_disclosure_agreement():
        return render_template('legal_models/non_disclosure_agreement.html')

    @app.route('/legal_models/appeal_form')
    def appeal_form():
        return render_template('legal_models/appeal_form.html')

    @app.route('/legal_models/rental_agreement')
    def rental_agreement():
        return render_template('legal_models/rental_agreement.html')

    @app.route('/document_analysis')
    def document_analysis():
        return render_template('document_analysis.html')

    @app.route('/login')
    def login():
        return render_template('auth/login.html')

    @app.route('/register')
    def register():
        return render_template('auth/register.html')

    @app.route('/user/dashboard')
    def user_dashboard():
        # بيانات تجريبية
        user = {
            'name': 'مستخدم تجريبي',
            'email': 'user@example.com'
        }
        stats = {
            'analysis_count': 5,
            'documents_count': 3,
            'consultations_count': 2
        }
        recent_analyses = [
            {
                'date': '2024-03-20',
                'type': 'تحليل عقد',
                'result': 'مكتمل'
            },
            {
                'date': '2024-03-18',
                'type': 'تحليل قضية',
                'result': 'قيد المراجعة'
            }
        ]
        return render_template('user_dashboard.html', 
                             user=user, 
                             stats=stats, 
                             recent_analyses=recent_analyses)

    if __name__ == '__main__':
        try:
            print("Starting Flask server...")
            print("Debug mode: enabled")
            print("Host: 0.0.0.0")
            print("Port: 5001")
            app.run(debug=True, host='0.0.0.0', port=5001)
        except Exception as e:
            print("Error starting server:")
            print(str(e))
            print(traceback.format_exc())

except Exception as e:
    print("Error occurred:")
    print(traceback.format_exc())
    
    # محاولة طباعة تفاصيل الاستيراد
    def print_import_details(module_name):
        try:
            module = importlib.import_module(module_name)
            print(f"Successfully imported {module_name}")
            print(f"Module path: {module.__file__}")
        except ImportError as ie:
            print(f"Failed to import {module_name}")
            print(ie)
    
    print_import_details('routes.analysis_routes')
    print_import_details('routes.document_analysis_routes')
    print_import_details('chat_builder.routes.chat_routes')