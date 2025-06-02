"""
Debug script to check timer settings
"""
import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'trackify.settings')
django.setup()

from django.contrib.auth import get_user_model
from planner.models import UserSettings

User = get_user_model()

def check_timer_settings():
    # Get all users
    users = User.objects.all()
    
    print(f"Found {users.count()} users")
    
    for user in users:
        print(f"\nUser: {user.username}")
        
        try:
            settings = UserSettings.objects.get(user=user)
            print(f"  Work duration: {settings.work_duration} minutes")
            print(f"  Short break duration: {settings.short_break_duration} minutes")
            print(f"  Long break duration: {settings.long_break_duration} minutes")
            print(f"  Long break interval: {settings.long_break_interval} sessions")
            print(f"  Sounds enabled: {settings.enable_sounds}")
        except UserSettings.DoesNotExist:
            print(f"  No settings found for user {user.username}")

if __name__ == "__main__":
    check_timer_settings()
