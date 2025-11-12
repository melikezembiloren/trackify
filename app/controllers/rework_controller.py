from flask import Blueprint, render_template, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.rework_service import ReworkListService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


rework_bp = Blueprint("rework", __name__)

@rework_bp.route('/rework', methods=['GET'])
@jwt_required()
def reworkpage():
    return render_template('rework_list.html')


@rework_bp.route('/rework/list', methods=['GET'])
@jwt_required()
def get_rework_list():

    try:
        line_id = get_jwt_identity()
        result, status = ReworkListService.get_rework_list(line_id)
        return jsonify(result), status

    except Exception as e:
        return jsonify({"message": "Rework listesi alınamadı", "error": str(e)}), 500
    

    
@rework_bp.route('/rework/complete', methods=['POST'])
@jwt_required()
def complete_rework():

    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Geçersiz istek, JSON bekleniyor"}), 400

        defect_id = data.get("defect_id")
        applied_solution_id = data.get("applied_solution_id")
        rework_by_pin = data.get("rework_by_pin")
        solution_text = data.get("solution_text")
        caused_by_name = data.get("caused_by_name")  # opsiyonel

        result, status = ReworkListService.create_rework_action(
            defect_id=defect_id,
            applied_solution_id=applied_solution_id,
            solution_text=solution_text,
            rework_by_pin=rework_by_pin,
            caused_by_name=caused_by_name
        )

        return jsonify(result), status

    except Exception as e:
        logger.exception("Rework tamamlama sırasında hata oluştu")
        return jsonify({"message": "Rework tamamlanamadı", "error": str(e)}), 500
