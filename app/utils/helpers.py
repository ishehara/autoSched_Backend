from datetime import datetime, timedelta
import json
from bson import ObjectId
import re

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return super(JSONEncoder, self).default(obj)

def parse_datetime(date_str, time_str=None):
    """
    Parse date and time strings into datetime object
    """
    if not date_str:
        return None
        
    try:
        if time_str:
            datetime_str = f"{date_str} {time_str}"
            return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
        else:
            return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return None

def is_valid_email(email):
    """
    Check if an email is valid
    """
    if not email:
        return False
        
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    """
    Check if a phone number is valid
    """
    if not phone:
        return False
        
    # Remove spaces, dashes, parentheses
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it's all digits and has a reasonable length
    return phone.isdigit() and 8 <= len(phone) <= 15

def get_time_slots(start_time, end_time, duration_minutes):
    """
    Generate time slots between start_time and end_time with given duration
    """
    slots = []
    current_time = start_time
    
    while current_time + timedelta(minutes=duration_minutes) <= end_time:
        end_slot = current_time + timedelta(minutes=duration_minutes)
        slots.append((current_time, end_slot))
        current_time = end_slot
    
    return slots