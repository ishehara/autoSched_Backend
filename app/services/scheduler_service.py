from app.models.presentation import Presentation
from app.models.examiner import Examiner
from app.models.venue import Venue
from app.services.ai_service import AIService
from app.config import Config
from datetime import datetime, timedelta, time
from bson import ObjectId

class SchedulerService:
    def __init__(self):
        self.ai_service = AIService()
        self.start_hour = Config.WORKING_START_HOUR
        self.end_hour = Config.WORKING_END_HOUR
        self.presentation_duration = Config.PRESENTATION_DURATION
    
    def schedule_presentations(self, presentations, start_date, end_date):
        """
        Schedule presentations within the given date range
        """
        # Sort presentations by priority (if any)
        # For now, we'll just use required_examiners as a priority metric
        presentations = sorted(presentations, key=lambda p: p.get('required_examiners', 1), reverse=True)
        
        scheduled_presentations = []
        current_date = start_date
        delta = timedelta(days=1)
        
        while current_date <= end_date and presentations:
            # Skip weekends
            if current_date.weekday() >= 5:  # 5=Saturday, 6=Sunday
                current_date += delta
                continue
            
            # Generate time slots for the day
            time_slots = self._generate_time_slots(current_date)
            
            # Try to schedule presentations for each time slot
            for start_time, end_time in time_slots:
                if not presentations:
                    break
                
                # Find available venues for this time slot
                available_venues = Venue.get_available_venues(
                    current_date, 
                    start_time, 
                    end_time
                )
                
                if not available_venues:
                    continue
                
                # For each available venue, try to schedule a presentation
                for venue in available_venues:
                    if not presentations:
                        break
                    
                    presentation = presentations[0]
                    
                    # Get required number of examiners
                    num_required_examiners = presentation.get('required_examiners', 1)
                    
                    # Find available examiners for this time slot
                    available_examiners = Examiner.get_available_examiners(
                        current_date,
                        start_time,
                        end_time
                    )
                    
                    if len(available_examiners) < num_required_examiners:
                        continue
                    
                    # Use AI to match examiners based on expertise
                    matched_examiners = self.ai_service.match_examiners(
                        presentation,
                        available_examiners,
                        num_required_examiners
                    )
                    
                    if len(matched_examiners) < num_required_examiners:
                        continue
                    
                    # Schedule the presentation
                    presentation_data = {
                        'venue_id': ObjectId(venue['_id']) if isinstance(venue['_id'], str) else venue['_id'],
                        'examiner_ids': [ObjectId(e['_id']) if isinstance(e['_id'], str) else e['_id'] for e in matched_examiners],
                        'date': current_date.strftime('%Y-%m-%d'),
                        'start_time': start_time.strftime('%H:%M'),
                        'end_time': end_time.strftime('%H:%M'),
                        'scheduled': True
                    }
                    
                    Presentation.update(presentation['_id'], presentation_data)
                    
                    # Add scheduled presentation to results and remove from queue
                    scheduled_presentation = {**presentation, **presentation_data}
                    
                    # Convert ObjectId to string before adding to the result
                    if 'venue_id' in scheduled_presentation:
                        if isinstance(scheduled_presentation['venue_id'], ObjectId):
                            scheduled_presentation['venue_id'] = str(scheduled_presentation['venue_id'])
                    
                    if 'examiner_ids' in scheduled_presentation:
                        scheduled_presentation['examiner_ids'] = [
                            str(eid) if isinstance(eid, ObjectId) else eid 
                            for eid in scheduled_presentation['examiner_ids']
                        ]
                    
                    if '_id' in scheduled_presentation and isinstance(scheduled_presentation['_id'], ObjectId):
                        scheduled_presentation['_id'] = str(scheduled_presentation['_id'])
                    
                    scheduled_presentations.append(scheduled_presentation)
                    presentations.pop(0)
            
            # Move to next day
            current_date += delta
        
        return scheduled_presentations
    
    def _generate_time_slots(self, date):
        """
        Generate time slots for a given date
        """
        time_slots = []
        slot_duration = timedelta(minutes=self.presentation_duration)
        
        current_time = time(self.start_hour, 0)  # 8:00 AM
        end_time = time(self.end_hour, 0)        # 5:00 PM
        
        while current_time < end_time:
            slot_start = current_time
            
            # Calculate slot end time
            hr, min = current_time.hour, current_time.minute + self.presentation_duration
            if min >= 60:
                hr += 1
                min -= 60
            slot_end = time(hr, min)
            
            if slot_end <= end_time:
                time_slots.append((slot_start, slot_end))
            
            # Move to next slot
            current_time = slot_end
        
        return time_slots