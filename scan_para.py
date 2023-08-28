import os
import shutil
import subprocess

# Define the ranges for MPOL and RBC values
mpol_range = range(3, 5)
rbc_range = [i * 0.001 for i in range(10, 12)]

# Define the input file name
input_file_name = "input.test_FixBC.vmec"

# Define the output directory
output_dir = "output"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Loop through parameter combinations and generate input files
for mpol in mpol_range:
    for rbc_value in rbc_range:
        # Create a modified input file name
        new_input_file_name = "input.m{}_RBC{:.3f}.vmec".format(mpol, rbc_value)

        print("Generating and running {}...".format(new_input_file_name))

        # Copy the original input file to the modified name
        shutil.copy(input_file_name, new_input_file_name)

        # Modify the content of the copied input file
        with open(new_input_file_name, "r+") as f:
            lines = f.readlines()
            f.seek(0)
            for line in lines:
                if "MPOL" in line:
                    line = "MPOL = {}\n".format(mpol)
                elif "RBC(0,2)" in line:
                    line = "RBC(0,2) = {:.3f}\n".format(rbc_value)
                f.write(line)
            f.truncate()

        output_cmd = "./xvmec {} > tmp.txt".format(new_input_file_name)

        print("Running:", output_cmd)
            
        subprocess.run(output_cmd, shell=True)

        # Create distinct output file names
        #file_names = {
        #    "dcon": "dcon_m{}_RBC{:.3f}.vmec.txt".format(mpol, rbc_value),
        #    "threed1": "threed1_m{}_RBC{:.3f}.vmec".format(mpol, rbc_value),
        #    "wout": "wout_m{}_RBC{:.3f}.vmec.nc".format(mpol, rbc_value),
        #    "jxbout": "jxbout_m{}_RBC{:.3f}.vmec.nc".format(mpol, rbc_value),
        #    "mercier": "mercier_m{}_RBC{:.3f}.vmec".format(mpol, rbc_value)
        #}

        ## Move output files to appropriate directories with distinct names
        #for key, file_name in file_names.items():
        #    source_file = "{}*".format(key)
        #    #print(source_file)
        #    target_path = "{}/{}/".format(output_dir, key)
        #    #print(target_path)
        #    subprocess.run("mv {} {}".format(source_file,target_path),shell=True)


print("Script execution completed.")

