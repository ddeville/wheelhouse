#!/bin/bash

set -eu -o pipefail

python -m pip install cibuildwheel==2.22.0

export CIBW_BUILD='cp312-*'
export CIBW_SKIP='*-musllinux_* *-manylinux_i686 *-manylinux_ppc64le *-manylinux_s390x *-manylinux_armv7l'

mkdir sdist
mkdir wheelhouse

curl -L "$1" | tar xzvf - --strip-components=1 -C sdist

pushd sdist
python -m cibuildwheel --output-dir ../wheelhouse
popd

if [ "$(find wheelhouse -type f -name '*.whl' | wc -l)" -ne 1 ]; then
  echo "Expected exactly one wheel, but found $(find wheelhouse -type f -name '*.whl')"
  exit 1
fi
