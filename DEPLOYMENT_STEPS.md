# Portfolio Analyzer Backend - Deployment Steps

## ⚠️ IMPORTANT: Complete BEFORE Pushing to Git

### Step 1: Create Kubernetes Secret (REQUIRED)

The deployment will fail without this secret. Run ONE of these commands:

#### Option A: Using the script (Recommended)
```bash
# 1. Edit .env and add your actual OpenAI API key
# 2. Run the script
./create-k8s-secret.sh
```

#### Option B: Manual command
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://postgresadmin:admin10.@postgres-service:5432/portfoliodb' \
  --from-literal=openai-api-key='YOUR_ACTUAL_OPENAI_KEY_HERE' \
  --from-literal=anthropic-api-key='' \
  --namespace=default
```

**Verify the secret was created:**
```bash
kubectl get secret portfolio-analyzer-secrets -n default
```

---

### Step 2: Verify GitHub Secrets

Check that these secrets exist in your GitHub repository settings:
https://github.com/subasico/portfolioanalyzerbackend/settings/secrets/actions

Required secrets:
- ✅ `GH_ACCESS_TOKEN` - GitHub Personal Access Token with packages:write
- ✅ `AZURE_CLIENT_SECRET` - Azure service principal credentials (full JSON)
- ✅ `AKS_CLUSTER_NAME` - pdfexlporerstagingaks
- ✅ `AKS_RESOURCE_GROUP` - Your Azure resource group name

---

### Step 3: Deploy to AKS

Once the Kubernetes secret is created, push to trigger deployment:

```bash
# Stage all changes
git add .

# Commit with deployment message
git commit -m "Deploy Portfolio Analyzer Backend to AKS

- Updated dependencies for Python 3.13 compatibility
- Fixed Pydantic type annotations
- Added local development setup
- Tested locally with OpenAI GPT-4o integration
- Stock data using Yahoo Finance (yfinance)
- Ready for production deployment"

# Push to trigger GitHub Actions workflow
git push origin main
```

---

### Step 4: Monitor Deployment

#### Watch GitHub Actions
Visit: https://github.com/subasico/portfolioanalyzerbackend/actions

#### Watch Kubernetes Deployment
```bash
# Watch pods status
kubectl get pods -n default -l app=portfolio-analyzer-backend -w

# Check pod logs
kubectl logs -n default -l app=portfolio-analyzer-backend --tail=100 -f

# Check deployment status
kubectl rollout status deployment/portfolio-analyzer-backend -n default
```

---

### Step 5: Verify Deployment

Once pods are running:

```bash
# Check pods are healthy
kubectl get pods -n default -l app=portfolio-analyzer-backend

# Check service
kubectl get svc -n default portfolio-analyzer-backend-service

# Check ingress
kubectl get ingress -n default portfolio-analyzer-backend-ingress

# Test health endpoint
curl https://api-portfolio.allaboutai.com/api/v1/health
```

---

## 🔧 Troubleshooting

### Pods stuck in CreateContainerConfigError
- **Cause**: Missing Kubernetes secret
- **Fix**: Create the `portfolio-analyzer-secrets` secret (see Step 1)

### Pods stuck in ImagePullBackOff
- **Cause**: GitHub Container Registry authentication issue
- **Fix**: Verify `ghcr-secret` exists and `GH_ACCESS_TOKEN` is valid

### GitHub Actions workflow fails
- **Cause**: Missing GitHub secrets
- **Fix**: Verify all required secrets are configured (see Step 2)

### API returns 500 errors
- **Cause**: Missing or invalid OpenAI API key
- **Fix**: Verify the secret contains a valid OpenAI API key

---

## 📊 Deployment Timeline

- Docker build: ~2-3 minutes
- Image push to GHCR: ~1 minute
- AKS deployment: ~1-2 minutes
- Pod startup: ~30 seconds
- **Total: ~5-7 minutes**

---

## ✅ Success Criteria

After deployment, you should see:
- ✅ GitHub Actions workflow completes successfully
- ✅ Pods in `Running` status (2 replicas)
- ✅ Health check returns HTTP 200
- ✅ API accessible at `https://api-portfolio.allaboutai.com`
- ✅ Swagger UI available at `https://api-portfolio.allaboutai.com/docs`

---

## 🚨 Current Status

**Kubernetes Secret:** ❌ NOT CREATED - **CREATE THIS FIRST!**

Run this command NOW before pushing:
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://postgresadmin:admin10.@postgres-service:5432/portfoliodb' \
  --from-literal=openai-api-key='PUT_YOUR_ACTUAL_KEY_HERE' \
  --from-literal=anthropic-api-key='' \
  --namespace=default
```

Then proceed with git push.
