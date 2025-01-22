from flask import Flask, request, jsonify
import google.generativeai as genai
import os
import tempfile
import streamlit as st

app = Flask(__name__)

# Access secrets
gemini_api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=gemini_api_key)
st.write(f"Using API Key: {gemini_api_key[:4]}****")

# System instruction for the model
instruction = """
You are a helpful wellness assistant that provides health and wellness advice based on user input.
Your responsibilities include:
1. Food Image Analysis: Analyze nutritional content of food images
2. Wellness Chat: Provide supportive responses for mental and physical health
3. Daily Productivity Tips: Offer actionable wellness-focused productivity advice
4. Mood Tracking: Respond to emotional states with empathy and practical suggestions
5. Exercise Recommendations: Suggest safe and effective exercises
6. Health Assessment: Provide comprehensive health-related feedback
7. Goal Tracking: Support users in their wellness journey with encouragement

Always prioritize:
- Safety and well-being
- Evidence-based recommendations
- Inclusive and supportive language
- Privacy-conscious responses
- Clear warnings about consulting healthcare professionals when needed
"""

# Initialize chat model
model = genai.GenerativeModel("models/gemini-1.5-pro", system_instruction=instruction)
chat = model.start_chat(history=[])

def save_temp_file(file_data, extension='.tmp'):
    """Save uploaded file data to a temporary file"""
    temp_file = tempfile.NamedTemporaryFile(suffix=extension, delete=False)
    temp_file.write(file_data)
    temp_file.close()
    return temp_file.name

def process_request(prompt, files=None):
    try:
        content_parts = [prompt]
        temp_files = []

        if files:
            for file_data in files:
                # Save the file data to a temporary file
                temp_path = save_temp_file(file_data)
                # Upload the file using genai.upload_file
                uploaded_file = genai.upload_file(temp_path)
                content_parts.append(uploaded_file)
                temp_files.append(temp_path)

        # Send message to chat
        response = chat.send_message(content_parts).text

        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass

        return response
    except Exception as e:
        # Clean up temporary files in case of error
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        return str(e)

# 1. Food Image Analysis
@app.route('/analyze-food', methods=['POST'])
def analyze_food():
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image provided"}), 400
    
    try:
        image_data = request.files['image'].read()
        
        prompt = """
        Analyze this food image and provide:
        1. Estimated nutritional content (calories, protein, fats, carbs)
        2. Health score out of 100
        3. Nutritional recommendations
        4. Potential allergens or dietary considerations
        5. Meal timing suggestions
        Format as a detailed but concise analysis.
        """
        
        response = process_request(prompt, [image_data])
        return jsonify({"status": "success", "analysis": response})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# 2. Wellness Chat with Context
@app.route('/chat', methods=['POST'])
def handle_chat():
    # Handle both JSON and form data
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()

    if not data or 'message' not in data:
        return jsonify({"status": "error", "message": "No message provided"}), 400
    
    # Handle context files
    context_files_data = []
    if request.files:
        for file in request.files.getlist('context_files'):
            context_files_data.append(file.read())
    
    prompt = f"""
    Consider the user's message and any provided context files to give a comprehensive wellness response.
    
    User message: {data['message']}
    
    Provide:
    1. Empathetic acknowledgment
    2. Relevant wellness advice
    3. Actionable next steps
    4. Any relevant health considerations
    """
    
    response = process_request(prompt, context_files_data if context_files_data else None)
    return jsonify({"status": "success", "response": response})

# 3. Daily Productivity Tips
@app.route('/daily-tips', methods=['GET', 'POST'])
def daily_tips():
    data = {}
    if request.method == 'POST':
        if request.is_json:
            data = request.json
        else:
            data = request.form.to_dict()
    
    context_files_data = []
    if 'context_files' in request.files:
        for file in request.files.getlist('context_files'):
            context_files_data.append(file.read())
    
    prompt = f"""
    Generate personalized productivity tips considering:
    - Time of day: {data.get('time_of_day', 'not specified')}
    - Energy level: {data.get('energy_level', 'not specified')}
    - Work environment: {data.get('environment', 'not specified')}
    
    Provide:
    1. 3-5 actionable tips
    2. Estimated time investment for each
    3. Expected wellness benefits
    """
    
    response = process_request(prompt, context_files_data if context_files_data else None)
    return jsonify({"status": "success", "tips": response})

# 4. Mood Tracking
@app.route('/mood', methods=['POST'])
def track_mood():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
        
    if not data or 'mood' not in data:
        return jsonify({"status": "error", "message": "No mood provided"}), 400
    
    # Handle mood history files
    mood_history_data = []
    if 'mood_history' in request.files:
        for file in request.files.getlist('mood_history'):
            mood_history_data.append(file.read())
    
    prompt = f"""
    Analyze the current mood '{data['mood']}' and any provided mood history.
    
    Consider:
    - Time: {data.get('time', 'not specified')}
    - Triggers: {data.get('triggers', [])}
    - Duration: {data.get('duration', 'not specified')}
    
    Include:
    1. Validation of their feelings
    2. A practical suggestion for mood improvement
    3. A positive affirmation
    4. Coping strategies
    """
    
    response = process_request(prompt, mood_history_data if mood_history_data else None)
    return jsonify({"status": "success", "analysis": response})

# 5. Exercise Recommendations
@app.route('/exercise-recommendations', methods=['POST'])
def exercise_recommendations():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
        
    # Handle fitness history files
    fitness_files_data = []
    if 'fitness_history' in request.files:
        for file in request.files.getlist('fitness_history'):
            fitness_files_data.append(file.read())
    
    prompt = f"""
    Generate personalized exercise recommendations considering:
    - Fitness level: {data.get('fitness_level', 'beginner')}
    - Preferences: {data.get('preferences', [])}
    - Limitations: {data.get('limitations', [])}
    - Available equipment: {data.get('equipment', [])}
    
    Include:
    1. Exercise name
    2. Duration
    3. Expected benefits
    4. Safety considerations
    5. Progressive overload suggestions
    """
    
    response = process_request(prompt, fitness_files_data if fitness_files_data else None)
    return jsonify({"status": "success", "recommendations": response})

# 6. Health Assessment
@app.route('/health-assessment', methods=['POST'])
def health_assessment():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
        
    if not data:
        return jsonify({"status": "error", "message": "No assessment data provided"}), 400
    
    # Handle health documents
    health_docs_data = []
    if 'health_documents' in request.files:
        for file in request.files.getlist('health_documents'):
            health_docs_data.append(file.read())
    
    prompt = f"""
    Provide a health assessment based on the following information:
    - Age: {data.get('age')}
    - Weight: {data.get('weight')}
    - Height: {data.get('height')}
    - Activity Level: {data.get('activity_level')}
    - Sleep Hours: {data.get('sleep_hours')}
    - Stress Level: {data.get('stress_level')}
    
    Include:
    1. General health overview
    2. Areas of concern
    3. Improvement recommendations
    4. Follow-up suggestions
    """
    
    response = process_request(prompt, health_docs_data if health_docs_data else None)
    return jsonify({"status": "success", "assessment": response})

# 7. Goal Tracking
@app.route('/goal-tracking', methods=['POST'])
def goal_tracking():
    if request.is_json:
        data = request.json
    else:
        data = request.form.to_dict()
        
    if not data or 'goal' not in data or 'progress' not in data:
        return jsonify({"status": "error", "message": "Missing goal or progress data"}), 400
    
    # Handle progress tracking files
    progress_files_data = []
    if 'progress_data' in request.files:
        for file in request.files.getlist('progress_data'):
            progress_files_data.append(file.read())
    
    prompt = f"""
    Analyze goal progress and provide feedback:
    Goal: {data['goal']}
    Current Progress: {data['progress']}
    Timeline: {data.get('timeline', 'not specified')}
    Challenges: {data.get('challenges', [])}
    
    Include:
    1. Progress analysis
    2. Milestone achievements
    3. Adjustment recommendations
    4. Next steps
    5. Motivation strategies
    """
    
    response = process_request(prompt, progress_files_data if progress_files_data else None)
    return jsonify({"status": "success", "feedback": response})

if __name__ == '__main__':
    if not gemini_api_key:
        raise ValueError("Please set the GOOGLE_API_KEY environment variable")
    app.run(debug=True)
