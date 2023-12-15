#!/bin/bash

# single file
equil_file=${1}

# Store the current directory
current_dir=$(pwd)
dcon_dir="/home/linshih/workspace/dcon_3.80/dcon_3.80/rundir/Linux"

# Change directory to where "dcon" is located
cp ${equil_file} ${dcon_dir}
cd ${dcon_dir}
echo "befor change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename
filename=$(basename "$equil_file")
sed -i "s|eq_filename=.*|eq_filename=\"${filename}\"|" ${dcon_dir}/equil.in
#sed -i "s|eq_filename=.*|eq_filename=\"${current_dir}\/${equil_file}\"|" ${dcon_dir}/equil.in

echo "after change path and file >>> "
cat ${dcon_dir}/equil.in | grep eq_filename

for n in {1..1}
do
	sed -i "s|nn=.*|nn=${n}|" ${dcon_dir}/dcon.in
	./dcon 
done


# Run "dcon" with the current file as an argument
#./xdraw dcon

# Change back to the original directory
#cd "$current_dir"

