from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Gemini API Configuration
GEMINI_API_KEY = "api-key"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# In-memory storage
solutions = []
situations = {"current": None, "history": []}

@app.route("/generate_situation", methods=["GET"])
def generate_situation():
    try:
        prompt = (
            "Generate a short, dynamic, and engaging problem-solving scenario (10 words or less). "
            "It could involve anything from social dilemmas, workplace decisions, puzzles, and personal challenges."
        )
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}", headers=headers, json=data, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            situation = response_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            
            # Limit to 10 words
            situation_words = situation.split()
            if len(situation_words) > 10:
                situation = " ".join(situation_words[:10])
            
            # Store current situation and maintain history
            situations["current"] = situation
            situations["history"].append(situation)
            
            return jsonify({"situation": situation})
        else:
            return jsonify({"error": f"API error: {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/submit_solution", methods=["POST"])
def submit_solution():
    data = request.json
    if not data.get("solution") or not situations["current"]:
        return jsonify({"error": "Invalid solution or no situation available"}), 400

    solutions.append({"situation": situations["current"], "solution": data["solution"], "approved": False, "feedback": ""})
    return jsonify({"message": "Solution submitted successfully!"})

@app.route("/get_solutions", methods=["GET"])
def get_solutions():
    return jsonify(solutions)

@app.route("/approve_solution", methods=["POST"])
def approve_solution():
    data = request.json
    index = data.get("index")
    feedback = data.get("feedback", "")
    if index is not None and 0 <= index < len(solutions):
        solutions[index]["approved"] = True
        solutions[index]["feedback"] = feedback
        return jsonify({"message": "Solution approved!"})
    return jsonify({"error": "Invalid index"}), 400

@app.route("/generate_feedback", methods=["POST"])
def generate_feedback():
    data = request.json
    situation = data.get("situation")
    solution = data.get("solution")
    
    # Generate feedback using Gemini API
    feedback_prompt = f"Provide constructive feedback on the following solution for the situation: '{situation}'. Solution: '{solution}'."
    feedback_data = {"contents": [{"parts": [{"text": feedback_prompt}]}]}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(f"{GEMINI_ENDPOINT}?key={GEMINI_API_KEY}", headers=headers, json=feedback_data, timeout=10)
        if response.status_code == 200:
            response_json = response.json()
            feedback = response_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            return jsonify({"feedback": feedback})
        else:
            return jsonify({"error": "Failed to generate feedback"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/get_approved_solutions", methods=["GET"])
def get_approved_solutions():
    approved = [sol for sol in solutions if sol["approved"]]
    return jsonify(approved)

if __name__ == "__main__":
    app.run(debug=True)
