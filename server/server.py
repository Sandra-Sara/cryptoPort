from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
from datetime import datetime
import json

app = Flask(__name__)

# ----------------------------------------------------
# DIRECTORIES
# ----------------------------------------------------
DATA_DIR = "server_data"
RECEIVED_DIR = os.path.join(DATA_DIR, "received")
HISTORY_DIR = os.path.join(DATA_DIR, "history")

os.makedirs(RECEIVED_DIR, exist_ok=True)
os.makedirs(HISTORY_DIR, exist_ok=True)


# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------
def sanitize_email(email):
    """
    Converts user email into filesystem-safe folder name.
    Example: sarafaria@gmail.com → sarafaria_at_gmail_com
    """
    return email.replace("@", "_at_").replace(".", "_")


def now_ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ----------------------------------------------------
# HISTORY UTILS
# ----------------------------------------------------
def history_file(email):
    safe_email = sanitize_email(email)
    return os.path.join(HISTORY_DIR, f"{safe_email}.json")


def load_user_history(email):
    safe_email = sanitize_email(email)
    path = history_file(email)
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_user_history(email, history_list):
    safe_email = sanitize_email(email)
    path = history_file(email)
    with open(path, "w") as f:
        json.dump(history_list, f, indent=4)


# ----------------------------------------------------
# TEST ROUTE
# ----------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "CryptPort Flask Server Running"}), 200


# ----------------------------------------------------
# 1️⃣ FILE UPLOAD
# ----------------------------------------------------
@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    receiver = request.form.get("receiver")
    sender = request.form.get("sender")

    if not receiver:
        return jsonify({"error": "Missing receiver"}), 400

    # Safe folder name
    safe_receiver = sanitize_email(receiver)
    receiver_dir = os.path.join(RECEIVED_DIR, safe_receiver)
    os.makedirs(receiver_dir, exist_ok=True)

    file_id = str(uuid.uuid4())
    filename = secure_filename(file.filename)
    stored_as = f"{file_id}_{filename}"

    save_path = os.path.join(receiver_dir, stored_as)
    file.save(save_path)

    # Save history
    history = load_user_history(receiver)
    history.append({
        "timestamp": now_ts(),
        "action": "received file",
        "filename": filename,
        "stored_as": stored_as,
        "sender": sender
    })
    save_user_history(receiver, history)

    return jsonify({
        "status": "success",
        "file_id": file_id,
        "stored_as": stored_as,
        "original_filename": filename
    }), 200


# ----------------------------------------------------
# 2️⃣ LIST FILES
# ----------------------------------------------------
@app.route("/list/<receiver>", methods=["GET"])
def list_files(receiver):
    safe_receiver = sanitize_email(receiver)
    receiver_dir = os.path.join(RECEIVED_DIR, safe_receiver)

    if not os.path.exists(receiver_dir):
        return jsonify({"files": []})

    return jsonify({"files": os.listdir(receiver_dir)})


# ----------------------------------------------------
# 3️⃣ DOWNLOAD FILE
# ----------------------------------------------------
@app.route("/download/<receiver>/<filename>", methods=["GET"])
def download(receiver, filename):
    safe_receiver = sanitize_email(receiver)
    folder = os.path.join(RECEIVED_DIR, safe_receiver)

    file_path = os.path.join(folder, filename)
    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    # Add history log
    original_name = filename.split("_", 1)[-1]
    history = load_user_history(receiver)
    history.append({
        "timestamp": now_ts(),
        "action": "downloaded file",
        "filename": original_name,
        "stored_as": filename
    })
    save_user_history(receiver, history)

    return send_from_directory(folder, filename, as_attachment=True)


# ----------------------------------------------------
# 4️⃣ READ HISTORY
# ----------------------------------------------------
@app.route("/history/<email>", methods=["GET"])
def get_history(email):
    return jsonify(load_user_history(email))


# ----------------------------------------------------
# 5️⃣ CLEAR HISTORY
# ----------------------------------------------------
@app.route("/history/<email>/clear", methods=["DELETE"])
def delete_history(email):
    path = history_file(email)
    if os.path.exists(path):
        os.remove(path)
    return jsonify({"status": "cleared"})


# ----------------------------------------------------
# RUN SERVER
# ----------------------------------------------------
if __name__ == "__main__":
    print("🚀 CryptPort Flask Server running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
