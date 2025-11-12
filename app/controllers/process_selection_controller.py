from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.repositories.auth_repo import AuthRepository
from app.utils.db_connection import get_db  # SQLAlchemy session al

process_bp = Blueprint("process", __name__)

@process_bp.route('/process/selection', methods=['GET'])
@jwt_required()
def selectionpage():
    db = next(get_db())  # SQLAlchemy session al
    current_user = get_jwt_identity()  # JWT içindeki kullanıcı kimliği
    jwt_data = get_jwt()               # JWT’nin tamamını al
    line_claim = jwt_data.get("line")  # JWT’ye eklediğimiz "line" claim’ini al

    if not line_claim:
        return "JWT içinde line bilgisi bulunamadı", 400

    # 🔹 Repository katmanını kullanarak veritabanından line bilgisini çek
    line = AuthRepository.get_user_by_line(db, line_claim)

    if not line:
        return f"Line '{line_claim}' bulunamadı", 404

    # 🔹 Template'e line ve kullanıcı bilgisini gönder
    return render_template(
        'selection.html',
        user=current_user,
        line=line
    )