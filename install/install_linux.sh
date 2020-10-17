#! /bin/bash

if [[ $# > 0 ]]; then
	VERSION="linux-$1"

else
	VERSION="linux-latest"
fi

echo $VERSION