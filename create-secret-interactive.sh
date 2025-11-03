#!/bin/bash

# Interactive script to create portfolio-analyzer-secrets in Kubernetes
# This script will prompt for sensitive values instead of reading from .env

set -e

echo "🔐 Portfolio Analyzer - Kubernetes Secret Creation"
echo "=================================================="
echo ""
echo "This script will create the 'portfolio-analyzer-secrets' in Kubernetes."
echo ""

# Check kubectl connection
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ Error: Cannot connect to Kubernetes cluster"
    echo "Please ensure kubectl is configured correctly"
    exit 1
fi

CURRENT_CONTEXT=$(kubectl config current-context)
echo "Current Kubernetes context: $CURRENT_CONTEXT"
echo ""

# Confirm context
read -p "Is this the correct cluster? (yes/no): " CONFIRM
if [ "$CONFIRM" != "yes" ]; then
    echo "Aborted"
    exit 1
fi

echo ""
echo "Please provide the following values:"
echo ""

# Database URL
echo "Database URL for Kubernetes (use postgres-service as host):"
read -p "Database URL [postgresql://postgresadmin:admin10.@postgres-service:5432/portfoliodb]: " DATABASE_URL
DATABASE_URL=${DATABASE_URL:-postgresql://postgresadmin:admin10.@postgres-service:5432/portfoliodb}

# OpenAI API Key
echo ""
echo "OpenAI API Key (starts with sk-proj- or sk-):"
read -s -p "OpenAI API Key: " OPENAI_KEY
echo ""

# Anthropic API Key (optional)
echo ""
echo "Anthropic API Key (optional, press Enter to skip):"
read -s -p "Anthropic API Key: " ANTHROPIC_KEY
echo ""

# Validate
if [ -z "$OPENAI_KEY" ] && [ -z "$ANTHROPIC_KEY" ]; then
    echo ""
    echo "❌ Error: At least one API key (OpenAI or Anthropic) is required"
    exit 1
fi

echo ""
echo "Creating secret in namespace: default"

# Create the secret
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url="$DATABASE_URL" \
  --from-literal=openai-api-key="$OPENAI_KEY" \
  --from-literal=anthropic-api-key="$ANTHROPIC_KEY" \
  --namespace=default \
  --dry-run=client -o yaml | kubectl apply -f -

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Secret 'portfolio-analyzer-secrets' created/updated successfully!"
    echo ""
    echo "Verify with:"
    echo "  kubectl get secret portfolio-analyzer-secrets -n default"
    echo ""
    echo "You can now proceed with deployment (git push)"
else
    echo ""
    echo "❌ Error creating secret"
    exit 1
fi
