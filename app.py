from flask import Flask, render_template, request
import json
import subprocess
import tempfile
import os

app = Flask(__name__)


@app.route("/")
def home():
    return "Debug Detective is live"


@app.route("/case/1")
def case_one():
    with open("cases/case001.json", "r") as file:
        case = json.load(file)

    return render_template("case.html", case=case)


@app.route("/run", methods=["POST"])
def run_code():
    code = request.form.get("code", "")

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".py",
            delete=False
        ) as temp:
            temp.write(code)
            temp_path = temp.name

        result = subprocess.run(
            ["python", temp_path],
            capture_output=True,
            text=True,
            timeout=5
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        os.remove(temp_path)

        if error:
            return {
                "success": False,
                "output": error
            }

        expected = (
            "Processing: Rice\n"
            "Processing: Milk\n"
            "Processing: Sugar\n"
            "Processing: Tea\n"
            "Processing: Oil"
        )

        if output == expected:
            return {
                "success": True,
                "output": output,
                "message": "🎉 Correct! You fixed the bug!"
            }

        return {
            "success": False,
            "output": output,
            "message": "❌ The code runs, but the output is not correct."
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "⏱️ Code took too long to run."
        }

    except Exception as e:
        return {
            "success": False,
            "output": str(e)
        }


if __name__ == "__main__":
    app.run(debug=True)