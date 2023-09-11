#! /bin/bash

ARCH="$(dpkg-architecture -q DEB_BUILD_ARCH)"
DIST="$(. /etc/os-release; echo ${VERSION_CODENAME/*, /})"

cd repo
reprepro list "$DIST" | awk '{print "sudo apt-get install -y "$2}' | sh
