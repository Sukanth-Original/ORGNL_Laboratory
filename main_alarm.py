import datetime
import time
import webbrowser
import csv
import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def git_push_changes():
    """Automatically add, commit, and push CSV changes to Git"""
    try:
        # Check if there are changes to commit
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode().strip()
        if not status:
            logging.info("No changes to commit")
            return

        # Perform Git operations
        subprocess.check_call(['git', 'add', 'alarm_logs.csv'])
        commit_message = f"Alarm log update {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        subprocess.check_call(['git', 'commit', '-m', commit_message])
        push_result = subprocess.check_output(['git', 'push', 'origin', 'main'], stderr=subprocess.STDOUT)
        logging.info("Successfully pushed changes to Git repository")
        return True
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Git operation failed: {e.output.decode().strip()}")
        return False
    except Exception as e:
        logging.error(f"Error in Git automation: {str(e)}")
        return False

def log_alarm(scheduled_time, trigger_time, playlist_url):
    """Log alarm data to CSV file and trigger Git push"""
    filename = "alarm_logs.csv"
    file_exists = os.path.isfile(filename)
    
    try:
        with open(filename, 'a', newline='') as csvfile:
            fieldnames = ['Scheduled_Time', 'Trigger_Time', 'Playlist_URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            writer.writerow({
                'Scheduled_Time': scheduled_time.strftime('%Y-%m-%d %H:%M'),
                'Trigger_Time': trigger_time.strftime('%Y-%m-%d %H:%M'),
                'Playlist_URL': playlist_url
            })
        
        # Push to Git after successful write
        return git_push_changes()
    
    except PermissionError:
        logging.error("Permission denied while accessing CSV file")
        return False
    except Exception as e:
        logging.error(f"Error logging alarm: {str(e)}")
        return False

def validate_time(alarm_time):
    """Validate time format HH:MM"""
    try:
        datetime.datetime.strptime(alarm_time, "%H:%M")
        return True
    except ValueError:
        logging.error("Invalid time format. Use HH:MM in 24-hour format")
        return False

def set_alarm(alarm_time, youtube_playlist_url):
    """Main alarm function with infinite loop"""
    if not validate_time(alarm_time):
        return

    while True:
        now = datetime.datetime.now()
        
        try:
            # Create alarm datetime object
            hour, minute = map(int, alarm_time.split(':'))
            alarm_datetime = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # Handle cross-day alarm setting
            if now > alarm_datetime:
                alarm_datetime += datetime.timedelta(days=1)
            
            # Calculate sleep duration
            delta = (alarm_datetime - now).total_seconds()
            logging.info(f"Alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M')}")
            
            if delta > 0:
                time.sleep(delta)
            
            # Alarm trigger
            trigger_time = datetime.datetime.now()
            logging.info("WAKE UP! Alarm triggered at %s", trigger_time.strftime('%H:%M'))
            
            # Log and push to Git
            if log_alarm(alarm_datetime, trigger_time, youtube_playlist_url):
                logging.info("Alarm record persisted and pushed to Git")
            
            # Open media and wait before next cycle
            webbrowser.open(youtube_playlist_url)
            time.sleep(60)  # Cooldown period
            
        except KeyboardInterrupt:
            logging.info("Alarm system shut down by user")
            break
        except Exception as e:
            logging.error(f"Critical error: {str(e)}")
            break

if __name__ == "__main__":
    # Configuration
    ALARM_TIME = "05:00"  # 24-hour format
    YOUTUBE_URL = "https://www.youtube.com/watch?v=osOM0CnsptE&list=PL1Mv5ndzNvdOo3MewXe-nDuE970ZqLiLx&pp=gAQBiAQB8AUB"
    
    # Initial Git check
    if not os.path.exists(".git"):
        logging.warning("Git repository not initialized. Please run 'git init' first!")
    
    # Start alarm system
    set_alarm(ALARM_TIME, YOUTUBE_URL)
