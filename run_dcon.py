import os
import shutil
import argparse
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dryRun', help='do not submit jobs', action='store_true')
args = parser.parse_args()

# Get the current directory
current_dir = os.getcwd()
target_directory = "{}/output/curr_2p/dcon/".format(current_dir)
dcon_dir = "/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"
dcon_output = "{}/dcon_output.txt".format(current_dir)
dcon_input = "{}/test.in".format(dcon_dir)
equil_file_list=[]

# for local test
#dcon_input = "{}/test.in".format(current_dir)
#dcon_dir = current_dir
#target_directory = "{}/testdcon".format(current_dir)

# Remove the dcon_output.txt and dcon_stable_case.txt if they exist
if os.path.exists(dcon_output):
    os.remove(dcon_output)

dcon_stable_case_txt = os.path.join(current_dir, "dcon_stable_case.test.txt")
if os.path.exists(dcon_stable_case_txt):
    os.remove(dcon_stable_case_txt)

# Function to run dcon
def replace_equilfile():
    for files in equil_file_list:
        if os.path.exists(dcon_input):
            with open(dcon_input, "r") as fin:
                contents = fin.readlines()
            for index, line in enumerate(contents):
                if not 'eq_filename=' in line:
                    continue
                new_eq_filename = "\"{}\"".format(files)
                contents[index] = "        eq_filename={}\n".format(new_eq_filename)
                with open(dcon_input, "w") as fin:
                     fin.writelines(contents)
                run_dcon()
                check_stable()
                print(contents[index])
        else:
            print("equil.in not found in {}".format(dcon_dir))

def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command,shell=True)


def run_dcon():
    commands = ["cd {}".format(dcon_dir),
               "./dcon >> {}".format(dcon_output)
              ]
    for cmd in commands:
        exe(cmd)
    #subprocess.run([dcon_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dcon_dir)

def check_stable():
    if args.dryRun():
       print("check stable for equilibria: {}".format(equil_file))
    else:
        with open(dcon_output, "r") as dcon_output_file:
            output_contents = dcon_output_file.read()
   
        if "Zero" in output_contents or "unstable" in output_contents:
            print("unstable case is found in '{}'.".format(equil_file))
        else:
           print("'Zero' or 'unstable' is not found, then check q factor.")
           with open(os.path.join(current_dir, "dcon_stable_case.test.txt"), "a") as stable_case_file:
                stable_case_file.write(os.path.realpath(equil_file) + "\n")

def create_file_list():
    for root, _, files in os.walk(target_directory):
        for file in files:
            equil_file = os.path.join(root, file)
            equil_file_list.append(equil_file)


if __name__=="__main__":

    create_file_list()
    replace_equilfile()
    

# Change back to the original directory
    os.chdir(current_dir)

