from flask import Flask, request, jsonify, render_template
import ollama

app = Flask(__name__)

# Allowed languages for Dockerfile generation
ALLOWED_LANGUAGES = ["python", "java", "golang", "javascript", "php", "typescript"]

# Allowed Kubernetes objects
ALLOWED_K8S_OBJECTS = ["pod", "deployment", "service", "configmap", "secret", "hpa", "pvc", "pv", "daemonset", "podDisruptionBudget", "podSecurityPolicy"]

# Function to generate Dockerfile using Ollama
def generate_dockerfile(language):
    prompt = f"""
    Generate a secure, optimized Dockerfile for a {language} application.
    Ensure it follows best practices such as:
    - Multi-stage builds (if applicable)
    - Using a non-root user for security
    - Minimal base images
    - Caching layers efficiently
    Provide only the Dockerfile content.
    """
    response = ollama.chat(model='llama3:8b', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

# Function to generate Kubernetes YAML using Ollama
def generate_k8s_yaml(k8s_object, app_name):
    prompt = f"""
    Generate a Kubernetes {k8s_object} YAML for an application named {app_name}.
    Ensure it follows best practices, security, and scalability guidelines.
    Provide only the YAML content.
    """
    response = ollama.chat(model='llama3:8b', messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate/dockerfile', methods=['POST'])
def dockerfile_endpoint():
    data = request.json
    language = data.get("language")

    if language not in ALLOWED_LANGUAGES:
        return jsonify({"error": "Invalid language! Choose from: " + ", ".join(ALLOWED_LANGUAGES)}), 400

    dockerfile_content = generate_dockerfile(language)
    return jsonify({"message": f"Dockerfile for {language} generated successfully.", "content": dockerfile_content})

@app.route('/generate/k8s', methods=['POST'])
def k8s_endpoint():
    data = request.json
    k8s_object = data.get("k8s_object")
    app_name = data.get("app_name")

    if k8s_object not in ALLOWED_K8S_OBJECTS:
        return jsonify({"error": "Invalid Kubernetes object! Choose from: " + ", ".join(ALLOWED_K8S_OBJECTS)}), 400

    yaml_content = generate_k8s_yaml(k8s_object, app_name)
    return jsonify({"message": f"Kubernetes YAML for {k8s_object} generated successfully.", "content": yaml_content})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  #allowing external access to the flask app and listening on all interfaces
