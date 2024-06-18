#!/usr/bin/python
import numpy as np

bsj_path = '/home/linshih/workspace/terp_bootsj'
input_path = f'{bsj_path}/fort.43'

def discretise_ohmic_profile(s):
    #return 1-s-s**2+s**3
    return 2 * (1 - s**7)**2 - (1 - s**3)**2

def read_fort43(input_path):
    try:
        if input_path:
            with open(input_path,'r') as inputfile:
                 lines = inputfile.readlines()
            
            # exclude the last line
            lines = lines[:-1]
    
            bsj_profile = []
            for line in lines:
                bsj_profile.extend(map(float,line.split()))
            return np.array(bsj_profile) #np.array is more efficient than return bsj_profile
    except:
        print(f'{input_path} does not exist')
        return False

def normalise_profile(numbers):
    return (numbers-min(numbers))/(max(numbers)-min(numbers))

def iterate_profile(ohmic_profile, scale, bsj_profile):
    return (1-scale) * ohmic_profile +scale* bsj_profile

def write_new_profile(new_profile,filename):
    with open(filename, 'w') as file:
        for i, p in enumerate(new_profile):
            if i > 0 and i % 5 == 0:
                file.write('\n')
            file.write(f"{p:.8E} ")
        file.write('\n')

def print_profile(profile):   
    for i, p in enumerate(profile):
        if i > 0 and i % 5 == 0:
            print()
        print(f"{p:.8E} ", end="")
    print()

def main():
    
    # discritise ohmic_profile from VMEC
    ns = 286
    s_values = np.linspace(0, 1, ns)  
    ohmic_profile = discretise_ohmic_profile(s_values)
    norm_ohmic_profile = normalise_profile(ohmic_profile)
    #print_profile(norm_ohmic_profile)
    
    # read fort.43
    bsj_profile = read_fort43(input_path)
    norm_bsj_profile = normalise_profile(-bsj_profile)
    #print_profile(bsj_profile)
    #print("\n")
    #print_profile(norm_bsj_profile)
    
    # subtract profiles
    # Need to add %
    #scale = (133343)/800000
    scale = 0.
    new_profile = iterate_profile(norm_ohmic_profile,scale,norm_bsj_profile)
    write_new_profile(new_profile,'new_profile.txt')
    print_profile(new_profile)
    print("scale: %.3f " % scale)


main() 
