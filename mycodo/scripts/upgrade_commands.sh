#!/bin/bash
#
#  upgrade_commands.sh - Mycodo commands
#

exec 2>&1

# Current Mycodo major version number
MYCODO_MAJOR_VERSION="8"

# Dependency versions/URLs
PIGPIO_URL="https://github.com/joan2937/pigpio/archive/v79.tar.gz"
MCB2835_URL="http://www.airspayce.com/mikem/bcm2835/bcm2835-1.50.tar.gz"
WIRINGPI_URL="https://project-downloads.drogon.net/wiringpi-latest.deb"
INFLUXDB_VERSION="1.8.10"
VIRTUALENV_VERSION="20.7.0"
SETUPTOOLS_VERSION="60.10.0"  # Also set version in install/requirements.txt

# Required apt packages. This has been tested with Raspbian for the
# Raspberry Pi and Ubuntu, it should work with most Debian-based systems.
APT_PKGS="gawk gcc g++ git libffi-dev libi2c-dev logrotate moreutils nginx sqlite3 wget python3 python3-pip python3-dev python3-setuptools rng-tools netcat"

PYTHON_BINARY_SYS_LOC="$(python3 -c "import os; print(os.environ['_'])")"

UNAME_TYPE=$(uname -m)
MACHINE_TYPE=$(dpkg --print-architecture)

# Get the Mycodo root directory
SOURCE="${BASH_SOURCE[0]}"

while [[ -h "$SOURCE" ]]; do # resolve $SOURCE until the file is no longer a symlink
    DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
    SOURCE="$(readlink "$SOURCE")"
    [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done

MYCODO_PATH="$( cd -P "$( dirname "${SOURCE}" )/../.." && pwd )"

cd "${MYCODO_PATH}" || return

HELP_OPTIONS="upgrade_commands.sh [option] - Program to execute various mycodo commands

Options:
  backup-create                 Create a backup of the ~/Mycodo directory
  backup-restore [backup]       Restore [backup] location, which must be the full path to the backup.
                                Ex.: '/var/Mycodo-backups/Mycodo-backup-2018-03-11_21-19-15-5.6.4/'
  compile-mycodo-wrapper        Compile mycodo_wrapper.c
  compile-translations          Compile language translations for web interface
  create-files-directories      Create required directories
  create-symlinks               Create required symlinks
  create-user                   Create 'mycodo' user and add to appropriate groups
  initialize                    Issues several commands to set up directories/files/permissions
  generate-widget-html          Generate HTML templates for all widgets
  restart-daemon                Restart the Mycodo daemon
  setup-virtualenv              Create a Python virtual environment
  setup-virtualenv-full         Create a Python virtual environment and install dependencies
  ssl-certs-generate            Generate SSL certificates for the web user interface
  ssl-certs-regenerate          Regenerate SSL certificates
  uninstall-apt-pip             Uninstall the apt version of pip
  update-alembic                Use alembic to upgrade the mycodo.db settings database
  update-alembic-post           Execute script following all alembic upgrades
  update-apt                    Update apt sources
  update-cron                   Update cron entries
  update-dependencies           Check for updates to dependencies and update
  install-bcm2835               Install bcm2835
  install-wiringpi              Install wiringpi
  install-pigpiod               Install pigpiod
  uninstall-pigpiod             Uninstall pigpiod
  disable-pigpiod               Disable pigpiod
  enable-pigpiod-low            Enable pigpiod with 1 ms sample rate
  enable-pigpiod-high           Enable pigpiod with 5 ms sample rate
  enable-pigpiod-disabled       Create empty service to indicate pigpiod is disabled
  update-pigpiod                Update to latest version of pigpiod service file
  update-influxdb               Update influxdb to the latest version
  update-influxdb-db-user       Create the influxdb database and user
  update-logrotate              Install logrotate script
  update-mycodo-startup-script  Install the Mycodo daemon startup script
  update-packages               Ensure required apt packages are installed/up-to-date
  update-permissions            Set permissions for Mycodo directories/files
  update-pip3                   Update pip
  update-pip3-packages          Update required pip packages
  update-swap-size              Ensure swap size is sufficiently large (512 MB)
  upgrade-mycodo                Upgrade Mycodo to latest compatible release and preserve database and virtualenv
  upgrade-release-major {ver}   Upgrade Mycodo to a major version release {ver} and preserve database and virtualenv
  upgrade-release-wipe {ver}    Upgrade Mycodo to a major version release {ver} and wipe database and virtualenv
  upgrade-master                Upgrade Mycodo to the master branch at https://github.com/kizniche/Mycodo
  upgrade-post                  Execute post-upgrade script
  web-server-connect            Attempt to connect to the web server
  web-server-reload             Reload the web server
  web-server-restart            Restart the web server
  web-server-update             Update the web server configuration files

Docker-specific Commands:
  docker-update-pip             Update pip
  docker-update-pip-packages    Update required pip packages
  install-docker-ce-cli         Install Docker Client
"

case "${1:-''}" in
    'backup-create')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/mycodo_backup_create.sh
    ;;
    'backup-restore')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/mycodo_backup_restore.sh "${2}"
    ;;
    'compile-mycodo-wrapper')
        printf "\n#### Compiling mycodo_wrapper\n"
        gcc "${MYCODO_PATH}"/mycodo/scripts/mycodo_wrapper.c -o "${MYCODO_PATH}"/mycodo/scripts/mycodo_wrapper
        chmod 4770 "${MYCODO_PATH}"/mycodo/scripts/mycodo_wrapper
    ;;
    'compile-translations')
        printf "\n#### Compiling Translations\n"
        cd "${MYCODO_PATH}"/mycodo || return
        "${MYCODO_PATH}"/env/bin/pybabel compile -d mycodo_flask/translations
    ;;
    'create-files-directories')
        printf "\n#### Creating files and directories\n"
        mkdir -p "${MYCODO_PATH}/logs"
        mkdir -p "${MYCODO_PATH}/backups"
        mkdir -p "${MYCODO_PATH}"/install
        mkdir -p "${MYCODO_PATH}"/mycodo
        mkdir -p "${MYCODO_PATH}"/databases
        mkdir -p "${MYCODO_PATH}"/note_attachments
        mkdir -p "${MYCODO_PATH}"/mycodo/scripts
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/ssl_certs
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/static/js/user_js
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/static/css/user_css

        if [[ ! -e ${MYCODO_PATH}/logs/mycodo.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodo.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodobackup.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodobackup.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodokeepup.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodokeepup.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycododependency.log ]]; then
            touch ${MYCODO_PATH}/logs/mycododependency.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodoupgrade.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodoupgrade.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodorestore.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodorestore.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/login.log ]]; then
            touch ${MYCODO_PATH}/logs/login.log
        fi

        # Create empty mycodo database file if it doesn't exist
        if [[ ! -e ${MYCODO_PATH}/databases/mycodo.db ]]; then
            touch "${MYCODO_PATH}/databases/mycodo.db"
        fi
    ;;
    'generate-widget-html')
        printf "\n#### Generating widget HTML files\n"
        "${MYCODO_PATH}"/env/bin/python "${MYCODO_PATH}"/mycodo/utils/widget_generate_html.py
    ;;
    'initialize')
        printf "\n#### Running initialization\n"
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh compile-mycodo-wrapper
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh create-files-directories
    ;;
    'restart-daemon')
        printf "\n#### Restarting the Mycodo daemon\n"
        service mycodo restart
    ;;
    'setup-virtualenv')
        printf "\n#### Checking python 3 virtualenv\n"
        if [[ ! -e ${MYCODO_PATH}/env/bin/python3 ]]; then
            printf "#### Virtualenv doesn't exist. Creating...\n"
            python3 -m pip install virtualenv==${VIRTUALENV_VERSION}
            rm -rf "${MYCODO_PATH}"/env
            python3 -m virtualenv -p "${PYTHON_BINARY_SYS_LOC}" "${MYCODO_PATH}"/env
        else
            printf "#### Virtualenv already exists, skipping creation\n"
        fi
    ;;
    'setup-virtualenv-full')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh setup-virtualenv
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh update-pip3-packages
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh update-dependencies
    ;;
    'ssl-certs-generate')
        printf "\n#### Generating SSL certificates at %s/mycodo/mycodo_flask/ssl_certs (replace with your own if desired)\n" "${MYCODO_PATH}"
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/ssl_certs
        cd "${MYCODO_PATH}"/mycodo/mycodo_flask/ssl_certs/ || return
        rm -f ./*.pem ./*.csr ./*.crt ./*.key

        openssl genrsa -out server.pass.key 4096
        openssl rsa -in server.pass.key -out server.key
        rm -f server.pass.key
        openssl req -new -key server.key -out server.csr \
            -subj "/O=mycodo/OU=mycodo/CN=mycodo"
        openssl x509 -req \
            -days 3653 \
            -in server.csr \
            -signkey server.key \
            -out server.crt
    ;;
    'ssl-certs-regenerate')
        printf "\n#### Regenerating SSL certificates at %s/mycodo/mycodo_flask/ssl_certs\n" "${MYCODO_PATH}"
        rm -rf "${MYCODO_PATH}"/mycodo/mycodo_flask/ssl_certs/*.pem
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh ssl-certs-generate
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh initialize
        sudo service nginx restart
        sudo service mycodoflask restart
    ;;
    'uninstall-apt-pip')
        printf "\n#### Uninstalling apt version of pip (if installed)\n"
        sudo apt purge -y python-pip
    ;;
    'update-alembic')
        printf "\n#### Upgrading Mycodo database with alembic (if needed)\n"
        cd "${MYCODO_PATH}"/alembic_db || return
        "${MYCODO_PATH}"/env/bin/alembic upgrade head
    ;;
    'update-alembic-post')
        printf "\n#### Executing post-alembic script\n"
        "${MYCODO_PATH}"/env/bin/python "${MYCODO_PATH}"/alembic_db/alembic_post.py
    ;;
    'update-apt')
        printf "\n#### Updating apt repositories\n"
        sudo apt update -y
    ;;
    'update-cron')  # TODO: Remove at next major revision
        printf "\n#### Remove Mycodo restart monitor crontab entry (if it exists)\n"
        /bin/bash "${MYCODO_PATH}"/install/crontab.sh restart_daemon --remove
    ;;
    'update-dependencies')
        printf "\n#### Checking for updates to dependencies\n"
        "${MYCODO_PATH}"/env/bin/python "${MYCODO_PATH}"/mycodo/utils/update_dependencies.py
    ;;
    'install-bcm2835')
        printf "\n#### Installing bcm2835\n"
        cd "${MYCODO_PATH}"/install || return
        sudo apt install -y automake libtool
        wget ${MCB2835_URL} -O bcm2835.tar.gz
        mkdir bcm2835
        tar xzf bcm2835.tar.gz -C bcm2835 --strip-components=1
        cd bcm2835 || return
        autoreconf -vfi
        ./configure
        make
        sudo make check
        sudo make install
        cd "${MYCODO_PATH}"/install || return
        rm -rf ./bcm2835
    ;;
    'install-wiringpi')
        if [[ ${MACHINE_TYPE} == 'armhf' ]]; then
            cd "${MYCODO_PATH}"/install || return
            wget ${WIRINGPI_URL} -O wiringpi-latest.deb
            dpkg -i wiringpi-latest.deb
        else
            printf "\n#### WiringPi not supported on this architecture, skipping.\n"
        fi
    ;;
    'build-pigpiod')
        sudo apt install -y python3-pigpio
        cd "${MYCODO_PATH}"/install || return
        # wget --quiet -P "${MYCODO_PATH}"/install abyz.co.uk/rpi/pigpio/pigpio.zip
        wget ${PIGPIO_URL} -O pigpio.tar.gz
        mkdir PIGPIO
        tar xzf pigpio.tar.gz -C PIGPIO --strip-components=1
        cd "${MYCODO_PATH}"/install/PIGPIO || return
        make -j4
        make install
        cd "${MYCODO_PATH}"/install || return
        rm -rf ./PIGPIO
        rm -rf pigpio.tar.gz
    ;;
    'install-pigpiod')
        printf "\n#### Installing pigpiod\n"
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh build-pigpiod
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh disable-pigpiod
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh enable-pigpiod-high
        mkdir -p /opt/mycodo
        touch /opt/mycodo/pigpio_installed
    ;;
    'uninstall-pigpiod')
        printf "\n#### Uninstalling pigpiod\n"
        sudo apt remove -y python3-pigpio
        sudo apt install -y jq
        cd "${MYCODO_PATH}"/install || return
        # wget --quiet -P "${MYCODO_PATH}"/install abyz.co.uk/rpi/pigpio/pigpio.zip
        wget ${PIGPIO_URL} -O pigpio.tar.gz
        mkdir PIGPIO
        tar xzf pigpio.tar.gz -C PIGPIO --strip-components=1
        cd "${MYCODO_PATH}"/install/PIGPIO || return
        make uninstall
        cd "${MYCODO_PATH}"/install || return
        rm -rf ./PIGPIO
        rm -rf pigpio.tar.gz
        touch /etc/systemd/system/pigpiod_uninstalled.service
        rm -f /opt/mycodo/pigpio_installed
    ;;
    'disable-pigpiod')
        printf "\n#### Disabling installed pigpiod startup script\n"
        service pigpiod stop
        systemctl disable pigpiod.service
        rm -rf /etc/systemd/system/pigpiod.service
        systemctl disable pigpiod_low.service
        rm -rf /etc/systemd/system/pigpiod_low.service
        systemctl disable pigpiod_high.service
        rm -rf /etc/systemd/system/pigpiod_high.service
        rm -rf /etc/systemd/system/pigpiod_disabled.service
        rm -rf /etc/systemd/system/pigpiod_uninstalled.service
    ;;
    'enable-pigpiod-low')
        printf "\n#### Enabling pigpiod startup script (1 ms sample rate)\n"
        systemctl enable "${MYCODO_PATH}"/install/pigpiod_low.service
        service pigpiod restart
    ;;
    'enable-pigpiod-high')
        printf "\n#### Enabling pigpiod startup script (5 ms sample rate)\n"
        systemctl enable "${MYCODO_PATH}"/install/pigpiod_high.service
        service pigpiod restart
    ;;
    'enable-pigpiod-disabled')
        printf "\n#### pigpiod has been disabled. It can be enabled in the web UI configuration\n"
        touch /etc/systemd/system/pigpiod_disabled.service
    ;;
    'update-pigpiod')
        printf "\n#### Checking which pigpiod startup script is being used\n"
        GPIOD_SAMPLE_RATE=99
        if [[ -e /etc/systemd/system/pigpiod_low.service ]]; then
            GPIOD_SAMPLE_RATE=1
        elif [[ -e /etc/systemd/system/pigpiod_high.service ]]; then
            GPIOD_SAMPLE_RATE=5
        elif [[ -e /etc/systemd/system/pigpiod_disabled.service ]]; then
            GPIOD_SAMPLE_RATE=100
        fi

        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh disable-pigpiod

        if [[ "$GPIOD_SAMPLE_RATE" -eq "1" ]]; then
            /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh enable-pigpiod-low
        elif [[ "$GPIOD_SAMPLE_RATE" -eq "5" ]]; then
            /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh enable-pigpiod-high
        elif [[ "$GPIOD_SAMPLE_RATE" -eq "100" ]]; then
            /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh enable-pigpiod-disabled
        else
            printf "#### Could not determine pgiod sample rate. Setting up pigpiod with 1 ms sample rate\n"
            /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_commands.sh enable-pigpiod-low
        fi
    ;;
    'update-influxdb')
        printf "\n#### Ensuring compatible version of influxdb is installed ####\n"
        INSTALL_ADDRESS="https://dl.influxdata.com/influxdb/releases/"
        INSTALL_FILE="influxdb_${INFLUXDB_VERSION}_${MACHINE_TYPE}.deb"
        CORRECT_VERSION="${INFLUXDB_VERSION}-1"
        CURRENT_VERSION=$(apt-cache policy influxdb | grep 'Installed' | gawk '{print $2}')
        if [[ "${CURRENT_VERSION}" != "${CORRECT_VERSION}" ]]; then
            echo "#### Incorrect InfluxDB version (v${CURRENT_VERSION}) installed. Installing v${CORRECT_VERSION}..."
            wget --quiet "${INSTALL_ADDRESS}${INSTALL_FILE}"
            dpkg -i "${INSTALL_FILE}"
            rm -rf "${INSTALL_FILE}"
            service influxdb restart
        else
            printf "Correct version of InfluxDB currently installed\n"
        fi
    ;;

    'update-influxdb-db-user')
        printf "\n#### Creating InfluxDB database and user\n"
        # Attempt to connect to influxdb 10 times, sleeping 60 seconds every fail
        for _ in {1..10}; do
            # Check if influxdb has successfully started and be connected to
            printf "#### Attempting to connect...\n" &&
            curl -sL -I localhost:8086/ping > /dev/null &&
            influx -execute "CREATE DATABASE mycodo_db" &&
            influx -database mycodo_db -execute "CREATE USER mycodo WITH PASSWORD 'mmdu77sj3nIoiajjs'" &&
            printf "#### Influxdb database and user successfully created\n" &&
            break ||
            # Else wait 60 seconds if the influxd port is not accepting connections
            # Everything below will begin executing if an error occurs before the break
            printf "#### Could not connect to Influxdb. Waiting 60 seconds then trying again...\n" &&
            sleep 60
        done
    ;;
    'update-logrotate')
        printf "\n#### Installing logrotate scripts\n"
        if [[ -e /etc/cron.daily/logrotate ]]; then
            printf "logrotate execution moved from cron.daily to cron.hourly\n"
            mv -f /etc/cron.daily/logrotate /etc/cron.hourly/
        fi
        cp -f "${MYCODO_PATH}"/install/logrotate_mycodo /etc/logrotate.d/mycodo
        printf "Mycodo logrotate script installed\n"
    ;;
    'update-mycodo-startup-script')
        printf "\n#### Disabling installed mycodo startup script\n"
        systemctl disable mycodo.service
        rm -rf /etc/systemd/system/mycodo.service
        printf "#### Enabling current mycodo startup script\n"
        systemctl enable "${MYCODO_PATH}"/install/mycodo.service
    ;;
    'update-packages')
        printf "\n#### Installing prerequisite apt packages and update pip\n"
        sudo apt remove -y apache2 python-cffi-backend python3-cffi-backend
        sudo apt install -y ${APT_PKGS}
    ;;
    'update-permissions')
        printf "\n#### Setting permissions\n"
        chown -LR mycodo.mycodo "${MYCODO_PATH}"
        chown -R mycodo.mycodo /var/log/mycodo
        chown -R mycodo.mycodo /var/Mycodo-backups
        chown -R influxdb.influxdb /var/lib/influxdb/data/

        find "${MYCODO_PATH}" -type d -exec chmod u+wx,g+wx {} +
        find "${MYCODO_PATH}" -type f -exec chmod u+w,g+w,o+r {} +

        chown root:mycodo "${MYCODO_PATH}"/mycodo/scripts/mycodo_wrapper
        chmod 4770 "${MYCODO_PATH}"/mycodo/scripts/mycodo_wrapper
    ;;
    'update-pip3')
        printf "\n#### Updating pip\n"
        "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade pip
    ;;
    'update-pip3-packages')
        printf "\n#### Installing pip requirements\n"
        if [[ ! -d ${MYCODO_PATH}/env ]]; then
            printf "\n## Error: Virtualenv doesn't exist. Create with %s setup-virtualenv\n" "${0}"
        else
            "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade pip setuptools=="${SETUPTOOLS_VERSION}"
            "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade -r "${MYCODO_PATH}"/install/requirements.txt
            "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade -r "${MYCODO_PATH}"/install/requirements-rpi.txt
            "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade -r "${MYCODO_PATH}"/install/requirements-testing.txt
        fi
    ;;
    'update-swap-size')
        printf "\n#### Checking if swap size is 100 MB and needs to be changed to 512 MB\n"
        if grep -q -s "CONF_SWAPSIZE=100" "/etc/dphys-swapfile"; then
            printf "#### Swap currently set to 100 MB. Changing to 512 MB and restarting\n"
            sed -i 's/CONF_SWAPSIZE=100/CONF_SWAPSIZE=512/g' /etc/dphys-swapfile
            /etc/init.d/dphys-swapfile stop
            /etc/init.d/dphys-swapfile start
        else
            printf "#### Swap not currently set to 100 MB. Not changing.\n"
        fi
    ;;
    'upgrade-mycodo')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_download.sh upgrade-release-major "${MYCODO_MAJOR_VERSION}"
    ;;
    'upgrade-release-major')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_download.sh upgrade-release-major "${2}"
    ;;
    'upgrade-release-wipe')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_download.sh upgrade-release-wipe "${2}"
    ;;
    'upgrade-master')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_download.sh force-upgrade-master
    ;;
    'upgrade-post')
        /bin/bash "${MYCODO_PATH}"/mycodo/scripts/upgrade_post.sh
    ;;
    'web-server-connect')
        printf "\n#### Connecting to http://localhost (creates Mycodo database if it doesn't exist)\n"
        # Attempt to connect to localhost 10 times, sleeping 60 seconds every fail
        for _ in {1..10}; do
            wget --quiet --no-check-certificate -p http://localhost/ -O /dev/null &&
            printf "#### Successfully connected to http://localhost\n" &&
            break ||
            # Else wait 60 seconds if localhost is not accepting connections
            # Everything below will begin executing if an error occurs before the break
            printf "#### Could not connect to http://localhost. Waiting 60 seconds then trying again (up to 10 times)...\n" &&
            sleep 60 &&
            printf "#### Trying again...\n"
        done
    ;;
    'web-server-reload')
        printf "\n#### Restarting nginx\n"
        service nginx restart
        sleep 5
        printf "#### Reloading mycodoflask\n"
        service mycodoflask reload
    ;;
    'web-server-restart')
        printf "\n#### Restarting nginx\n"
        service nginx restart
        sleep 5
        printf "#### Restarting mycodoflask\n"
        service mycodoflask restart
    ;;
    'web-server-update')
        printf "\n#### Installing and configuring nginx web server\n"
        systemctl disable mycodoflask.service
        rm -rf /etc/systemd/system/mycodoflask.service
        ln -sf "${MYCODO_PATH}"/install/mycodoflask_nginx.conf /etc/nginx/sites-enabled/default
        systemctl enable nginx
        systemctl enable "${MYCODO_PATH}"/install/mycodoflask.service
    ;;


    #
    # Docker-specific commands
    #

    'docker-create-files-directories-symlinks')
        printf "\n#### Creating files and directories\n"
        mkdir -p /var/log/mycodo
        mkdir -p /var/Mycodo-backups
        mkdir -p /usr/local/mycodo

        mkdir -p "${MYCODO_PATH}"/install
        mkdir -p "${MYCODO_PATH}"/mycodo
        mkdir -p "${MYCODO_PATH}"/databases
        mkdir -p "${MYCODO_PATH}"/note_attachments
        mkdir -p "${MYCODO_PATH}"/mycodo/scripts
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/static/js/user_js
        mkdir -p "${MYCODO_PATH}"/mycodo/mycodo_flask/static/css/user_css

        if [[ ! -e ${MYCODO_PATH}/logs/mycodo.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodo.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodobackup.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodobackup.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodokeepup.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodokeepup.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycododependency.log ]]; then
            touch ${MYCODO_PATH}/logs/mycododependency.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodoupgrade.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodoupgrade.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/mycodorestore.log ]]; then
            touch ${MYCODO_PATH}/logs/mycodorestore.log
        fi
        if [[ ! -e ${MYCODO_PATH}/logs/login.log ]]; then
            touch ${MYCODO_PATH}/logs/login.log
        fi

        # Create empty mycodo database file if it doesn't exist
        if [[ ! -e /home/mycodo/databases/mycodo.db ]]; then
            touch /home/mycodo/databases/mycodo.db
        fi

        ln -sfn "${MYCODO_PATH}" /var/mycodo-root
    ;;
    'docker-compile-translations')
        printf "\n#### Compiling Translations\n"
        cd "${MYCODO_PATH}"/mycodo || exit
        "${MYCODO_PATH}"/env/bin/pybabel compile -d mycodo_flask/translations
    ;;
    'docker-update-pip')
        printf "\n#### Updating pip\n"
        "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade pip
    ;;
    'docker-update-pip-packages')
        printf "\n#### Installing pip requirements\n"
        "${MYCODO_PATH}"/env/bin/python -m pip install --upgrade pip setuptools=="${SETUPTOOLS_VERSION}"
        "${MYCODO_PATH}"/env/bin/python -m pip install --no-cache-dir -r /home/mycodo/install/requirements.txt
    ;;
    'install-docker-ce-cli')
        printf "\n#### Installing Docker Client\n"
        sudo apt update
        sudo apt -y install \
            apt-transport-https \
            ca-certificates \
            curl \
            gnupg2 \
            software-properties-common
        curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -

        if [[ ${UNAME_TYPE} == 'x86_64' ]]; then
            sudo add-apt-repository -y \
               "deb [arch=amd64] https://download.docker.com/linux/debian \
               $(lsb_release -cs) \
               stable"
        elif [[ ${MACHINE_TYPE} == 'armhf' ]]; then
            add-apt-repository -y \
               "deb [arch=armhf] https://download.docker.com/linux/debian \
               $(lsb_release -cs) \
               stable"
        elif [[ ${MACHINE_TYPE} == 'arm64' ]]; then
            add-apt-repository -y \
               "deb [arch=arm64] https://download.docker.com/linux/debian \
               $(lsb_release -cs) \
               stable"
        else
            printf "\nCould not detect architecture\n"
            exit 1
        fi
        apt update
        apt -y install docker-ce-cli
    ;;
    *)
        printf "Error: Unrecognized command: %s\n%s" "${1}" "${HELP_OPTIONS}"
    ;;
esac
