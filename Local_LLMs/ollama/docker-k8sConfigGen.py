import ollama

# Allowed programming languages for Dockerfile generation
ALLOWED_LANGUAGES = ["python", "java", "golang", "javascript"]

# Allowed Kubernetes objects
K8S_OBJECTS = ["pod", "deployment", "service", "configmap", "secret", "hpa"]

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

    print(f"\nDockerfile for {language} generated successfully: {filename}")
    print("=" * 40)
    print(dockerfile_content)

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

    print(f"\nKubernetes YAML for {k8s_object} generated successfully: {filename}")
    print("=" * 40)
    print(yaml_content)

if __name__ == "__main__":
    while True:
        choice = input("Do you want to generate a Dockerfile or a Kubernetes YAML? (dockerfile/k8s): ").strip().lower()

        if choice == "dockerfile":
            user_input = input(f"Enter a language ({', '.join(ALLOWED_LANGUAGES)}): ").strip().lower()
            if user_input in ALLOWED_LANGUAGES:
                generate_dockerfile(user_input)
                break
            else:
                print(f"Invalid choice! Please select from {ALLOWED_LANGUAGES}.")

        elif choice == "k8s":
            k8s_object = input(f"Enter the Kubernetes object ({', '.join(K8S_OBJECTS)}): ").strip().lower()
            if k8s_object in K8S_OBJECTS:
                app_name = input("Enter the application name: ").strip().lower()
                generate_k8s_yaml(k8s_object, app_name)
                break
            else:
                print(f"Invalid choice! Please select from {K8S_OBJECTS}.")

        else:
            print("Invalid choice! Please enter 'dockerfile' or 'k8s'.")
