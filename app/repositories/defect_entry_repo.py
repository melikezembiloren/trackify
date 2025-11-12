from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.models import Operators, DefectCatalog, Defect, TV, TvCatalog, DefectHistory, DefectStatus, DefectEventType
from app.utils.now_utc import Now
import logging

logging. basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DefectEntryRepository():

    @staticmethod
    def get_operator_by_pin(db:Session, pin:str):

        try:
            return db.query(Operators).filter(Operators.pin_code == str(pin)).first()

        
        except Exception as e:
            logger.error(f"Error getting operator by pin code: {str(e)}")
            raise

    @staticmethod
    def get_tv_catalog_by_barcode_prefix(db:Session, tv_serial:str):
        try:
            catalogs = db.query(TvCatalog).all()

            for c in catalogs:
                if tv_serial.startswith(c.barcode_prefix):
                    return c
            return None
        
        except Exception as e:
            logger.error(f"Error getting catalog by serial prefix: {str(e)}")
            raise
        

    @staticmethod
    def get_tv_by_serial(db:Session, tv_serial:int):

        try: 
            return db.query(TV).filter(TV.tv_seri_no == tv_serial).first()
        
        except Exception as e:
            logger.error(f"Error getting TV: {str(e)}")
            raise
    
    @staticmethod
    def create_tv(db:Session, tv_seri_no: str, line_id:int, catalog_id:str):

        try:

            tv = TV(
                tv_seri_no = tv_seri_no,
                line_id = line_id,
                catalog_id = catalog_id
            )

            db.add(tv)
            db.commit()
            db.refresh(tv)
            db.commit()
            logger.info("TV başarıyla kaydedildi.")

            return tv
        
        except Exception as e:
            db.rollback()
            logger.error(f"Commit hatası: {e}")
            raise
    

    @staticmethod
    def create_defect(db: Session, tv_id: int, defect_catalog_id: int, found_by_id: int, status: str, line_id: int):
        try:
            # Defect oluştur
            defect = Defect(
                tv_id=tv_id,
                line_id=line_id,
                defect_catalog_id=defect_catalog_id,
                found_by_id=found_by_id,
                status=status,
                created_at=Now.now_utc()
            )

            db.add(defect)
            db.commit()       # her defect için ayrı commit
            db.refresh(defect)

            # History kaydı oluştur
            event_type = 'REWORK_START' if status == "REWORK" else "HURDA"
            history = DefectHistory(
                defect_id=defect.id,
                event_type=event_type,
                operator_id=found_by_id,
                created_at=Now.now_utc()
            )
            db.add(history)
            db.commit()       # history için de commit
            db.refresh(history)

            logger.info(f"Defect oluşturuldu: {defect.id}")

            return defect

        except Exception as e:
            db.rollback()
            logger.error(f"Defect oluşturulamadı: {e}")
            raise
