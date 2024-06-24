#!/usr/bin/python
'''
Created by Shih Lin
Date: 2024/03/20

Description:
	DESCUR convert R, phi ,z points into RBC ZBS coefficients in VMEC.
Usage:
	./descur2vmec.py -u
   	 
'''
import os
import numpy as np
import argparse
import datetime
import subprocess

outputFileName = 'rz_points'
descur_path = "/home/linshih/workspace/Stellarator-Tools/build/_deps/descur-build"

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user', help='interactive mode', action='store_true')
    return parser.parse_args()

def get_user_input(parameter_name):
    try:
        value = float(input("!Enter {}: ".format(parameter_name)))
        if value == 0:
            raise ValueError("Value cannot be 0.")
        return value
    except ValueError as e:
        print(e)
        print("Invalid input. Please enter a valid numerical value.")
        return get_user_input(parameter_name)

def record_parameters(user_inputs, parameters):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    with open("parameters_log.txt", "a") as log_file:
        log_file.write(f"Timestamp: {timestamp}\n\n")
        for param in parameters:
            log_file.write(f"{param}: {user_inputs[param]:<10}\n")
        log_file.write("\n")

def generate_points(R0, aspect, elong, triang, numPoints):
    a = R0 / aspect  # minor radius
    Z0 = 0.0

    theta = np.linspace(0, 2 * np.pi, numPoints)

    # outputFileName = f"RPhiZ_R{R0}_epsi{aspect}_k{elong}_del{triang}"
    with open(outputFileName, 'w') as fid:
        fid.write('%d 1 1\n' % (numPoints))
        for i in range(numPoints):
            fR = R0 + a * np.cos(theta[i] + triang * np.sin(theta[i]))
            fZ = Z0 + a * elong * np.sin(theta[i])
            fid.write('%f %f %f\n' % (fR, theta[i], fZ))

def main():
    default_user_inputs = {
        "major radius (R0)     ": 0.45,
        "aspect ratio (epsilon)": 1.5,
        "elongation (kappa)    ": 2.0,
        "triangularity (delta) ": 0.5,
        "number of points      ": 100
    }

    args = parse_arguments()

    if args.user:
        user_inputs = {param: get_user_input(param) for param in default_user_inputs.keys()}
    else:
        user_inputs = default_user_inputs

    generate_points(
        user_inputs["major radius (R0)     "],
        user_inputs["aspect ratio (epsilon)"],
        user_inputs["elongation (kappa)    "],
        user_inputs["triangularity (delta) "],
        int(user_inputs["number of points      "])
    )

    record_parameters(user_inputs, default_user_inputs.keys())

def exe(command):
    
    subprocess.run(command,shell=True,check=True)

def move_files():

    cmd = f"mv {outputFileName} {descur_path}"
    exe(cmd)

def run_descur():

    os.chdir(descur_path)
    execute = os.path.join(descur_path, "xdescur")
    process = subprocess.Popen(execute,stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    input_values = "4\nv\n0\nrz_points\nn\n"
    process.stdin.write(input_values)
    process.stdin.flush()
    process.stdin.close()
    process.wait()
    cmd = "cat tovmec"
    exe(cmd)
    
def final_message():

    print("\n[INFO] Finsih all jobs")

if __name__ == "__main__":
    main()
    move_files()
    run_descur()
    final_message()    
