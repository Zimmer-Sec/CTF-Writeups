import subprocess

pw_list = ["f09e", "4dcf", "87ab", "dba8", "752e", "3961", "f159"]

for guess in pw_list:
    proc = subprocess.Popen(
        ["python3", "lvl3_checker.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = proc.communicate(input=guess + "\n")

    print(f"Trying: {guess}")
    print(f"STDOUT: {stdout.strip()}")
    print(f"STDERR: {stderr.strip()}")
    print(f"Return Code: {proc.returncode}")
    print("-" * 40)
    if "pico" in stdout.strip():
        break
