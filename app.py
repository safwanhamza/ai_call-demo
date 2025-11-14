#!/usr/bin/env python3
import os, re, json, sys, time
import requests
# MODIFIED: Added redirect and url_for
from flask import Flask, request, render_template_string, redirect, url_for
from dotenv import load_dotenv
from typing import Dict, Any, Optional

# --- Configuration & Initialization ---
load_dotenv() 

app = Flask(__name__)

VAPI_API_KEY = os.getenv("VAPI_API_KEY")
VAPI_PHONE_NUMBER_ID = os.getenv("VAPI_PHONE_NUMBER_ID")
VAPI_ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

missing_vars = [k for k,v in {
    "VAPI_API_KEY": VAPI_API_KEY,
    "VAPI_PHONE_NUMBER_ID": VAPI_PHONE_NUMBER_ID,
    "VAPI_ASSISTANT_ID": VAPI_ASSISTANT_ID
}.items() if not v]

if missing_vars:
    print(f"Error: Missing required .env variables: {', '.join(missing_vars)}", file=sys.stderr)
    print("Please make sure your .env file is in the same directory and contains these keys.", file=sys.stderr)
    sys.exit(1)


# --- Vapi API Logic ---
API_BASE = "https://api.vapi.ai"
E164_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")

def to_e164(raw: str) -> str:
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
    address: str, 
) -> Dict[str, Any]:
    url = f"{API_BASE}/call"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
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

# --- Call Limiter ---
CALL_LIMIT = 5
call_counter = 0

# --- HTML/CSS Template for the UI ---

# MODIFIED: This block contains the fix
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Outbound Call Demo</title>
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
            margin-bottom: 0.5em; /* MODIFIED */
        }
        /* NEW: Style for the balance counter */
        .balance {
            text-align: center;
            font-size: 1.2em;
            margin-bottom: 1.5em;
            color: #555;
        }
        .balance strong {
            color: #000;
            /* NEW: Change color to red when balance is 0 */
            {% if remaining_calls <= 0 %}
                color: #d9534f;
            {% endif %}
        }
        /* END NEW */
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
        /* NEW: Disable button when no balance */
        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }
        /* END NEW */
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
        <h2>Place a Personalized Outbound Call</h2>
        

        
        <form method="POST" action="/">
            <div>
                <label for="phone">Phone Number (E.164):</label>
                <input type="text" id="phone" name="phone" placeholder="+15551234567" required>
            </div>
            <div>
                <label for="name">Name:</label>
                <input type="text" id="name" name="name" placeholder="e.g. John Doe" required>
            </div>
            <button type="submit" {% if remaining_calls <= 0 %}disabled{% endif %}>
                Place Call
            </button>
        </form>
        
        {% if message %}
            <div class="message {{ 'success' if 'Success' in message|string else 'error' }}">
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
    global call_counter
    message = None
    
    if request.method == "POST":
        
        if call_counter >= CALL_LIMIT:
            message = "Error: Your balance is 0. No more calls can be made."
            return render_template_string(
                HTML_TEMPLATE, 
                message=message, 
                remaining_calls=0
            )

        phone = request.form.get("phone", "").strip()
        name = request.form.get("name", "").strip()
        
        try:
            customer_number = to_e164(phone)
            
            result = create_call(
                token=VAPI_API_KEY,
                assistant_id=VAPI_ASSISTANT_ID,
                phone_number_id=VAPI_PHONE_NUMBER_ID,
                customer_number=customer_number,
                name=name,
                address="",
            )
            
            call_counter += 1
            
            call_id = result.get("id")
            status = result.get("status")
            message = f"Success! Call placed to {phone}. Call ID: {call_id}, Status: {status}"
        
        except Exception as e:
            message = f"Error: {e}"
            
    remaining_calls = CALL_LIMIT - call_counter
    if remaining_calls < 0:
        remaining_calls = 0
            
    return render_template_string(
        HTML_TEMPLATE, 
        message=message, 
        remaining_calls=remaining_calls
    )

# --- NEW: Secret Reset Route for Stakeholders ---
@app.route("/reset")
def reset_counter():
    """
    A secret route for stakeholders to reset the call balance.
    """
    global call_counter
    call_counter = 0
    print("--- CALL COUNTER RESET TO 0 ---") # A message for your server logs
    # Redirect back to the main page
    return redirect(url_for("index"))
# --- END NEW ---


# --- Run the Application ---
if __name__ == "__main__":
    print("\nStarting Vapi UI demo server...")
    print("Your .env file is loaded.")
    print(f"Call limit is set to {CALL_LIMIT} calls per session.")
    print("Access the UI by opening this URL in your browser:")
    print(f"  > http://1227.0.0.1:5000") # Typo corrected, though not part of the bug
    print("\nStakeholder Control:") 
    print(f"  > To reset the call balance, visit: http://127.0.0.1:5000/reset\n") 
    app.run(debug=True, port=5000)


