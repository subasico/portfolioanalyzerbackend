#!/bin/bash

# Script to create portfolio-analyzer-secrets in Kubernetes
# Usage: ./create-k8s-secret.sh

set -e

echo "🔐 Creating portfolio-analyzer-secrets in Kubernetes..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found!"
    exit 1
fi

# Load environment variables from .env
export $(cat .env | grep -v '^#' | xargs)

# Validate required variables
if [ -z "$DATABASE_URL" ]; then
    echo "❌ Error: DATABASE_URL not set in .env"
    exit 1
fi

if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ Error: At least one API key (OPENAI_API_KEY or ANTHROPIC_API_KEY) must be set in .env"
    exit 1
fi

echo "Creating secret in namespace: default"
echo ""

# Create the secret
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=openai-api-key="${OPENAI_API_KEY:-}" \
  --from-literal=anthropic-api-key="${ANTHROPIC_API_KEY:-}" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

echo ""
echo "✅ Secret 'portfolio-analyzer-secrets' created/updated successfully!"
echo ""
echo "Verify with: kubectl get secret portfolio-analyzer-secrets -n default"
echo "View keys with: kubectl get secret portfolio-analyzer-secrets -n default -o jsonpath='{.data}' | jq 'keys'"
