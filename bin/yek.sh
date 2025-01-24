#!/bin/bash
# Run the yek tool

# determine script directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ] ; do SOURCE="$(readlink "$SOURCE")"; done
SCRIPT_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

pushd "$SCRIPT_DIR/.." > /dev/null || exit 1

yek --max-size 32000 --tokens

popd > /dev/null || exit 1