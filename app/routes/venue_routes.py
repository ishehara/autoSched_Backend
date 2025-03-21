from flask import Blueprint, request, jsonify
from app.models.venue import Venue
from bson import ObjectId
import datetime

venue_bp = Blueprint('venue_bp', __name__)

@venue_bp.route('/', methods=['POST'])
def create_venue():
    venue_data = request.json
    venue_id = Venue.create(venue_data)
    return jsonify({"message": "Venue created successfully", "venue_id": venue_id}), 201

@venue_bp.route('/', methods=['GET'])
def get_all_venues():
    venues = Venue.get_all()
    return jsonify(venues), 200

@venue_bp.route('/<venue_id>', methods=['GET'])
def get_venue(venue_id):
    venue = Venue.get_by_id(venue_id)
    if not venue:
        return jsonify({"message": "Venue not found"}), 404
    return jsonify(venue), 200

@venue_bp.route('/<venue_id>', methods=['PUT'])
def update_venue(venue_id):
    venue_data = request.json
    venue = Venue.get_by_id(venue_id)
    
    if not venue:
        return jsonify({"message": "Venue not found"}), 404
    
    updated_venue = Venue.update(venue_id, venue_data)
    return jsonify({"message": "Venue updated successfully", "venue": updated_venue}), 200

@venue_bp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.get_by_id(venue_id)
    
    if not venue:
        return jsonify({"message": "Venue not found"}), 404
    
    success = Venue.delete(venue_id)
    if success:
        return jsonify({"message": "Venue deleted successfully"}), 200
    return jsonify({"message": "Failed to delete venue"}), 500

@venue_bp.route('/available', methods=['GET'])
def get_available_venues():
    date_str = request.args.get('date')
    start_time_str = request.args.get('start_time')
    end_time_str = request.args.get('end_time')
    facilities = request.args.getlist('facilities')
    
    if not all([date_str, start_time_str, end_time_str]):
        return jsonify({"message": "Missing required parameters"}), 400
    
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.datetime.strptime(start_time_str, "%H:%M").time()
        end_time = datetime.datetime.strptime(end_time_str, "%H:%M").time()
    except ValueError:
        return jsonify({"message": "Invalid date or time format"}), 400
    
    venues = Venue.get_available_venues(date, start_time, end_time, facilities)
    return jsonify(venues), 200