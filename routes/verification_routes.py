from flask import Blueprint, jsonify, request
from services.verification_service import VerificationService

verification_bp = Blueprint('verification', __name__)
verification_service = VerificationService()

@verification_bp.route('/api/verify', methods=['POST'])
def verify_stage():
    """
    Endpoint to verify a stage's legal text
    """
    try:
        data = request.get_json()
        stage_text = data.get('text')
        stage_type = data.get('stage_type')
        
        if not stage_text or not stage_type:
            return jsonify({
                'success': False,
                'error': 'النص ونوع المرحلة مطلوبان'
            }), 400
            
        is_matching, result, source = verification_service.verify_legal_text(
            stage_text=stage_text,
            stage_type=stage_type
        )
        
        return jsonify({
            'success': True,
            'is_matching': is_matching,
            'result': result,
            'source': source
        })
        
    except Exception as e:
        print(f"Error in verification: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500 