from flask import Flask, render_template, request, send_file
import requests

# Your Google Maps API Key
API_KEY = "YOAIzaSyB-EXAMPLEAPIKEY12345ABCDE67890"

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_street_view", methods=["POST"])
def get_street_view():
    # Get form data
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    heading = request.form.get("heading", 0)  # Default to 0 if not provided
    pitch = request.form.get("pitch", 0)     # Default to 0 if not provided
    fov = request.form.get("fov", 90)        # Default to 90 if not provided

    # Base URL for Google Maps Street View API
    base_url = "https://maps.googleapis.com/maps/api/streetview"
    params = {
        "size": "600x400",
        "location": f"{latitude},{longitude}",
        "heading": heading,
        "pitch": pitch,
        "fov": fov,
        "key": API_KEY
    }

    # Fetch the Street View image
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        # Save the image
        image_path = "static/street_view_image.jpg"
        with open(image_path, "wb") as file:
            file.write(response.content)
        return render_template("index.html", image_url=image_path)
    else:
        error_message = f"Failed to fetch Street View image. HTTP Status Code: {response.status_code}"
        return render_template("index.html", error=error_message)

if __name__ == "__main__":
    app.run(debug=True)
