from app.repositories.get_defect_catalog_repo import GetDefectCatalogRepository
from app.utils.db_connection import get_db
import logging
from flask import Response, json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    

class GetDefectCatalogService:

    @staticmethod
    def get_all_defects():

        try:
            db = next(get_db())
            defect_catalog_list = GetDefectCatalogRepository.get_defect_catalog(db)

            return [

                {
                    "id": d.id,
                    "defect_code": d.defect_code,
                    "defect_name": d.defect_name,
                    "defect_description": d.defect_description
                    
                }
                for d in defect_catalog_list
            ], 200

        except Exception as e:
            logger.error(f"Error in DefectCatalogService.get_all_defects: {str(e)}")
            return {"message": "Hata kataloğu alınamadı"}, 500       
