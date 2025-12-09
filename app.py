# app.py
import os
import tempfile
import shutil
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

MAX_CODE_LENGTH = 5000
TIMEOUT_SECONDS = 10
OUTPUT_LIMIT = 20000

# Supported languages
LANG_IMAGES = {
    "python": "python:3.11-slim",
    "js": "node:20-slim"
}


def indent(code):
    return "\n".join("    " + line for line in code.splitlines())


def wrap_python(code):
    return f"""
import resource, sys
resource.setrlimit(resource.RLIMIT_AS, (128*1024*1024, 128*1024*1024))

try:
{indent(code)}
except MemoryError:
    print("MemoryError: Out of memory")
except Exception as e:
    print("RuntimeError:", e)
"""


def wrap_js(code):
    return f"""
try {{
{code}
}} catch (e) {{
    console.error("RuntimeError:", e);
}}
"""


def build_docker_cmd(workdir, lang):
    image = LANG_IMAGES[lang]

    cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "128m",
        "--cpus", "0.5",
        "--pids-limit", "64",
        "--read-only",
        "-v", f"{workdir}:/code:ro",
        image
    ]

    if lang == "python":
        cmd += ["python3", "/code/script.py"]
    else:
        cmd += ["node", "/code/script.js"]

    return cmd


@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json(force=True)
    lang = data.get("language", "python")
    code = data.get("code", "")

    if lang not in LANG_IMAGES:
        return jsonify({"error": "Invalid language"}), 400

    if not isinstance(code, str):
        return jsonify({"error": "Code must be a string"}), 400

    if len(code) > MAX_CODE_LENGTH:
        return jsonify({"error": "Code too long"}), 400

    tempdir = tempfile.mkdtemp(prefix="safe_exec_")

    try:
        filename = "script.py" if lang == "python" else "script.js"
        wrapper = wrap_python(code) if lang == "python" else wrap_js(code)

        script_path = os.path.join(tempdir, filename)
        with open(script_path, "w") as f:
            f.write(wrapper)

        cmd = build_docker_cmd(tempdir, lang)

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=TIMEOUT_SECONDS
            )
        except subprocess.TimeoutExpired:
            return jsonify({"output": "Execution timed out"}), 200

        output = (result.stdout + result.stderr).strip()
        if not output:
            output = "No output"

        if len(output) > OUTPUT_LIMIT:
            output = output[:OUTPUT_LIMIT] + "\n... truncated ..."

        return jsonify({"output": output})

    finally:
        shutil.rmtree(tempdir, ignore_errors=True)


@app.route("/")
def home():
    return open("static/index.html").read()


if __name__ == "__main__":
    print("Running Safe Code Executor at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000)
