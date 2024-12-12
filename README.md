# TAMAD: Task Manager Application Development

## I. Project Overview
TAMAD (Task Manager Application Development) is a Python-based desktop application that helps users efficiently manage their daily tasks. It includes features such as task creation, marking tasks as completed, viewing task history, and toggling between light and dark modes. With an intuitive graphical interface, TAMAD simplifies task management, boosting productivity and organization for users.

---

## II. Application of Python Concepts and Libraries
The project demonstrates the practical application of various Python concepts and libraries:
- **Tkinter**: Used for creating an intuitive graphical user interface (GUI).
- **SQLite3**: Enables efficient local database management for task storage.
- **Pygame**: Provides background music functionality to enhance the user experience.
- **Pillow (PIL)**: Handles image processing for GUI elements.
- **Modular Design**: The code is structured into reusable functions for easier maintenance and scalability.

---

## III. Sustainable Development Goals (SDGs) Integration
This project integrates two Sustainable Development Goals:  

### **SDG 4: Quality Education**  
TAMAD supports students and educators by promoting better task organization, aiding in deadline management, and fostering productivity in educational settings. It serves as a practical tool to help users balance study schedules, assignments, and learning objectives effectively.  

### **SDG 8: Decent Work and Economic Growth**  
By promoting efficient time and task management, TAMAD enables users to optimize their workflow, improve work-life balance, and reduce stress. It supports the goal of achieving productive employment and fostering sustained economic growth through personal productivity improvements.  

---

## IV. Instructions for Running the Program
To successfully run TAMAD, 
follow these steps:

### **Step 1: Install Required Libraries**
   a. Open a terminal or command prompt.  
   b. Run the following command to install necessary libraries:  
   pip install pygame pillow
   
Step 2: Prepare Application Files
a. Ensure that the following media files are included in the project directory:
- Download.mp3: Background music for the application.
 - Images such as image.gif, view.jpg, and save_icon.png for the graphical interface.
 b. Confirm that the SQLite database file (tasks_manager.db) is present for task storage.

Step 3: Run the Main Program
a. Navigate to the directory where main.py is stored.
b. Execute the following command to launch the program:

python main.py
Step 4: Use the Application
a. Add Tasks: Enter a task in the input field and click "Save" to add it to your list.
b. Mark as Completed: Select tasks and mark them as completed.
c. View Task History: Navigate to the history screen to view all completed tasks.
d. Dark/Light Mode: Toggle between light and dark themes using the mode switch.

Step 5: Troubleshooting
a. If the application fails to start, ensure all dependencies are correctly installed.
b. Verify that required assets (media files and database) are in the correct directory.
c. If the database is corrupted or missing, recreate it by running the database initialization script (if provided).

Note: Ensure Python 3.x is installed on your system. For best results, run the program in a virtual environment to avoid dependency conflicts.
