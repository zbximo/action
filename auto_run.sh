#!/bin/bash
ROOT="/public/home/c14009/action"
LOG_ROOT="/public/home/c14009/action/log"
ANACONDA_ROOT="/opt/conda/bin/"

#ROOT="/home/amax/haidongxu/python"
#LOG_ROOT="/home/amax/haidongxu/python/log"
#ANACONDA_ROOT="/opt/anaconda3/bin"

LOG_NAME="auto.log"
time=`date +%Y-%m-%d_%H:%M:%S`

source ${ANACONDA_ROOT}/activate action && gunicorn -c gunicorn_teacher.py --daemon run_teacher:app
source ${ANACONDA_ROOT}/activate action && gunicorn -c gunicorn_student.py --daemon run_student:app
source ${ANACONDA_ROOT}/activate action && gunicorn -c gunicorn_other.py --daemon run_other:app
echo "["${time}"] restart"  >> ${LOG_ROOT}/${LOG_NAME}



