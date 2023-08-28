#!/bin/bash
# created by Lin Shih 
# date: 23/8/15 
# Just want to change variables quickly

inputfile='input.test_FixBC_elog3.vmec'

NFP=${1}
NTOR=${2}
MPOL=${3}
NZETA=${4}

echo "Before change variable:"
cat ${inputfile} | grep NFP
cat ${inputfile} | grep NTOR
cat ${inputfile} | grep MPOL
cat ${inputfile} | grep NZETA

sed -i "s/NTOR = [0-9]*/NTOR = ${NTOR}/" ${inputfile}
sed -i "s/MPOL = [0-9]*/MPOL = ${MPOL}/" ${inputfile}
sed -i "s/NFP = [0-9]*/NFP = ${NFP}/" ${inputfile}
sed -i "s/NZETA = [0-9]*/NZETA = ${NZETA}/" ${inputfile}

echo "After change variable:"
cat ${inputfile} | grep NFP
cat ${inputfile} | grep NTOR
cat ${inputfile} | grep MPOL
cat ${inputfile} | grep NZETA

./xvmec ${inputfile}

echo " "
echo "Move all mercier/wout/jxbout/threed1 to output/elog3 "
mv mercier.* output/elog3/mercier/mercier.FixBC_nfp${NFP}n${NTOR}m${MPOL}.vmec
mv wout_*    output/elog3/wout/wout_FixBC_nfp${NFP}n${NTOR}m${MPOL}.vmec.nc
mv jxbout_*  output/elog3/jxbout/jxbout_FixBC_nfp${NFP}n${NTOR}m${MPOL}.vmec.nc
mv threed1.* output/elog3/threed/threed1.FixBC_nfp${NFP}n${NTOR}m${MPOL}.vmec
mv dcon_*    output/elog3/dcon/dcon_FixBC_nfp${NFP}n${NTOR}m${MPOL}.vmec.txt


echo " "
echo "Copy new file from ${inputfile} to input.FixBC_elog3_nfp${NFP}n${NTOR}m${MPOL}.vmec"
cp ${inputfile}  input/elog3/input.FixBC_nfp${NFP}n${NTOR}m${MPOL}vmec
echo " "
