#!/usr/bin/python 
import os
import re
import time
import shutil
import argparse
import subprocess

'''
Created by Shih Lin
Date: 2023/09/20
Status: temporary script, could be changed in the future

Description:
	- The script checks the stabiltiy of all equilibrium files under
	a specific directory from equil code.
	- It changes the inputs (eq_filename) in equil.in and loop nn=1 to 5 
	in dcon.in.
	- Once the equilibrium is confirmed to be stable in each mode
	and q > 1, the filename	will be writen into dcon_stable_case.txt.
Note:
	- I'm investigating how to save plots after ./xdraw dcon.
	- No way to check the Ideal, Resisitve and Balooning mode so far.
	- One should change equil_dir and dcon_dir to correct path.
Usage:
	python run_dcon.py -h (to check all commands)
	python run_dcon.py -d -i input.first_init.vmec (to list jobs) 
	python run_dcon.py 
	python run_dcon.py 2>/dev/null (without showing system note)
	 
'''

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dryRun', help='do not execute the script', action='store_true')
parser.add_argument("-t","--tag"   , help = "tags: profile type and scale", default = "unknown", type=str, required=True)

args = parser.parse_args()
tag  = args.tag
name = tag

current_dir = os.getcwd()
dcon_dir = "/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"
#name="curr_2p"
#name="curr_2p_gs_pres_10e3"

# path to be defined maunally
equil_dir = f'vmec'

# path of input and output files
dcon_output   = f"{dcon_dir}/dcon_output.txt"
dcon_equil_in = f"{dcon_dir}/equil.in"
dcon_in       = f"{dcon_dir}/dcon.in"
stable_result = f"{dcon_dir}/dcon_stable_{name}.txt"


# Remove the dcon_output.txt and dcon_stable_case.txt if they exist
if os.path.exists(dcon_output):
    os.remove(dcon_output)

#if os.path.exists(stable_result):
#    os.remove(stable_result)

###############################################
#					
#	Functions
#
###############################################

def exe(command):
    if args.dryRun:
        print(command)
    else:
        #subprocess.call(command,shell=True)
        start_time = time.time()
        time.sleep(0.1)  # Simulating some initial delay
    
        try:
            # Run the command with a timeout of 5 seconds
            subprocess.run(command, shell=True, check=True, timeout=5)
        except subprocess.TimeoutExpired:
            # Handle timeout
            print("Execution time exceeded 5 seconds. Terminating function...")
            return
        except subprocess.CalledProcessError as e:
            # Handle other exceptions, if any
            print(f"Error: {e}")
            return
    
        # Continue with the function's normal execution
        elapsed_time = time.time() - start_time
        print(f"dcon terminated normally in {elapsed_time:.2f} seconds.")


def move_equil_files():
    
    cmds = [f"rm -rf {equil_dir}",
            f"mkdir -p {equil_dir} ",
            f"cp -r {current_dir}/depo/output/{name}/dcon {dcon_dir}/{equil_dir}"
           ]
    for cmd in cmds:
        exe(cmd)

def replace_equilfile(files):
    if os.path.exists(dcon_equil_in):
        with open(dcon_equil_in, "r") as fin:
            contents = fin.readlines()
        for index, line in enumerate(contents):
            if not 'eq_filename=' in line:
                continue
            new_eq_filename = "\"{}\"".format(files)
            contents[index] = "        eq_filename={}\n".format(new_eq_filename)
            with open(dcon_equil_in, "w") as fin:
                 fin.writelines(contents)
            # print(contents[index])
    else:
        print("equil.in not found in {}".format(dcon_dir))

def replace_nn_mode(new_nn):
    with open(dcon_in, "r") as fin:
        contents = fin.readlines()
    for index, line in enumerate(contents):
        if not 'nn=' in line:
            continue
        contents[index] = "        nn={}\n".format(new_nn)
        with open(dcon_in, "w") as fin:
             fin.writelines(contents)

def run_dcon():
#    start_time = time.time()
#    time.sleep(0.1)

    command = "./dcon > {}".format(dcon_output)
    #command = "./dcon 2>&1 | tee {}".format(dcon_output)
    exe(command)
#    elapsed_time = time.time() - start_time
#    if elapsed_time > 1:
#        print("Execution time exceeded 5 seconds. Terminating function...")
#        return
#
#    # Continue with the function's normal execution
#    print("dcon terminated normal.")

def check_stable(nn):
    if args.dryRun:
       print("check stable for equilibria: {}".format(equil_file))
    else:
       with open(dcon_output, "r") as dcon_output_file:
           output_contents = dcon_output_file.read()
       if "Zero" in output_contents or "unstable" in output_contents or "NaN" in output_contents:
          print("\t\tunstable case in nn = {} mode, skipped ".format(nn))
          return False
       else: 
          print("\t\tSTABLE case in nn = {} mode".format(nn))
          if nn==2:
             with open(stable_result, "a") as result_file:
                  result_file.write(os.path.realpath(equil_file)+"\n")
          return True


def check_q_factor(nn):
    if not args.dryRun:
       with open(dcon_output, "r") as dcon_output_file:
           lines = dcon_output_file.readlines()
           for index,line in enumerate(lines):
               match = re.search(r'qmin\s*=\s*([\d.E+-]+)', line)
               if match:
                  qmin_str = match.group(1)  # Extract the qmin string
                  qmin = float(qmin_str)    # Convert the qmin string to a float
                  if qmin < 1:
                     print("\tqmin: {} < 1, discard it".format(qmin))
                     return False
                  else: 
                     print("\tqmin: {} > 1 is found in nn={} mode.".format(qmin,nn))
                     print("\tCheck stability in nn=1~5")
                     return True
   
                  break
    
def print_final_message():
    if args.dryRun:
        print("[INFO] this is the end of dryRun mode (print commands only)")
    else:
        print("[INFO] all jobs completed!")
###############################################

if __name__=="__main__":
    
    os.chdir(dcon_dir)
    move_equil_files()
    for root, _, files in os.walk(equil_dir):
        for file in files:
            equil_file = os.path.join(root, file)
            print("\nRunning {}".format(equil_file))
            '''
             0.  replace equil_file
             1.  run dcon in nn=1
             2.  during nn=1, check if qmin > 1, otherwise return false
             3.  check stability in nn=1
             4.  check stability in nn=2~5

            '''
            replace_equilfile(equil_file)
            replace_nn_mode(1)
            run_dcon()
            q_larger_1= check_q_factor(1)
            if not q_larger_1:
                continue
            else:
                stable = check_stable(1)
                if not stable:
                    continue
                else:
                    for i in range(2,3):
                        replace_nn_mode(i)
                        run_dcon()
                        check_stable(i)


    # Change back to the original directory
    os.chdir(current_dir)
    print_final_message()

