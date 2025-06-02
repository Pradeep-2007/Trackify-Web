"""
Script to sync all existing Django tasks to MongoDB
"""
import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

from planner.models import Task as DjangoTask
from tasks.models import Task as MongoTask

def sync_all_tasks():
    """Sync all Django tasks to MongoDB"""
    print("Starting task synchronization...")
    
    # Get all Django tasks
    django_tasks = DjangoTask.objects.all()
    print(f"Found {django_tasks.count()} Django tasks")
    
    # Track counts
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for django_task in django_tasks:
        try:
            # Check if MongoDB task already exists
            mongo_task = MongoTask.objects(django_id=django_task.id).first()
            
            if mongo_task:
                # Update existing MongoDB task
                mongo_task.title = django_task.title
                mongo_task.description = django_task.description
                mongo_task.priority = django_task.priority
                mongo_task.category = django_task.category
                mongo_task.due_date = django_task.due_date
                mongo_task.completed = django_task.completed
                mongo_task.estimated_duration = django_task.estimated_duration
                mongo_task.updated_at = datetime.datetime.now()
                mongo_task.save()
                updated_count += 1
            else:
                # Create new MongoDB task
                mongo_task = MongoTask(
                    user_id=django_task.user.id,
                    username=django_task.user.username,
                    title=django_task.title,
                    description=django_task.description,
                    priority=django_task.priority,
                    category=django_task.category,
                    due_date=django_task.due_date,
                    completed=django_task.completed,
                    estimated_duration=django_task.estimated_duration,
                    django_id=django_task.id,
                    created_at=django_task.created_at,
                    updated_at=django_task.updated_at
                )
                mongo_task.save()
                created_count += 1
                
            print(f"Processed task: {django_task.title}")
        except Exception as e:
            print(f"Error syncing task {django_task.id}: {e}")
            error_count += 1
    
    print("\nSynchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

if __name__ == "__main__":
    sync_all_tasks()
