# 🚀 Deploy Portfolio Analyzer with OpenAI

This guide shows you how to deploy the Portfolio Analyzer using **OpenAI GPT-4o** instead of Anthropic Claude.

## ✅ What's Already Done

- ✅ Backend configured to use OpenAI by default
- ✅ All GitHub secrets already set (AKS_CLUSTER_NAME, AKS_RESOURCE_GROUP, AZURE_CLIENT_SECRET, GH_ACCESS_TOKEN)
- ✅ Deployment uses `gpt-4o` model

## 🔑 Step 1: Get Your OpenAI API Key (5 minutes)

### Create OpenAI Account & Get API Key:

1. **Go to OpenAI Platform**: https://platform.openai.com/

2. **Sign in or Sign up**: Create an account if you don't have one

3. **Get API Key**:
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Name it: "Portfolio Analyzer"
   - **Copy the key immediately** (starts with `sk-proj-...` or `sk-...`)
   - Save it somewhere safe!

4. **Add Payment Method**:
   - Go to: https://platform.openai.com/settings/organization/billing/overview
   - Click "Add payment method"
   - Add your credit/debit card
   - Set a monthly budget limit (e.g., $5-10 for safety)

5. **Check Credits**:
   - New accounts usually get $5 free credits
   - After that, it's pay-as-you-go (very cheap!)

### OpenAI Pricing (Very Affordable!)

**GPT-4o** (Recommended - Best quality):
- Input: $2.50 per 1M tokens (~$0.0025 per 1K)
- Output: $10 per 1M tokens (~$0.01 per 1K)
- **Cost per analysis: ~$0.005-0.01** (less than 1 cent!)

**GPT-4o-mini** (Cheaper alternative):
- Input: $0.15 per 1M tokens
- Output: $0.60 per 1M tokens
- **Cost per analysis: ~$0.0003-0.001** (fraction of a cent!)

**GPT-3.5-Turbo** (Cheapest):
- Input: $0.50 per 1M tokens
- Output: $1.50 per 1M tokens
- **Cost per analysis: ~$0.001-0.002** (still very cheap!)

With **$5**, you can do:
- ~500-1000 analyses with GPT-4o
- ~5000+ analyses with GPT-4o-mini
- ~2500+ analyses with GPT-3.5-Turbo

## 📝 Step 2: Create Kubernetes Secrets (10 minutes)

### Connect to AKS:
```bash
# Get your cluster credentials
az aks get-credentials \
  --resource-group <YOUR_RESOURCE_GROUP> \
  --name <YOUR_AKS_CLUSTER_NAME> \
  --overwrite-existing
```

### Create Application Secrets:

**Option A: With PostgreSQL (Full Setup)**
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://postgres:<YOUR_PASSWORD>@staging-postgre.postgres.database.azure.com:5432/portfoliodb' \
  --from-literal=openai-api-key='sk-proj-YOUR_OPENAI_KEY_HERE' \
  --from-literal=anthropic-api-key='' \
  --dry-run=client -o yaml | kubectl apply -f -
```

**Option B: Without PostgreSQL (Simpler - Works in-memory)**
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:pass@localhost:5432/portfoliodb' \
  --from-literal=openai-api-key='sk-proj-YOUR_OPENAI_KEY_HERE' \
  --from-literal=anthropic-api-key='' \
  --dry-run=client -o yaml | kubectl apply -f -
```

> **Note**: The database is optional for Phase 1. The app works fine without it!

### Create GHCR Pull Secret:

```bash
# Use your GH_ACCESS_TOKEN value or create a new GitHub PAT
# To create new PAT: https://github.com/settings/tokens/new (scope: read:packages)

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=<YOUR_GITHUB_PAT> \
  --docker-email=subasico@users.noreply.github.com \
  --dry-run=client -o yaml | kubectl apply -f -
```

### Verify Secrets:
```bash
kubectl get secrets | grep portfolio
kubectl get secrets | grep ghcr

# Should show:
# portfolio-analyzer-secrets   Opaque   3      10s
# ghcr-secret                   kubernetes.io/dockerconfigjson   1      5s
```

## 🚀 Step 3: Deploy to AKS (2 minutes)

Trigger the deployment:

```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/portfolioanalyzerbackend
git commit --allow-empty -m "Deploy with OpenAI GPT-4o"
git push
```

### Watch the Deployment:

**GitHub Actions** (build & deploy):
https://github.com/subasico/portfolioanalyzerbackend/actions

**Kubernetes Pods**:
```bash
# Watch pods start up
kubectl get pods -l app=portfolio-analyzer-backend -w

# Check logs
kubectl logs -l app=portfolio-analyzer-backend -f
```

You should see:
```
Starting Portfolio Analyzer Backend v1.0.0
Environment: production
Debug mode: False
CORS origins: ['https://allaboutai.com', 'https://www.allaboutai.com']
```

## 🌐 Step 4: Configure DNS (5 minutes)

### Get Ingress IP:
```bash
kubectl get svc -n ingress-nginx

# Look for EXTERNAL-IP of ingress-nginx-controller
# Example: 20.123.45.67
```

### Add DNS Record:

In your DNS provider (Cloudflare, GoDaddy, etc.):
- **Type**: A
- **Name**: `api-portfolio` (or `api-portfolio.allaboutai.com`)
- **Value**: `<EXTERNAL-IP from above>`
- **TTL**: 300 (5 minutes)

### Wait for DNS Propagation:
```bash
# Test DNS (may take 2-10 minutes)
nslookup api-portfolio.allaboutai.com

# When ready, it should show your ingress IP
```

## ✅ Step 5: Test the API (5 minutes)

### Health Check:
```bash
curl https://api-portfolio.allaboutai.com/api/v1/health

# Expected response:
# {"status":"healthy","version":"1.0.0","timestamp":"2025-10-31T..."}
```

### Test Portfolio Analysis:
```bash
curl -X POST https://api-portfolio.allaboutai.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "AAPL", "allocation": 30.0},
      {"symbol": "MSFT", "allocation": 25.0},
      {"symbol": "GOOGL", "allocation": 20.0},
      {"symbol": "JPM", "allocation": 15.0},
      {"symbol": "JNJ", "allocation": 10.0}
    ]
  }'
```

You should get a detailed analysis with AI insights powered by GPT-4o! 🎉

### Check API Documentation:
Open in browser: https://api-portfolio.allaboutai.com/docs

## 🎨 Step 6: Update Frontend (1 minute)

Update the Portfolio Analyzer frontend to use the production API:

```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai

# Edit templates/portfolio-analyzer.html
# Find line ~28 and change:
# const API_URL = 'http://localhost:8000/api/v1';
# To:
# const API_URL = 'https://api-portfolio.allaboutai.com/api/v1';
```

Or use this command:
```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai

# Update the API URL
sed -i.bak "s|const API_URL = 'http://localhost:8000/api/v1'|const API_URL = 'https://api-portfolio.allaboutai.com/api/v1'|g" templates/portfolio-analyzer.html

# Commit and push
git add templates/portfolio-analyzer.html
git commit -m "Connect Portfolio Analyzer to production API (OpenAI GPT-4o)"
git push
```

## 🎉 Success!

Your Portfolio Analyzer is now live!

- ✅ **Frontend**: https://allaboutai.com/portfolio-analyzer.html
- ✅ **API**: https://api-portfolio.allaboutai.com/api/v1
- ✅ **Docs**: https://api-portfolio.allaboutai.com/docs
- ✅ **Powered by**: OpenAI GPT-4o 🤖

## 💰 Cost Monitoring

Monitor your OpenAI usage:
- **Dashboard**: https://platform.openai.com/usage
- **Set limits**: https://platform.openai.com/settings/organization/limits

Tips to save money:
1. Start with GPT-4o-mini for testing (much cheaper!)
2. Set a monthly budget limit ($5-10)
3. Monitor usage regularly
4. Cache common portfolio patterns (future enhancement)

## 🔄 Switching Models

To use a different OpenAI model, update the deployment:

**For GPT-4o-mini** (cheaper):
```bash
kubectl set env deployment/portfolio-analyzer-backend LLM_MODEL=gpt-4o-mini
```

**For GPT-3.5-Turbo** (cheapest):
```bash
kubectl set env deployment/portfolio-analyzer-backend LLM_MODEL=gpt-3.5-turbo
```

**Back to GPT-4o** (best quality):
```bash
kubectl set env deployment/portfolio-analyzer-backend LLM_MODEL=gpt-4o
```

Or edit `k8s/deployment.yaml` and redeploy.

## 🔧 Troubleshooting

### Issue: "Invalid API key"
```bash
# Check if secret has correct key
kubectl get secret portfolio-analyzer-secrets -o jsonpath='{.data.openai-api-key}' | base64 -d
echo

# Update secret if needed
kubectl delete secret portfolio-analyzer-secrets
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=openai-api-key='sk-proj-YOUR_NEW_KEY' \
  --from-literal=anthropic-api-key=''

# Restart pods
kubectl rollout restart deployment/portfolio-analyzer-backend
```

### Issue: "Rate limit exceeded"
- You've hit OpenAI's rate limit
- Wait a minute and try again
- Consider upgrading to a paid tier for higher limits

### Issue: "Insufficient quota"
- You've run out of OpenAI credits
- Add more credits at: https://platform.openai.com/settings/organization/billing/overview

## 📊 Monitoring

```bash
# Check deployment
kubectl get deployment portfolio-analyzer-backend

# Check pods
kubectl get pods -l app=portfolio-analyzer-backend

# View logs
kubectl logs -l app=portfolio-analyzer-backend --tail=100 -f

# Check HPA (auto-scaling)
kubectl get hpa

# Check resource usage
kubectl top pods -l app=portfolio-analyzer-backend
```

## 🎯 Summary

✅ **Total Setup Time**: ~30 minutes
✅ **Cost**: ~$0.01 per portfolio analysis with GPT-4o
✅ **Free Credits**: New OpenAI accounts get $5 free
✅ **Database**: Optional (works without it)
✅ **Scaling**: Auto-scales 2-10 pods based on load

---

**Repository**: https://github.com/subasico/portfolioanalyzerbackend
**Model**: OpenAI GPT-4o
**Status**: Ready to Deploy! 🚀

Enjoy your AI-powered Portfolio Analyzer! 💼📊
