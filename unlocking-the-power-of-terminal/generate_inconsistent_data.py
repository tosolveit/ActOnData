import os
import random
from faker import Faker

# Initialize the Faker generator
fake = Faker()

# Base directory for the file structure
BASE_DIR = "sample_data_inconsistent"
MAX_FILES = 1000  # Maximum number of files to create across all folders
file_count = 0  # Counter for total files created

# Example partitioned directories, mixing date-based and geography-based structures
directories = [
    ("date", "2023/09/01"),
    ("geography", "Europe/Germany/Berlin"),
    ("date", "2022/08/15"),
    ("geography", "Asia/Japan/Tokyo"),
    ("date", "2021/07/10"),
    ("geography", "North_America/USA/New_York"),
    ("date", "2023/09/02"),
    ("geography", "Africa/Kenya/Nairobi"),
]

# Event types for the log (more realistic categories)
event_types = ["ERROR", "INFO", "WARNING", "DEBUG", "CRITICAL", "NOTICE", "SUCCESS", "FAILURE"]

# Common device platforms
device_platforms = ["Windows", "Linux", "macOS", "iOS", "Android"]

# Function to generate random fake data for a row with a random number of columns, but consistent "Event" column
def generate_random_row():
    # Event type is selected from the list of log event states
    event_type = random.choice(event_types)

    # At least 2 columns with realistic log-related data
    additional_columns = [
        fake.ipv4_private(),  # IP Address
        fake.city(),  # Location
        fake.user_name(),  # User ID
        fake.date_time_this_year().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
        random.choice(["GET", "POST", "DELETE", "PUT"]),  # HTTP method
        random.choice(device_platforms)  # Device platform
    ]

    # Combine event name with additional columns (randomized to include between 2 and all columns)
    selected_columns = [event_type] + additional_columns[:random.randint(2, len(additional_columns))]

    # Join the columns with a comma separator to simulate CSV-like structure
    return ",".join(selected_columns)

# Function to create a file in a given folder with randomized data
def create_file(folder_path):
    global file_count
    if file_count >= MAX_FILES:
        return  # Stop creating files if the limit is reached

    # Create random file data
    file_name = os.path.join(folder_path, f"data_file_{random.randint(1000, 9999)}.txt")

    # Write data to the file, with a consistent "Event" field
    with open(file_name, "w") as f:
        # Always include the header with realistic columns
        header = "EVENT,IP_Address,Location,User_ID,Timestamp,HTTP_Method,Device\n"
        f.write(header)

        # Write random rows (2 to 5 rows)
        for _ in range(random.randint(2, 5)):
            f.write(f"{generate_random_row()}\n")

    file_count += 1
    print(f"Generated file: {file_name}")

# Function to create folder structure and distribute file creation across directories
def generate_structure():
    global file_count
    while file_count < MAX_FILES:
        for partition_type, partition_value in directories:
            if file_count >= MAX_FILES:
                break  # Stop creating files once the limit is reached

            # Create the folder path based on partition type
            if partition_type == "date":
                folder_path = os.path.join(BASE_DIR, partition_value)
            else:  # geography
                folder_path = os.path.join(BASE_DIR, "geography", partition_value)

            # Ensure the directory exists
            os.makedirs(folder_path, exist_ok=True)

            # Create a file in this directory
            create_file(folder_path)

# Generate the folder structure and files
generate_structure()

print(f"Total files created: {file_count}")

