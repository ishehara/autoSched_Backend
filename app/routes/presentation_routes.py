from flask import Blueprint, request, jsonify
from app.models.presentation import Presentation
from app.models.examiner import Examiner
from app.models.venue import Venue
from app.services.scheduler_service import SchedulerService
from app.services.email_service import EmailService
from bson import ObjectId
import datetime

presentation_bp = Blueprint('presentation_bp', __name__)

@presentation_bp.route('/', methods=['POST'])
def create_presentation():
    presentation_data = request.json
    
    # Validate required fields
    required_fields = ['group_id', 'module', 'num_attendees', 'required_examiners', 'technology_category']
    missing_fields = [field for field in required_fields if field not in presentation_data]
    
    if missing_fields:
        return jsonify({"message": f"Missing required fields: {', '.join(missing_fields)}"}), 400
    
    # Create the presentation without scheduling
    presentation_id = Presentation.create(presentation_data)
    
    return jsonify({
        "message": "Presentation created successfully", 
        "presentation_id": presentation_id
    }), 201

@presentation_bp.route('/', methods=['GET'])
def get_all_presentations():
    presentations = Presentation.get_all()
    return jsonify(presentations), 200

@presentation_bp.route('/<presentation_id>', methods=['GET'])
def get_presentation(presentation_id):
    presentation = Presentation.get_by_id(presentation_id)
    if not presentation:
        return jsonify({"message": "Presentation not found"}), 404
    return jsonify(presentation), 200

@presentation_bp.route('/<presentation_id>', methods=['PUT'])
def update_presentation(presentation_id):
    presentation_data = request.json
    presentation = Presentation.get_by_id(presentation_id)
    
    if not presentation:
        return jsonify({"message": "Presentation not found"}), 404
    
    updated_presentation = Presentation.update(presentation_id, presentation_data)
    return jsonify({
        "message": "Presentation updated successfully", 
        "presentation": updated_presentation
    }), 200

@presentation_bp.route('/<presentation_id>', methods=['DELETE'])
def delete_presentation(presentation_id):
    presentation = Presentation.get_by_id(presentation_id)
    
    if not presentation:
        return jsonify({"message": "Presentation not found"}), 404
    
    success = Presentation.delete(presentation_id)
    if success:
        return jsonify({"message": "Presentation deleted successfully"}), 200
    return jsonify({"message": "Failed to delete presentation"}), 500

@presentation_bp.route('/schedule', methods=['POST'])
def schedule_presentations():
    data = request.json
    date_range = data.get('date_range', [])
    
    if not date_range or len(date_range) != 2:
        return jsonify({"message": "Invalid date range"}), 400
    
    try:
        start_date = datetime.datetime.strptime(date_range[0], "%Y-%m-%d").date()
        end_date = datetime.datetime.strptime(date_range[1], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400
    
    # Get unscheduled presentations
    unscheduled_presentations = list(Presentation.get_all())
    unscheduled_presentations = [p for p in unscheduled_presentations if 'scheduled' not in p or not p['scheduled']]
    
    if not unscheduled_presentations:
        return jsonify({"message": "No presentations to schedule"}), 200
    
    scheduler = SchedulerService()
    scheduled_presentations = scheduler.schedule_presentations(unscheduled_presentations, start_date, end_date)
    
    try:
        email_service = EmailService()
        email_service.send_schedule_notifications(scheduled_presentations)
    except Exception as e:
        print(f"Failed to send email notifications: {str(e)}")
    
    return jsonify({
        "message": f"Successfully scheduled {len(scheduled_presentations)} presentations",
        "scheduled_presentations": scheduled_presentations
    }), 200

@presentation_bp.route('/examiner/<examiner_id>', methods=['GET'])
def get_by_examiner(examiner_id):
    presentations = Presentation.get_by_examiner(examiner_id)
    return jsonify(presentations), 200

@presentation_bp.route('/venue/<venue_id>', methods=['GET'])
def get_by_venue(venue_id):
    presentations = Presentation.get_by_venue(venue_id)
    return jsonify(presentations), 200

@presentation_bp.route('/date/<date>', methods=['GET'])
def get_by_date(date):
    try:
        # Check if date is in YYYY-MM-DD format
        datetime.datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        return jsonify({"message": "Invalid date format"}), 400
    
    presentations = Presentation.get_by_date(date)
    return jsonify(presentations), 200