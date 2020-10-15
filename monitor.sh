#!/bin/bash

# Ejecuta tweeter streamer y si se para ejecución
# por excepción lo ejecuta de nuevo automáticamente

# Es necesario ejecutar como SuperUSer: $ sudo su
# Después Ejecutar en terminal: $ sudo nohup ./monitor.sh &

myscript(){
    python twitter_stream_download.py -q proptech -d proptech
}

until myscript; do
    echo "'myscript' crashed with exit code $?. Restarting..." >&2
    sleep 1
done