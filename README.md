Running the Backend

Create a virtual environment (optional but recommended):
python -m venv venv
venv\Scripts\activate

Install the requirements:
pip install -r requirements.txt

Create a .env file in the root directory

Run the application:
python run.py

The API will be available at http://localhost:5000/api


Postman Testing Instructions
Here are instructions for testing the backend using Postman:

Setup Environment:

Create a new environment in Postman
Add a variable base_url with value http://localhost:5000/api


Create Collection:

Create a new collection named "AutoSched API"


Setup Requests:
Examiners API:

Create Examiner:

Method: POST
URL: {{base_url}}/examiners/
Body (raw JSON):

json{
  "name": "Dr. John Smith",
  "email": "john.smith@example.com",
  "phone_number": "1234567890",
  "department": "Computer Science",
  "position": "Senior Lecturer",
  "areas_of_expertise": ["Machine Learning", "Artificial Intelligence", "Database Systems"],
  "availability": [
    {
      "date": "2025-04-01",
      "start_time": "08:00",
      "end_time": "17:00"
    },
    {
      "date": "2025-04-02",
      "start_time": "08:00",
      "end_time": "17:00"
    }
  ]
}

Get All Examiners:

Method: GET
URL: {{base_url}}/examiners/


Get Examiner by ID:

Method: GET
URL: {{base_url}}/examiners/{examiner_id}


Update Examiner:

Method: PUT
URL: {{base_url}}/examiners/{examiner_id}
Body (raw JSON):

json{
  "name": "Dr. John Smith",
  "email": "john.smith.updated@example.com"
}

Delete Examiner:

Method: DELETE
URL: {{base_url}}/examiners/{examiner_id}


Get Available Examiners:

Method: GET
URL: {{base_url}}/examiners/available?date=2025-04-01&start_time=10:00&end_time=10:15



Venues API:

Create Venue:

Method: POST
URL: {{base_url}}/venues/
Body (raw JSON):

json{
  "venue_name": "Room A1",
  "organizer_email": "admin@example.com",
  "location": "Main Building, Floor 1",
  "capacity": 30,
  "available_facilities": ["Projector", "Whiteboard", "AC", "Sound System"]
}

Get All Venues:

Method: GET
URL: {{base_url}}/venues/


Get Venue by ID:

Method: GET
URL: {{base_url}}/venues/{venue_id}


Update Venue:

Method: PUT
URL: {{base_url}}/venues/{venue_id}
Body (raw JSON):

json{
  "capacity": 35,
  "available_facilities": ["Projector", "Whiteboard", "AC", "Sound System", "Mic"]
}

Delete Venue:

Method: DELETE
URL: {{base_url}}/venues/{venue_id}


Get Available Venues:

Method: GET
URL: {{base_url}}/venues/available?date=2025-04-01&start_time=10:00&end_time=10:15&facilities=Projector&facilities=Whiteboard



Presentations API:

Create Presentation:

Method: POST
URL: {{base_url}}/presentations/
Body (raw JSON):

json{
  "group_id": "Y3S2-WE-23",
  "module": "IT3040",
  "num_attendees": 5,
  "required_examiners": 2,
  "technology_category": "Artificial Intelligence"
}

Get All Presentations:

Method: GET
URL: {{base_url}}/presentations/


Get Presentation by ID:

Method: GET
URL: {{base_url}}/presentations/{presentation_id}


Update Presentation:

Method: PUT
URL: {{base_url}}/presentations/{presentation_id}
Body (raw JSON):

json{
  "num_attendees": 6,
  "technology_category": "Machine Learning"
}

Delete Presentation:

Method: DELETE
URL: {{base_url}}/presentations/{presentation_id}


Schedule Presentations:

Method: POST
URL: {{base_url}}/presentations/schedule
Body (raw JSON):

json{
  "date_range": ["2025-04-01", "2025-04-05"]
}

Get Presentations by Date:

Method: GET
URL: {{base_url}}/presentations/date/2025-04-01