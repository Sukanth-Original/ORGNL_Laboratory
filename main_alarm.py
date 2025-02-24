import datetime
import time
import webbrowser

def set_alarm(alarm_time, youtube_playlist_url):
    while True:
        # Get the current time and date
        now = datetime.datetime.now()
        
        # Create a datetime object for today's alarm time
        alarm_datetime = now.replace(hour=int(alarm_time.split(":")[0]), 
                                     minute=int(alarm_time.split(":")[1]), 
                                     second=0, microsecond=0)
        
        # If alarm time has already passed today, set it for tomorrow
        if now > alarm_datetime:
            alarm_datetime += datetime.timedelta(days=1)
        
        # Calculate the time to wait
        time_to_wait = (alarm_datetime - now).total_seconds()
        
        print(f"Alarm set for {alarm_datetime.strftime('%Y-%m-%d %H:%M')}, ORGNL")
        
        # Wait until the alarm time
        time.sleep(time_to_wait)
        
        print("Time to wake up!")
        webbrowser.open(youtube_playlist_url)
        
        # Wait for 1 minute before resetting the alarm for the next day
        time.sleep(60)

# Example usage
alarm_time = "05:00"  # Set alarm time in HH:MM format (24-hour format)
youtube_playlist_url = "https://www.youtube.com/watch?v=osOM0CnsptE&list=PL1Mv5ndzNvdOo3MewXe-nDuE970ZqLiLx&pp=gAQBiAQB8AUB"

# Run the alarm indefinitely
set_alarm(alarm_time, youtube_playlist_url)