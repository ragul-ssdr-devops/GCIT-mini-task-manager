from flask import Flask, request, jsonify, render_template
from datetime import datetime
import uuid

app = Flask(__name__)

tasks = []
VALID_STATUS = ["pending", "in-progress", "completed"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data or not data["title"]:
        return jsonify({"error": "Title is required"}), 400

    task = {
        "id": str(uuid.uuid4()),
        "title": data["title"],
        "description": data.get("description", ""),
        "status": "pending",
        "created_at": datetime.utcnow().isoformat()
    }

    tasks.append(task)
    return jsonify(task), 201


@app.route("/tasks", methods=["GET"])
def list_tasks():
    status = request.args.get("status")

    if status:
        filtered = [t for t in tasks if t["status"] == status]
        return jsonify(filtered)

    return jsonify(tasks)


@app.route("/tasks/<task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()

    for task in tasks:
        if task["id"] == task_id:

            if "status" in data:
                if data["status"] not in VALID_STATUS:
                    return jsonify({"error": "Invalid status"}), 400
                task["status"] = data["status"]

            if "title" in data:
                task["title"] = data["title"]

            if "description" in data:
                task["description"] = data["description"]

            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks

    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return jsonify({"message": "Deleted"}), 200

    return jsonify({"error": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
