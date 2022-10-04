#!/usr/bin/env bash
set -euo pipefail # -x

grep -r "2022-07-13T05:30:00.000000Z GET /" | grep "front-app.front"