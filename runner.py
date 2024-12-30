from subprocess import Popen

for script in ["simple_server.py", "simple_client.py"]:
    Popen(["start", "cmd", "/k", "python", script], shell=True)
    
    