#!/bin/bash

# Script to create GitHub Container Registry pull secret in Kubernetes
# Usage: ./create-ghcr-secret.sh <github-username> <github-token>

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <github-username> <github-personal-access-token>"
    echo ""
    echo "To create a Personal Access Token (PAT):"
    echo "1. Go to https://github.com/settings/tokens/new"
    echo "2. Select scope: 'read:packages'"
    echo "3. Generate token and use it here"
    exit 1
fi

GITHUB_USERNAME=$1
GITHUB_TOKEN=$2
NAMESPACE=${3:-default}

echo "Creating GitHub Container Registry pull secret..."

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username="$GITHUB_USERNAME" \
  --docker-password="$GITHUB_TOKEN" \
  --docker-email="$GITHUB_USERNAME@users.noreply.github.com" \
  --namespace="$NAMESPACE" \
  --dry-run=client -o yaml | kubectl apply -f -

echo "✅ Secret 'ghcr-secret' created successfully in namespace '$NAMESPACE'"
echo ""
echo "Verify with: kubectl get secret ghcr-secret -n $NAMESPACE"
