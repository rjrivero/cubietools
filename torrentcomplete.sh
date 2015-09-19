#!/usr/bin/env bash

# Asumimos que el script se almacena dentro de la carpeta del virtualenv
export CWD=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source "${CWD}/../bin/activate"
exec python ${CWD}/torrentcomplete.py
