from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CAT_API_KEY = os.getenv("CAT_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
CAT_API_URL = "https://api.thecatapi.com/v1/images/search"
CAT_BREEDS_URL = "https://api.thecatapi.com/v1/breeds"

app = Flask(__name__)
CORS(app)

# Global variable to cache breed information
breeds_cache = {}


# Fetch all breeds from The Cat API
def fetch_all_breeds():
    headers = {"x-api-key": CAT_API_KEY}
    response = requests.get(CAT_BREEDS_URL, headers=headers)

    if response.status_code != 200:
        return None

    return {breed["name"].lower(): breed["id"] for breed in response.json()}


# Fetch cat images based on breed and number
def get_cat_images(breed_id=None, num=3):
    headers = {"x-api-key": CAT_API_KEY}
    params = {"limit": num, "has_breeds": 1}
    if breed_id:
        params["breed_ids"] = breed_id

    response = requests.get(CAT_API_URL, headers=headers, params=params)
    if response.status_code != 200:
        return {"error": response.json()}, response.status_code

    return response.json()


# Helper function to use OpenAI for breed and number extraction
def parse_input_with_openai(user_input):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an assistant that extracts information about cat breeds and the number of images requested. "
                    "Return the breed name and the number of images in JSON format like this: "
                    '{"breed": "sphynx", "num": 4}. If no number is mentioned, default to 3. If no breed is mentioned, set '
                    '"breed" to None.'
                ),
            },
            {"role": "user", "content": user_input},
        ],
    }

    response = requests.post(OPENAI_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return None, f"OpenAI API error: {response.json()}"

    try:
        parsed_response = response.json()
        breed_data = parsed_response["choices"][0]["message"]["content"]
        return eval(breed_data), None  # Convert string JSON to dict
    except Exception as e:
        return None, f"Error parsing OpenAI response: {str(e)}"


@app.route("/chat", methods=["POST"])
def chat_with_assistant_or_cats():
    global breeds_cache

    # Ensure breed cache is loaded
    if not breeds_cache:
        breeds_cache = fetch_all_breeds()
        if not breeds_cache:
            return jsonify({"error": "Failed to load breed data from The Cat API."}), 500

    data = request.json
    user_input = data.get("user_input")
    if not user_input:
        return jsonify({"error": "User input is required"}), 400

    if "cat" in user_input.lower():
        # Parse user input for breed and number
        parsed_data, error = parse_input_with_openai(user_input)
        if error:
            return jsonify({"error": error}), 400

        breed_name = parsed_data.get("breed")
        num = parsed_data.get("num", 3)

        # Match breed name with breed ID
        breed_id = breeds_cache.get(breed_name.lower()) if breed_name else None

        # Use default values if no valid breed or number is found
        if not breed_name or not breed_id:
            breed_name = None
            breed_id = None
            num = 3

        # Fetch cat images
        cat_images = get_cat_images(breed_id, num)
        if isinstance(cat_images, dict) and "error" in cat_images:
            return jsonify({"error": "Failed to fetch cat images."}), 500

        return jsonify({"breed": breed_name, "num": num, "images": cat_images})

    # Fallback to OpenAI chat for non-cat-related inputs
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": user_input}],
    }

    response = requests.post(OPENAI_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return jsonify({"error": response.json()}), response.status_code

    return jsonify(response.json()["choices"][0]["message"]["content"])


if __name__ == "__main__":
    app.run(debug=True)
