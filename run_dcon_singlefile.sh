#!/bin/bash

# single file
equil_file="dcon_first_init.vmec.txt"

# Store the current directory
current_dir=$(pwd)
dcon_dir="/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"

# Change directory to where "dcon" is located
cd /home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux
echo "befor change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename

sed -i "s|eq_filename=.*|eq_filename=\"${current_dir}\/${equil_file}\"|" ${dcon_dir}/equil.in
echo "after change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename

# Run "dcon" with the current file as an argument
./dcon 
./xdraw crit

# Change back to the original directory
#cd "$current_dir"

