from flask import Flask, send_from_directory

app = Flask(__name__, static_folder="frontend")

@app.route("/")
def serve_frontend():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0")
