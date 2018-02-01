import subprocess

command = ['sudo', 'docker', 'run', '-P', 'lowerquality/gentle']

subprocess.call(command)
