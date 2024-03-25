#!/usr/bin/python 
import subprocess
import argparse
import interface.parallel_utils as pu

'''
Created by Shih Lin
Date: 2023/09/20
Status: temporary script, could be changed in the future

Description:
	The script deals with parameters scan of current profile in VMEC (Oak-Ridge).
	By importing "interface.parallel_utils as pu" to run multiprocessing.
	Input file: input.first_init.vmec
	After executing ./xvmec, all output files are categorised automatically.
Usage:
	./replace_paramAC.py -h (to check all commands)
	./replace_paramAC.py -d -i input.first_init.vmec (to list jobs) 
	./replace_paramAC.py -i input.first_init.vmec (to run)
   	 
'''

#def scientific_notation(value):
#    try:
#        return float(value)
#    except ValueError:
#        msg = f"Invalid float value: {value}"
#        raise argparse.ArgumentTypeError(msg)
parser = argparse.ArgumentParser()
parser.add_argument("-d","--dryRun", help = "do not submit jobs", action="store_true")
parser.add_argument("-t","--tag"   , help = "tag of this parameter scan", default = "unknown", type=str, required=True)
parser.add_argument("-i","--input" , help = "input filename of parameters",  default="input.first_init.vmec", type=str)

parser.add_argument("--pres_ranges"  , help = "Ranges of pressure scale as a list of integers",  nargs="+", type=int)#, required=True)
parser.add_argument("--curr_ranges"  , help = "Ranges of current scale as a list of integers",  nargs="+", type=int)#, required=True)
args = parser.parse_args()

filename = args.input
tag      = args.tag
new_input_file_list = []
new_input_file_list_tmp = []
command_list = []
if args.pres_ranges:
    pres_ranges = [range(args.pres_ranges[i], args.pres_ranges[i+1]) for i in range(0, len(args.pres_ranges), 2)]
else:
    pres_ranges = []
if args.curr_ranges:
    curr_ranges = [range(args.curr_ranges[i], args.curr_ranges[i+1]) for i in range(0, len(args.curr_ranges), 2)]
else:
    curr_ranges = []
'''
 Change stuff below manually
 
'''
profile = tag

step_pres = 50
step_curr = 100

count=0
def sed_am_power_series(filename,pres_ranges):    
    print(pres_ranges)
    global count
    with open(filename, 'r') as fin:
        contents = fin.readlines() 
    for index, line in enumerate(contents):   
        if not 'PRES_SCALE = ' in line:
            continue
        for i in pres_ranges:
            pres_value = i/step_pres;
            contents[index] = f'PRES_SCALE ={pres_value}\n'
            count+=1
             if args.dryRun:
                print(contents[index])
                print("create new namelist: {}".format(new_input_name))
             else:
                 with open(new_input_name,'w') as new_input_file:
                      new_input_file.writelines(contents)
    
             new_input_file_list.append(new_input_name)


def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command,shell=True)


def create_commands():
    
    for files in new_input_file_list:
        command = './xvmec {} '.format(files)
        #command = './xvmec {} > tmp_xvmec.txt'.format(files)
        command_list.append(command)

def submit_jobs():
    if args.dryRun:
        for command in command_list: print(command)
    else:
        for command in command_list: exe(command)
        #pu.submit_jobs(command_list,20)

def mkdir():
    command = ("mkdir -p depo/output/{}/threed1 "
              "depo/output/{}/wout "
              "depo/output/{}/dcon "
              "depo/output/{}/jxbout "
              "depo/output/{}/mercier "
              "depo/input/{}"
               ).format(profile,profile,profile,profile,profile,profile,profile)
    exe(command)

def move():
    commands = ["mv threed1*.vmec*   depo/output/{}/threed1".format(profile),
                "mv dcon*.vmec*      depo/output/{}/dcon".format(profile),
                "mv wout*.vmec*      depo/output/{}/wout".format(profile),
                "mv mercier*.vmec*   depo/output/{}/mercier".format(profile),
                "mv jxbout*.vmec*    depo/output/{}/jxbout".format(profile),
                "mv input.cur*.vmec* depo/input/{}".format(profile)
                ]
    for command in commands:
        exe(command)

def print_final_message():
    if args.dryRun:
        print(f"[INFO] this is the end of dryRun mode (print commands only). Will created {count} files.")
    else:
        print(f"[INFO] all jobs completed! Created {count} files.")
    
if __name__ == "__main__":

    #mkdir()
    create_commands()
    submit_jobs()
    #move()
    print_final_message()
