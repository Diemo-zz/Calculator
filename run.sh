#!/bin/bash
# ref: https://askubuntu.com/questions/425754/how-do-i-run-a-sudo-command-inside-a-script
if ! [ $(id -u) = 0 ]; then
   echo "The script need to be run as root." >&2
   exit 1
fi

if [ $SUDO_USER ]; then
    real_user=$SUDO_USER
else
    real_user=$(whoami)
fi

/bin/bash scripts/install_docker.sh
/bin/bash scripts/initialise_docker_swarm.sh
/bin/bash scripts/run_calculator.sh
