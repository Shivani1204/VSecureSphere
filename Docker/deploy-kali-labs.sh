#!/bin/bash

set -e

BASE_DIR=$(pwd)
LAB_DIR="Kali"

echo "🚀 Deploying Kubernetes Kali labs (apply-if-not-exists)"
echo "====================================================="

resource_exists() {
  KIND=$1
  NAME=$2
  kubectl get "$KIND" "$NAME" >/dev/null 2>&1
}

if [ ! -d "$LAB_DIR" ]; then
  echo "❌ Directory '$LAB_DIR' not found"
  exit 1
fi

for LAB_FOLDER in "$LAB_DIR"/*; do
  [ -d "$LAB_FOLDER" ] || continue

  echo "📁 Lab: $(basename "$LAB_FOLDER")"
  cd "$LAB_FOLDER"

  for FILE in *.y*ml; do
    [ -f "$FILE" ] || continue

    KIND=$(grep -m1 '^kind:' "$FILE" | awk '{print $2}')
    NAME=$(grep -m1 '^  name:' "$FILE" | awk '{print $2}')

    if [[ "$KIND" == "Deployment" || "$KIND" == "Service" ]]; then
      if resource_exists "${KIND,,}" "$NAME"; then
        echo "⏭️  $KIND/$NAME already exists → skipping"
      else
        echo "✅ Creating $KIND/$NAME"
        kubectl apply -f "$FILE"
      fi
    fi
  done

  echo "-----------------------------------------------------"
  cd "$BASE_DIR"
done

echo "🎉 Kali lab deployment completed"

