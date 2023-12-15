#!/usr/bin/python 
import os
import re
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-t","--tag"   , help = "tags: profile type and scale", default = "unknown", type=str, required=True)
parser.add_argument('-d','--dryRun', help = 'do not submit jobs', action='store_true')
#parser.add_argument('-i','--input' , help = 'input filename', default='', type=str)
args = parser.parse_args()
#filename = args.input
tag = args.tag

#========================================================
name = tag
dcon_path = '~/workspace/dcon_3.80/dcon_3.80/rundir/Linux'
vmec_dir  = '/home/linshih/workspace/Stellarator-Tools/build/_deps/parvmec-build'
vmec_depo_dir    = f'{vmec_dir}/depo'
vmec_depo_input  = f'{vmec_depo_dir}/input/{name}'
vmec_depo_output = f'{vmec_depo_dir}/output/{name}'
vmec_input       = f'{vmec_dir}/input/{name}'
vmec_output      = f'{vmec_dir}/output/{name}'
count=0
tag_list = ['dcon','mercier','wout','jxbout','threed1']
stable_list = []
vmec_input_list  = []
vmec_output_list = [[],[],[],[],[]]
save_input_list  = []
save_output_list = [[],[],[],[],[]]

def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command, shell=True)

def append_files():
    if not args.dryRun:
       # append stable cases
       with open(filename, 'r') as fin:
           contents = fin.readlines()
           for index, line in enumerate(contents):
               str=string_manager(line)
               stable_list.append(str)
   
       # append all output files in depo
       for idx, tag in enumerate(tag_list):
           path = f'{vmec_depo_output}/{tag}'
           files = os.listdir(path)
           for f in files:
               #print(f"{idx} -> {tag} -- {f}")
               vmec_output_list[idx].append(f)
           
       # append all input.namelist.vmec in depo
       files = os.listdir(vmec_depo_input)
       for f in files:
           vmec_input_list.append(f)
def create_dir():

    icmd = f"mkdir -p {vmec_input} {vmec_output} "
    exe(icmd)

    for idx, tag in enumerate(tag_list):
        ocmd = f"mkdir -p {vmec_output}/{tag}"
        exe(ocmd) 

def move_stable_files():

    for file in save_input_list:
        icommand = f"mv {vmec_depo_input}/{file} {vmec_input}"
        exe(icommand)

    for idx, tag in enumerate(tag_list):
        print(f"processing tag: {tag}")
        for file in save_output_list[idx]:
            command = f"mv {vmec_depo_output}/{tag}/{file} {vmec_output}/{tag}"
            exe(command)

def rm_unstable_files():

    cmds = f"rm -rf depo/output/{name} depo/input/{name} "
    exe(cmds)


def match_vmec_file():
    global count
    for str in stable_list:
       # match input
       for input_str in vmec_input_list:
           if not re.search(str,input_str):
               continue;
           else:
               count+=1
               save_input_list.append(input_str)
               print(f"{str} is matched to {input_str}")

       # match output
       for idx, tag in enumerate(tag_list):
           for output_str in vmec_output_list[idx]:
               if not re.search(str,output_str):
                   continue;
               else:
                   save_output_list[idx].append(output_str)
                   print(f"{str} is matched to {output_str}")
           
    

def string_manager(file_path):
    file = os.path.basename(file_path)
    str = file.replace('dcon_','').replace('.vmec.txt\n','')
    return str

def check_existing_files(filename):
    full_path = os.path.expanduser(os.path.join(dcon_path, filename))
    if not os.path.exists(full_path):
        print(f"[ERROR] File {filename} in path {dcon_path} does not exist. Stopping the script.")
        cmd = f"rm -rf {dcon_path}/vmec"
        exe(cmd)
        print(cmd)
        rm_unstable_files()
        exit(1)

def print_final_message():
    if args.dryRun:
        print("[INFO] this is the end of dryRun mode (print commands only)")
    else:
        print("[INFO] all jobs completed!")

if __name__ == "__main__":

    filename = f"dcon_stable_{tag}.txt"

    check_existing_files(filename)

    cmd = f"cp {dcon_path}/{filename} ."
    exe(cmd)
    append_files() 
    match_vmec_file()
    create_dir()
    move_stable_files()
    rm_unstable_files()

    print("result: found {} matched, executing over.".format(count))
    print_final_message()

