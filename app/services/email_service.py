from flask_mail import Message
from app import mail
from app.database import db
from bson import ObjectId

class EmailService:
    def send_schedule_notifications(self, scheduled_presentations):
        """
        Send email notifications to examiners about their scheduled presentations
        """
        # Group presentations by examiner
        examiner_presentations = {}
        
        for presentation in scheduled_presentations:
            examiner_ids = presentation.get('examiner_ids', [])
            for examiner_id in examiner_ids:
                if isinstance(examiner_id, ObjectId):
                    examiner_id = str(examiner_id)
                
                if examiner_id not in examiner_presentations:
                    examiner_presentations[examiner_id] = []
                
                examiner_presentations[examiner_id].append(presentation)
        
        # Send emails to each examiner
        for examiner_id, presentations in examiner_presentations.items():
            examiner = db.examiners.find_one({"_id": ObjectId(examiner_id)})
            if not examiner or 'email' not in examiner:
                # Skip if examiner not found or has no email
                continue
                
            self.send_examiner_schedule_email(examiner, presentations)
    
    def send_examiner_schedule_email(self, examiner, presentations):
        """
        Send schedule email to a specific examiner
        """
        email = examiner.get('email')
        if not email:
            return
            
        name = examiner.get('name', 'Examiner')
        
        # Create email content
        subject = "AutoSched: Your Presentation Schedule"
        
        # Sort presentations by date and time
        presentations = sorted(
            presentations, 
            key=lambda p: (p.get('date', ''), p.get('start_time', ''))
        )
        
        # Build email body
        body = f"Dear {name},\n\n"
        body += "We are pleased to inform you about your upcoming presentation schedule:\n\n"
        
        for i, presentation in enumerate(presentations):
            # Get venue details
            venue_id = presentation.get('venue_id')
            venue = db.venues.find_one({"_id": ObjectId(venue_id)}) if venue_id else None
            venue_name = venue.get('venue_name', 'TBD') if venue else 'TBD'
            
            # Format presentation details
            date = presentation.get('date', 'TBD')
            start_time = presentation.get('start_time', 'TBD')
            end_time = presentation.get('end_time', 'TBD')
            group_id = presentation.get('group_id', 'TBD')
            module = presentation.get('module', 'TBD')
            
            body += f"Presentation {i+1}:\n"
            body += f"  Date: {date}\n"
            body += f"  Time: {start_time} - {end_time}\n"
            body += f"  Group: {group_id}\n"
            body += f"  Module: {module}\n"
            body += f"  Venue: {venue_name}\n\n"
        
        body += "Please make sure to be present at the specified venues on time.\n\n"
        body += "Thank you,\nAutoSched Team"
        
        try:
            # Create and send the message
            msg = Message(
                subject=subject,
                recipients=[email],
                body=body
            )
            
            mail.send(msg)
        except Exception as e:
            print(f"Failed to send email to {email}: {str(e)}")