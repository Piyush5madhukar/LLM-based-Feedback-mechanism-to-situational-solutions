import streamlit as st
import requests

SERVER_URL = "http://127.0.0.1:5000"

st.title("User Situation Solver")

# Fetch or generate a situation
if "situation" not in st.session_state:
    st.session_state.situation = None

if st.button("Generate New Situation"):
    response = requests.get(f"{SERVER_URL}/generate_situation")
    if response.status_code == 200:
        st.session_state.situation = response.json()["situation"]
        st.success("New situation generated!")
    else:
        st.error("Failed to generate a situation.")

if st.session_state.situation:
    st.markdown(f"### Situation: {st.session_state.situation}")
else:
    st.info("Click the button above to generate a situation.")

# Solution submission
user_solution = st.text_area("Your Solution", placeholder="Describe your solution here...")
if st.button("Submit Solution"):
    if not st.session_state.situation or not user_solution.strip():
        st.error("Please generate a situation and provide a solution before submitting.")
    else:
        response = requests.post(
            f"{SERVER_URL}/submit_solution",
            json={"solution": user_solution.strip()}
        )
        if response.status_code == 200:
            st.success("Solution submitted successfully! Await admin feedback.")
        else:
            st.error("Failed to submit the solution.")

# Show approved solutions
st.markdown("## Approved Solutions")
response = requests.get(f"{SERVER_URL}/get_approved_solutions")
if response.status_code == 200:
    approved_solutions = response.json()
    if approved_solutions:
        # Only show solutions for the current situation
        for sol in approved_solutions:
            if sol["situation"] == st.session_state.situation:
                st.markdown(f"**Situation:** {sol['situation']}")
                st.write(f"**Solution:** {sol['solution']}")
                # Display feedback from admin
                feedback = sol.get("feedback", "Feedback is not available yet.")
                st.write(f"**Feedback:** {feedback}")
                break  # Show only one approved solution for the current situation
        else:
            st.info("No approved solutions available for the current situation.")
    else:
        st.info("No approved solutions available yet.")
else:
    st.error("Failed to fetch approved solutions.")

# Refresh Button to check if there are approved solutions
if st.button("Refresh Approved Solutions"):
    # Fetch updated approved solutions
    # response = requests.get(f"{SERVER_URL}/get_approved_solutions")
    # if response.status_code == 200:
    #     approved_solutions = response.json()
    #     # Filter out approved solutions related to the current situation
    #     for sol in approved_solutions:
    #         if sol["situation"] == st.session_state.situation and sol["approved"]:
    #             st.markdown(f"**Situation:** {sol['situation']}")
    #             st.write(f"**Solution:** {sol['solution']}")
    #             # Show feedback from admin
    #             feedback = sol.get("feedback", "Feedback is not available yet.")
    #             st.write(f"**Feedback:** {feedback}")
    #             break
    #     else:
    #         st.info("No approved solutions available yet.")
    # else:
    #     st.error("Failed to fetch approved solutions.")
    # Fetch and display approved solutions
# st.markdown("## Debug Approved Solutions")
    response = requests.get(f"{SERVER_URL}/get_approved_solutions")
    if response.status_code == 200:
        st.write("Server Response:", response.json())  # Debug response
        approved_solutions = response.json()
        if approved_solutions:
            st.markdown("### Approved Solutions")
            for sol in approved_solutions:
                if sol["situation"] == st.session_state.situation:
                    st.markdown(f"**Situation:** {sol['situation']}")
                    st.write(f"**Solution:** {sol['solution']}")
                    st.write(f"**Feedback:** {sol['feedback']}")
                    break
            else:
                st.info("No approved solutions available for the current situation.")
        else:
            st.info("No approved solutions available yet.")
    else:
        st.error("Failed to fetch approved solutions.")
