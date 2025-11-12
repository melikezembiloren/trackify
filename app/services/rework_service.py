from app.repositories.rework_repo import ReworkListRepository
from app.utils.db_connection import get_db
import logging
from flask import Response, json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    

class ReworkListService:

    @staticmethod
    def get_rework_list(line_id):

        try:
            db = next(get_db())
            reworks = ReworkListRepository.get_rework_list(db, line_id)

            rework_list = [{
                "id": rework.id,
                "tv_id": rework.tv_id,
                "tv_model": rework.tv.catalog.model_name,
                "defect_code": rework.defect_catalog.defect_code,
                "defect_name": rework.defect_catalog.defect_name,
                "defect_description": rework.defect_catalog.defect_description,
                "status": rework.status,
                "created_at": rework.created_at,
                "line_id": rework.line_id,
                "tv_seri_no": rework.tv.tv_seri_no,
                } 
                for rework in reworks]

            return {"status": "success", "message": "success", "data": rework_list}, 200
        
                 
        except Exception as e:
            logger.error(f"Error in ReworkListService.get_rework_list: {str(e)}")
            return {"message": "Rework listesi alınamadı"}, 500 
        

    @staticmethod
    def get_solution_list(defect_id):
        
        try:
            db = next(get_db())

            solutions = ReworkListRepository.get_solutions_by_defect(db, defect_id)

            if not solutions:

                return {"message": "Çözüm bulunamadı"}, 404
            
            solution_list = [{
                "id": s.id,
                "solution_name": s.solution_name
               
                }
                
                for s in solutions]
            
            return {"status": "success", "message": "success", "data": solution_list}, 200
        
        except Exception as e:
            logger.error(f"Error in ReworkListService.get_solutions_by_defect: {str(e)}")
            return {"message": "çözüm listesi alınamadı"}, 500 
            
            



    @staticmethod
    def create_rework_action(defect_id:int, 
                            applied_solution_id:int,
                            rework_by_pin: str,
                            solution_text: str = None,
                            caused_by_name: int = None):
        
        if not defect_id or not applied_solution_id:
            return {"message": "Zorunlu alanlar boş olamaz"}, 400
        
        
        db = next(get_db())
        
        rework_by = ReworkListRepository.get_operator_by_pin(db, rework_by_pin)    
        if not rework_by:
            return {"message": "Rework operatörü bulunamadı"}, 400
        
        
        defect = ReworkListRepository.get_defect_by_id(db, defect_id)
        if not defect:
            return {"message": "Hata bulunamadı"}, 400
        
        
        caused_by_id = None
        if caused_by_name:
            parts = caused_by_name.strip().split()

            if len(parts) >= 2:
                first_name = " ".join(parts[:-1])
                last_name = parts[-1]
                caused_by = ReworkListRepository.get_operator_by_name(db, first_name, last_name)
                if caused_by:
                    caused_by_id = caused_by.id
                else:
                    return {"message": "Sebep olan operatör bulunamadı"}, 404
            else:
                  return {"message": "Sebep olan operatör adı eksik girildi"}, 400 
            
        rework = ReworkListRepository.update_defect(
            db=db,
            defect_id=defect.id,
            rework_by_id=rework_by.id,
            caused_by_id=caused_by_id,
            applied_solution_id=applied_solution_id,
            solution_text=solution_text

        )

        logger.info(f"Rework tamamlandı: {rework.id}")

        return {
            "message": "Rework başarıyla tamamlandı"

        }, 201

        
        

