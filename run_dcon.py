import os
import re
import shutil
import argparse
import subprocess
import warnings

# Mute all warnings
warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dryRun', help='do not submit jobs', action='store_true')
args = parser.parse_args()

# Get the current directory
current_dir = os.getcwd()
target_directory = "{}/output/curr_2p/dcon/".format(current_dir)
dcon_dir = "/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"
dcon_output = "{}/dcon_output.txt".format(current_dir)
dcon_equil_in = "{}/equil.in".format(dcon_dir)
dcon_in= "{}/dcon.in".format(dcon_dir)
equil_file_list=[]

# for local test
#dcon_equil_in = "{}/test.in".format(current_dir)
#dcon_dir = current_dir
#target_directory = "{}/testdcon".format(current_dir)

# Remove the dcon_output.txt and dcon_stable_case.txt if they exist
if os.path.exists(dcon_output):
    os.remove(dcon_output)

dcon_stable_case_txt = os.path.join(current_dir, "dcon_stable_case.txt")
if os.path.exists(dcon_stable_case_txt):
    os.remove(dcon_stable_case_txt)

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

def check_nn_mode(new_nn):
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
       if "Zero" in output_contents or "unstable" in output_contents:
          print("....... unstable case, skipped.\n")
       else: 
          print("....... STABLE case, check qmin:\n")
          with open(dcon_output, "r") as dcon_output_file:
             lines = dcon_output_file.readlines()
             for index,line in enumerate(lines):
                 if 'qmin' not in line:
                    continue
                 check_q_factor(line,nn)


def check_q_factor(line,nn):
    match = re.search(r'qmin\s*=\s*([\d.E+-]+)', line)

    if match:
       qmin_str = match.group(1)  # Extract the qmin string
       qmin = float(qmin_str)    # Convert the qmin string to a float
       if qmin < 1:
          print("         qmin: {} < 1, discard it\n".format(qmin))
       else: 
          print("         qmin: {} > 1 is found in n={} mode, preserve it\n".format(qmin,nn))
          #print("STABLE case is found in {}".format(equil_file))
          with open(dcon_stable_case_txt, "a") as stable_case_file:
               stable_case_file.write(os.path.realpath(equil_file) + " with {} mode\n".format(nn))

    

if __name__=="__main__":
    
    os.chdir(dcon_dir)
    for root, _, files in os.walk(target_directory):
        for file in files:
            equil_file = os.path.join(root, file)
            print("Running {}".format(equil_file))
            replace_equilfile(equil_file)
            for i in range(1,6):
                check_nn_mode(i)
                run_dcon()
                check_stable(i)

    # Change back to the original directory
    os.chdir(current_dir)

