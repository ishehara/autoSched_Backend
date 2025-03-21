from app.database import db
from bson import ObjectId
from datetime import datetime

class Presentation:
    @staticmethod
    def create(presentation_data):
        result = db.presentations.insert_one(presentation_data)
        return str(result.inserted_id)
    
    @staticmethod
    def get_all():
        presentations = list(db.presentations.find())
        for presentation in presentations:
            presentation['_id'] = str(presentation['_id'])
            if 'venue_id' in presentation and presentation['venue_id']:
                presentation['venue_id'] = str(presentation['venue_id'])
            if 'examiner_ids' in presentation and presentation['examiner_ids']:
                presentation['examiner_ids'] = [str(eid) for eid in presentation['examiner_ids']]
        return presentations
    
    @staticmethod
    def get_by_id(presentation_id):
        presentation = db.presentations.find_one({"_id": ObjectId(presentation_id)})
        if presentation:
            presentation['_id'] = str(presentation['_id'])
            if 'venue_id' in presentation and presentation['venue_id']:
                presentation['venue_id'] = str(presentation['venue_id'])
            if 'examiner_ids' in presentation and presentation['examiner_ids']:
                presentation['examiner_ids'] = [str(eid) for eid in presentation['examiner_ids']]
        return presentation
    
    @staticmethod
    def update(presentation_id, presentation_data):
        db.presentations.update_one(
            {"_id": ObjectId(presentation_id)},
            {"$set": presentation_data}
        )
        return Presentation.get_by_id(presentation_id)
    
    @staticmethod
    def delete(presentation_id):
        result = db.presentations.delete_one({"_id": ObjectId(presentation_id)})
        return result.deleted_count > 0
    
    @staticmethod
    def get_by_examiner(examiner_id):
        presentations = list(db.presentations.find({
            "examiner_ids": ObjectId(examiner_id)
        }))
        
        for presentation in presentations:
            presentation['_id'] = str(presentation['_id'])
            if 'venue_id' in presentation and presentation['venue_id']:
                presentation['venue_id'] = str(presentation['venue_id'])
            if 'examiner_ids' in presentation and presentation['examiner_ids']:
                presentation['examiner_ids'] = [str(eid) for eid in presentation['examiner_ids']]
        
        return presentations
    
    @staticmethod
    def get_by_venue(venue_id):
        presentations = list(db.presentations.find({
            "venue_id": ObjectId(venue_id)
        }))
        
        for presentation in presentations:
            presentation['_id'] = str(presentation['_id'])
            if 'venue_id' in presentation and presentation['venue_id']:
                presentation['venue_id'] = str(presentation['venue_id'])
            if 'examiner_ids' in presentation and presentation['examiner_ids']:
                presentation['examiner_ids'] = [str(eid) for eid in presentation['examiner_ids']]
        
        return presentations
    
    @staticmethod
    def get_by_date(date):
        if isinstance(date, str):
            date_str = date
        else:
            date_str = date.strftime("%Y-%m-%d")
            
        presentations = list(db.presentations.find({
            "date": date_str
        }))
        
        for presentation in presentations:
            presentation['_id'] = str(presentation['_id'])
            if 'venue_id' in presentation and presentation['venue_id']:
                presentation['venue_id'] = str(presentation['venue_id'])
            if 'examiner_ids' in presentation and presentation['examiner_ids']:
                presentation['examiner_ids'] = [str(eid) for eid in presentation['examiner_ids']]
        
        return presentations