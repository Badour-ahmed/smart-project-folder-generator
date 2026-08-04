# Smart Project Folder Generator

## Project Description

Smart Project Folder Generator is a Python automation tool that creates an organized folder structure for different project types.

The user can select the save location, enter the project name, and choose one of the following project types:

- GIS
- Survey
- Drone
- Remote Sensing

The program creates the required folders automatically based on the selected project type.

## Features

- Select the project save location.
- Create organized project folders automatically.
- Support different project types.
- Copy a report template into the Reports folder.
- Check current weather for Drone and Survey projects.
- Save weather information in a text file.
- Prevent duplicate project names.
- Handle basic errors.

## Technologies Used

- Python
- os
- shutil
- requests
- tkinter
- Open-Meteo API
- Object-Oriented Programming

## How to Run the Project

1. Install Python.

2. Install the requests library:

```bash
pip install requests
```

3. Run the project:

```bash
python smart_project_folder_generator.py
```

4. Select the project save location.

5. Enter the project name.

6. Enter one of the following project types:

```text
GIS
Survey
Drone
Remote Sensing
```

7. For Drone or Survey projects, enter the project location.

## Project Structure

```text
Final Project
│
├── smart_project_folder_generator.py
├── README.md
└── Template
    └── 04_Reports
        └── PROGRESS REPORT_V1.docx
```

## Output

The program creates a new project folder with organized subfolders based on the selected project type.

For Drone and Survey projects, the program also creates:

```text
01_Admin/Weather_Check.txt
```

## Author

Badour Ahmed Al Riyami
bedooralriyami7@gmail.com