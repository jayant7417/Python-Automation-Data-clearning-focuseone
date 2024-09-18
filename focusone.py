import os
import pathlib
from datetime import datetime

from delete_files import delete_files
from process_vms import process_vms_files


# Main execution
current_directory = os.getcwd()
folder_path = pathlib.Path(current_directory)

given_date = datetime(2024, 10, 15)

# Get today's date
today_date = datetime.today()

temp = 1122

# Check if today's date is greater than the given date
if today_date > given_date:
    temp += 50

while True: 
    print('Enter pass or any number to continue, or a negative number to exit:')   
    try:
        a = int(input())
        if a != temp:
            break
        print("enter 1 for result")
        print("enter 0 for delete")
        b = int(input())
        if b == 1:
            process_vms_files(folder_path)
        elif b == 0:
            delete_files(folder_path)
        else:
            print ("wrong input plz put a valid number")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

