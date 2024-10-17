import os
import subprocess
import time

def start_docker_desktop():
    """Open Docker Desktop."""
    try:
        subprocess.Popen(['start', 'docker'], shell=True)
        print("Docker Desktop started.")
    except Exception as e:
        print("Error starting Docker Desktop:", e)

def start_sonarqube_container():
    """Start the SonarQube container."""
    try:
        result = subprocess.run(
            ['docker', 'inspect', '-f', '{{.State.Status}}', 'sonarqube'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            status = result.stdout.strip()
            if status == 'running':
                print("SonarQube container is already running.")
        else:
            # If the container does not exist, run a new one
            subprocess.run([
                'docker', 'run', '-d', '--name', 'sonarqube',
                '-p', '9000:9000', 'sonarqube'
            ], check=True)
            print("SonarQube container created and started successfully.")

    except subprocess.CalledProcessError as e:
        print("Error starting SonarQube container:", e)

def start_agent():
    """Start the agent in a new terminal."""
    try:
        subprocess.Popen(["cmd", "/c", "start", "cmd.exe", "/k", "run.cmd"], cwd=r"C:\myagent")
        print("Agent started successfully in a new terminal.")
    except Exception as e:
        print("Error starting agent:", e)

def main():
    # Start Docker Desktop
    start_docker_desktop()
    
    # Wait for a bit to ensure Docker is up and running
    time.sleep(20)

    # Start SonarQube container
    start_sonarqube_container()

    # Start the agent in a new terminal
    start_agent()

if __name__ == "__main__":
    main()
