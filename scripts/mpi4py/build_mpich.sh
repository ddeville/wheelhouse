#!/bin/bash

set -eu -o pipefail

MPICH_VERSION=4.2.3
MPICH_HASH=7a019180c51d1738ad9c5d8d452314de65e828ee240bcb2d1f80de9a65be88a8

pushd /tmp

curl -LO https://github.com/pmodels/mpich/releases/download/v${MPICH_VERSION}/mpich-${MPICH_VERSION}.tar.gz
echo "${MPICH_HASH}  mpich-${MPICH_VERSION}.tar.gz" | shasum -a 256 --check -

tar -xzf mpich-${MPICH_VERSION}.tar.gz

pushd mpich-${MPICH_VERSION}

PREFIX=/usr/local

mkdir -p $PREFIX

./configure \
  --prefix=$PREFIX \
  --disable-dependency-tracking \
  --disable-fortran \
  --disable-maintainer-mode \
  --disable-option-checking \
  --disable-rpath \
  --disable-silent-rules \
  --disable-wrapper-rpath \
  --enable-fast=all,O3 \
  --enable-g=dbg \
  --enable-romio \
  --enable-shared \
  --with-pm=hydra \
  --with-wrapper-dl-type=none \
  --without-pmix \
  --without-yaksa

make -j "$(env -i PATH="$PATH" nproc)"
make install

popd

popd
