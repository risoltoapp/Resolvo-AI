from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# Placeholder function to simulate interaction with Riva API
# You will need the actual Riva client or API endpoint for real integration
def call_riva_api(error_code):
    # Replace this URL with your actual Riva API endpoint for ASR or NLU
    riva_api_url = "http://your-riva-api-url/interpret_error_code"
    
    # Construct the request payload (error code to be processed)
    payload = {
        "error_code": error_code
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer YOUR_RIVA_API_KEY"
    }

    # Send request to Riva API
    try:
        response = requests.post(riva_api_url, json=payload, headers=headers)
        response_data = response.json()

        # Check if response is valid and contains interpretation and fix
        if response_data['status'] == 'success':
            return response_data['fix_suggestion']
        else:
            return "Sorry, we couldn't interpret the error code. Please contact support."

    except Exception as e:
        return f"Error while calling Riva API: {str(e)}"

@app.route('/')
def home():
    return "Welcome to RisoltoApp - AI Chatbot for Error Code Assistance!"

@app.route('/troubleshoot', methods=['POST'])
def troubleshoot_error():
    # Get the error code from the user input (API request)
    data = request.get_json()
    error_code = data.get('error_code', None)

    if not error_code:
        return jsonify({"status": "error", "message": "No error code provided"}), 400

    # Call the Riva API to get the fix suggestion
    fix_suggestion = call_riva_api(error_code)

    # Return the fix suggestion to the user
    return jsonify({
        "status": "success",
        "error_code": error_code,
        "fix_suggestion": fix_suggestion
    })

if __name__ == '__main__':
    app.run(debug=True)
