# Portfolio Analyzer - GHCR Migration Summary

## ✅ Migration Complete!

Successfully migrated from Azure Container Registry (ACR) to **GitHub Container Registry (GHCR)**.

## 🔄 What Changed

### Before (ACR)
- Required Azure Container Registry setup
- Needed ACR_USERNAME and ACR_PASSWORD secrets
- More complex authentication
- Additional Azure resource to manage
- Potential additional costs

### After (GHCR)
- Uses GitHub's free container registry
- Automatic authentication with GITHUB_TOKEN
- Simpler setup and configuration
- No additional infrastructure needed
- Free for public repositories

## 📝 Changes Made

### 1. GitHub Actions Workflow (`.github/workflows/deploy.yaml`)
**Changed:**
- Registry from `{ACR_NAME}.azurecr.io` → `ghcr.io`
- Authentication from ACR credentials → `GITHUB_TOKEN` (automatic)
- Image path to `ghcr.io/subasico/portfolioanalyzerbackend`
- Azure credentials from JSON format → individual secrets

**New environment variables:**
```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: portfolio-analyzer-backend
```

**Updated Azure authentication:**
```yaml
creds: |
  {
    "clientId": "${{ secrets.AZURE_CLIENT_ID }}",
    "clientSecret": "${{ secrets.AZURE_CLIENT_SECRET }}",
    "subscriptionId": "${{ secrets.AZURE_SUBSCRIPTION_ID }}",
    "tenantId": "${{ secrets.AZURE_TENANT_ID }}"
  }
```

### 2. Kubernetes Deployment (`k8s/deployment.yaml`)
**Changed:**
- Container image: `YOUR_ACR_NAME.azurecr.io/portfolio-analyzer-backend` → `ghcr.io/subasico/portfolioanalyzerbackend`
- Image pull secret: `acr-secret` → `ghcr-secret`

### 3. Documentation Updates
**Updated files:**
- `README.md` - Replaced ACR instructions with GHCR
- `SETUP_INSTRUCTIONS.md` - Updated with GHCR setup steps
- Added `QUICK_START.md` - Comprehensive deployment guide
- Added `k8s/create-ghcr-secret.sh` - Helper script for secret creation

## 🔐 New Secrets Required

### GitHub Repository Secrets (Already Set)
✅ `AKS_CLUSTER_NAME` - Your AKS cluster name
✅ `AKS_RESOURCE_GROUP` - Your resource group
✅ `AZURE_CLIENT_SECRET` - Service principal secret

### GitHub Repository Secrets (Need to Add)
❌ `AZURE_CLIENT_ID` - Service principal app ID
❌ `AZURE_SUBSCRIPTION_ID` - Your Azure subscription ID
❌ `AZURE_TENANT_ID` - Your Azure tenant ID

### Kubernetes Secrets (Need to Create)
❌ `portfolio-analyzer-secrets` - Application secrets (API keys, DB)
❌ `ghcr-secret` - Container registry pull secret

## 📋 Action Items

### Step 1: Add GitHub Secrets (5 min)
```bash
# Get service principal info
az ad sp create-for-rbac --name "github-actions-portfolio-analyzer" \
  --role contributor \
  --scopes /subscriptions/{subscription}/resourceGroups/{resource-group}

# Get subscription ID
az account show --query id -o tsv

# Get tenant ID
az account show --query tenantId -o tsv
```

Add to: https://github.com/subasico/portfolioanalyzerbackend/settings/secrets/actions

### Step 2: Create Kubernetes Secrets (10 min)

**Application secrets:**
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=anthropic-api-key='sk-ant-...' \
  --from-literal=openai-api-key='sk-...'
```

**GHCR pull secret:**

1. Create GitHub PAT: https://github.com/settings/tokens/new
   - Scope: `read:packages`
   - Name: "AKS Portfolio Analyzer"

2. Create secret:
```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=<YOUR_GITHUB_TOKEN> \
  --docker-email=subasico@users.noreply.github.com
```

### Step 3: Deploy (2 min)
```bash
# Trigger deployment
git commit --allow-empty -m "Trigger deployment"
git push
```

Or use GitHub Actions UI:
https://github.com/subasico/portfolioanalyzerbackend/actions

### Step 4: Update Frontend (1 min)

File: `allaboutai/templates/portfolio-analyzer.html`

Change:
```javascript
const API_URL = 'https://api-portfolio.allaboutai.com/api/v1';
```

## 🎯 Benefits of GHCR

1. **Cost Savings**: Free for public repositories
2. **Simplified Authentication**: Uses GITHUB_TOKEN automatically
3. **Fewer Secrets**: No ACR credentials needed
4. **Better Integration**: Native GitHub integration
5. **Easier Maintenance**: One less Azure resource to manage
6. **Public Visibility**: Package visible at github.com/subasico/portfolioanalyzerbackend/pkgs

## 📊 Verification

After deployment, verify:

1. **GitHub Packages**: https://github.com/subasico/portfolioanalyzerbackend/pkgs/container/portfolioanalyzerbackend
2. **GitHub Actions**: https://github.com/subasico/portfolioanalyzerbackend/actions
3. **API Health**: `curl https://api-portfolio.allaboutai.com/api/v1/health`
4. **Kubernetes**: `kubectl get pods -l app=portfolio-analyzer-backend`

## 🚀 Current Status

- ✅ Code repository: https://github.com/subasico/portfolioanalyzerbackend
- ✅ GHCR configuration complete
- ✅ Documentation updated
- ⏳ GitHub secrets (3 missing)
- ⏳ Kubernetes secrets (need creation)
- ⏳ Initial deployment (pending)
- ⏳ Frontend API URL update (pending)

## 📚 Documentation

- [QUICK_START.md](QUICK_START.md) - Step-by-step deployment
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Detailed setup
- [README.md](README.md) - Full documentation
- [PORTFOLIO_ANALYZER_PROJECT_SUMMARY.md](PORTFOLIO_ANALYZER_PROJECT_SUMMARY.md) - Project overview

## 💡 Next Steps

1. Add the 3 missing GitHub secrets
2. Create Kubernetes secrets in AKS
3. Trigger deployment via GitHub Actions
4. Verify deployment and test API
5. Update frontend API URL
6. Test end-to-end functionality

**Estimated time to deployment**: ~20 minutes

---

**Migration Date**: 2025-10-31
**Repository**: https://github.com/subasico/portfolioanalyzerbackend
**Status**: ✅ Configuration Complete, ⏳ Awaiting Deployment
