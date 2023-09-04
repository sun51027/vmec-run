#!/bin/bash

# Store the current directory
current_dir=$(pwd)
dcon_dir="/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"

# Change directory to where "dcon" is located
cd /home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux
echo "befor change path and file >>> "
cat ${dcon_dir}/test.in | grep eq_filename

# Loop over all files in the target directory
for file in /home/linshih/workspace/Stellarator-Tools/build/_deps/parvmec-build/output/dcon/*; do
 # echo $file
  sed -i "s|eq_filename=.*|eq_filename=\"$file\"|" ${dcon_dir}/equil.in
  echo "after change path and file >>> "
  cat ${dcon_dir}/test.in | grep eq_filename
  # Check if the file is a regular file (not a directory)
 if [ -f "$file" ]; then
  # Run "dcon" with the current file as an argument
  ./dcon 
 fi
done

# Change back to the original directory
cd "$current_dir"

