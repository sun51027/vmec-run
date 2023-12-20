inputvmec=${1}
vmec_dir=$(pwd)
vmec2tpr_dir="/home/linshih//workspace/vmec2tpr"
terps_dir="/home/linshih/workspace/TERPS_TypeOneEnergy_codetransfer"


echo "VMEC input namelist: input.${inputvmec}.vmec"
#./xvmec input.${inputvmec}.vmec

echo "Copy wout to fort.8 and run vm2ptr..."
#cp wout_${inputvmec}.txt ${vmec2tpr_dir}
cp wout_${inputvmec}.vmec.txt ${vmec2tpr_dir}
cd ${vmec2tpr_dir}
cp wout_${inputvmec}.vmec.txt fort.8
./vmec2terps.x

echo "Copy fort.18 to TEPRS dir and run TERPSICODE..."
cp fort.18 ${terps_dir}


cd ${terps_dir}
rm tpr16_dat_wall
time ./tpr_ap.x < test_vertical.dat
#time ./tpr_ap.x < test_n2.dat
#time ./tpr_ap.x < test.dat
#time ./tpr_ap.x < ripple_test.dat
#time ./tpr_ap.x < axisym_test.dat

echo "[INFO] all jobs are done"


