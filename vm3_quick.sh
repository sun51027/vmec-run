#!/bin/bash

current_dir=$(pwd)
inputvmec=${1}
wout=${current_dir}/wout_${inputvmec}.txt
vm3dp_dir='/home/linshih/workspace/vm3dp'
vmec2terps_dir='/home/linshih/workspace/vmec2tpr'

echo "VMEC input namelist: input.${inputvmec} & ${wout}.txt"
if [ ! -e "wout_$inputvmec.txt" ]; then
  echo "Error: Input file 'wout_$inputvmec.txt' not found. Exiting script."
  exit 1
fi
ns=$(awk 'NR==3 {print $2}' wout_${inputvmec}.txt)
echo "ns_array from wout.txt: $ns"

echo "VMEC to TERP..."
cd ${vmec2terps_dir}
cp ${wout} fort.8
./vmec2terps.x
mv fort.73 ${vm3dp_dir}/fort.23

echo "Recompile vm3dp and Plot snake ..."
cd ${vm3dp_dir}
new_value=$((ns-1))
sed -i "3s/nit=[0-9]*/nit=${new_value}/" plovma.inc
make clean && make
./vm3dbm90.x < vmaplo.dat_snake_n3
cp fort.37 f6snake
cp f6snake f6snake_${inputvmec}

# open MATLAB
# run snake_plot.m
# in matlab

#nturns=5
#[r,v,p]=snake_plot(nturns)

echo "Plot toroidal plan..."

# here is different!
./vm3dbm90.x < vmaplo.data
cp fort.37 f6sph
cp f6sph f6sph_${inputvmec}
echo "[Info] All jobs done!"
