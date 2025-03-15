
# wsl -d Ubuntu
# bash darbas3.sh

# $1 is given or not username
username=$1
mapfile -t bash_processes < <(ps -eo comm:20,pid:5,pcpu,pmem,uname:20)
file_time=$(date +"%Y-%m-%d-%H-%M-%S")
log_extension="log"


function create_logs_dir () {
    mkdir -p logs
}

function remove_logs_dir () {
    rm -rf logs
}

function create_log_file () {
    file_name_=$1
    echo $(date +"%Y-%m-%d") > $file_name_
    echo $(date +"%H:%M:%S") >> $file_name_
}


function is_user_valid () {
    user_=$1
    if grep -q "^$user_:" /etc/passwd
    then
        return 0
    else
        return 1
    fi
}

function create_log_file_for_user () {
    user_=$1

    create_logs_dir
    logs_file_name="logs/$user_-process-log-$file_time.$log_extension"
    create_log_file $logs_file_name
    

    for process in "${bash_processes[@]}"
    do
        IFS=' ' read -r comm pid pcpu pmem uname <<< "$process"

        if [[ $uname == "$user_" ]]
        then
            echo "PROCESS $comm: pid=$pid pcpu=$pcpu pmem=$pmem" >> $logs_file_name
        fi
    done
}

function all_logs_statistical_output () {
    # file_name lines_within
    # and later total line count

    local total_lines=0
    for file in $(ls logs) 
    do
        lines=$(wc -l < logs/$file)
        total_lines=$(($total_lines + $lines))
        echo "File: $file with $lines lines"
    done
    echo "Total log lines: $total_lines"

}

# ps -eo uname:20,pid,pcpu,pmem,sz,tty,stat,time,cmd


if [ -z "$username" ]
then
    echo "Username is not given, logs will be created for all users"
    for user in $(ls /home)
    do
        echo "Creating logs for $user"
        create_log_file_for_user $user
    done
    all_logs_statistical_output

    read -p "Script has paused. Press enter to continue"
    remove_logs_dir
    exit 0


    
else
    echo "username '$username' was given, cheking if it is valid"
    is_user_valid $username
    if [ $? -ne 0 ]
    then
        echo "$username USER NOT FOUND!" >&2
        exit 1
    else
        echo "$username FOUND! Creating logs..."
        create_log_file_for_user $username
        all_logs_statistical_output

        # Because a specific user was provided
        # I need to, after all output
        # To print out this users log
        echo "$(<logs/$username-process-log-$file_time.$log_extension )"


        read -p "Script has paused. Press enter to continue"
        remove_logs_dir
        exit 0 
    fi

fi