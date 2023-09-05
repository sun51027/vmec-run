import os
import shutil
import subprocess

# Define the ranges for PRES_SCALE
press_range = [i * 100 for i in range(1, 10)]

# Define the input file name
input_file_name = "input.first_init.vmec"

# Define the output directory
output_dir = "output/"
subdirectories = ["dcon", "threed1","mercier","wout","jxbout"]

try:
    os.makedirs(output_dir, exist_ok=True)
    for subdirectory in subdirectories:
        os.makedirs(os.path.join(output_dir, subdirectory), exist_ok=True)
except OSError as e:
    print("Error creating directories:", e)

# Loop through parameter combinations and generate input files
for press in press_range:
    # Create a modified input file name
    new_input_file_name = "input.pres_{}.vmec".format(press)

    print("Generating and running {}...".format(new_input_file_name))

    # Copy the original input file to the modified name
    shutil.copy(input_file_name, new_input_file_name)

    # Modify the content of the copied input file
    with open(new_input_file_name, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if "PRES_SCALE" in line:
                line = "PRES_SCALE = {}\n".format(press)
            f.write(line)
        f.truncate()

    output_cmd = "./xvmec {} > tmp.txt".format(new_input_file_name)

    print("Running:", output_cmd)
        
    subprocess.run(output_cmd, shell=True)

    # Create distinct output file names
    file_names = {
        "dcon": "dcon_pres_{}.vmec.txt".format( press),
        "threed1": "threed1.pres_{}.vmec".format( press),
        "wout": "wout_pres_{}.vmec.nc".format( press),
        "jxbout": "jxbout_pres_{}.vmec.nc".format( press),
        "mercier": "mercier.pres_{}.vmec".format( press)
    }

    # Move output files to appropriate directories with distinct names
    for key, file_name in file_names.items():
        source_file = "{}*".format(key)
        #print(source_file)
        target_path = "{}/{}/".format(output_dir, key)
        #print(target_path)
        subprocess.run("mv {} {}".format(source_file,target_path),shell=True)

    subprocess.run("mv {} input".format(new_input_file_name),shell=True)

print("Script execution completed.")

