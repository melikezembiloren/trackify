from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.defect_entry_service import DefectEntryService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


defect_entry_bp = Blueprint("defect", __name__)

@defect_entry_bp.route('/defect', methods=['GET'])
@jwt_required()
def defectpage():
    return render_template('defect_entry.html')


@defect_entry_bp.route('/defect/entry', methods=['POST'])
@jwt_required()
def addDefect():
    
    try:

        data = request.get_json()
        if not data:
            return jsonify({"message": "Geçersiz istek formatı. JSON bekleniyor."}), 400
        
        tv_seri_no = data.get('tv_seri_no')
        defect_catalog_id = data.get('defect_catalog_id')
        found_by_pin = data.get('found_by_pin') #optional
        status = data.get('status')

        line_id = get_jwt_identity()

        result, status = DefectEntryService.add_defect(
            tv_seri_no=tv_seri_no,
            defect_catalog_id=defect_catalog_id,
            found_by_pin=found_by_pin,
            status=status,
            line_id=line_id,
            catalog_id=None  
        )

        return jsonify(result), status       


    except Exception as e:
        logger.exception("Hata eklenirken bir sorun oluştu.")
        return jsonify({"message": "Sunucu hatası oluştu.", "error": str(e)}), 500







