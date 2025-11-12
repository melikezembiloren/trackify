from app.repositories.get_all_list_repo import GetAllListRepository
from app.utils.db_connection import get_db
import logging
from flask import Response, json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GEtAllListService:
    @staticmethod
    def get_all_list(line_id):
        try:
            db = next(get_db())
            all_defects = GetAllListRepository.get_all_list(db, line_id)

            all_list = []
            for a in all_defects:
                try:
                    all_list.append({
                        "id": a.id,
                        "tv_id": a.tv_id,
                        "tv_model": a.tv.catalog.model_name if a.tv and a.tv.catalog else None,
                        "defect_code": a.defect_catalog.defect_code if a.defect_catalog else None,
                        "defect_name": a.defect_catalog.defect_name if a.defect_catalog else None,
                        "defect_description": a.defect_catalog.defect_description if a.defect_catalog else None,
                        "status": a.status,
                        "created_at": a.created_at.isoformat() if a.created_at else None,
                        "line_id": a.line_id,
                        "tv_seri_no": a.tv.tv_seri_no if a.tv else None,
                        
                         # ✅ Operatör isimleri
                        "found_by": f"{a.found_by.first_name} {a.found_by.last_name}" if a.found_by else None,
                        "caused_by": f"{a.caused_by.first_name} {a.caused_by.last_name}" if a.caused_by else None,
                        "rework_by": f"{a.rework_by.first_name} {a.rework_by.last_name}" if a.rework_by else None,
                    })
                except Exception as e:
                    logger.error(f"Error processing defect id {a.id}: {str(e)}")


    
            return {"status": "success", "message": "success", "data": all_list}, 200

        except Exception as e:
            logger.error(f"Error in GetAllListService.get_all_list: {str(e)}")
            return {"message": "Liste alınamadı"}, 500