# Setup Instructions for Portfolio Analyzer Backend

## ✅ Step 1: Create GitHub Repository

**COMPLETED** - Repository created at https://github.com/subasico/portfolioanalyzerbackend

## ✅ Step 2: Push to GitHub

**COMPLETED** - Code has been pushed to GitHub

## Step 3: Configure GitHub Secrets

Go to https://github.com/subasico/portfolioanalyzerbackend/settings/secrets/actions

### Required Secrets (some already configured):

✅ **AKS_CLUSTER_NAME** - Already configured
✅ **AKS_RESOURCE_GROUP** - Already configured
✅ **AZURE_CLIENT_SECRET** - Already configured

### Additional Secrets Needed:

1. **AZURE_CLIENT_ID**: Your Azure service principal client ID
   ```bash
   # Get from your service principal or create new one:
   az ad sp create-for-rbac --name "github-actions-portfolio-analyzer" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group}

   # Use the "appId" value as AZURE_CLIENT_ID
   ```

2. **AZURE_SUBSCRIPTION_ID**: Your Azure subscription ID
   ```bash
   # Get subscription ID:
   az account show --query id -o tsv
   ```

3. **AZURE_TENANT_ID**: Your Azure tenant ID
   ```bash
   # Get tenant ID:
   az account show --query tenantId -o tsv
   ```

Note: The workflow now uses **GitHub Container Registry (GHCR)** instead of Azure Container Registry, so no ACR credentials are needed!

## ✅ Step 4: Configuration Files

**COMPLETED** - All configuration files have been updated to use GitHub Container Registry (GHCR).

- ✅ `.github/workflows/deploy.yaml` configured to use GHCR
- ✅ `k8s/deployment.yaml` configured to pull from `ghcr.io/subasico/portfolioanalyzerbackend`
- ✅ Using GitHub secrets for AKS cluster and resource group

## Step 5: Create Kubernetes Secrets

Before deploying, create the required secrets in your AKS cluster:

**5.1: Application Secrets**

```bash
# Connect to your AKS cluster (use your actual cluster name and resource group)
az aks get-credentials --resource-group <YOUR_RESOURCE_GROUP> --name <YOUR_AKS_CLUSTER_NAME>

# Create the application secrets
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:password@postgres-service:5432/portfoliodb' \
  --from-literal=anthropic-api-key='your_anthropic_api_key_here' \
  --from-literal=openai-api-key='your_openai_api_key_here'

# Verify the secret was created
kubectl get secrets
```

**5.2: GitHub Container Registry Pull Secret**

Create a GitHub Personal Access Token (PAT):
1. Go to https://github.com/settings/tokens/new
2. Name: "AKS Portfolio Analyzer"
3. Select scope: `read:packages`
4. Click "Generate token"
5. Copy the token (you won't see it again!)

Then create the pull secret:

```bash
# Option 1: Using the helper script
./k8s/create-ghcr-secret.sh subasico <YOUR_GITHUB_TOKEN>

# Option 2: Manually
kubectl create secret docker-registry ghcr-secret \
  --docker-server=ghcr.io \
  --docker-username=subasico \
  --docker-password=<YOUR_GITHUB_TOKEN> \
  --docker-email=subasico@users.noreply.github.com

# Verify
kubectl get secret ghcr-secret
```

## Step 6: Set Up Database (if using PostgreSQL)

If you want to use PostgreSQL with pgvector for future enhancements:

```sql
-- Connect to your PostgreSQL database
CREATE DATABASE portfoliodb;

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Future: Add tables for storing analysis history, user preferences, etc.
```

For now, the application works without a database (using in-memory analysis only).

## Step 7: Configure DNS (Optional but Recommended)

1. Get the external IP of your ingress controller:
   ```bash
   kubectl get svc -n ingress-nginx
   ```

2. Create an A record in your DNS provider:
   - Name: `api-portfolio.allaboutai.com`
   - Type: A
   - Value: [External IP from above]
   - TTL: 300

3. Wait for DNS propagation (can take a few minutes to hours)

## Step 8: Update Frontend API URL

Once deployed, update the API URL in the frontend:

File: `/Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/allaboutai/templates/portfolio-analyzer.html`

Change:
```javascript
const API_URL = 'http://localhost:8000/api/v1'; // Development
```

To:
```javascript
const API_URL = 'https://api-portfolio.allaboutai.com/api/v1'; // Production
```

## Step 9: Test the Deployment

### Local Testing (Development):

```bash
# Create .env file
cp .env.example .env
# Edit .env with your API keys

# Install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload

# Test in browser
open http://localhost:8000/docs
```

### Test API Endpoints:

```bash
# Health check
curl https://api-portfolio.allaboutai.com/api/v1/health

# Test portfolio analysis
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

## Step 10: Monitor Deployment

```bash
# Watch pods
kubectl get pods -l app=portfolio-analyzer-backend -w

# View logs
kubectl logs -l app=portfolio-analyzer-backend -f

# Check deployment status
kubectl get deployment portfolio-analyzer-backend
kubectl get svc portfolio-analyzer-backend-service
kubectl get ingress portfolio-analyzer-backend-ingress

# Check HPA
kubectl get hpa
```

## Troubleshooting

### Issue: Pods not starting

```bash
# Describe pod to see errors
kubectl describe pod <pod-name>

# Check logs
kubectl logs <pod-name>

# Common issues:
# - Missing secrets: Create the secrets as shown in Step 5
# - Image pull errors: Check ACR credentials
# - API key issues: Verify secrets contain valid API keys
```

### Issue: Can't access API

```bash
# Check ingress
kubectl get ingress
kubectl describe ingress portfolio-analyzer-backend-ingress

# Check if cert-manager is working
kubectl get certificate
kubectl describe certificate portfolio-analyzer-tls

# Test internal service
kubectl port-forward svc/portfolio-analyzer-backend-service 8080:80
curl http://localhost:8080/api/v1/health
```

### Issue: High memory/CPU usage

The HPA will automatically scale, but you can also:

```bash
# Manually scale
kubectl scale deployment portfolio-analyzer-backend --replicas=5

# Check resource usage
kubectl top pods -l app=portfolio-analyzer-backend
```

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENVIRONMENT` | No | `development` | Environment name |
| `DEBUG` | No | `True` | Enable debug mode |
| `API_PREFIX` | No | `/api/v1` | API prefix path |
| `ALLOWED_ORIGINS` | Yes | - | CORS allowed origins |
| `DATABASE_URL` | No | - | PostgreSQL connection (optional) |
| `ANTHROPIC_API_KEY` | Yes* | - | Claude API key |
| `OPENAI_API_KEY` | Yes* | - | OpenAI API key |
| `LLM_PROVIDER` | No | `anthropic` | LLM provider |
| `LLM_MODEL` | No | `claude-3-5-sonnet-20241022` | Model name |

*At least one LLM API key is required

## Next Steps

1. Monitor the application performance and logs
2. Set up monitoring with Prometheus/Grafana (optional)
3. Configure alerts for errors and high resource usage
4. Implement session management (Phase 2)
5. Add user authentication (Phase 2)
6. Store analysis history in PostgreSQL (Phase 2)

## Support

For issues or questions:
- Check logs: `kubectl logs -l app=portfolio-analyzer-backend`
- Review GitHub Actions runs
- Check Azure Portal for AKS and ACR status
