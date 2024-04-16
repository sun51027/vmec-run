#
#
# ./terp_quick name 
# name without wout_xxx.txt
#
inputvmec=${1}
vmec_dir=$(pwd)

vmec2tpr_dir="/home/linshih/workspace/vmec2tpr"
terps_dir="/home/linshih/workspace/TERPS_TypeOneEnergy_codetransfer"


echo "VMEC input namelist: input.${inputvmec}"

# get ns from wout file
ns=$(awk 'NR==3 {print $2}' wout_${inputvmec}.txt)
echo "-- ns_array from wout.txt: $ns"

# convert to boozer coordinate
echo "-- Copy wout to fort.8 and run vm2ptr..."
cp wout_${inputvmec}.txt ${vmec2tpr_dir}
cd ${vmec2tpr_dir}
cp wout_${inputvmec}.txt fort.8
./vmec2terps.x
echo "-- Copy fort.18 to TEPRS dir and run TERPSICODE..."
cp fort.18 ${terps_dir}

# replace NI in terpsichore routine 
cd ${terps_dir}
file="tpr_modules_ap.f"
NI_value=$((ns-1))
echo "-- Changing the value of NI in line 3 of $file to $NI_value"
sed -i "3s/\(NI=\)[0-9]*/\1$NI_value/" "$file"
if [ "$NI_value" -lt 0 ]; then
    echo "[Error]: NI is less than 0. Stopping the script."
    exit 1
fi
cat ${file} | grep NI=

echo "-- Recompile after modifying $file"
make clean && make
mkdir -p obj 
mv *.o *.mod obj/
rm tpr16_dat_wall

#time ./tpr_ap.x < QAS3_nw1r52a375e12pv1p45n4_test.dat
#time ./tpr_ap.x < test_vertical.dat
#time ./tpr_ap.x < test_n2.dat
time ./tpr_ap.x < test.dat
#time ./tpr_ap.x < ripple_test.dat
##time ./tpr_ap.x < axisym_test.dat

echo "[INFO] all jobs are done"


# test
#vmec2tpr_dir="/home/linshih/testspace/vmecv92terps"
#terps_dir="/home/linshih/testspace/TERPS_TypeOneEnergy_codetransfer"

#./vmecv92terps.x
