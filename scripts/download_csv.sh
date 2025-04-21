#!/bin/bash
set -e

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
LIST_FILE="$SCRIPT_DIR/list.txt"
WORKDIR="$SCRIPT_DIR/../data"

mkdir -p "$WORKDIR"

while read -r url; do
  filename=$(basename "$url")
  zip_path="$WORKDIR/$filename"

  echo "Downloading $url..."
  curl -sSL "$url" -o "$zip_path"

  echo "Unzipping $zip_path..."
  unzip -o "$zip_path" -d "$WORKDIR"

  echo "Removing $zip_path..."
  rm -f "$zip_path"
done <"$LIST_FILE"
