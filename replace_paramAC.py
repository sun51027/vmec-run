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
	python replace_paramAC.py -h (to check all commands)
	python replace_paramAC.py -d -i input.first_init.vmec (to list jobs) 
	python replace_paramAC.py -i input.first_init.vmec (to run)
   	 
'''

parser = argparse.ArgumentParser()
parser.add_argument('-d','--dryRun', help='do not submit jobs', action='store_true')
parser.add_argument('-t','--test', help='just for test', action='store_true')
parser.add_argument('-i','--input', help='input filename of parameters', default='', type=str)
args = parser.parse_args()

filename = args.input
new_input_file_list = []
command_list = []

'''
 Change stuff below manually
 
'''
curr_prof = "curr_2p" #two_power
#curr_prof = "2p_gs" #two_power_gs

AC_Ranges = (range(1,3),range(3,5),range(9,11))
#AC_Ranges = (range(1,10),range(3,10),range(5,11))

# open files

def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command,shell=True)

def replace_parameters(filename):    
    if args.dryRun:
        print("Will create several new input_file_list")
    else:
        with open(filename, 'r') as fin:
            contents = fin.readlines() # record all contents 
        for index, line in enumerate(contents):   
            if not 'AC = ' in line:
                continue
            ac1, ac2, ac3 = AC_Ranges        
            for i in ac1:
                for j in ac2:
                    for k in ac3:
                        new_ac = "{}.0, {}.0, {}.0".format(i,j,k)
                        contents[index] = "AC = {}\n".format(new_ac)
                        new_input_name = "input.{}_AC_{}_{}_{}.vmec".format(curr_prof,i,j,k)
                        if args.dryRun:
                           print("create new namelist: {}".format(new_input_name))
                        else:
                            with open(new_input_name,'w') as new_input_file:
                                 new_input_file.writelines(contents)
    
                        new_input_file_list.append(new_input_name)

def create_commands():
    
    for files in new_input_file_list:
        command = './xvmec {} '.format(files)
        #command = './xvmec {} > tmp_xvmec.txt'.format(files)
        command_list.append(command)

def submit_jobs():
    if args.dryRun:
        for command in command_list: print(command)
    else:
        #for command in command_list: exe(command)
        pu.submit_jobs(command_list,10)

def mkdir():
    command = ("mkdir -p output/{}/threed1 "
              "output/{}/wout "
              "output/{}/dcon "
              "output/{}/jxbout "
              "output/{}/mercier "
              "input/{}"
               ).format(curr_prof,curr_prof,curr_prof,curr_prof,curr_prof,curr_prof,curr_prof)
    exe(command)

def move():
    commands = ["mv threed1* output/{}/threed1".format(curr_prof),
                "mv dcon* output/{}/dcon".format(curr_prof),
                "mv wout* output/{}/wout".format(curr_prof),
                "mv mercier* output/{}/mercier".format(curr_prof),
                "mv jxbout* output/{}/jxbout".format(curr_prof),
                "mv input.curr* input/{}".format(curr_prof)
                ]
    for command in commands:
        exe(command)

def create_testfile():
    command = 'touch threed1.txt dcon.txt wout.txt mercier.txt jxbout.txt'
    print(command)
    subprocess.call(command,shell=True)
    
if __name__ == "__main__":

    if args.test:
        create_testfile()
    else:
        mkdir()
        replace_parameters(filename)
        create_commands()
        submit_jobs()
        move()

