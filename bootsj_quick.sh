#
#  Created by Lin Shih
#  2023/12/11 
#  VMEC -> vmec2tpr -> bootsj
#

inputvmec=${1}
iteration=${2}
vmec_dir=$(pwd)
vmec2tpr_dir="/home/linshih//workspace/vmec2tpr"
bootsj="/home/linshih/workspace/terp_bootsj"


echo "VMEC input namelist: input.${inputvmec}"
#./xvmec input.${inputvmec}.vmec

ns=$(awk 'NR==3 {print $2}' wout_${inputvmec}.txt)
echo "ns_array from wout.txt: $ns"

echo "Copy wout to fort.8 and run vm2ptr (coordinate transform)"
cp wout_${inputvmec}.txt ${vmec2tpr_dir}
cd ${vmec2tpr_dir}
cp wout_${inputvmec}.txt fort.8
./vmec2terps.x

echo "Copy fort.18 to bootsj dir: ${bootsj}"
cp fort.18 ${bootsj}
cd ${bootsj}

echo "Run fort43_generator.sh:"
./fort43_generator.sh ${inputvmec} ${ns} ${iteration}

# create data file
if [ ! -e "${inputvmec}.data" ]; then
  cp ITER_ripple.data ${inputvmec}.data
  new_value=$((ns-3))
  if [ "$new_value" -lt 0 ]; then
      echo "Error: $new_value is less than 0. Stopping the script."
      exit 1
  fi
  sed -i '23s/22/'"$new_value"'/' "${inputvmec}.data"
  digit_count="${#new_value}"
  if [ "$digit_count" -eq 3 ]; then
     echo "$new_value is 3 digital number"
     sed -i '23s/  / /'  "${inputvmec}.data"
  else
     echo "$new_value is 2 digital number"
  fi


  short_inputvmec=$(echo "${inputvmec}" | cut -c1-7)
  sed -i "1s/.*/               $short_inputvmec/" "${inputvmec}.data"
  echo "New data ${inputvmec}.data file is created"
  diff ITER_ripple.data ${inputvmec}.data
fi

echo "Run bootsj"
time ./tprbal.x < ${inputvmec}.data 2>&1 | tee ${inputvmec}.log

echo "Back-up fort.43 and fort.44"
cp fort.43 fort.43_${inputvmec}
cp fort.44 fort.44_${inputvmec}

echo "[INFO] all jobs are done"


