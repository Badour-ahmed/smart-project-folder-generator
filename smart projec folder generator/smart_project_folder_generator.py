import os  # Work with folders and file paths
import shutil  # Copy files and folders
import requests  # Get weather data from an API
import tkinter as tk  # Create a simple window
from tkinter import filedialog  # Open a folder selection window


# Create a Project class to store project information and actions
class Project:

    # Initialize the project with its name, type, and save location
    def __init__(self, name, project_type, save_location):
        self.name = name
        self.project_type = project_type
        self.save_location = save_location

        # Create the full project path
        self.project_path = os.path.join(save_location, name)

    # Create folders inside the project
    def create_folders(self, folder_list):
        for folder in folder_list:
            folder_path = os.path.join(self.project_path, folder)
            os.mkdir(folder_path)

    # Copy the report template into the project reports folder
    def copy_report_template(self):

        # Get the folder where this Python file is located
        base_path = os.path.dirname(os.path.abspath(__file__))

        # Create the full path of the report template
        template_file = os.path.join(
            base_path,
            "Template",
            "04_Reports",
            "PROGRESS REPORT_V1.docx"
        )

        # Define the destination report folder
        destination_folder = os.path.join(
            self.project_path,
            "04_Reports"
        )

        # Check if the template file exists
        if os.path.exists(template_file):
            shutil.copy(template_file, destination_folder)
            print("Report template copied successfully.")
        else:
            print("Warning: Report template was not found.")

    # Get current weather data and save it inside the Admin folder
    def save_weather_check(self, location):

        try:
            # Search for the location coordinates
            geocoding_url = (
                "https://geocoding-api.open-meteo.com/v1/search"
            )

            geocoding_parameters = {
                "name": location,
                "count": 1,
                "language": "en",
                "format": "json"
            }

            geocoding_response = requests.get(
                geocoding_url,
                params=geocoding_parameters,
                timeout=10
            )

            # Stop if the API request failed
            geocoding_response.raise_for_status()

            geocoding_data = geocoding_response.json()

            # Check if the location was found
            if not geocoding_data.get("results"):
                print(
                    "Weather check failed: Location was not found."
                )
                return

            # Get the first matching location
            location_data = geocoding_data["results"][0]

            latitude = location_data["latitude"]
            longitude = location_data["longitude"]
            location_name = location_data["name"]

            # Request current weather data
            weather_url = (
                "https://api.open-meteo.com/v1/forecast"
            )

            weather_parameters = {
                "latitude": latitude,
                "longitude": longitude,
                "current": (
                    "temperature_2m,"
                    "precipitation,"
                    "wind_speed_10m,"
                    "wind_gusts_10m"
                ),
                "timezone": "auto"
            }

            weather_response = requests.get(
                weather_url,
                params=weather_parameters,
                timeout=10
            )

            # Stop if the weather request failed
            weather_response.raise_for_status()

            weather_data = weather_response.json()

            # Check that current weather data exists
            if "current" not in weather_data:
                print(
                    "Weather check failed: Weather data was not returned."
                )
                return

            current_weather = weather_data["current"]

            # Create the weather report path
            weather_file = os.path.join(
                self.project_path,
                "01_Admin",
                "Weather_Check.txt"
            )

            # Save the weather information in a text file
            with open(
                weather_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    f"Project Name: {self.name}\n"
                )

                file.write(
                    f"Project Type: "
                    f"{self.project_type.title()}\n"
                )

                file.write(
                    f"Location: {location_name}\n"
                )

                file.write(
                    f"Latitude: {latitude}\n"
                )

                file.write(
                    f"Longitude: {longitude}\n"
                )

                file.write(
                    f"Weather Time: "
                    f"{current_weather['time']}\n"
                )

                file.write(
                    f"Temperature: "
                    f"{current_weather['temperature_2m']} °C\n"
                )

                file.write(
                    f"Wind Speed: "
                    f"{current_weather['wind_speed_10m']} km/h\n"
                )

                file.write(
                    f"Wind Gusts: "
                    f"{current_weather['wind_gusts_10m']} km/h\n"
                )

                file.write(
                    f"Precipitation: "
                    f"{current_weather['precipitation']} mm\n"
                )

                file.write(
                    "\nNote: Review weather conditions, "
                    "site conditions, equipment limits, "
                    "and local regulations before field work."
                )

            print("Weather check saved successfully.")

        except requests.RequestException as error:
            print(f"Weather check failed: {error}")

        except KeyError:
            print(
                "Weather check failed: "
                "Some weather information was missing."
            )


# Create and hide the main Tkinter window
root = tk.Tk()
root.withdraw()

# Open a window to select the save location
save_location = filedialog.askdirectory(
    title="Select Project Save Location"
)

# Stop the program if no save location was selected
if save_location == "":
    print("Error: No save location was selected.")
    input("Press Enter to close...")
    exit()

print(f"Save location: {save_location}")

# Ask the user to enter the project name
project_name = input(
    "Enter project name: "
).strip()

# Check if the project name is empty
if project_name == "":
    print("Error: Project name cannot be empty.")
    input("Press Enter to close...")
    exit()

# Create the full project path
project_path = os.path.join(
    save_location,
    project_name
)

# Check if the project folder already exists
if os.path.exists(project_path):
    print(
        "Error: A project with this name "
        "already exists in the selected location."
    )
    input("Press Enter to close...")
    exit()

# Ask the user to enter the project type
project_type = input(
    "Enter project type "
    "(GIS, Survey, Drone, Remote Sensing): "
).strip().lower()

# Create a list containing the basic project folders
folders = [
    "01_Admin",
    "02_Raw_Data",
    "03_Processed_Data",
    "04_Reports",
    "05_Deliverables"
]

# Create folders based on the selected project type
if project_type == "gis":
    extra_folders = [
        "06_Geodatabase",
        "07_Shapes",
        "08_Maps",
        "09_QA_QC"
    ]

elif project_type == "survey":
    extra_folders = [
        "06_GNSS_Data",
        "07_GCPs",
        "08_CAD",
        "09_QA_QC"
    ]

elif project_type == "drone":
    extra_folders = [
        "06_Drone_Images",
        "07_Pix4D",
        "08_Orthomosaic",
        "09_DSM_DTM"
    ]

elif project_type == "remote sensing":
    extra_folders = [
        "06_Satellite_Data",
        "07_Processing",
        "08_Classification",
        "09_Analysis"
    ]

else:
    print("Error: Invalid project type.")
    input("Press Enter to close...")
    exit()

# Create a Project object
project = Project(
    project_name,
    project_type,
    save_location
)

try:
    # Create the main project folder
    os.mkdir(project.project_path)

    # Create the basic folders
    project.create_folders(folders)

    # Create the additional folders
    project.create_folders(extra_folders)

    # Copy the report template
    project.copy_report_template()

    # Get and save weather data for Drone and Survey projects
    if project_type in ["drone", "survey"]:
        location = input(
            "Enter the project location: "
        ).strip()

        if location != "":
            project.save_weather_check(location)
        else:
            print(
                "Weather check skipped: "
                "Location was not entered."
            )

    # Display the final project information
    print()
    print(
        f"Project type: "
        f"{project.project_type.title()}"
    )

    print(
        f"Project created in: "
        f"{project.project_path}"
    )

    print(
        "Project folders created successfully."
    )

except OSError as error:
    print(
        f"Project creation failed: {error}"
    )

# Keep the window open so the user can read the results
input("Press Enter to close...")