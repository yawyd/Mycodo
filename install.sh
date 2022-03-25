#
#  install - Mycodo install script
#
#  Do not execute this script if the Mycodo archive has been downloaded and extracted.
#  If Mycodo has been extracted (~/Mycodo/ already exists), then execute:
#
#  sudo /bin/bash ~/Mycodo/install/setup.sh
#
#
#  If Mycodo has not yet been downloaded/extracted, execute the following to install:
#
#  curl -L https://kizniche.github.io/Mycodo/install | bash
#

INSTALL_DIRECTORY=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd -P )

if [ "$EUID" -eq 0 ]; then
    printf "Do not run as root. Run as non-root user: \"/bin/bash %s/install\"\n" "${INSTALL_DIRECTORY}"
    exit 1
fi

if [ -d ~/Mycodo ]; then
  printf "## Error: Install aborted. Cause: The ~/Mycodo directory already exists. The install cannot continue because a previous Mycodo install was detected. Please either move or delete the ~/Mycodo directory and rerun this script to initiate the install or run ~/Mycodo/install/setup.sh.\n"
  exit 1
fi

sudo apt update
sudo apt install -y jq whiptail python3

cd ~
curl -s https://api.github.com/repos/kizniche/Mycodo/releases/latest | \
jq -r '.tarball_url' | wget -i - -O mycodo-latest.tar.gz
mkdir Mycodo
tar xzf mycodo-latest.tar.gz -C Mycodo --strip-components=1
rm -f mycodo-latest.tar.gz
cd Mycodo/install
sudo /bin/bash ./setup.sh
