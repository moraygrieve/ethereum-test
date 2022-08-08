#!/usr/bin/env bash

set -euo pipefail
cwd_path=`pwd`
root_path=`pwd`/../..

docker build -t testnetobscuronet.azurecr.io/obscuronet/obscuro_test:latest -f ./image.Dockerfile "${root_path}"
