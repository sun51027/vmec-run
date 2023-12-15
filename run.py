#!/usr/bin/python 
import subprocess
import argparse
import datetime
parser = argparse.ArgumentParser()
parser.add_argument("-t","--tag"        , help = "tags: profile type and scale", default = "unknown", type=str, required=True)
parser.add_argument("-e","--exe_all"    , help = "execute all scripts "        , action="store_true")
parser.add_argument("-d","--dryRun"     , help = "do not submit job"           , action="store_true")
parser.add_argument("--ac_ranges"       , help="AC Ranges as a list of integers", nargs='+', type=str, required=True)


args = parser.parse_args()

tag = args.tag
ac_ranges = args.ac_ranges

def run(cmd):
    if args.exe_all:
        subprocess.call(cmd, shell=True)
    elif args.dryRun:
        print(cmd)

def record_parameters(tag, ac_ranges):
    if not args.dryRun:
       now = datetime.datetime.now()
       timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
       with open("parameters_log.txt", "a") as log_file:
           log_file.write(f"Parameters for {tag}:\n")
           log_file.write(f"AC Ranges: {ac_ranges}\n")
           log_file.write(f"Timestamp: {timestamp}\n\n")

if __name__ == "__main__":
    print("hello world")
    ac_ranges_str = " ".join(map(str, ac_ranges))
    cmds = [f"./replace_param.py --tag {tag} --input input.first_init.vmec --ac_ranges {ac_ranges_str}",
            f"./run_dcon.py --tag {tag} 2>/dev/null",
            f"./file_manager.py --tag {tag}"
            ]
    for cmd in cmds:
        run(cmd)
     
    record_parameters(tag, ac_ranges)
