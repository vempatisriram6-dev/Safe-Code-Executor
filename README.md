# Safe-Code-Executor
 
 - A minimal, production-minded sandbox for executing untrusted code safely using Docker.
   
# Overview 

Safe Code Executor is a lightweight sandbox service that executes user-submitted Python or JavaScript code inside isolated Docker containers with strict security controls:

- CPU, memory & PID limits

- Disabled networking

- Forced execution timeouts

- Read-only filesystem (optional)

- Clear API responses for both success & errors
  
### This project is perfect for

- Learning container security

- Building a “run code” feature for tutorials

- Experimenting with Docker isolation

- Teaching students about sandboxing
  
### use cases

- Teaching sandboxing and container security

- Building a tiny "run code" feature for a learning site

- Experimenting with isolation and resource limits

# Architecture Overview
```
User → Flask API → Docker Sandbox Container → Code Output
```
✓ Each execution runs in a fresh disposable container with strong isolation:

- No internet

- Max 128MB memory

- Max 0.5 CPU

- Killed after timeout

- Optional read-only filesystem

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
# Step 4 — Build the secure Docker runner image

```
docker build -t python-runner-image -f Dockerfile.runner .

```

# STEP 5 — Run the server

```
python3 app.py

```
# STEP 6 — Testing the API

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
# STEP 7 — Docker Security Experiments

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
# Key Learning Outcomes
✓ Docker isolates processes but does not prevent reading container files

✓ Memory & CPU limits work reliably

✓ Network can be fully disabled

✓ Infinite loops must be handled manually with a timeout

✓ --read-only prevents file modifications inside the container

✓ Docker containers safely protect your host machine

# Conclusion

Safe Code Executor is a practical, real-world sandbox project that teaches:

- Docker’s security boundaries

- How to safely run untrusted code

- API + container orchestration

- Resource and filesystem isolation

✓ It's a perfect stepping stone toward container security, DevOps, hacking defense, and backend engineering.





