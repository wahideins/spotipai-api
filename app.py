from flask import Flask, jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    r = requests.post(url, data=data)
    return r.json().get("access_token")

@app.route("/spotify/current")
def current_song():
    token = get_access_token()
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers=headers
    )

    if r.status_code == 204:
        return jsonify({"status": "paused"})

    if r.status_code != 200:
        return jsonify({"status": "error", "code": r.status_code})

    data = r.json()

    return jsonify({
        "status": "playing",
        "song": data["item"]["name"],
        "artist": data["item"]["artists"][0]["name"],
        "playing": data["is_playing"]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
