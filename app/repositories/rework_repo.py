from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.models import Operators, DefectHistory, Defect, DefectCatalog, DefectSolution
from app.utils.now_utc import Now
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ReworkListRepository:

    @staticmethod
    def get_rework_list(db: Session, line_id:int):
        """
        Rework durumundaki tüm TV ve defect kayıtlarını listele
        """
        try:
            return db.query(Defect).filter(
                Defect.status == "REWORK",
                Defect.line_id == line_id ).all()
        except Exception as e:
            logger.error(f"Error getting rework defect list: {str(e)}")
            raise

    @staticmethod
    def get_operator_by_name(db: Session, first_name: str, last_name: str):
        try:
            if not first_name or not last_name:
                return None

            return db.query(Operators).filter(
                func.unaccent(Operators.first_name).ilike(func.unaccent(f"%{first_name}%")),
                func.unaccent(Operators.last_name).ilike(func.unaccent(f"%{last_name}%"))
            ).first()

        except Exception as e:
            logger.error(f"Error getting operator by name: {str(e)}")
            raise

    @staticmethod
    def get_operator_by_pin(db:Session, pin:str):

        try:
            return db.query(Operators).filter(Operators.pin_code == str(pin)).first()

        
        except Exception as e:
            logger.error(f"Error getting operator by pin code: {str(e)}")
            raise   

    
    @staticmethod
    def get_solutions_by_defect(db:Session, defect_id):
        try:
            defect = db.query(Defect).filter(Defect.id == defect_id).first()
            if not defect:
                return None
            
            return db.query(DefectSolution).filter(DefectSolution.defect_catalog_id == defect.defect_catalog_id).all()
    
     
        
        except Exception as e:
            logger.error(f"Error getting solutionn list: {str(e)}")
            raise   


    
    @staticmethod
    def get_defect_by_id(db:Session, defect_id:int):
        try:
            return db.query(Defect).filter(Defect.id == defect_id).first()
        
        except Exception as e:
            logger.error(f"Error getting defect: {str(e)}")
            raise  



    @staticmethod
    def update_defect(
        db: Session, 
        defect_id: int,  
        applied_solution_id: int,
        rework_by_id: int,
        solution_text: str = None,
        caused_by_id: int = None
    ):
        try:
            defect = db.query(Defect).filter(Defect.id == defect_id).first()
            
            if not defect:
                return None

            defect.applied_solution_id = applied_solution_id
            defect.status = "OK"
            defect.rework_by_id = rework_by_id
            defect.solution_text = solution_text
            defect.caused_by_id = caused_by_id


            db.commit()
            db.refresh(defect)

            history = DefectHistory(
                defect_id=defect.id,
                event_type="REWORK_DONE",
                operator_id=rework_by_id,
                commit=solution_text,
                created_at=Now.now_utc()
            )

            db.add(history)
            db.commit()

            return defect

        except Exception as e:
            db.rollback()
            logger.error(f"Error updating defect: {str(e)}")
            raise
