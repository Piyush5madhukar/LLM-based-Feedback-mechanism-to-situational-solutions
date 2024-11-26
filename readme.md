The SolutionHub is a web-based platform where users can:

Generate problem-solving scenarios.
Submit solutions.
Receive feedback and approval from an admin.
View approved solutions along with feedback.
Components:
Frontend (User Interface)

User Interface (UI): A Streamlit app for users and admins.
User: Users can generate a situation, submit their solutions, and view approved solutions.
Admin: Admins can view submitted solutions, generate feedback, and approve or reject solutions.
Backend (Server)

Flask Server: Handles API calls for generating situations, submitting solutions, generating feedback, and approving solutions.
Gemini API: Used for generating scenarios and feedback.
Database/Storage: In-memory storage for solutions, feedback, and approval status.
Workflow
Generate Scenario (User)

Action: User clicks "Generate New Situation" on the UI.
API Call: Streamlit frontend calls the /generate_situation endpoint in the Flask server.
Gemini API: The server generates a problem-solving situation by calling the Gemini API.
Output: The situation is displayed to the user.
Submit Solution (User)

Action: User writes a solution and clicks "Submit Solution."
API Call: The frontend sends the solution to the /submit_solution endpoint.
Backend: The server stores the solution along with the current situation.
Output: User is notified that the solution has been submitted successfully.
View Approved Solutions (User)

Action: User clicks on "Approved Solutions."
API Call: The frontend requests the /get_approved_solutions endpoint.
Backend: The server fetches all approved solutions from the storage and returns them.
Output: The user sees approved solutions with feedback.
Admin Dashboard

Action: Admin accesses the admin dashboard via Streamlit.
API Call: Admin fetches the list of submitted solutions using /get_solutions from the Flask server.
Output: All pending solutions are displayed to the admin.
Generate Feedback (Admin)

Action: Admin generates feedback for a specific solution.
API Call: The admin clicks "Generate Feedback," and the system calls the /generate_feedback endpoint with the situation and solution details.
Gemini API: The server uses the Gemini API to generate detailed feedback.
Output: The generated feedback is displayed to the admin.
Approve Solution (Admin)

Action: After reviewing the feedback, the admin approves the solution.
API Call: Admin clicks "Approve Solution," triggering the /approve_solution endpoint in the Flask server.
Backend: The server updates the solution status to approved and stores the feedback.
Output: The solution is marked as approved in the system.
Notify User (Backend)

Action: Once approved, the feedback is associated with the solution, and the system can send an email or notification to the user (optional step).
Output: User is informed that their solution has been approved, along with the feedback.
Technologies Used:
Backend: Flask
Frontend: Streamlit (for both user and admin interfaces)
API Integration: Gemini API for generating content and feedback
Storage: In-memory database (for simplicity, you could later migrate to a more robust solution like PostgreSQL or MongoDB)
Detailed User Flow
User Side:

Step 1: User generates a situation.
Step 2: User submits a solution.
Step 3: User waits for admin approval and feedback.
Step 4: User can view approved solutions.
Admin Side:

Step 1: Admin reviews submitted solutions.
Step 2: Admin generates feedback for each solution.
Step 3: Admin approves or rejects solutions.
Step 4: Admin views all approved solutions.
APIs:
/generate_situation (GET)

Description: Generates a new problem-solving scenario.
Response: A new situation in the form of a string.
/submit_solution (POST)

Description: Submits a solution for the current situation.
Input: {"solution": "User's solution text"}
Response: Success or error message.
/get_solutions (GET)

Description: Fetches all submitted solutions.
Response: A list of solutions.
/approve_solution (POST)

Description: Approves a solution with feedback.
Input: {"index": solution_index, "feedback": "Admin feedback"}
Response: Success or error message.
/generate_feedback (POST)

Description: Generates feedback for a solution.
Input: {"situation": "Problem", "solution": "Proposed solution"}
Response: Generated feedback.
/get_approved_solutions (GET)

Description: Fetches all approved solutions with feedback.
Response: A list of approved solutions and feedback.
