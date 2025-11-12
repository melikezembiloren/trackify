from sqlalchemy.orm import Session
from sqlalchemy import func
from app.utils.models import Defect
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GetAllListRepository:

    @staticmethod
    def get_all_list(db, line_id=None):
        query = db.query(Defect).order_by(Defect.created_at.asc())
        if line_id:
            query = query.filter(Defect.line_id == line_id)
        return query.all()
