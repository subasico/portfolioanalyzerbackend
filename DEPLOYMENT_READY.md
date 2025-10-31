# 🚀 Portfolio Analyzer Backend - Ready for Deployment!

## ✅ All GitHub Secrets Already Configured!

Your repository already has all the required secrets set up:

- ✅ **AKS_CLUSTER_NAME** - Your AKS cluster name
- ✅ **AKS_RESOURCE_GROUP** - Your Azure resource group
- ✅ **AZURE_CLIENT_SECRET** - Azure credentials (JSON format)
- ✅ **GH_ACCESS_TOKEN** - GitHub PAT for container registry

**No additional GitHub secrets needed!** 🎉

## 📋 Quick Deployment Checklist

### Step 1: Create Kubernetes Secrets (10 min)

Connect to your AKS cluster and create two secrets:

```bash
# Connect to AKS
az aks get-credentials --resource-group <YOUR_RG> --name <YOUR_CLUSTER>

# 1. Create application secrets (API keys)
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:password@postgres-service:5432/portfoliodb' \
  --from-literal=anthropic-api-key='sk-ant-your-claude-api-key' \
  --from-literal=openai-api-key='sk-your-openai-key'

# 2. Create GHCR pull secret
# First, get your GitHub PAT from GH_ACCESS_TOKEN or create new one at:
# https://github.com/settings/tokens/new (scope: read:packages)

kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=<YOUR_GITHUB_PAT> \
  --docker-email=subasico@users.noreply.github.com

# Verify secrets
kubectl get secrets | grep portfolio
kubectl get secrets | grep ghcr
```

### Step 2: Deploy (1 min)

Trigger deployment by pushing to main:

```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/portfolioanalyzerbackend
git commit --allow-empty -m "Deploy Portfolio Analyzer to AKS"
git push
```

Watch deployment:
- GitHub Actions: https://github.com/subasico/portfolioanalyzerbackend/actions
- Kubernetes: `kubectl get pods -l app=portfolio-analyzer-backend -w`

### Step 3: Configure DNS (5 min)

```bash
# Get ingress IP
kubectl get svc -n ingress-nginx

# Add DNS A record:
# Name: api-portfolio.allaboutai.com
# Type: A
# Value: [EXTERNAL-IP from above]
# TTL: 300
```

### Step 4: Test API (2 min)

```bash
# Wait for DNS propagation, then test
curl https://api-portfolio.allaboutai.com/api/v1/health

# Test portfolio analysis
curl -X POST https://api-portfolio.allaboutai.com/api/v1/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "AAPL", "allocation": 30},
      {"symbol": "MSFT", "allocation": 25},
      {"symbol": "GOOGL", "allocation": 20},
      {"symbol": "JPM", "allocation": 15},
      {"symbol": "JNJ", "allocation": 10}
    ]
  }'
```

### Step 5: Update Frontend (1 min)

```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai

# Edit templates/portfolio-analyzer.html
# Change line ~28:
# const API_URL = 'https://api-portfolio.allaboutai.com/api/v1';

# Commit and deploy
git add templates/portfolio-analyzer.html
git commit -m "Connect Portfolio Analyzer to production API"
git push
```

## 🎯 Expected Results

After successful deployment:

- ✅ Backend API: https://api-portfolio.allaboutai.com/api/v1/health
- ✅ API Docs: https://api-portfolio.allaboutai.com/docs
- ✅ Frontend: https://allaboutai.com/portfolio-analyzer.html
- ✅ Container: https://github.com/subasico/portfolioanalyzerbackend/pkgs/container/portfolioanalyzerbackend
- ✅ Pods running: `kubectl get pods -l app=portfolio-analyzer-backend`

## 📊 Monitoring Commands

```bash
# Check deployment status
kubectl get deployment portfolio-analyzer-backend
kubectl get pods -l app=portfolio-analyzer-backend
kubectl get svc portfolio-analyzer-backend-service
kubectl get ingress portfolio-analyzer-backend-ingress

# View logs
kubectl logs -l app=portfolio-analyzer-backend -f --tail=50

# Check HPA (auto-scaling)
kubectl get hpa

# Port forward for local testing
kubectl port-forward svc/portfolio-analyzer-backend-service 8080:80
# Then access: http://localhost:8080/api/v1/health
```

## 🔧 Troubleshooting

### Issue: ImagePullBackOff

```bash
# Check secret exists
kubectl get secret ghcr-secret

# Verify image is public or secret is correct
kubectl describe pod <pod-name>

# Make package public:
# Go to: https://github.com/users/subasico/packages/container/portfolioanalyzerbackend/settings
# Set "Package visibility" to Public
```

### Issue: CrashLoopBackOff

```bash
# Check logs
kubectl logs <pod-name>

# Common causes:
# - Missing portfolio-analyzer-secrets
# - Invalid API keys in secrets
# - Database connection issues (optional, can be ignored for now)

# Verify secrets
kubectl get secret portfolio-analyzer-secrets -o yaml
```

### Issue: Can't Access API (404/502)

```bash
# Check ingress
kubectl get ingress
kubectl describe ingress portfolio-analyzer-backend-ingress

# Check if pods are ready
kubectl get pods -l app=portfolio-analyzer-backend

# Check DNS
nslookup api-portfolio.allaboutai.com

# Test service directly
kubectl port-forward svc/portfolio-analyzer-backend-service 8080:80
curl http://localhost:8080/api/v1/health
```

## 💡 Key Differences from allaboutai Deployment

| Feature | allaboutai | portfolioanalyzerbackend |
|---------|-----------|-------------------------|
| Container Image | ghcr.io/subasico/allaboutai | ghcr.io/subasico/portfolioanalyzerbackend |
| Deployment | k8s/deploypod.yaml | k8s/deployment.yaml |
| Service | LoadBalancer | ClusterIP + Ingress |
| Scaling | Manual | HPA (2-10 replicas) |
| Health Checks | None | Liveness + Readiness |
| Ingress | Direct | NGINX with SSL/TLS |

## 🎉 Success Criteria

Your deployment is successful when:

1. ✅ GitHub Actions workflow completes without errors
2. ✅ Pods are in "Running" state
3. ✅ Health endpoint returns `{"status": "healthy"}`
4. ✅ API docs accessible at `/docs`
5. ✅ Portfolio analysis returns valid results
6. ✅ Frontend can communicate with backend

## 📚 Additional Documentation

- [QUICK_START.md](QUICK_START.md) - Detailed deployment guide
- [SETUP_INSTRUCTIONS.md](SETUP_INSTRUCTIONS.md) - Complete setup reference
- [README.md](README.md) - Full project documentation
- [API Docs](https://api-portfolio.allaboutai.com/docs) - Interactive API documentation (after deployment)

## 🚦 Deployment Status

**Current Status**: ✅ Ready for deployment

**What's configured**:
- ✅ GitHub repository with code
- ✅ All GitHub secrets
- ✅ GHCR configuration
- ✅ Kubernetes manifests
- ✅ CI/CD pipeline
- ✅ Documentation

**What's needed**:
- ⏳ Kubernetes secrets (2 secrets)
- ⏳ DNS configuration
- ⏳ Initial deployment
- ⏳ Frontend API URL update

**Estimated time to live**: ~20 minutes

---

**Repository**: https://github.com/subasico/portfolioanalyzerbackend
**Last Updated**: 2025-10-31
**Ready to Deploy**: YES ✅

Good luck with the deployment! 🚀
