from flask import Blueprint, jsonify
from app.services.get_defect_catalog_service import GetDefectCatalogService
import logging

logger = logging.getLogger(__name__)
defect_catalog_bp = Blueprint("defect_catalog", __name__)

@defect_catalog_bp.route("/catalog", methods=["GET"])
def get_defect_catalog():
    try:
        result, status = GetDefectCatalogService.get_all_defects()
        
        return jsonify(result), status
    except Exception as e:
        logger.exception("Katalog verisi alınamadı")
        return jsonify({"message": "Sunucu hatası"}), 500
