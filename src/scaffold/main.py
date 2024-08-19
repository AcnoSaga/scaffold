import os
import subprocess
import argparse
import json
import shutil

def load_config():
    config_path = os.path.expanduser('~/.scaffold_config.json')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return json.load(f)
    return {}

def save_config(config):
    config_path = os.path.expanduser('~/.scaffold_config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)

def get_template_path(project_type):
    return os.path.join(os.path.dirname(__file__), 'templates', project_type)

def copy_to_container(container_name, source_path, dest_path):
    subprocess.run(['docker', 'cp', source_path, f"{container_name}:{dest_path}"], check=True)

def run_command(command, check=True):
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        print(f"Command '{' '.join(command)}' executed successfully.")
        print(f"Output: {result.stdout}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{' '.join(command)}':")
        print(f"Exit code: {e.returncode}")
        print(f"Output: {e.output}")
        print(f"Error: {e.stderr}")
        raise

def create_project(project_type, project_name, directory):
    # Create project directory
    project_path = os.path.abspath(os.path.expanduser(os.path.join(directory, project_name)))
    os.makedirs(project_path, exist_ok=True)

    template_path = get_template_path(project_type)

    # Copy all files from the template directory to the project directory
    for item in os.listdir(template_path):
        s = os.path.join(template_path, item)
        d = os.path.join(project_path, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy2(s, d)

    # Build Docker image
    image_name = f"{project_name.lower()}-dev:latest"
    subprocess.run(['docker', 'build', '-t', image_name, project_path], check=True)

    # Run Docker container
    container_name = f"{project_name.lower()}-container"
    subprocess.run(['docker', 'run', '-d', '--name', container_name, image_name], check=True)

    # Copy all files from the project directory to the container
    for item in os.listdir(project_path):
        item_path = os.path.join(project_path, item)
        if os.path.isfile(item_path):
            copy_to_container(container_name, item_path, '/usr/src/app/')
        elif os.path.isdir(item_path):
            # For directories, we need to create them first in the container
            # subprocess.run(['docker', 'exec', container_name, 'mkdir', '-p', f'/usr/src/app/{item}'], check=True)
            copy_to_container(container_name, item_path, f'/usr/src/app/{item}')

    print(f"Project '{project_name}' has been created and Docker container is running.")
    print(f"Container name: {container_name}")
    print(f"To enter the container, run: docker exec -it {container_name} /bin/bash")
    print(f"To stop the container, run: docker stop {container_name}")
    print(f"To start the container again, run: docker start {container_name}")

def main():
    parser = argparse.ArgumentParser(description="A CLI tool to setup developer environment hosted on Docker locally.")
    parser.add_argument('--directory', help='Project directory')
    parser.add_argument('--type', help='Project type')
    parser.add_argument('--name', help='Project name')
    args = parser.parse_args()

    config = load_config()

    if args.directory:
        config['last_directory'] = args.directory
        save_config(config)
    
    directory = args.directory or config.get('last_directory') or input("Enter project directory: ")
    project_type = args.type or input("Enter project type (e.g., node, python, fastapi): ")
    project_name = args.name or input("Enter project name: ")

    create_project(project_type, project_name, directory)

if __name__ == "__main__":
    main()