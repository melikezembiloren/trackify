from sqlalchemy.orm import Session
from app.utils.models import Users, Lines
import logging

logging. basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuthRepository():

    @staticmethod
    def get_user_by_username(db:Session, username:str):

        try:
            return db.query(Users).filter(Users.username == username).first()
        
        except Exception as e:
            logger.error(f"Error getting user by username: {str(e)}")
            raise

    
    @staticmethod
    def get_user_by_linename(db:Session, linename:str):

        try:
            return db.query(Lines).filter(Lines.line_name == linename).first()
        
        except Exception as e:
            logger.error(f"Error getting user by line name: {str(e)}")
            raise

    @staticmethod
    def get_user_by_line(db: Session, line:str):
        try:
            return db.query(Lines).filter(Lines.line == line).first()
        
        except Exception as e:
            logger.error(f"Error getting user by line name: {str(e)}")
            raise

