from flask import Flask, jsonify, render_template
import subprocess
import sys
import os

app = Flask(__name__)

# This is the Python executable running Flask (venv python)
PYTHON_EXE = sys.executable

@app.route("/")
def home():
    return render_template("run.html")

@app.route("/run-test", methods=["POST"])
def run_test():
    try:
        p = subprocess.Popen(
            [PYTHON_EXE, "-u", "main.py"],   # run blink script using SAME python
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=os.getcwd()
        )

        bpm = None
        status = None

        while True:
            line = p.stdout.readline()
            if not line:
                break

            print("PY:", line.strip())

            if line.startswith("RESULT:"):
                data = line.replace("RESULT:", "").strip()
                bpm, status = data.split(",")
                break

        p.wait()

        if bpm is None:
            err = p.stderr.read()
            print("ERR:", err)
            return jsonify({"error": "No result received from blink script"})

        return jsonify({"bpm": bpm, "status": status})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
