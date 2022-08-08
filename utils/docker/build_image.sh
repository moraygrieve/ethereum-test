#!/usr/bin/env bash

set -euo pipefail

script_path="$(cd "$(dirname "${0}")" && pwd)"
root_path="${script_path}/../../"

docker build -t testnetobscuronet.azurecr.io/obscuronet/obscuro_test:latest -f ./image.Dockerfile "${root_path}"
