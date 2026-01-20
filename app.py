from flask import Flask, jsonify, render_template
import subprocess

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("run.html")

@app.route("/run-test", methods=["POST"])
def run_test():
    try:
        p = subprocess.Popen(
            ["python", "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        bpm = None
        status = None

        while True:
            line = p.stdout.readline()
            if not line:
                break

            print("PY:", line.strip())  # debug in terminal

            if line.startswith("RESULT:"):
                data = line.replace("RESULT:", "").strip()
                bpm, status = data.split(",")
                break

        p.wait()

        if bpm is None:
            return jsonify({"error": "No result received from blink script"})

        return jsonify({"bpm": bpm, "status": status})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)

