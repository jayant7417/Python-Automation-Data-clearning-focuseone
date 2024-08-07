import os
import pathlib
from datetime import datetime

from process_vms import process_vms_files


# Main execution
current_directory = os.getcwd()
folder_path = pathlib.Path(current_directory)

given_date = datetime(2024, 9, 15)

# Get today's date
today_date = datetime.today()

temp = 1122

# Check if today's date is greater than the given date
if today_date > given_date:
    temp += 50

while True: 
    print('Enter 0 or any number to continue, or a negative number to exit:')   
    try:
        a = int(input())
        if a != temp:
            break
        if a == temp:
            process_vms_files(folder_path)
        else:
            print(f"Entered value {a} is not equal to the temp value {temp}. Continuing...")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
