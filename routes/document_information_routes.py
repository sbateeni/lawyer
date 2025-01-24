from flask import Blueprint, render_template

document_information_bp = Blueprint('document_information', __name__)

@document_information_bp.route('/family-law')
def family_law():
    return render_template('family_law.html')

@document_information_bp.route('/intellectual-property-law')
def intellectual_property_law():
    return render_template('intellectual_property_law.html') 