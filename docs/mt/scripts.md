### Collection of Useful Scripts

#### Server Launching Script

````bash
#!/bin/bash
#---------------------------------------------------------------------
# File information

# Name          : Server Utility
# Purpose       : Simplify launching server
# License       : MIT
# Revision      : 0.1.210429

#---------------------------------------------------------------------
# Parameters
binpath="$HOME/multicraft/bin/multicraftserver"
worldname="${1:-adventure}"
port=30029
world="$HOME/worlds/${worldname}"
logfile="$HOME/logs/${worldname}/`date +"%Y-%m-%d"`.txt"
config="$HOME/config/${worldname}.conf"
#---------------------------------------------------------------------
# Note to myself compile with ncurses to use --terminal
# Check for binary file
if [[ $1 == "--setup" ]]; then
    if [[ ! $2 ]]; then
        echo "Invalid syntax : Use --setup <world>"
        exit 1
    fi
    mkdir -p "$HOME/logs/${2}"
    mkdir -p "$HOME/config"
    mkdir -p "$HOME/worlds/${2}"
    touch "$HOME/config/${2}.conf"
    echo "Setup Done..."
    exit 1
fi

echo "Running Minetest Server..."
if [[ ! -x "$binpath" ]]; then
   echo "ERROR: no server binary found" >&2
   exit 69
fi
echo "Found server binary"

if [[ ! -d $world ]]; then
    echo -e "\nWorld ${worldname} not found at ${world}"
    echo -e "\033[33mAborted.\n \033[0m"
    exit 1
fi
echo "Found world at ${world}"

if [[ ! -f $config ]]; then
    echo -en "\n\033[33m[Warning] ${config} file not found\033[0m"
    echo -e "\033[33m : Using default config file\033[0m"
    unset config
else
    echo -e "\nFound config file at ${config}"
fi

if [[ ! -d $HOME/logs/${worldname} ]]; then
    echo -en "\033[33m[Warning] ${logfile} file not found\033[0m"
    echo -e "\033[33 : mUsing default debug.txt file\033[0m"
    unset logfile
else
    echo "Starting Logging in file ${logfile}"
fi

opts=(
    ${world:+--world "$world"}
    ${port:+--port "$port"}
    ${logfile:+--logfile "$logfile"}
    ${config:+--config "$config"}
    --gameid minetest
    --terminal
)
echo "Attaching 'mcserver' screen in background... "
# Command to start screen in background
# [[ -z "$STY" ]] && exec screen -d -m -S mcserver /usr/bin/bash "$0"
# echo "${binpath} ${opts[@]}"
timer=3
while sleep ${timer}; do
   logfile="$HOME/logs/${worldname}/`date +"%Y-%m-%d"`.txt"
   "${binpath}" "${opts[@]}"
   echo -e "\033[33mRetrying in ${timer}s...\033[0m"
   logfile="$HOME/logs/${worldname}/`date +"%Y-%m-%d"`.txt"
   opts[5]=${logfile}
   # timer=$((timer+3))
done
#---------------------------------------------------------------------
````

#### 