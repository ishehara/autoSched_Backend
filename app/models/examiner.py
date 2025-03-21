from app.database import db
from bson import ObjectId
import datetime

class Examiner:
    @staticmethod
    def create(examiner_data):
        result = db.examiners.insert_one(examiner_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all():
        examiners = list(db.examiners.find())
        for examiner in examiners:
            examiner['_id'] = str(examiner['_id'])
        return examiners
    
    @staticmethod
    def get_by_id(examiner_id):
        examiner = db.examiners.find_one({"_id": ObjectId(examiner_id)})
        if examiner:
            examiner['_id'] = str(examiner['_id'])
        return examiner
    
    @staticmethod
    def update(examiner_id, examiner_data):
        db.examiners.update_one(
            {"_id": ObjectId(examiner_id)},
            {"$set": examiner_data}
        )
        return Examiner.get_by_id(examiner_id)
    
    @staticmethod
    def delete(examiner_id):
        result = db.examiners.delete_one({"_id": ObjectId(examiner_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def get_available_examiners(date, start_time, end_time):
        # Find examiners who don't have conflicting schedules
        examiners = list(db.examiners.find({
            "availability": {
                "$elemMatch": {
                    "date": {"$eq": date.strftime("%Y-%m-%d")},
                    "start_time": {"$lte": start_time.strftime("%H:%M")},
                    "end_time": {"$gte": end_time.strftime("%H:%M")}
                }
            }
        }))
        
        # Find scheduled presentations for that time slot
        scheduled_presentations = list(db.presentations.find({
            "date": date.strftime("%Y-%m-%d"),
            "$or": [
                {
                    "start_time": {"$lt": end_time.strftime("%H:%M")},
                    "end_time": {"$gt": start_time.strftime("%H:%M")}
                }
            ]
        }))
        
        # Extract examiner IDs from scheduled presentations
        scheduled_examiner_ids = []
        for presentation in scheduled_presentations:
            # Check if examiner_ids field exists in the presentation
            if "examiner_ids" in presentation:
                # Add each examiner ID to the list
                for examiner_id in presentation["examiner_ids"]:
                    scheduled_examiner_ids.append(str(examiner_id))
        
        # Filter out examiners who are already scheduled
        available_examiners = [
            examiner for examiner in examiners 
            if str(examiner["_id"]) not in scheduled_examiner_ids
        ]
        
        for examiner in available_examiners:
            examiner["_id"] = str(examiner["_id"])
            
        return available_examiners
    
    @staticmethod
    def get_by_expertise(expertise_area):
        examiners = list(db.examiners.find({
            "areas_of_expertise": expertise_area
        }))
        
        for examiner in examiners:
            examiner["_id"] = str(examiner["_id"])
            
        return examiners