#!/bin/bash

current_dir=$(pwd)
inputfile=${1}
wout=${current_dir}/${inputfile}
vm3dp_dir='/home/linshih/workspace/vm3dp'
vmec2terps_dir='/home/linshih/workspace/vmec2tpr'
echo ${wout}

original_string=${inputfile}
substring=$(echo "$original_string" | sed -n 's/^wout_\(.*\)\.txt$/\1/p')
echo $substring

echo "Plot snake structure:"
cd ${vmec2terps_dir}
cp ${wout} fort.8
./vmec2terps.x
mv fort.73 ${vm3dp_dir}/fort.23
cd ${vm3dp_dir}
./vm3dbm90.x < vmaplo.dat_snake_n3
cp fort.37 f6snake
cp f6snake f6snake_${substring}

# open MATLAB
# run snake_plot.m
# in matlab

#nturns=5
#[r,v,p]=snake_plot(nturns)

echo "Plot toroidal plan..."

# here is different!
./vm3dbm90.x < vmaplo.data
cp fort.37 f6sph
cp f6sph f6sph_${substring}
