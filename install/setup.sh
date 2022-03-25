#!/bin/bash
#
#  setup.sh - Mycodo install script
#
#  Usage: sudo /bin/bash ~/Mycodo/install/setup.sh
#

INSTALL_DIRECTORY="./Mycodo"
INSTALL_CMD="/bin/bash ${INSTALL_DIRECTORY}/mycodo/scripts/upgrade_commands.sh"
LOG_LOCATION=${INSTALL_DIRECTORY}/install/setup.log


set -e

# 确保swap够大
# ${INSTALL_CMD} update-swap-size 2>&1 | tee -a "${LOG_LOCATION}" 

# apt update
${INSTALL_CMD} update-apt 2>&1 | tee -a "${LOG_LOCATION}"

# install apt packages
${INSTALL_CMD} update-packages 2>&1 | tee -a "${LOG_LOCATION}"

# 创建 env, python > 3.6
${INSTALL_CMD} setup-virtualenv 2>&1 | tee -a "${LOG_LOCATION}"

${INSTALL_CMD} update-pip3 2>&1 | tee -a "${LOG_LOCATION}"
${INSTALL_CMD} update-pip3-packages 2>&1 | tee -a "${LOG_LOCATION}"
${INSTALL_CMD} install-wiringpi 2>&1 | tee -a "${LOG_LOCATION}"

${INSTALL_CMD} initialize 2>&1 | tee -a "${LOG_LOCATION}"


sudo apt install ow-shell # one wire devices
# 处理积累的日志
#${INSTALL_CMD} update-logrotate 2>&1 | tee -a "${LOG_LOCATION}"

# ${INSTALL_CMD} ssl-certs-generate 2>&1 | tee -a "${LOG_LOCATION}"

# 使用 service的方式启动 mycodo
# ${INSTALL_CMD} update-mycodo-startup-script 2>&1 | tee -a "${LOG_LOCATION}"

# 翻译
# ${INSTALL_CMD} compile-translations 2>&1 | tee -a "${LOG_LOCATION}"

# 生成html文件，需要把Mycodo安装文件夹加入到PYTHONPATH
${INSTALL_CMD} generate-widget-html 2>&1 | tee -a "${LOG_LOCATION}"

${INSTALL_CMD} initialize 2>&1 | tee -a "${LOG_LOCATION}"

# 设置nginx service
# ${INSTALL_CMD} web-server-update 2>&1 | tee -a "${LOG_LOCATION}"
# ${INSTALL_CMD} web-server-restart 2>&1 | tee -a "${LOG_LOCATION}"
# ${INSTALL_CMD} web-server-connect 2>&1 | tee -a "${LOG_LOCATION}"

# ${INSTALL_CMD} restart-daemon 2>&1 | tee -a "${LOG_LOCATION}"


# 需要先启动 mycodo_flask.py来生成 sqlite db记录，再启动mycodo_daemon.py