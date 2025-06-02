"""
Script to sync all existing Django data to MongoDB
"""
import os
import django
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

from django.contrib.auth import get_user_model
from planner.models import Task as DjangoTask, UserSettings as DjangoUserSettings
from planner.models import TimerSession as DjangoTimerSession, StudySession as DjangoStudySession
from tasks.models import Task as MongoTask
from tasks.auth_models import MongoUser, MongoUserSettings, MongoTimerSession, MongoStudySession

User = get_user_model()

def sync_all_users():
    """Sync all Django users to MongoDB"""
    print("Syncing users...")
    
    # Get all Django users
    django_users = User.objects.all()
    print(f"Found {django_users.count()} Django users")
    
    # Track counts
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for django_user in django_users:
        try:
            # Check if MongoDB user already exists
            mongo_user = MongoUser.objects(django_id=django_user.id).first()
            
            if mongo_user:
                # Update existing MongoDB user
                mongo_user.username = django_user.username
                mongo_user.email = django_user.email
                mongo_user.first_name = django_user.first_name
                mongo_user.last_name = django_user.last_name
                mongo_user.is_active = django_user.is_active
                mongo_user.last_login = django_user.last_login
                mongo_user.save()
                updated_count += 1
            else:
                # Create new MongoDB user
                mongo_user = MongoUser(
                    django_id=django_user.id,
                    username=django_user.username,
                    email=django_user.email,
                    first_name=django_user.first_name,
                    last_name=django_user.last_name,
                    is_active=django_user.is_active,
                    date_joined=django_user.date_joined,
                    last_login=django_user.last_login
                )
                mongo_user.save()
                created_count += 1
                
            print(f"Processed user: {django_user.username}")
        except Exception as e:
            print(f"Error syncing user {django_user.id}: {e}")
            error_count += 1
    
    print("\nUser synchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

def sync_all_user_settings():
    """Sync all Django user settings to MongoDB"""
    print("\nSyncing user settings...")
    
    # Get all Django user settings
    django_settings = DjangoUserSettings.objects.all()
    print(f"Found {django_settings.count()} Django user settings")
    
    # Track counts
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for django_setting in django_settings:
        try:
            # Check if MongoDB user settings already exist
            mongo_settings = MongoUserSettings.objects(user_id=django_setting.user.id).first()
            
            if mongo_settings:
                # Update existing MongoDB user settings
                mongo_settings.username = django_setting.user.username
                mongo_settings.work_duration = django_setting.work_duration
                mongo_settings.short_break_duration = django_setting.short_break_duration
                mongo_settings.long_break_duration = django_setting.long_break_duration
                mongo_settings.long_break_interval = django_setting.long_break_interval
                mongo_settings.most_productive_time = django_setting.most_productive_time
                mongo_settings.daily_goal = django_setting.daily_goal
                mongo_settings.weekly_goal = django_setting.weekly_goal
                mongo_settings.enable_dark_mode = django_setting.enable_dark_mode
                mongo_settings.enable_sounds = django_setting.enable_sounds
                mongo_settings.updated_at = datetime.datetime.now()
                mongo_settings.save()
                updated_count += 1
            else:
                # Create new MongoDB user settings
                mongo_settings = MongoUserSettings(
                    user_id=django_setting.user.id,
                    username=django_setting.user.username,
                    work_duration=django_setting.work_duration,
                    short_break_duration=django_setting.short_break_duration,
                    long_break_duration=django_setting.long_break_duration,
                    long_break_interval=django_setting.long_break_interval,
                    most_productive_time=django_setting.most_productive_time,
                    daily_goal=django_setting.daily_goal,
                    weekly_goal=django_setting.weekly_goal,
                    enable_dark_mode=django_setting.enable_dark_mode,
                    enable_sounds=django_setting.enable_sounds
                )
                mongo_settings.save()
                created_count += 1
                
            print(f"Processed settings for user: {django_setting.user.username}")
        except Exception as e:
            print(f"Error syncing settings for user {django_setting.user.id}: {e}")
            error_count += 1
    
    print("\nUser settings synchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

def sync_all_tasks():
    """Sync all Django tasks to MongoDB"""
    print("\nSyncing tasks...")
    
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
    
    print("\nTask synchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

def sync_all_timer_sessions():
    """Sync all Django timer sessions to MongoDB"""
    print("\nSyncing timer sessions...")
    
    # Get all Django timer sessions
    django_sessions = DjangoTimerSession.objects.all()
    print(f"Found {django_sessions.count()} Django timer sessions")
    
    # Track counts
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for django_session in django_sessions:
        try:
            # Check if MongoDB timer session already exists
            mongo_session = MongoTimerSession.objects(
                user_id=django_session.user.id,
                start_time=django_session.start_time
            ).first()
            
            task_id = django_session.task.id if django_session.task else None
            task_title = django_session.task.title if django_session.task else None
            
            if mongo_session:
                # Update existing MongoDB timer session
                mongo_session.username = django_session.user.username
                mongo_session.session_type = django_session.session_type.lower()
                mongo_session.duration = django_session.duration
                mongo_session.task_id = task_id
                mongo_session.task_title = task_title
                mongo_session.end_time = django_session.end_time
                mongo_session.save()
                updated_count += 1
            else:
                # Create new MongoDB timer session
                mongo_session = MongoTimerSession(
                    user_id=django_session.user.id,
                    username=django_session.user.username,
                    session_type=django_session.session_type.lower(),
                    duration=django_session.duration,
                    task_id=task_id,
                    task_title=task_title,
                    start_time=django_session.start_time,
                    end_time=django_session.end_time
                )
                mongo_session.save()
                created_count += 1
                
            print(f"Processed timer session: {django_session.id}")
        except Exception as e:
            print(f"Error syncing timer session {django_session.id}: {e}")
            error_count += 1
    
    print("\nTimer session synchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

def sync_all_study_sessions():
    """Sync all Django study sessions to MongoDB"""
    print("\nSyncing study sessions...")
    
    # Get all Django study sessions
    django_sessions = DjangoStudySession.objects.all()
    print(f"Found {django_sessions.count()} Django study sessions")
    
    # Track counts
    created_count = 0
    updated_count = 0
    error_count = 0
    
    for django_session in django_sessions:
        try:
            # Check if MongoDB study session already exists
            mongo_session = MongoStudySession.objects(
                user_id=django_session.user.id,
                start_time=django_session.start_time
            ).first()
            
            task_id = django_session.task.id if django_session.task else None
            task_title = django_session.task.title if django_session.task else None
            
            if mongo_session:
                # Update existing MongoDB study session
                mongo_session.username = django_session.user.username
                mongo_session.duration = django_session.duration
                mongo_session.productivity_score = django_session.productivity_score
                mongo_session.distractions = django_session.distractions
                mongo_session.task_id = task_id
                mongo_session.task_title = task_title
                mongo_session.end_time = django_session.end_time
                mongo_session.save()
                updated_count += 1
            else:
                # Create new MongoDB study session
                mongo_session = MongoStudySession(
                    user_id=django_session.user.id,
                    username=django_session.user.username,
                    duration=django_session.duration,
                    productivity_score=django_session.productivity_score,
                    distractions=django_session.distractions,
                    task_id=task_id,
                    task_title=task_title,
                    start_time=django_session.start_time,
                    end_time=django_session.end_time
                )
                mongo_session.save()
                created_count += 1
                
            print(f"Processed study session: {django_session.id}")
        except Exception as e:
            print(f"Error syncing study session {django_session.id}: {e}")
            error_count += 1
    
    print("\nStudy session synchronization complete!")
    print(f"Created: {created_count}")
    print(f"Updated: {updated_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {created_count + updated_count}")

if __name__ == "__main__":
    print("Starting data synchronization to MongoDB...")
    sync_all_users()
    sync_all_user_settings()
    sync_all_tasks()
    sync_all_timer_sessions()
    sync_all_study_sessions()
    print("\nAll data synchronized to MongoDB!")
