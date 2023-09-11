import os
import shutil
import subprocess

# Define the ranges for MPOL and RBC values
am1_range = range(1,2)
am2_range = range(1,2)
am3_range = range(1,2)

# Define the input file name
input_file_name = "input.first_init.vmec"

# Define the output directory
output_dir = "output"
subdirectories = ["am"]

try:
    os.makedirs(output_dir, exist_ok=True)
    for subdirectory in subdirectories:
        os.makedirs(os.path.join(output_dir, subdirectory), exist_ok=True)
except OSError as e:
    print("Error creating directories:", e)

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through parameter combinations and generate input files
for am1 in am1_range:
    for am2 in am2_range:
        for am3 in am3_range:
            
          # Create a modified input file name
           new_input_file_name = "input.am_{}_{}_{}.vmec".format(am1,am2,am3)
           print("Generating and running {}...".format(new_input_file_name))
        
          # Copy the original input file to the modified name
           shutil.copy(input_file_name, new_input_file_name)

          # Modify the content of the copied input file
           with open(new_input_file_name, "r+") as f:
                lines = f.readlines()
                f.seek(0)
                for line in lines:
                  if "AM" in line:
                      # Split the line into individual values
                      values = lines[i].split("=")[1].strip().split(",")

                     # Check if there are enough values to replace
                     if len(values) == len(am_values):
                         # Replace each value with a value from the am_values list
                         for j in range(len(values)):
                             values[j] = str(am_values[j])
                         # Reconstruct the line
                         lines[i] = "AM = " + ", ".join(values) + "\n"
                f.truncate()

            output_cmd = "./xvmec {} > tmp.txt".format(new_input_file_name)

            print("Running:", output_cmd)
            
            subprocess.run(output_cmd, shell=True)

           # Create distinct output file names
           #file_names = {
           #    "dcon": "dcon_m{}_RBC{:.3f}.vmec.txt".format(mpol, rbc_value),
           #    "threed1": "threed1.m{}_RBC{:.3f}.vmec".format(mpol, rbc_value),
           #    "wout": "wout_m{}_RBC{:.3f}.vmec.nc".format(mpol, rbc_value),
           #    "jxbout": "jxbout_m{}_RBC{:.3f}.vmec.nc".format(mpol, rbc_value),
           #    "mercier": "mercier.m{}_RBC{:.3f}.vmec".format(mpol, rbc_value)
           #}

           ## Move output files to appropriate directories with distinct names
           #for key, file_name in file_names.items():
           #    source_file = "{}*".format(key)
           #    #print(source_file)
           #    target_path = "{}/{}/".format(output_dir, key)
           #    #print(target_path)
           #    subprocess.run("mv {} {}".format(source_file,target_path),shell=True)


print("Script execution completed.")

