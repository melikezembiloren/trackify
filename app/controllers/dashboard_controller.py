from flask import Blueprint, request, jsonify, render_template
from app.services.auth_service import AuthService
from app.utils.db_connection import get_db
from app.utils.models import TV, Lines, Users
from flask_jwt_extended import jwt_required

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def login_page():
    return render_template('dashboard.html')


@dashboard_bp.route("/lines", methods=["GET"])
def get_lines():
    db = next(get_db())
    lines = db.query(Lines).all()

    result = []
    for line in lines:
        # TV tablosundan hatalı sayısını al
        defective_tv_count = db.query(TV).filter(TV.line_id==line.id).count()
        result.append({
            "line_id": line.id,
            "line_name": line.line_name,
            "line_code": line.line,
            "daily_target": getattr(line, "daily_target", 0),
            "weekly_target": getattr(line, "weekly_target", 0),
            "monthly_target": getattr(line, "monthly_target", 0),
            "defective_tv": defective_tv_count
        })
    return jsonify(result)


# Kullanıcı profil bilgisi
@dashboard_bp.route("/user/profile", methods=["GET"])
def get_profile():
    db = next(get_db())
    # Örnek: user_id session veya token’dan alınmalı
    user = db.query(Users).filter(Users.id==1).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "user_id": user.id,
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "title": user.title
    })

