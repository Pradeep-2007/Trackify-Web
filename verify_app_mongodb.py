"""
Script to verify that the application is properly connecting to MongoDB
"""
import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

# Import models
from tasks.models import Task
from tasks.auth_models import MongoUser, MongoUserSettings

def verify_app_mongodb_connection():
    print("Verifying MongoDB connection from the application...")
    
    try:
        # Check if we can query users
        users_count = MongoUser.objects.count()
        print(f"Found {users_count} users in MongoDB")
        
        # Check if we can query user settings
        settings_count = MongoUserSettings.objects.count()
        print(f"Found {settings_count} user settings in MongoDB")
        
        # Check if we can query tasks
        tasks_count = Task.objects.count()
        print(f"Found {tasks_count} tasks in MongoDB")
        
        # Try to create a test task
        test_task = Task(
            user_id=1,  # Assuming user with ID 1 exists
            username="Test",
            title="Test Task from Verification Script",
            description="This is a test task to verify MongoDB connection",
            priority="M",
            category="STUDY",
            due_date=datetime.datetime.now() + datetime.timedelta(days=1)
        )
        test_task.save()
        print(f"Created test task with ID: {test_task.id}")
        
        # Retrieve the task
        retrieved_task = Task.objects(id=test_task.id).first()
        print(f"Retrieved task: {retrieved_task.title}")
        
        # Delete the test task
        test_task.delete()
        print("Test task deleted")
        
        print("MongoDB connection verification completed successfully!")
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    verify_app_mongodb_connection()
