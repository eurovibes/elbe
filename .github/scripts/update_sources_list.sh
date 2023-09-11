#! /bin/bash

DIST="$(. /etc/os-release; echo ${VERSION_CODENAME/*, /})"

echo "deb [trusted=yes] file://$(pwd)/repo ${DIST} main" \
     > /etc/apt/sources.list.d/elbe.list

apt-get update
