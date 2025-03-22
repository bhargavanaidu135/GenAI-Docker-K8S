from flask import Flask, request, jsonify
import ollama

app = Flask(__name__)

# Allowed programming languages for Dockerfile generation
ALLOWED_LANGUAGES = ["python", "java", "golang", "javascript", "php", "typescript"]

# Allowed Kubernetes objects
K8S_OBJECTS = ["pod", "deployment", "service", "configmap", "secret", "hpa", "pvc", "pv", "daemonset", "pdb", "psp"]

def generate_dockerfile(language):
    """Generates a secure Dockerfile using Ollama LLM for the selected language."""
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

    dockerfile_content = response['message']['content']

    # Save the Dockerfile
    filename = f"Dockerfile.{language.lower()}"
    with open(filename, "w") as file:
        file.write(dockerfile_content)

    return {
        "message": f"Dockerfile for {language} generated successfully.",
        "filename": filename,
        "content": dockerfile_content
    }

def generate_k8s_yaml(k8s_object, app_name):
    """Generates a Kubernetes YAML file for the specified object type."""
    prompt = f"""
    Generate a Kubernetes YAML configuration for a {k8s_object} named {app_name}.
    Ensure it follows best practices such as:
    - Proper labels and selectors
    - Secure and minimal configurations
    - Best practices for high availability (if applicable)
    Provide only the YAML content.
    """

    response = ollama.chat(model='llama3:8b', messages=[{"role": "user", "content": prompt}])

    yaml_content = response['message']['content']

    # Save the YAML file
    filename = f"{app_name}-{k8s_object}.yaml"
    with open(filename, "w") as file:
        file.write(yaml_content)

    return {
        "message": f"Kubernetes YAML for {k8s_object} generated successfully.",
        "filename": filename,
        "content": yaml_content
    }

@app.route('/generate/dockerfile', methods=['POST'])
def dockerfile_api():
    """API Endpoint to generate Dockerfile"""
    data = request.json
    language = data.get("language", "").lower()

    if language not in ALLOWED_LANGUAGES:
        return jsonify({"error": f"Invalid language! Choose from {ALLOWED_LANGUAGES}"}), 400

    result = generate_dockerfile(language)
    return jsonify(result)

@app.route('/generate/k8s', methods=['POST'])
def k8s_api():
    """API Endpoint to generate Kubernetes YAML"""
    data = request.json
    k8s_object = data.get("k8s_object", "").lower()
    app_name = data.get("app_name", "").lower()

    if k8s_object not in K8S_OBJECTS:
        return jsonify({"error": f"Invalid Kubernetes object! Choose from {K8S_OBJECTS}"}), 400
    if not app_name:
        return jsonify({"error": "Application name is required!"}), 400

    result = generate_k8s_yaml(k8s_object, app_name)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
