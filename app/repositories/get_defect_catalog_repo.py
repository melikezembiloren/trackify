from sqlalchemy.orm import Session
from app.utils.models import DefectCatalog
import logging

logging. basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GetDefectCatalogRepository():

    @staticmethod
    def get_defect_catalog(db:Session):

        try:
            return db.query(DefectCatalog).order_by(DefectCatalog.id.asc()).all()
        
        except Exception as e:
            logger.error(f"Error getting defect catalog: {str(e)}")
            raise

