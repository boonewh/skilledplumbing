# Scheduling Appointment Management on PythonAnywhere

This document explains how to set up scheduled tasks on PythonAnywhere to automatically manage your appointment slots throughout the day.

## Prerequisites

- You have a paid PythonAnywhere account
- Your Flask app is set up and running
- The `manage_appointments.py` script is uploaded to your PythonAnywhere account

## Setting Up Scheduled Tasks

Since you're on a paid plan, you can schedule up to 20 tasks that run at specific times. Here's how to set up the tasks we need:

### 1. Navigate to the Tasks Tab

Go to the "Tasks" tab on your PythonAnywhere dashboard.

### 2. Create the Morning Cleanup Task (UTC Time)

If you're in Eastern Time (ET), set the task to run at 10:00 or 11:00 AM UTC (depending on standard/daylight saving time).
If you're in Central Time (CT), set it to 11:00 AM or 12:00 PM UTC.
If you're in Mountain Time (MT), set it to 12:00 PM or 1:00 PM UTC.
If you're in Pacific Time (PT), set it to 1:00 PM or 2:00 PM UTC.

- Command: `source /home/boonewh/skilledplumbing/venv/bin/activate && python /home/boonewh/skilledplumbing/manage_appointments.py morning`

This will remove the 8am, 9am, and 10am slots at the beginning of the day.

### 3. Create the Midday Cleanup Task (UTC Time)

Set this task to run 2 hours after the morning task in UTC time.

- Command: `source /home/boonewh/skilledplumbing/venv/bin/activate && python /home/boonewh/skilledplumbing/manage_appointments.py midday`

This will remove the 11am, 12pm, and 1pm slots.

### 4. Create the Afternoon Cleanup Task (UTC Time)

Set this task to run 2 hours after the midday task in UTC time.

- Command: `source /home/boonewh/skilledplumbing/venv/bin/activate && python /home/boonewh/skilledplumbing/manage_appointments.py afternoon`

This will remove the 2pm and 3pm slots.

### 5. Create the Noon Task (UTC Time)

Set this task to run at your local noon time, converted to UTC:
For ET: 4:00 or 5:00 PM UTC
For CT: 5:00 or 6:00 PM UTC
For MT: 6:00 or 7:00 PM UTC
For PT: 7:00 or 8:00 PM UTC

- Command: `source /home/boonewh/skilledplumbing/venv/bin/activate && python /home/boonewh/skilledplumbing/manage_appointments.py noon`

This will remove any remaining available slots for the current day and add a new day to the end of the schedule.

## Important Notes

1. **Time Zones**: PythonAnywhere runs tasks in UTC time. Make sure to adjust the scheduled times according to your local time zone.

2. **Virtual Environment**: If your Flask app uses a virtual environment, you'll need to modify the commands. For example:
   ```
   source /home/yourusername/.virtualenvs/yourenvname/bin/activate && python /path/to/your/app/manage_appointments.py morning
   ```

3. **Monitoring**: You can check the logs for each task by clicking on the task in the "Tasks" tab after it has run.

4. **Testing**: Before relying on the scheduled tasks, you can test the script by running it manually in a console:
   ```
   python manage_appointments.py all
   ```

## Customizing the Schedule

If you want to adjust the times when appointments are removed:

1. Edit the `manage_appointments.py` script to change the hours that are removed.
2. Change the scheduled task times on PythonAnywhere.

Remember that with a paid account, you can have up to 20 scheduled tasks, so you have flexibility to customize your scheduling as needed.