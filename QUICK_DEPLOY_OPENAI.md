# ⚡ Quick Deploy with OpenAI - Cheat Sheet

## 🎯 Super Quick Steps (20 minutes)

### 1. Get OpenAI API Key (5 min)
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-proj-...`)
4. Add payment method: https://platform.openai.com/settings/organization/billing/overview

### 2. Create Kubernetes Secrets (5 min)
```bash
# Connect to AKS
az aks get-credentials --resource-group <RG> --name <CLUSTER>

# Create app secrets (replace YOUR_OPENAI_KEY and YOUR_POSTGRES_PASSWORD)
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://postgres:YOUR_POSTGRES_PASSWORD@staging-postgre.postgres.database.azure.com:5432/portfoliodb' \
  --from-literal=openai-api-key='YOUR_OPENAI_KEY' \
  --from-literal=anthropic-api-key=''

# Create GHCR secret (use your GH_ACCESS_TOKEN)
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=YOUR_GITHUB_PAT \
  --docker-email=subasico@users.noreply.github.com

# Verify
kubectl get secrets | grep -E "portfolio|ghcr"
```

### 3. Deploy (1 min)
```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/portfolioanalyzerbackend
git commit --allow-empty -m "Deploy with OpenAI"
git push
```

Watch: https://github.com/subasico/portfolioanalyzerbackend/actions

### 4. Configure DNS (5 min)
```bash
# Get IP
kubectl get svc -n ingress-nginx

# Add A record in your DNS:
# api-portfolio.allaboutai.com → EXTERNAL-IP
```

### 5. Test (2 min)
```bash
# Health check
curl https://api-portfolio.allaboutai.com/api/v1/health

# Test analysis
curl -X POST https://api-portfolio.allaboutai.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{"holdings":[{"symbol":"AAPL","allocation":30},{"symbol":"MSFT","allocation":25},{"symbol":"GOOGL","allocation":20},{"symbol":"JPM","allocation":15},{"symbol":"JNJ","allocation":10}]}'
```

### 6. Update Frontend (1 min)
```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai

# Edit templates/portfolio-analyzer.html line ~28:
# const API_URL = 'https://api-portfolio.allaboutai.com/api/v1';

git add templates/portfolio-analyzer.html
git commit -m "Connect to production API"
git push
```

## ✅ Done!
- Frontend: https://allaboutai.com/portfolio-analyzer.html
- API: https://api-portfolio.allaboutai.com/api/v1

## 💰 Costs
- GPT-4o: ~$0.01 per analysis
- With $5: ~500 analyses
- New accounts get $5 free!

## 📚 Detailed Guide
See [DEPLOY_WITH_OPENAI.md](DEPLOY_WITH_OPENAI.md) for full instructions.
