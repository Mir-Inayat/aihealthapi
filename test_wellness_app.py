import unittest
import requests
import os
from PIL import Image
import io
import json
import tempfile
import numpy as np

class TestWellnessApp(unittest.TestCase):
    BASE_URL = "http://localhost:5000"
    
    @classmethod
    def setUpClass(cls):
        """Create test files and data that will be used across multiple tests"""
        # Create a test image
        cls.create_test_image()
        
        # Create a test mood history file
        cls.create_mood_history()
        
        # Create a test fitness history file
        cls.create_fitness_history()
        
        # Create a test health document
        cls.create_health_document()
        
        # Create a test progress tracking file
        cls.create_progress_data()

    @classmethod
    def create_test_image(cls):
        """Create a simple test image of a plate with food"""
        img = Image.new('RGB', (100, 100), color='white')
        cls.test_image_path = 'test_food.jpg'
        img.save(cls.test_image_path)

    @classmethod
    def create_mood_history(cls):
        """Create a test mood history file"""
        mood_data = "Date,Mood,Notes\n2024-01-01,Happy,Great day\n2024-01-02,Tired,Busy workday"
        cls.mood_history_path = 'mood_history.csv'
        with open(cls.mood_history_path, 'w') as f:
            f.write(mood_data)

    @classmethod
    def create_fitness_history(cls):
        """Create a test fitness history file"""
        fitness_data = "Date,Exercise,Duration,Intensity\n2024-01-01,Running,30,High\n2024-01-02,Yoga,45,Medium"
        cls.fitness_history_path = 'fitness_history.csv'
        with open(cls.fitness_history_path, 'w') as f:
            f.write(fitness_data)

    @classmethod
    def create_health_document(cls):
        """Create a test health document"""
        health_data = "Recent health checkup results and vital signs..."
        cls.health_doc_path = 'health_doc.txt'
        with open(cls.health_doc_path, 'w') as f:
            f.write(health_data)

    @classmethod
    def create_progress_data(cls):
        """Create a test progress tracking file"""
        progress_data = "Week,Weight,Steps,Sleep_Hours\n1,70,8000,7\n2,69.5,8500,7.5"
        cls.progress_data_path = 'progress_data.csv'
        with open(cls.progress_data_path, 'w') as f:
            f.write(progress_data)

    def test_1_food_analysis(self):
        """Test the food analysis endpoint"""
        url = f"{self.BASE_URL}/analyze-food"
        
        with open(self.test_image_path, 'rb') as img:
            files = {'image': ('test_food.jpg', img, 'image/jpeg')}
            response = requests.post(url, files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('analysis', data)

    def test_2_wellness_chat(self):
        """Test the wellness chat endpoint"""
        url = f"{self.BASE_URL}/chat"
        
        # Test without context files
        payload = {"message": "I'm feeling stressed about work"}
        response = requests.post(url, json=payload)
        self.assertEqual(response.status_code, 200)
        
        # Test with context files
        with open(self.mood_history_path, 'rb') as f:
            files = {'context_files': ('mood_history.csv', f)}
            response = requests.post(url, 
                                  data= {"message": "I'm feeling stressed"},
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('response', data)

    def test_3_daily_tips(self):
        """Test the daily tips endpoint"""
        url = f"{self.BASE_URL}/daily-tips"
        
        payload = {
            "time_of_day": "morning",
            "energy_level": "high",
            "environment": "home office"
        }
        
        with open(self.progress_data_path, 'rb') as f:
            files = {'context_files': ('progress_data.csv', f)}
            response = requests.post(url, 
                                  data=payload,
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('tips', data)

    def test_4_mood_tracking(self):
        """Test the mood tracking endpoint"""
        url = f"{self.BASE_URL}/mood"
        
        payload = {
            "mood": "anxious",
            "time": "morning",
            "triggers": ["work deadline", "lack of sleep"],
            "duration": "2 hours"
        }
        
        with open(self.mood_history_path, 'rb') as f:
            files = {'mood_history': ('mood_history.csv', f)}
            response = requests.post(url,
                                  data=payload,
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('analysis', data)

    def test_5_exercise_recommendations(self):
        """Test the exercise recommendations endpoint"""
        url = f"{self.BASE_URL}/exercise-recommendations"
        
        payload = {
            "fitness_level": "intermediate",
            "preferences": ["running", "yoga"],
            "limitations": ["knee pain"],
            "equipment": ["dumbbells", "yoga mat"]
        }
        
        with open(self.fitness_history_path, 'rb') as f:
            files = {'fitness_history': ('fitness_history.csv', f)}
            response = requests.post(url,
                                  data=payload,
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('recommendations', data)

    def test_6_health_assessment(self):
        """Test the health assessment endpoint"""
        url = f"{self.BASE_URL}/health-assessment"
        
        payload = {
            "age": 30,
            "weight": 70,
            "height": 175,
            "activity_level": "moderate",
            "sleep_hours": 7,
            "stress_level": "medium",
            "additional_info": {
                "chronic_conditions": None,
                "medications": None
            }
        }
        
        with open(self.health_doc_path, 'rb') as f:
            files = {'health_documents': ('health_doc.txt', f)}
            response = requests.post(url,
                                  data=payload,
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('assessment', data)

    def test_7_goal_tracking(self):
        """Test the goal tracking endpoint"""
        url = f"{self.BASE_URL}/goal-tracking"
        
        payload = {
            "goal": "Lose 5kg in 3 months",
            "progress": "Lost 2kg in 1 month",
            "timeline": "3 months",
            "challenges": ["late night snacking", "irregular exercise"]
        }
        
        with open(self.progress_data_path, 'rb') as f:
            files = {'progress_data': ('progress_data.csv', f)}
            response = requests.post(url,
                                  data=payload,
                                  files=files)
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('feedback', data)

    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        test_files = [
            cls.test_image_path,
            cls.mood_history_path,
            cls.fitness_history_path,
            cls.health_doc_path,
            cls.progress_data_path
        ]
        
        for file_path in test_files:
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

if __name__ == '__main__':
    print("Starting Wellness App Tests...")
    print("Make sure the Flask application is running on http://localhost:5000")
    unittest.main(verbosity=2)