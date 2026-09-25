import os
from flask import Flask, render_template, send_from_directory, jsonify
from dotenv import load_dotenv
from config import Config
from models import db, Crop
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.disease import disease_bp
from routes.assistant import assistant_bp
from routes.weather import weather_bp
from routes.reports import reports_bp

load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config: app.config.update(test_config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True); os.makedirs(os.path.dirname(app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")), exist_ok=True)
    db.init_app(app)
    app.register_blueprint(auth_bp); app.register_blueprint(dashboard_bp); app.register_blueprint(disease_bp); app.register_blueprint(assistant_bp); app.register_blueprint(weather_bp); app.register_blueprint(reports_bp)
    with app.app_context():
        db.create_all()
        if not Crop.query.count(): db.session.add_all([Crop(name=name) for name in ["Tomato", "Potato", "Rice", "Wheat", "Cotton", "Soybean", "Maize"]]); db.session.commit()
    @app.post("/api/soil/analyze")
    def soil_api():
        from flask import request, session
        from models import SoilAnalysis
        from services.recommendation_engine import soil_recommendation
        if not session.get("user_id"): return jsonify(error="Login required"), 401
        data = request.get_json(silent=True) or {}
        required = ["crop", "ph", "nitrogen", "phosphorus", "potassium", "moisture"]
        if any(key not in data or data[key] == "" for key in required): return jsonify(error="All soil fields are required."), 400
        try: result = soil_recommendation(data); row = SoilAnalysis(user_id=session["user_id"], crop=data["crop"], ph=float(data["ph"]), nitrogen=float(data["nitrogen"]), phosphorus=float(data["phosphorus"]), potassium=float(data["potassium"]), moisture=float(data["moisture"]), **result); db.session.add(row); db.session.commit(); return jsonify(result), 201
        except (ValueError, TypeError): return jsonify(error="Soil values must be numeric."), 400
    @app.post("/api/fertilizer/recommend")
    def fertilizer_api():
        from flask import request, session
        from models import Recommendation
        from services.recommendation_engine import fertilizer_recommendation
        if not session.get("user_id"): return jsonify(error="Login required"), 401
        data = request.get_json(silent=True) or {}
        try: result = fertilizer_recommendation(data); row = Recommendation(user_id=session["user_id"], crop=data.get("crop", ""), growth_stage=data.get("growth_stage", ""), **result); db.session.add(row); db.session.commit(); return jsonify(result), 201
        except (ValueError, TypeError, KeyError): return jsonify(error="Complete all fertilizer fields with numeric nutrient values."), 400
    @app.get("/uploads/<path:filename>")
    def uploaded_file(filename): return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
    @app.errorhandler(413)
    def too_large(_): return jsonify(error="Image is too large. Maximum size is 8 MB."), 413
    return app

app = create_app()

if __name__ == "__main__": app.run(debug=True)
