from flask import Blueprint, render_template, request, jsonify
from app.services.rework_service import ReworkListService
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


solution_bp = Blueprint("solution", __name__)
@solution_bp.route('/solutions/list', methods = ['POST'])
def get_solution_list():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Geçersiz istek, JSON bekleniyor"}), 400

        defect_id = data.get("defect_id")
        result,status = ReworkListService.get_solution_list(defect_id)
        return jsonify(result), status
    
    except Exception as e:
        return jsonify({"message": "Çözüm listesi alınamadı", "error": str(e)}), 500
    