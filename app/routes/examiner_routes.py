from flask import Blueprint, request, jsonify
from app.models.examiner import Examiner
from app.database import db
from bson import ObjectId
import datetime

examiner_bp = Blueprint('examiner_bp', __name__)

@examiner_bp.route('/', methods=['POST'])
def create_examiner():
    try:
        examiner_data = request.json
        
        # Convert dates and times to proper format
        if 'availability' in examiner_data:
            for slot in examiner_data['availability']:
                if 'date' in slot:
                    # Ensure date is in YYYY-MM-DD format
                    slot['date'] = slot['date']
        
        examiner_id = Examiner.create(examiner_data)
        return jsonify({"message": "Examiner created successfully", "examiner_id": examiner_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rest of the routes remain the same...

@examiner_bp.route('/', methods=['GET'])
def get_all_examiners():
    examiners = Examiner.get_all()
    return jsonify(examiners), 200

@examiner_bp.route('/<examiner_id>', methods=['GET'])
def get_examiner(examiner_id):
    examiner = Examiner.get_by_id(examiner_id)
    if not examiner:
        return jsonify({"message": "Examiner not found"}), 404
    return jsonify(examiner), 200

@examiner_bp.route('/<examiner_id>', methods=['PUT'])
def update_examiner(examiner_id):
    examiner_data = request.json
    examiner = Examiner.get_by_id(examiner_id)
    
    if not examiner:
        return jsonify({"message": "Examiner not found"}), 404
    
    updated_examiner = Examiner.update(examiner_id, examiner_data)
    return jsonify({"message": "Examiner updated successfully", "examiner": updated_examiner}), 200

@examiner_bp.route('/<examiner_id>', methods=['DELETE'])
def delete_examiner(examiner_id):
    examiner = Examiner.get_by_id(examiner_id)
    
    if not examiner:
        return jsonify({"message": "Examiner not found"}), 404
    
    success = Examiner.delete(examiner_id)
    if success:
        return jsonify({"message": "Examiner deleted successfully"}), 200
    return jsonify({"message": "Failed to delete examiner"}), 500

@examiner_bp.route('/available', methods=['GET'])
def get_available_examiners():
    date_str = request.args.get('date')
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    
    if not all([date_str, start_time_str, end_time_str]):
        return jsonify({"message": "Missing required parameters"}), 400
    
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError:
        return jsonify({"message": "Invalid date or time format"}), 400
    
    examiners = Examiner.get_available_examiners(date, start_time, end_time)
    return jsonify(examiners), 200

@examiner_bp.route('/expertise/<expertise_area>', methods=['GET'])
def get_by_expertise(expertise_area):
    examiners = Examiner.get_by_expertise(expertise_area)
    return jsonify(examiners), 200