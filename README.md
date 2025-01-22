# README.md

# Flask Gemini App

This project is a Flask application that integrates with the Gemini API to provide various health and wellness features. The application allows users to analyze food images, engage in wellness chats, receive daily productivity tips, track their mood, get exercise recommendations, undergo health assessments, and set goals.

## Features

- **Food Image Analysis**: Users can upload food images to receive nutritional information and recommendations.
- **Wellness Chat**: Engage in a chat with the application to receive wellness advice.
- **Daily Productivity Tips**: Get tips to enhance daily productivity and well-being.
- **Mood Tracking**: Users can input their mood and receive feedback.
- **Exercise Recommendations**: Suggestions for physical activities based on user preferences.
- **Health Assessment**: Users can submit health-related data for assessment.
- **Goal Tracking**: Track personal goals and receive motivational messages.

## Project Structure

```
flask-gemini-app
├── src
│   ├── app.py                # Entry point of the Flask application
│   ├── config
│   │   └── settings.py       # Configuration settings, including API keys
│   ├── services
│   │   └── gemini_service.py  # Logic for interacting with the Gemini API
│   ├── utils
│   │   └── prompts.py        # Curated prompts for Gemini API requests
│   └── templates
│       └── base_prompts.py   # Base templates for prompts
├── .env                       # Environment variables, including API keys
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd flask-gemini-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables in the `.env` file, including your Gemini API key.

5. Run the application:
   ```
   python src/app.py
   ```

## Usage

Once the application is running, you can access the various features through the defined API endpoints. Use tools like Postman or curl to interact with the endpoints.

## License

This project is licensed under the MIT License.