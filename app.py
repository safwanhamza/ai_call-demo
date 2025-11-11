#!/usr/bin/env python3
import os, re, json, sys, time
import requests
from flask import Flask, request, render_template_string
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- Configuration & Initialization ---

# Load environment variables from .env file
# This loads VAPI_API_KEY, VAPI_PHONE_NUMBER_ID, etc.
load_dotenv() 

app = Flask(__name__)

# Read API configuration from environment
VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

# Validate that all required env variables are loaded
missing_vars = [k for k,v in {
    "VAPI_API_KEY": VAPI_API_KEY,
    "VAPI_PHONE_NUMBER_ID": VAPI_PHONE_NUMBER_ID,
    "VAPI_ASSISTANT_ID": VAPI_ASSISTANT_ID
}.items() if not v]

if missing_vars:
    print(f"Error: Missing required .env variables: {', '.join(missing_vars)}", file=sys.stderr)
    print("Please make sure your .env file is in the same directory and contains these keys.", file=sys.stderr)
    sys.exit(1)


# --- Vapi API Logic (from demo_call.py) ---

API_BASE = "https://api.vapi.ai"
E164_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")

def to_e164(raw: str) -> str:
    """Validates and formats a phone number to E.164 format."""
    # This function is from your demo_call.py
    raw = (raw or "").strip()
    if E164_REGEX.match(raw):
        return raw
    raise ValueError(f"Phone must be E.164 (e.g., +15551234567). Got: {raw}")

def create_call(
    token: str,
    assistant_id: str,
    phone_number_id: str,
    customer_number: str,
    name: str,
    address: str, # We'll pass an empty string from the UI
) -> Dict[str, Any]:
    """
    Makes the API call to Vapi to create an outbound call.
    This function is based on your demo_call.py
    """
    url = f"{API_BASE}/call"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    # Payload includes the assistantOverrides for name and address
    payload: Dict[str, Any] = {
        "assistantId": assistant_id,                 
        "phoneNumberId": phone_number_id,            
        "customer": {"number": customer_number},     
        "assistantOverrides": {                      
            "variableValues": { "name": name, "address": address }
        },
    }

    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(f"Vapi error {resp.status_code}: {resp.text}")
    return resp.json()

# --- HTML/CSS Template for the UI ---

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vapi Call Demo</title>
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 2em; 
            background: #f4f4f9;
            color: #333;
        }
        .container { 
            max-width: 500px; 
            margin: auto; 
            background: #fff; 
            padding: 2em; 
            border-radius: 8px; 
            box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        }
        h2 { 
            text-align: center; 
            color: #007bff;
        }
        form { 
            display: flex; 
            flex-direction: column; 
            gap: 1.2em; 
        }
        div {
            display: flex;
            flex-direction: column;
            gap: 0.5em;
        }
        label { 
            font-weight: bold; 
        }
        input[type="text"] { 
            padding: 0.8em; 
            border: 1px solid #ccc; 
            border-radius: 4px; 
            font-size: 1em;
        }
        button { 
            padding: 0.9em; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            font-size: 1em;
            font-weight: bold;
        }
        button:hover { 
            background: #0056b3; 
        }
        .message { 
            margin-top: 1.5em; 
            padding: 1em; 
            border-radius: 4px; 
            text-align: center; 
            word-wrap: break-word;
        }
        .success { 
            background: #d4edda; 
            color: #155724; 
            border: 1px solid #c3e6cb; 
        }
        .error { 
            background: #f8d7da; 
            color: #721c24; 
            border: 1px solid #f5c6cb; 
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Voice AI Demo</h2>
        <form method="POST" action="/">
            <div>
                <label for="phone">Phone Number (E.164):</label>
                <input type="text" id="phone" name="phone" placeholder="+15551234567" required>
            </div>
            <div>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" placeholder="e.g. John Doe" required>
            </div>
            <button type="submit">Place Call</button>
        </form>
        
        {% if message %}
            <div class="message {{ 'success' if 'Success' in message else 'error' }}">
                {{ message }}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""


# --- Flask Web Server Routes ---

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main route that handles both showing the form (GET)
    and processing the form (POST).
    """
    message = None
    if request.method == "POST":
        phone = request.form.get("phone", "").strip()
        name = request.form.get("name", "").strip()
        
        try:
            # 1. Validate phone number
            customer_number = to_e164(phone)
            
            # 2. Place the call using the logic from your script
            result = create_call(
                token=VAPI_API_KEY,
                assistant_id=VAPI_ASSISTANT_ID,
                phone_number_id=VAPI_PHONE_NUMBER_ID,
                customer_number=customer_number,
                name=name,
                address="",  # Address is not in the form, so we pass an empty string
            )
            
            call_id = result.get("id")
            status = result.get("status")
            message = f"Success! Call placed to {phone} (Name: {name}). Call ID: {call_id}, Status: {status}"
        
        except Exception as e:
            # Catch errors (e.g., invalid phone, API error)
            message = f"Error: {e}"
            
    # Render the HTML template, passing in the message if one exists
    return render_template_string(HTML_TEMPLATE, message=message)


# --- Run the Application ---

if __name__ == "__main__":
    print("\nStarting Vapi UI demo server...")
    print("Your .env file is loaded.")
    print("Access the UI by opening this URL in your browser:")
    print(f"  > http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)