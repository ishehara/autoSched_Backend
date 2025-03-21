from app.database import db
from bson import ObjectId
import datetime

class Venue:
    @staticmethod
    def create(venue_data):
        result = db.venues.insert_one(venue_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all():
        venues = list(db.venues.find())
        for venue in venues:
            venue['_id'] = str(venue['_id'])
        return venues
    
    @staticmethod
    def get_by_id(venue_id):
        venue = db.venues.find_one({"_id": ObjectId(venue_id)})
        if venue:
            venue['_id'] = str(venue['_id'])
        return venue
    
    @staticmethod
    def update(venue_id, venue_data):
        db.venues.update_one(
            {"_id": ObjectId(venue_id)},
            {"$set": venue_data}
        )
        return Venue.get_by_id(venue_id)
    
    @staticmethod
    def delete(venue_id):
        result = db.venues.delete_one({"_id": ObjectId(venue_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def get_available_venues(date, start_time, end_time, required_facilities=None):
        """
        Find available venues for a specific date and time range
        """
        # Base query to find venues with specified facilities
        query = {}
        if required_facilities:
            query["available_facilities"] = {"$all": required_facilities}
        
        venues = list(db.venues.find(query))
        
        # Find scheduled presentations for that time slot
        scheduled_venues = list(db.presentations.find({
            "date": date.strftime("%Y-%m-%d"),
            "$or": [
                {
                    "start_time": {"$lt": end_time.strftime("%H:%M")},
                    "end_time": {"$gt": start_time.strftime("%H:%M")}
                }
            ]
        }, {"venue_id": 1}))
        
        scheduled_venue_ids = [str(p["venue_id"]) for p in scheduled_venues if "venue_id" in p]
        
        # Filter out venues that are already booked
        available_venues = [
            venue for venue in venues 
            if str(venue["_id"]) not in scheduled_venue_ids
        ]
        
        for venue in available_venues:
            venue["_id"] = str(venue["_id"])
            
        return available_venues