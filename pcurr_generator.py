#!/usr/bin/python
import numpy as np
import argparse
'''
	Created by Lin Shih 
	Date: 2024.6.19
	usage:
	./pcurr_generator.py --bsj [raw result from bsj routine] --input [FIRST_mmdd] --iter 1
	./pcurr_generator.py --bsj [raw result from bsj routine] --input [FIRST_mmdd_bootsj1] --iter 2


'''
bsj_path = '/home/linshih/workspace/terp_bootsj'
input_path = f'{bsj_path}/fort.43'
parser = argparse.ArgumentParser()
parser.add_argument('--curtor', help = 'total toroidal current', default = 8E+05, type = float)
parser.add_argument('--bsj', help = 'raw bootstrap current', default = 0., type = str, required=True)
parser.add_argument('--input', help = 'input file name e.g. FIRST_mmdd_bootsj1', type = str, required=True)
parser.add_argument('--ns', help = 'ns_array (mesh)', default = 289, type = int)
#parser.add_argument('--iter', help = 'iteration', type = int, required=True)
args = parser.parse_args()

def discretise_ohmic_profile(s):
    #return 1-s-s**2+s**3
    #return 2 * (1 - s**7)**2 - (1 - s**3)**2
    return 2*( 1 - s**2)**2 - ( 1 - s )**2

def read_fort(input_fort_name):
    try:
        if "43" in input_fort_name:
            with open(f'{bsj_path}/{input_fort_name}','r') as inputfile:
                 lines = inputfile.readlines()
            
            # exclude the last line
            lines = lines[:-1]
    
            bsj_profile = []
            for line in lines:
                bsj_profile.extend(map(float,line.split()))
            return np.array(bsj_profile) #np.array is more efficient than return bsj_profile

        elif "48" in input_fort_name:
            with open(f'{bsj_path}/{input_fort_name}','r') as inputfile:
                 lines = inputfile.readlines()
            
            radial = []
            for line in lines:
                radial.extend(map(float,line.split()))
            return np.array(radial) #np.array is more efficient than return bsj_profile

    except:
        print(f'{bsj_path}/{input_fort_name} does not exist')
        return False

def normalise_profile(numbers):
    return (numbers-min(numbers))/(max(numbers)-min(numbers))

def iterate_profile(ohmic_profile, scale, bsj_profile):
    return (1-scale) * ohmic_profile +scale* bsj_profile

def write_new_profile(new_profile,radial,filename):
    with open(filename, 'w') as file:
        file.write('pcurr_type = \'Akima_spline_Ip\'\n')
        file.write('ac_aux_f = \n')
        for i, p in enumerate(new_profile):
            if i > 0 and i % 5 == 0:
                file.write('\n')
            file.write(f" {p:.8E} ")
        file.write('\n')
        file.write('ac_aux_s = \n')
        for i, p in enumerate(radial):
            if i > 0 and i % 5 == 0:
                file.write('\n')
            file.write(f" {p:.8E} ")
        file.write('\n')

def print_profile(profile):   
    for i, p in enumerate(profile):
        if i > 0 and i % 5 == 0:
            print()
        print(f"{p:.8E} ", end="")
    print()

def calculate_bsj_ratio():
    return float(args.bsj)/(4*np.pi*10**(-7))/args.curtor

def main():
    
    # discritise ohmic_profile from VMEC
    mesh = args.ns - 3
    s_values = np.linspace(0, 1, mesh)  
    ohmic_profile = discretise_ohmic_profile(s_values)
    norm_ohmic_profile = normalise_profile(ohmic_profile)
    #print_profile(norm_ohmic_profile)
        
    # read fort.43
    bsj_profile = read_fort(f'fort.43_{args.input}')
    norm_bsj_profile = normalise_profile(-bsj_profile)
    print_profile(bsj_profile)
    #print("\n")
    #print_profile(norm_bsj_profile)
    radial = read_fort('fort.48')
    print_profile(radial)
    
    '''get new profile'''
    scale = calculate_bsj_ratio()
    new_profile = iterate_profile(norm_ohmic_profile,scale,norm_bsj_profile)
    write_new_profile(new_profile,radial,f'new_profile_{args.input}.txt')
    #print_profile(new_profile)
    print("scale: %.5f " % scale)


main() 
