#!/bin/bash

# Function to display the help message
show_help() {
    echo "Usage: $0 [-h] [-c CERTAIN_STRING] ELOG"
    echo "       -h: Display this help message"
    echo "       -c CERTAIN_STRING: Specify a certain string to replace 'elog2'"
    echo "       ELOG: Elog string"
    exit 1
}

# Default values for options
certain_string=""
elog=""

# Parse command line options
while getopts "hc:" opt; do
    case $opt in
        h)
            show_help
            ;;
        c)
            certain_string="$OPTARG"
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            show_help
            ;;
    esac
done

# Remove the processed options from the arguments
shift $((OPTIND - 1))

# Now, $@ contains the remaining arguments (ELOG)
elog="${1}"
new_script="quick_${elog}.sh"

# Copy the content of quick_elog2.sh and replace "elog2" with the certain string
sed "s/elog2/${elog}/g" quick_elog2.sh > "$new_script"

# Make the new script executable
chmod +x "$new_script"

echo "New script $new_script created with $elog."

mkdir -p "output/${elog}"
mkdir -p "input/${elog}"

mkdir -p "output/${elog}/wout"
mkdir -p "output/${elog}/mercier"
mkdir -p "output/${elog}/threed"
mkdir -p "output/${elog}/jxbout"
mkdir -p "output/${elog}/dcon"

echo "New directories created with $elog."
echo "====> inside the input/"
ls input
echo "====> inside the output/"
ls output
echo "====> inside the output/${elog}"
ls "output/${elog}"

