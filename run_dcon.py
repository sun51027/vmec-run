import os
import shutil
import subprocess

# Get the current directory
current_dir = os.getcwd()
target_directory = "{}/output/curr_2p/dcon/".format(current_dir)
#target_directory = "/home/linshih/workspace/Stellarator-Tools/build/_deps/parvmec-build/output/curr_2p/dcon/"
dcon_dir = "/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"
dcon_output = "{}/dcon_output.txt".format(current_dir)
dcon_input = "{}/test.in".format(dcon_dir)

# Remove the dcon_output.txt and dcon_stable_case.txt if they exist
if os.path.exists(dcon_output):
    os.remove(dcon_output)

dcon_stable_case_txt = os.path.join(current_dir, "dcon_stable_case.test.txt")
if os.path.exists(dcon_stable_case_txt):
    os.remove(dcon_stable_case_txt)

# Function to run dcon
def replace_equilfile(eqil_file, dcon_output, current_dir, dcon_dir):
    if os.path.exists(dcon_input):
        with open(dcon_input, "r") as fin:
            contents = fin.readlines()
        for index, line in enumerate(contents):
            if not 'eq_filename=' in line:
                print(line)
                continue
            print(line)
            new_eq_filename = "\"{}\"".format(eqil_file)
            contents[index] = "        eq_filename={}\n".format(new_eq_filename)
            with open(dcon_input, "w") as fin:
                 fin.writelines(contents)
    else:
        print("equil.in not found in {}".format(dcon_dir))

def exe(command):
    if args.dryRun:
        print(command)
    else subprocess.call(command,shell=True)
#    dcon_command = os.path.join(dcon_dir, "dcon")
#    commands = ["cd {}".format(dcon_dir),
#               "./dcon >> {}".format(dcon_output)
#              ]
#    for cmd in commands:
#        subprocess.call(cmd,shell=True)
    #subprocess.run([dcon_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dcon_dir)

#    with open(dcon_output, "r") as dcon_output_file:
#        output_contents = dcon_output_file.read()
#
#    if "Zero" in output_contents or "unstable" in output_contents:
#        print("unstable case is found in '{}'.".format(eqil_file))
#    else:
#        print("'Zero' or 'unstable' is not found, then check q factor.")
#        with open(os.path.join(current_dir, "dcon_stable_case.test.txt"), "a") as stable_case_file:
#             stable_case_file.write(os.path.realpath(eqil_file) + "\n")


# Loop over all files in the target directory and run dcon
#file_list = []
#for f in os.listdir(target_directory):
#    if os.path.isfile(os.path.join(target_directory,f)):
#       equil_file = os.path.join(current_dir
#       replace_equilfile(f,dcon_output,current_dir,dcon_dir)


if __name__=="__main__":

    os.chdir(dcon_dir)
    for root, _, files in os.walk(target_directory):
        for file in files:
            eqil_file = os.path.join(root, file)
            replace_equilfile(eqil_file, dcon_output, current_dir, dcon_dir)

# Change back to the original directory
    os.chdir(current_dir)

