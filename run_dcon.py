import os
import re
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
	- One should change target_directory and dcon_dir to correct path.
Usage:
	python run_dcon.py -h (to check all commands)
	python run_dcon.py -d -i input.first_init.vmec (to list jobs) 
	python run_dcon.py 
	python run_dcon.py 2>/dev/null (without showing system note)
	 
'''

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dryRun', help='do not execute the script', action='store_true')
args = parser.parse_args()

# Get the current directory
current_dir = os.getcwd()

# path to be defined maunally
target_directory = "{}/output/curr_2p/dcon/".format(current_dir)
dcon_dir = "/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"

# path of input and output files
dcon_output = "{}/dcon_output.txt".format(current_dir)
dcon_equil_in = "{}/equil.in".format(dcon_dir)
dcon_in= "{}/dcon.in".format(dcon_dir)
dcon_stable_case_txt = "{}/dcon_stable_case.txt".format(current_dir)

## for local test
# dcon_equil_in = "{}/test.in".format(current_dir)
# dcon_dir = current_dir
# target_directory = "{}/testdcon".format(current_dir)

# Remove the dcon_output.txt and dcon_stable_case.txt if they exist
if os.path.exists(dcon_output):
    os.remove(dcon_output)

if os.path.exists(dcon_stable_case_txt):
    os.remove(dcon_stable_case_txt)

###############################################
#					
#	Functions
#
###############################################

def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command,shell=True)

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
    command = "./dcon > {}".format(dcon_output)
    exe(command)

def check_stable(nn):
    if args.dryRun:
       print("check stable for equilibria: {}".format(equil_file))
    else:
       with open(dcon_output, "r") as dcon_output_file:
           output_contents = dcon_output_file.read()
       if "Zero" in output_contents or "unstable" in output_contents or "NaN" in output_contents:
          print("......... unstable case in nn = {} mode, skipped ".format(nn))
          return False
       else: 
          print("......... STABLE case in nn = {} mode".format(nn))
          with open(dcon_stable_case_txt, "a") as stable_case_file:
               stable_case_file.write(os.path.realpath(equil_file) + " in nn = {} mode\n".format(nn))
          return True


def check_q_factor(nn):
    with open(dcon_output, "r") as dcon_output_file:
        lines = dcon_output_file.readlines()
        for index,line in enumerate(lines):
            match = re.search(r'qmin\s*=\s*([\d.E+-]+)', line)
            if match:
               qmin_str = match.group(1)  # Extract the qmin string
               qmin = float(qmin_str)    # Convert the qmin string to a float
               if qmin < 1:
                  print("......qmin: {} < 1, discard it".format(qmin))
                  return False
               else: 
                  print("......qmin: {} > 1 is found in nn={} mode, then check stability in nn=1~5".format(qmin,nn))
                  return True

               break
    
###############################################

if __name__=="__main__":
    
    os.chdir(dcon_dir)
    for root, _, files in os.walk(target_directory):
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
                    for i in range(2,6):
                        replace_nn_mode(i)
                        run_dcon()
                        check_stable(i)


    # Change back to the original directory
    os.chdir(current_dir)

