#!/bin/bash

set -eu -o pipefail

python -m pip install build==1.2.2

mkdir sdist
mkdir wheelhouse

curl -L "$1" | tar xzvf - --strip-components=1 -C sdist

pushd sdist
python -m build --wheel . -o ../wheelhouse
popd
