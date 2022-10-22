# Debianology
Recipe for Debian on Synology DSM as the secondary OS to work with NAS.

## Installation
Make sure that your Synology has Docker package installed.
Just copy over the files to Synology and run below from DSM as an user with Docker access. 
   
    bash ./debianology.sh

Login from the client machine:

    ssh -p 122 your-user@your-synology-host

Eventually update your client `.ssh/config` for convenience:

    Host debian-your-synology-host
        User your-user
        HostName your-synology-host
        Port 122
        ForwardAgent Yes

The Debian users have same access rights as the DSM users.

## Bash

DSM shell defaults to `sh`, which gets inherited by Debian container.
Usually Linux shell could be changed in `/etc/passwd` but DSM prohibits it.
As workaround to switch the default user shell to e.g. `bash` invoke below in your Debian user directory:

    echo "/bin/bash\nexit" > .profile


## Uninstall
To uninstall simply remove the container

    /usr/local/bin/docker stop debianology
    /usr/local/bin/docker rm debianology