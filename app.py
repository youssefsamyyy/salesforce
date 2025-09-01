import os
import pymysql
from flask import Flask, jsonify

app = Flask(__name__)

# Database connection info from environment variables
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "Cloud11@2025")
DB_NAME = os.getenv("DB_NAME", "testing")
INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME", "madina-432911:us-central1:salesforce-testing")

# Function to get a connection to Cloud SQL
def get_connection():
    unix_socket = f"/cloudsql/{INSTANCE_CONNECTION_NAME}"
    return pymysql.connect(
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        unix_socket=unix_socket,
        cursorclass=pymysql.cursors.DictCursor
    )

# Home route
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Welcome to Salesforce API",
        "available_endpoints": ["/Donations", "/Activities", "/health"]
    })

# Donations route
@app.route("/Donations", methods=["GET"])
def donations():
    query = """
        SELECT owneridname, new_donationamount, new_donationsourcename, new_donationstatusname
        FROM donations
        LIMIT 10
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        conn.close()
        if not results:
            return jsonify({"status": "No Data"})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Activities route
@app.route("/Activities", methods=["GET"])
def activities():
    query = """
        SELECT owneridname, actualstart, actualend
        FROM activities
        LIMIT 10
    """
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
        conn.close()
        if not results:
            return jsonify({"status": "No Data"})
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check route (for Cloud Run)
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

# Cloud Run requires listening on 0.0.0.0:$PORT
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
