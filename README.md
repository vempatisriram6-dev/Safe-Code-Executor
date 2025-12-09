# Safe-Code-Executor
 
- Safe Code Executor is a minimal, production-minded sandbox that executes short user-submitted code safely inside Docker containers.
 
- It enforces resource caps (memory, CPU, PIDs), blocks networking, mounts user code read-only, and enforces timeouts so that malicious or buggy code cannot crash your host. The service supports Python and JavaScript (Node.js) and includes a simple web UI.

### use cases

- Teaching sandboxing and container security

- Building a tiny "run code" feature for a learning site

- Experimenting with isolation and resource limits

# Features

- Runs Python code in isolated containers
- Memory limit: 128MB
- CPU limit: 0.5 cores
- Network disabled
- Timeout for infinite loops
- Read-only filesystem (optional)
- Clear error messages

# Repository layout
```text
safe-code-executor/
├── app.py                 # Flask backend (Python + Node support)
├── requirements.txt       # Python deps (Flask)
├── static/
│   └── index.html         # Simple frontend UI
├── .gitignore
└── README.md
```
# STEP 1 — Create & activate virtual environment (Linux / WSL)
```text

python3 -m venv venv

```
### Activate it
```
source venv/bin/activate

```
# STEP 2 — pip install -r requirements.txt

```
pip install -r requirements.txt

```
# STEP 3 — Start Docker Desktop (Windows)

```
docker ps
```
# STEP 4 — Run the server

```
python3 app.py

```
# STEP 5 — Testing the API

### Test 1: Normal Code

```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"print(\"Hello World\")"}'

```
### Test 2: Loop Attack

```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"while True: pass"}'
```
### Test 3: Memory Attack

```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"x = \"a\" * 1000000000"}'
```
### Test 4: Network Attack

 ```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\":\"import requests; print(requests.get('http://google.com'))\"}"
```
# STEP 6 — Docker Security Experiments

### Experiment 1
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"print(open('/etc/passwd').read())\"}"

```
### Experiment 2
```
curl -X POST http://127.0.0.1:5000/run \
  -H "Content-Type: application/json" \
  -d "{\"code\": \"open('/app/script.py', 'w').write('hacked')\"}"
```





