#!/bin/bash
LOGROOT="/public/home/c14009/action/log"
#LOGROOT="/home/amax/haidongxu/python/log"
LOGNAME="auto.log"
time=`date +%Y-%m-%d_%H:%M:%S`
PIDFILE="${LOGROOT}/teacher_gunicorn.pid"
echo $PIDFILE
if [ -f $PIDFILE ]; then
    echo "teacher pid file exists...."
    PID=$(cat $PIDFILE)
    echo "["${time}"] teacher pid: $PID, stop"    >> ${LOGROOT}/${LOGNAME}
    kill -TERM $PID
fi
PIDFILE="${LOGROOT}/student_gunicorn.pid"
if [ -f $PIDFILE ]; then
    echo "student pid file exists...."
    PID=$(cat $PIDFILE)
    echo "["${time}"] student pid: $PID, stop"    >> ${LOGROOT}/${LOGNAME}
    kill -TERM $PID
fi
PIDFILE="${LOGROOT}/other_gunicorn.pid"
if [ -f $PIDFILE ]; then
    echo "other pid file exists...."
    PID=$(cat $PIDFILE)
    echo "["${time}"] other pid: $PID, stop"    >> ${LOGROOT}/${LOGNAME}
    kill -TERM $PID
fi

