#!/usr/bin/env bash
# Script to build the latest image of the VM for running obscuro test
#

set -euo pipefail

script_path="$(cd "$(dirname "${0}")" && pwd)"
root_path="${script_path}/../../"

# build the wallet extension
${root_path}/get_artifacts.sh

# build the docker container
docker build -t obscuronet/obscuro_test:latest -f ${script_path}/image.Dockerfile "${root_path}"
