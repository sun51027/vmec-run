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
parser.add_argument("-t","--tag"   , help = "tags: profile type and scale", default = "unknown", type=str, required=True)
parser.add_argument("-i","--input" , help = "input filename of parameters",  default="input.first_init.vmec", type=str)
parser.add_argument("--ac_ranges"  , help = "AC Ranges as a list of integers",  nargs="+", type=int)#, required=True)
parser.add_argument("--ac_ps_list" , help = "AC parameters for power series (not a range)", type=str)#,  nargs="+")#, required=True)
parser.add_argument("--am_ps_list" , help = "AM parameters for power series (not a range)", type=str)#,  nargs="+")#, required=True)
args = parser.parse_args()

filename = args.input
tag      = args.tag
ac_ps_list = [float(x) for x in args.ac_ps_list.split()] if args.ac_ps_list else []
am_ps_list = [float(x) for x in args.am_ps_list.split()] if args.am_ps_list else []

#ac_ps_list = args.ac_ps_list
#am_ps_list = args.am_ps_list
new_input_file_list = []
new_input_file_list_tmp = []
command_list = []
if args.ac_ranges:
    ac_ranges = [range(args.ac_ranges[i], args.ac_ranges[i+1]) for i in range(0, len(args.ac_ranges), 2)]
else:
    ac_ranges = []
'''
 Change stuff below manually
 
'''
profile = tag
#profile = "curr_2p_gs_pres_10e3" 
#profile = "curr_2p" 

step = 10
count=0


def exe(command):
    if args.dryRun:
        print(command)
    else:
        subprocess.call(command,shell=True)

def sed_am_power_series(filename,am_ps_list):    
    print(am_ps_list)
    global count
    with open(filename, 'r') as fin:
        contents = fin.readlines() 
    for index, line in enumerate(contents):   
        if not 'AM = ' in line:
            continue
        contents[index] = f'AM = {", ".join(str(num) for num in am_ps_list)}\n'

    with open(filename, 'w') as file:
        file.writelines(contents)
    new_input_file_list.append(filename)

def sed_ac_power_series(filename,ac_ps_list):    
    print(ac_ps_list)
    global count
    with open(filename, 'r') as fin:
        contents = fin.readlines() 
    for index, line in enumerate(contents):   
        if not 'AC = ' in line:
            continue
        contents[index] = f'AC = {", ".join(str(num) for num in ac_ps_list)}\n'
        new_input_name = f"input.{profile}"

    with open(filename, 'w') as file:
        file.writelines(contents)
    new_input_file_list.append(filename)

        #if args.dryRun:
        #   print(contents[index])
        #   print("create new namelist: {}".format(new_input_name))
        #else:
        #    with open(new_input_name,'w') as new_input_file:
        #         new_input_file.writelines(contents)
        #    sed_am_power_series(new_input_name,am_ps_list)

def sed_ac_two_power(filename,ac_ranges):    
    global count
    with open(filename, 'r') as fin:
        contents = fin.readlines() # record all contents 
    for index, line in enumerate(contents):   
        if not 'AC = ' in line:
            continue
        #ac1, ac2, ac3 = AC_Ranges        
        for i in ac_ranges[0]:
            for j in ac_ranges[1]:
                for k in ac_ranges[2]:
                    value_i = i/step
                    value_j = j/step
                    value_k = k/step
                    new_ac = "{}, {}, {}".format(float(value_i),float(value_j),float(value_k))
                    contents[index] = "AC = {}\n".format(new_ac)
                    new_input_name = "input.{}_AC_{}_{}_{}.vmec".format(profile,i,j,k)
                    count+=1
                    if args.dryRun:
                       print(contents[index])
                       print("create new namelist: {}".format(new_input_name))
                    else:
                        with open(new_input_name,'w') as new_input_file:
                             new_input_file.writelines(contents)
    
                    new_input_file_list.append(new_input_name)

def sed_ac_two_power_gs(filename,ac_ranges):    
    global count
    with open(filename, 'r') as fin:
        contents = fin.readlines() # record all contents 
    for index, line in enumerate(contents):   
        if not 'AC = ' in line:
            continue
        #ac1, ac2, ac3, ac4, ac5, ac6 = AC_gs_Ranges        
        for i in ac_ranges[0]:
            for j in ac_ranges[1]:
                for k in ac_ranges[2]:
                    for l in ac_ranges[3]:
                        for m in ac_ranges[4]:
                            for n in ac_ranges[5]:
                                count+=1
                                value_i = i/step
                                value_j = j/step
                                value_k = k/step
                                value_l = l/step
                                value_m = m/100
                                value_n = n/100
                                new_ac = "{}, {}, {}, {}, {}, {}".format(float(value_i),float(value_j),float(value_k),\
                                                                         float(value_l),float(value_m),float(value_n))
                                contents[index] = "AC = {}\n".format(new_ac)
                                new_input_name = "input.{}_AC_{}_{}_{}_{}_{}_{}.vmec".format(profile,i,j,k,l,m,n)
                                if args.dryRun:
                                   print(contents[index])
                                   print("create new namelist: {}".format(new_input_name))
                                else:
                                    with open(new_input_name,'w') as new_input_file:
                                         new_input_file.writelines(contents)
                
                                new_input_file_list_tmp.append(new_input_name)
def sed_pcurr_type():
    if not args.dryRun:
       for new_file in new_input_file_list_tmp:
           print(new_file)
           with open(new_file, 'r') as fin:
               contents = fin.readlines() # record all contents 
           for index, line in enumerate(contents):   
               if not 'PCURR_TYPE = ' in line:
                   continue
               if "2p" in tag:
                   new_type = "two_power"
                   contents[index] = f"PCURR_TYPE = '{new_type}',\n"
               elif "2p_gs" in tag:
                   new_type = "two_power_gs"
                   contents[index] = f"PCURR_TYPE = '{new_type}',\n"
               elif "ps" in tag:
                   new_type = "power_series"
                   contents[index] = f"PCURR_TYPE = '{new_type}',\n"
               else :
                   print("Profile type must have 2p, 2p_gs, ps")
                   return 
               with open(new_file,'w') as new_input_file:
                    new_input_file.writelines(contents)
               new_input_file_list.append(new_file)
               

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

    # sed_pcurr_type() # abandoned temporarily, use power_series (default)
    if "gs" in tag:
        sed_ac_two_power_gs(filename,ac_ranges)
    elif "ps" in tag:
        sed_ac_power_series(filename,ac_ps_list)
        sed_am_power_series(filename,am_ps_list)  
    else:
        sed_ac_two_power(filename,ac_ranges)
    #mkdir()
    create_commands()
    submit_jobs()
    #move()
    print_final_message()
