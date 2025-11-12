from flask import Blueprint, jsonify, render_template
from app.services.get_all_list_service import GEtAllListService
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
import logging

logger = logging.getLogger(__name__)
all_list_bp = Blueprint("all_list", __name__)

@all_list_bp.route("/defect/list/all", methods=["GET"])
def view_defect_list():
    return render_template("defect_list.html")

@all_list_bp.route("/defect/list", methods=["GET"])
@jwt_required()
def get_all_list():
    try:
        line_id = get_jwt_identity()
        result, status = GEtAllListService.get_all_list(line_id)
        return jsonify(result), status

    except Exception as e:
        return jsonify({"message": "Liste alınamadı", "error": str(e)}), 500
    
