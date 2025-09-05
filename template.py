import os
import requests
from twilio.rest import Client

# --- Your Configuration Details ---
# Wordnik API Key (Sign up at https://www.wordnik.com/)
WORDNIK_API_KEY = "YOUR_WORDNIK_API_KEY"

# Twilio Credentials (From your Twilio dashboard)
TWILIO_ACCOUNT_SID = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" # Your Account SID
TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN"          # Your Auth Token
TWILIO_PHONE_NUMBER = "+15017122661"                  # Your Twilio phone number

# Your Personal Phone Number (The number to send the text to)
# Make sure to include the country code, e.g., "+12223334444"
MY_PHONE_NUMBER = "+12223334444"
# --- End of Configuration ---

def get_word_of_the_day():
    """Fetches the word of the day from the Wordnik API."""
    api_url = f"https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={WORDNIK_API_KEY}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raises an error for bad responses (4xx or 5xx)
        data = response.json()
        
        word = data.get("word", "N/A")
        # Get the first definition
        definition = data.get("definitions", [{}])[0].get("text", "No definition found.")
        # Get the first example
        example = data.get("examples", [{}])[0].get("text", "No example found.")
        
        return word, definition, example
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Wordnik: {e}")
        return None, None, None

def send_sms(message_body):
    """Sends the message using the Twilio API."""
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=MY_PHONE_NUMBER
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Error sending SMS via Twilio: {e}")

if __name__ == "__main__":
    word, definition, example = get_word_of_the_day()
    if word and definition:
        # Format the final text message
        final_message = (
            f"Word of the Day: {word.capitalize()}\n\n"
            f"Meaning: {definition}\n\n"
            f"Example: \"{example}\""
        )
        send_sms(final_message)
    else:
        print("Could not retrieve the word of the day. No message sent.")