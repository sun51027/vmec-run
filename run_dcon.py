import os
import subprocess

# Define paths
current_directory = os.getcwd()
dcon_executable_path = os.path.expanduser("~/workspace/dcon_3.80/dcon_3.80/rundir/Linux/dcon")
input_directory = os.path.expanduser("~/workspace/Stellarator-Tools/build/_deps/parvmec-build/output/dcon")

# Change directory to where the "dcon" executable is located
os.chdir(os.path.dirname(dcon_executable_path))

# List all files in the input directory
input_files = os.listdir(input_directory)

# Run "dcon" for each input file
for input_file in input_files:
    input_file_path = os.path.join(input_directory, input_file)
    
    # Construct the command to run "dcon" with the input file
    command = [dcon_executable_path, input_file_path]
    
    # Run the command using subprocess
    try:
        subprocess.run(command, check=True)
        print("dcon executed successfully for {}".format(input_file))
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    except subprocess.CalledProcessError as e:
        print("Error executing dcon for {}: {}".format(input_file, e))

# Change back to the original directory
os.chdir(current_directory)

