"""
Test script to verify MongoDB model connection
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

from tasks.models import Task
import datetime

def test_mongodb_model():
    try:
        # Create a new task
        task = Task(
            title="Test Task",
            description="This is a test task created to verify MongoDB connection",
            due_date=datetime.datetime.now() + datetime.timedelta(days=7),
            tags=["test", "mongodb", "connection"]
        )
        task.save()
        print(f"Task created with ID: {task.id}")
        
        # Retrieve the task
        retrieved_task = Task.objects(id=task.id).first()
        print(f"Retrieved task: {retrieved_task.title}")
        print(f"Description: {retrieved_task.description}")
        print(f"Created at: {retrieved_task.created_at}")
        print(f"Due date: {retrieved_task.due_date}")
        print(f"Tags: {retrieved_task.tags}")
        
        # List all tasks
        all_tasks = Task.objects()
        print(f"Total tasks in database: {len(all_tasks)}")
        
        # Clean up - delete the test task
        task.delete()
        print("Test task deleted")
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

if __name__ == "__main__":
    test_mongodb_model()
