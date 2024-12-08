from flask import Flask, render_template, request, flash
import requests
import json
from twilio.rest import Client
import random 

app = Flask(__name__)
app.secret_key = "Hardik@123456789"  # Use a strong and secure key for production

# Twilio Config
TWILIO_SID = 'AC2faf957ea2fab2bfe6e20b9dd13d509b'
TWILIO_AUTH_TOKEN = 'b72d26b69155ee07f46e1e9097befe64'
TWILIO_PHONE = '+17058065341'  # Ensure this is a valid Twilio number from your account
TO_PHONE = '+17059043333'  # Ensure this is a verified number if using a Twilio trial account


# API URLs
HARRY_POTTER_API = "https://hp-api.onrender.com/api/characters"
OPENWEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
OPENNOTIFY_API = "http://api.open-notify.org/astros.json"

# OpenWeather API Key
OPENWEATHER_KEY = "bd5e378503939ddaee76f12ad7a97608"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send', methods=['POST'])
def send_message():
    try:
        # Harry Potter API: Get random character
        hp_response = requests.get(HARRY_POTTER_API)
        hp_response.raise_for_status()  # Check for HTTP errors
        hp_data = hp_response.json()
        character = random.choice(hp_data)  # Fetch a random character

        # Extract character details
        character_name = character.get("name", "Unknown")
        character_house = character.get("house", "No House Information")
        character_patronus = character.get("patronus", "No Patronus Information")
        character_ancestry = character.get("ancestry", "Unknown ancestry")
        character_image = character.get("image", "No image available")  # Extract image URL

        # OpenWeather API: Weather for Sudbury
        weather_params = {"q": "Sudbury", "appid": OPENWEATHER_KEY, "units": "metric"}
        weather_response = requests.get(OPENWEATHER_API, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        weather = f"{weather_data['weather'][0]['description']} with {weather_data['main']['temp']}°C"

        # OpenNotify API: Number of people in space
        opennotify_response = requests.get(OPENNOTIFY_API)
        opennotify_response.raise_for_status()
        astronauts = opennotify_response.json()["number"]

        # Construct a beautiful and engaging message
        message = (
            f"✨ Greetings! Here’s some magical and worldly news for you! ✨\n\n"
            f"📖 *Harry Potter Character Spotlight*: Meet {character_name}.\n"
            f"🏠 *House*: {character_house}\n"
            f"🧙 *Ancestry*: {character_ancestry}\n"
            f"🦄 *Patronus*: {character_patronus}\n"
            f"🖼️ *Image*: {character_image if character_image != 'No image available' else 'Image not available'}\n\n"
            f"🌦 *Weather in Sudbury*: It’s currently {weather}.\n\n"
            f"🚀 *Fun Fact*: Did you know there are {astronauts} people in space right now?\n\n"
            f"Stay curious and have a magical day ahead! 🌟"
        )

        # Send SMS via Twilio
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        twilio_message = client.messages.create(
            body=message,
            from_=TWILIO_PHONE,
            to=TO_PHONE
        )

        # Log the message
        log_message({"message": message, "status": twilio_message.status})

        flash("Message sent successfully!", "success")
    except requests.exceptions.RequestException as req_err:
        flash(f"API error: {req_err}", "danger")
    except Exception as e:
        flash(f"An unexpected error occurred: {e}", "danger")

    return render_template('index.html')


def log_message(data):
    """Logs the message details to a file."""
    with open("messages.log", "a") as log_file:
        log_file.write(json.dumps(data, indent=4) + "\n")

if __name__ == "__main__":  # Corrected main entry point
    app.run(debug=True)
