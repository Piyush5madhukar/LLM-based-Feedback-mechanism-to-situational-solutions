import streamlit as st
import requests

SERVER_URL = "http://127.0.0.1:5000"

st.title("Admin Dashboard")

# Fetch submitted solutions
st.markdown("## Submitted Solutions")
response = requests.get(f"{SERVER_URL}/get_solutions")
if response.status_code == 200:
    solutions = response.json()
    if solutions:
        for i, sol in enumerate(solutions):
            if not sol["approved"]:
                st.markdown(f"**Situation:** {sol['situation']}")
                st.write(f"**Solution:** {sol['solution']}")
                
                # Generate feedback for the admin to review
                if st.button(f"Generate Feedback for Solution {i+1}", key=f"feedback_{i}"):
                    feedback_response = requests.post(
                        f"{SERVER_URL}/generate_feedback",
                        json={"situation": sol["situation"], "solution": sol["solution"]}
                    )
                    if feedback_response.status_code == 200:
                        feedback = feedback_response.json()["feedback"]
                        st.write(f"**Feedback:** {feedback}")
                        
                        # Approve solution along with feedback
                        if st.button(f"Approve Solution {i+1}", key=f"approve_{i}"):
                            approve_response = requests.post(
                                f"{SERVER_URL}/approve_solution",
                                json={"index": i, "feedback": feedback}
                            )
                            if approve_response.status_code == 200:
                                st.success(f"Solution {i+1} approved with feedback!")
                            else:
                                st.error("Failed to approve the solution.")
                    else:
                        st.error("Failed to generate feedback.")
    else:
        st.info("No solutions awaiting approval.")
else:
    st.error("Failed to fetch solutions.")
