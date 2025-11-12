from app.repositories.auth_repo import AuthRepository
from app.utils.db_connection import get_db
import logging
from app.utils.auth_helper import AuthHelper
from flask_jwt_extended import create_access_token, set_access_cookies
from flask import Response, json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
    


class AuthService:


    @staticmethod
    def auth_with_username(username:str , password: str):
        

        if not username or not password:
            return {"message": "username and password are required"}, 400
        
        
        try:
            db = next(get_db())


            user = AuthRepository.get_user_by_username(db, username)
            if not user:
                return {"message": "user not found"}, 404
            
            if not AuthHelper.verify_password(password, user.password_hash):
                return {"message": "Invalid password"}, 401
            
            access_token = create_access_token(
            identity=str(user.id)
        )

            
            resp = Response(
                response=json.dumps({
                    "message": "Login successful",
                    "user_id": user.id,
                    "user_name": user.username  
                }),
                status=200,
                mimetype='application/json'
            )

            # Cookie’ye token ekle
            set_access_cookies(resp, access_token)

            return resp
            
           
        except Exception as e:
            logger.error(f"Error in login_user: {str(e)}")
            return {"message": "Failed to login", "error": str(e)}, 500

        


    @staticmethod
    def auth_with_line_name(linename:str , password: str):

        

        if not linename or not password:
            return {"message": "line name and password are required"}, 400
        
        
        try:
            db = next(get_db())


            production_line = AuthRepository.get_user_by_linename(db, linename)
            if not production_line:
                return {"message": "Line not found"}, 404
            
            if not AuthHelper.verify_password(password, production_line.line_password_hash):
                return {"message": "Invalid password"}, 401
            
            access_token = create_access_token(
            identity=str(production_line.id),
            additional_claims={"line": production_line.line}
        )

            
            resp = Response(
                response=json.dumps({
                    "message": "Login successful",
                    "line_id": production_line.id,
                    "line_name": production_line.line_name
                }),
                status=200,
                mimetype='application/json'
            )

            # Cookie’ye token ekle
            set_access_cookies(resp, access_token)

            return resp
            
           
        except Exception as e:
            logger.error(f"Error in login_user: {str(e)}")
            return {"message": "Failed to login", "error": str(e)}, 500



    
