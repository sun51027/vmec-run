#!/bin/bash

# Store the current directory
current_dir=$(pwd)
dcon_dir="/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"
#dcon_output="/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux/dcon.out"
dcon_output=$current_dir/dcon_output.txt

# Change directory to where "dcon" is located
cd /home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux
echo "befor change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename

# Loop over all files in the target directory
for file in /home/linshih/workspace/Stellarator-Tools/build/_deps/parvmec-build/output/curr_2p/dcon/*; do
 # echo $file
  sed -i "s|eq_filename=.*|eq_filename=\"$file\"|" ${dcon_dir}/equil.in
  #echo "after change path and file >>> "
  cat ${dcon_dir}/equil.in | grep eq_filename
  # Check if the file is a regular file (not a directory)
 if [ -f "$file" ]; then
  # Run "dcon" with the current file as an argument
  echo "running $file ..............."

  #./dcon
  ./dcon > $dcon_output

  if grep -q "Zero\|unstable" "$dcon_output"; then
	continue;
     #echo "The string 'Zero' was found in '$file'."
  else
     echo "The string 'Zero' or 'unstable'  was not found in '$file'."
     realpath $file >> $current_dir/dcon_nonzero_case.txt

#  if grep -q "All free-boundary modes stable" "$dcon_output"; then
#
#     realpath $file >> $current_dir/dcon_nonzero_case.txt
  fi
 fi
done

# Change back to the original directory
cd "$current_dir"

