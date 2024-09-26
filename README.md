# Dynamic Survey Builder

## Description

The Dynamic Survey Builder is a robust backend system built with Django and Django REST Framework. It allows for the creation and management of complex, multi-step surveys with conditional logic and field dependencies. This system is designed to meet enterprise-level demands for flexibility and scalability in survey creation and data handling.

## Features

- Multi-step survey creation with sections and various field types
- Conditional logic for dynamic survey flows
- Field dependencies across different sections
- Real-time validation of survey submissions
- Partial response saving and resuming
- Optimized for high-volume survey submissions

## Technologies Used

- Python 3.8+
- Django 3.2+
- Django REST Framework 3.12+
- PostgreSQL (recommended for production use)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/a-samir97/dynamic-survey.git
   cd dynamic-survey
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

## Usage

### API Endpoints

- `POST /api/surveys/`: Create a new survey
- `GET /api/surveys/<id>/`: Retrieve a specific survey
- `POST /api/survey-responses/`: Submit a survey response
- `GET /api/survey-responses/<id>/`: Retrieve a specific survey response
- `PUT /api/survey-responses/<id>/`: Update a survey response (e.g., complete a partial response)

### Creating a Survey

To create a survey, send a POST request to `/api/surveys/` with the following structure:

```json
{
  "title": "Your Survey Title",
  "description": "Your survey description",
  "sections": [
    {
      "title": "Section Title",
      "order": 1,
      "fields": [
        {
          "label": "Field Label",
          "field_type": "text",
          "required": true,
          "order": 1,
          "options": null,
          "conditional_logic": null,
          "dependencies": null
        }
      ]
    }
  ]
}
```

### Submitting a Survey Response

To submit a survey response, send a POST request to `/api/survey-responses/` with the following structure:

```json
{
  "survey_id": 1,
  "answers": [
    {
      "field": 1,
      "value": "Answer text"
    }
  ]
}
```

## Testing

To run the test suite:

```
python manage.py test
```
