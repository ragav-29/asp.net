import os
import subprocess


def main():

    os.chdir(os.path.join("..","..","azagent"))
    print("changed directory to:", os.getcwd())

    try:
        subprocess.run(["cmd", "/c", "run.cmd"], check=True)
        print("Agent Started successfully.")
    except subprocess.CalledProcessError as e:
        print("Error starting agent :(", e)
        
if __name__=="__main__":
    main()
