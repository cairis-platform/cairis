#!/bin/bash
set -e

# Get version from parameter
VERSION=$1

if [[ "$VERSION" == "" ]]; then
	VERSION=latest
fi

# Copy from local repo
cp -R ../cairis ./

# Build
docker build -t shamalfaily/cairis:$VERSION -f Dockerfile.local .

# Clean up
rm -rf cairis
