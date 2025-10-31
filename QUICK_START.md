# Portfolio Analyzer Backend - Quick Start Guide

## ✅ What's Done

- ✅ Repository created: https://github.com/subasico/portfolioanalyzerbackend
- ✅ Code pushed to GitHub
- ✅ Configured to use GitHub Container Registry (GHCR)
- ✅ GitHub secrets already set:
  - AKS_CLUSTER_NAME
  - AKS_RESOURCE_GROUP
  - AZURE_CLIENT_SECRET (full JSON credentials)
  - GH_ACCESS_TOKEN (GitHub PAT for GHCR)

## 🎯 What You Need to Do

### 1. Verify GitHub Secrets ✅

**All required secrets are already configured!**

Go to: https://github.com/subasico/portfolioanalyzerbackend/settings/secrets/actions

Verify these exist:
- ✅ **AKS_CLUSTER_NAME**
- ✅ **AKS_RESOURCE_GROUP**
- ✅ **AZURE_CLIENT_SECRET** (should be full JSON with clientId, clientSecret, subscriptionId, tenantId)
- ✅ **GH_ACCESS_TOKEN**

If `AZURE_CLIENT_SECRET` needs to be updated to the JSON format:
```bash
az ad sp create-for-rbac --name "github-actions-portfolio-analyzer" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
# Copy the entire JSON output to AZURE_CLIENT_SECRET
```

### 2. Create Kubernetes Secrets (10 minutes)

**Step A: Connect to your AKS cluster**
```bash
az aks get-credentials --resource-group <YOUR_RESOURCE_GROUP> --name <YOUR_AKS_CLUSTER_NAME>
```

**Step B: Create application secrets**
```bash
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:password@postgres-service:5432/portfoliodb' \
  --from-literal=anthropic-api-key='sk-ant-your-key-here' \
  --from-literal=openai-api-key='sk-your-key-here'
```

**Step C: Create GHCR pull secret**

First, create a GitHub Personal Access Token:
1. Go to https://github.com/settings/tokens/new
2. Name: "AKS Portfolio Analyzer"
3. Select scope: **read:packages**
4. Generate and copy the token

Then create the secret:
```bash
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=<YOUR_GITHUB_TOKEN> \
  --docker-email=subasico@users.noreply.github.com
```

Verify both secrets:
```bash
kubectl get secrets | grep portfolio
kubectl get secrets | grep ghcr
```

### 3. Configure DNS (5 minutes)

**Step A: Get ingress IP**
```bash
kubectl get svc -n ingress-nginx
# Look for the EXTERNAL-IP of the ingress-nginx-controller
```

**Step B: Create DNS A record**

In your DNS provider (e.g., Cloudflare, GoDaddy):
- Type: **A**
- Name: **api-portfolio** (or api-portfolio.allaboutai.com)
- Value: **[EXTERNAL-IP from above]**
- TTL: **300** (5 minutes)

### 4. Deploy! (2 minutes)

Once steps 1-3 are complete:

```bash
# Make a small change to trigger deployment (or just push)
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/portfolioanalyzerbackend
git commit --allow-empty -m "Trigger initial deployment"
git push
```

Or manually trigger from GitHub:
- Go to https://github.com/subasico/portfolioanalyzerbackend/actions
- Click on "Build and Deploy to AKS" workflow
- Click "Run workflow" button

### 5. Monitor Deployment (5 minutes)

Watch the GitHub Actions workflow:
https://github.com/subasico/portfolioanalyzerbackend/actions

Watch Kubernetes pods:
```bash
kubectl get pods -l app=portfolio-analyzer-backend -w
```

Check logs:
```bash
kubectl logs -l app=portfolio-analyzer-backend -f
```

### 6. Test the API (2 minutes)

Wait for DNS propagation (2-10 minutes), then test:

```bash
# Health check
curl https://api-portfolio.allaboutai.com/api/v1/health

# Test analysis
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

### 7. Update Frontend (1 minute)

Update the API URL in the frontend:

File: `/Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai/templates/portfolio-analyzer.html`

Change line ~28:
```javascript
// From:
const API_URL = 'http://localhost:8000/api/v1';

// To:
const API_URL = 'https://api-portfolio.allaboutai.com/api/v1';
```

Commit and deploy the frontend:
```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai
git add templates/portfolio-analyzer.html
git commit -m "Update Portfolio Analyzer API URL to production"
git push
```

## 🎉 Done!

Your Portfolio Analyzer should now be live at:
- Frontend: https://allaboutai.com/portfolio-analyzer.html
- API: https://api-portfolio.allaboutai.com/api/v1

## 📊 Monitoring

Check deployment status:
```bash
kubectl get deployment portfolio-analyzer-backend
kubectl get pods -l app=portfolio-analyzer-backend
kubectl get svc portfolio-analyzer-backend-service
kubectl get ingress portfolio-analyzer-backend-ingress
kubectl get hpa portfolio-analyzer-backend-hpa
```

View logs:
```bash
kubectl logs -l app=portfolio-analyzer-backend --tail=100 -f
```

Scale manually (if needed):
```bash
kubectl scale deployment portfolio-analyzer-backend --replicas=5
```

## 🔧 Troubleshooting

**Problem: Pods not starting**
```bash
kubectl describe pod <pod-name>
kubectl logs <pod-name>
```

**Problem: ImagePullBackOff**
- Verify ghcr-secret exists: `kubectl get secret ghcr-secret`
- Verify GitHub token has `read:packages` scope
- Check if image exists: https://github.com/subasico/portfolioanalyzerbackend/pkgs/container/portfolioanalyzerbackend

**Problem: CrashLoopBackOff**
- Check logs: `kubectl logs <pod-name>`
- Verify portfolio-analyzer-secrets exists
- Verify API keys are valid

**Problem: Can't access API**
- Check ingress: `kubectl get ingress`
- Verify DNS points to correct IP
- Check cert-manager: `kubectl get certificate`
- Test internally: `kubectl port-forward svc/portfolio-analyzer-backend-service 8080:80`

## 📚 Additional Resources

- [Full Setup Instructions](SETUP_INSTRUCTIONS.md)
- [README](README.md)
- [GitHub Actions Logs](https://github.com/subasico/portfolioanalyzerbackend/actions)
- [API Documentation](https://api-portfolio.allaboutai.com/docs) (after deployment)

## 💡 Tips

1. **Enable package visibility**: Go to https://github.com/users/subasico/packages/container/portfolioanalyzerbackend/settings and set to public
2. **Monitor costs**: Check AKS resource usage regularly
3. **Update regularly**: Keep dependencies updated for security
4. **Backup secrets**: Save your API keys securely
5. **Test locally first**: Use `uvicorn app.main:app --reload` for local testing

## 🚀 Next Steps (Phase 2)

After successful deployment, consider:
- Session management with Redis
- User authentication (OAuth2/JWT)
- Portfolio history storage
- Email notifications
- PDF report generation
- Advanced analytics (Monte Carlo, backtesting)
- Monitoring dashboard (Prometheus + Grafana)

---

**Total Setup Time**: ~30 minutes
**Difficulty**: Medium
**Prerequisites**: Azure account, kubectl access, GitHub account

Good luck! 🎯
