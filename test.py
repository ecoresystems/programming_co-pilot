import subprocess,os,sys

def code_executor(cmd):
    os.environ['PYTHONUNBUFFERED'] = "1"
    proc = subprocess.Popen(cmd,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            )
    stdout, stderr = proc.communicate()

    return proc.returncode, stdout, stderr


if __name__ == "__main__":
    code, out, err = code_executor([sys.executable, 'main.py'])
    print(code)
    print(out.decode('utf-8'))
    # print(err)