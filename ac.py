import subprocess

def send_command(command):
  subprocess.run(["irsend", "send_once", "mitsubishi", command])
