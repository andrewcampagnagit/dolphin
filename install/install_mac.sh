#! /bin/bash

if [[ $# > 0 ]]; then
	VERSION="mac-$1"

else
	VERSION="mac-latest"
fi

DL_URL="https://github.com/andrewcampagnagit/dolphin/raw/beta-3/releases/${VERSION}.zip"
wget $DL_URL -O ${VERSION}.zip

