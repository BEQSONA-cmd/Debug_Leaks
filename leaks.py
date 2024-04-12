import subprocess
import os
import time
import sys
import re

BLUE = '\033[94m'
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

def usleep(mlsec):
    sec = mlsec / 1000000.0
    time.sleep(sec)

def wait_for_input(place, i):
    try:
        if i == 0:
            input(f"Create Leak here {BLUE}➡" + place + f"{BLUE}⬅{RESET}")
        else:
            input(f"Using here {BLUE}➡" + place + f"{BLUE}⬅{RESET}")
    except KeyboardInterrupt:
        sys.exit(1)
        
def check_if_segfault(program_name, *args):
    cmd = f'./{program_name} {" ".join(args)}'
    expected = "Segmentation fault"
    
    try:
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except KeyboardInterrupt:
        sys.exit(1)
    segfault = r.stderr.strip()

    if expected in segfault:
        return True
    else:
        return False

def check_leaks(program_name, *args):
    i = 0
    j = 1
    l = 0
    condi = 0
    if not os.path.isfile(program_name):
        print(f"{RED}[{program_name} not found ]{RESET}")
        sys.exit(1)
    print(f"{BLUE}=== Leaks Debugger ==={RESET}")


    cmd = f'valgrind --leak-check=full ./{program_name} {" ".join(args)}'
    rm_cmd = 'rm -f file3'
    expected = "0 errors from 0 contexts"

    if(check_if_segfault(program_name, *args)):
        print(f"{RED}[SEGFAULT]{RESET}")
        l = 1

    try:
        r = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except KeyboardInterrupt:
        sys.exit(1)

    leaks = r.stderr.strip().split('\n')
    l_s = leaks[-1]
    if(l == 1):
        l_l = "Segmentation fault"
    else:
        l_l = l_s.split("ERROR SUMMARY: ")[1]
    
    if l_l.startswith(expected):
        print(f"{GREEN}[MOK]{RESET}")
    else:
        print(f"{RED}[KO LEAKS]{RESET}")
        for line in leaks:
            parts = line.split()
            if "Conditional" in parts:
                condi = 1
            if "at" in parts:
                leak_in_func = parts[3]
                if(condi == 1):
                    print(f"{RED}uninitialised value in: {leak_in_func}(){RESET}")
                    wait_for_input(parts[4], 1)
                    condi = 0
                else:
                    condi = 2
            if "by" in parts and condi == 2:
                leak_func = parts[3]
                leak_place = parts[4]
                if(parts[3] != "2002-2017,"):
                    if(leak_in_func != "malloc" and leak_func != "main"):
                        i += 1
                    else:
                        if(i == 0):
                            print(f"{RED}Leak number:[{j}]{RESET}")
                        print(f"{RED}Leak from: {leak_func}(){RESET}")
                        wait_for_input(leak_place, i)
                        i += 1
                        if(leak_func == "main"):
                            i = 0
                            j += 1
        
def check_leaks_endles_program(program_name, *args):
    i = 0
    j = 1
    l = 0
    condi = 0
    if not os.path.isfile(program_name):
        print(f"{RED}[{program_name} not found ]{RESET}")
        sys.exit(1)
    print(f"{BLUE}=== Leaks Debugger ==={RESET}")

    cmd = f'valgrind --leak-check=full ./{program_name} {" ".join(args)}'
    expected = "0 errors from 0 contexts"

    try:
        r = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        while True:
            time.sleep(1)
            if r.poll() is not None:
                r.terminate()
                break
    except KeyboardInterrupt:
        r.terminate()

    leaks = r.stderr.read().strip().split('\n')
    l_s = leaks[-1]
    l_l = l_s.split("ERROR SUMMARY: ")[1]
    
    if l_l.startswith(expected):
        print(f"{GREEN}[MOK]{RESET}")
    else:
        print(f"{RED}[KO LEAKS]{RESET}")
        for line in leaks:
            parts = line.split()
            if "Conditional" in parts:
                condi = 1
            if "at" in parts:
                leak_in_func = parts[3]
                if(condi == 1):
                    print(f"{RED}uninitialised value in: {leak_in_func}(){RESET}")
                    wait_for_input(parts[4], 1)
                    condi = 0
                else:
                    condi = 2
            if "by" in parts and condi == 2:
                leak_func = parts[3]
                leak_place = parts[4]
                if(parts[3] != "2002-2017,"):
                    if(leak_in_func != "malloc" and leak_func != "main"):
                        i += 1
                    else:
                        if(i == 0):
                            print(f"{RED}Leak number:[{j}]{RESET}")
                        print(f"{RED}Leak from: {leak_func}(){RESET}")
                        wait_for_input(leak_place, i)
                        i += 1
                        if(leak_func == "main"):
                            i = 0
                            j += 1

def main():
    if len(sys.argv) < 2:
        print("dl Usage: dl ./Program Name (with/without arguments)")
        sys.exit(1)

    if(sys.argv[1] != "-e"):
        program_name = sys.argv[1]
        args = sys.argv[2:]
        check_leaks(program_name, *args)
    if(sys.argv[1] == "-e"):
        program_name = sys.argv[2]
        args = sys.argv[3:]
        check_leaks_endles_program(program_name, *args)
    
if __name__ == "__main__":
    main()
