# Setup Instructions for Portfolio Analyzer Backend

## Step 1: Create GitHub Repository

Since `gh` CLI is not available, create the repository manually:

1. Go to https://github.com/new
2. Repository name: `portfolioanalyzerbackend`
3. Description: `AI-powered portfolio analysis microservice built with FastAPI and deployed on Azure Kubernetes Service`
4. Visibility: Public
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Push to GitHub

After creating the repository, run these commands:

```bash
cd /Users/coskun.subasi/Library/CloudStorage/Dropbox/Repository/portfolioanalyzerbackend
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/portfolioanalyzerbackend.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Step 3: Configure GitHub Secrets

Go to your repository Settings > Secrets and variables > Actions, and add:

### Required Secrets:

1. **ACR_USERNAME**: Your Azure Container Registry username
   ```bash
   # Get from Azure Portal or run:
   az acr credential show --name YOUR_ACR_NAME --query username
   ```

2. **ACR_PASSWORD**: Your Azure Container Registry password
   ```bash
   # Get from Azure Portal or run:
   az acr credential show --name YOUR_ACR_NAME --query "passwords[0].value"
   ```

3. **AZURE_CREDENTIALS**: Azure service principal credentials (JSON format)
   ```bash
   # Create service principal:
   az ad sp create-for-rbac --name "github-actions-portfolio-analyzer" \
     --role contributor \
     --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
     --sdk-auth

   # Copy the entire JSON output to this secret
   ```

## Step 4: Update Configuration Files

### 4.1 Update `.github/workflows/deploy.yaml`

Replace placeholders with your actual values:
- `YOUR_ACR_NAME` → Your Azure Container Registry name
- `YOUR_AKS_CLUSTER_NAME` → Your AKS cluster name
- `YOUR_RESOURCE_GROUP` → Your Azure resource group

### 4.2 Update `k8s/deployment.yaml`

Replace:
- `YOUR_ACR_NAME` → Your Azure Container Registry name

## Step 5: Create Kubernetes Secrets

Before deploying, create the required secrets in your AKS cluster:

```bash
# Connect to your AKS cluster
az aks get-credentials --resource-group YOUR_RESOURCE_GROUP --name YOUR_AKS_CLUSTER_NAME

# Create the secret
kubectl create secret generic portfolio-analyzer-secrets \
  --from-literal=database-url='postgresql://user:password@postgres-service:5432/portfoliodb' \
  --from-literal=anthropic-api-key='your_anthropic_api_key_here' \
  --from-literal=openai-api-key='your_openai_api_key_here'

# Verify the secret was created
kubectl get secrets
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
