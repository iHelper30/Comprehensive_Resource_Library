import os
import sys
import json
import requests

def verify_cloudflare_deployment():
    """
    Comprehensive deployment verification script
    """
    # Cloudflare API Configuration
    CLOUDFLARE_API_TOKEN = os.environ.get('CLOUDFLARE_API_TOKEN')
    CLOUDFLARE_ACCOUNT_ID = os.environ.get('CLOUDFLARE_ACCOUNT_ID')
    
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ACCOUNT_ID:
        print("❌ Cloudflare API credentials not found")
        sys.exit(1)
    
    # Cloudflare Pages Project Configuration
    PROJECT_NAME = 'comprehensive-resource-library'
    
    # Cloudflare API Endpoint
    API_BASE_URL = f'https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/pages/projects/{PROJECT_NAME}'
    
    # Headers for API Request
    headers = {
        'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    try:
        # Fetch Project Details
        response = requests.get(API_BASE_URL, headers=headers)
        response.raise_for_status()
        
        project_data = response.json()
        
        # Deployment Verification Checks
        deployment_checks = {
            'Project Exists': project_data['success'],
            'Deployment Enabled': project_data['result'].get('deployment_enabled', False),
            'Production Branch': project_data['result'].get('production_branch') == 'main',
            'Latest Deployment Status': None
        }
        
        # Fetch Latest Deployment
        deployments_url = f'{API_BASE_URL}/deployments'
        deployments_response = requests.get(deployments_url, headers=headers)
        deployments_response.raise_for_status()
        
        deployments_data = deployments_response.json()
        
        if deployments_data['result']:
            latest_deployment = deployments_data['result'][0]
            deployment_checks['Latest Deployment Status'] = latest_deployment.get('status')
        
        # Generate Verification Report
        print("🚀 Cloudflare Deployment Verification Report")
        print("=" * 50)
        
        for check, status in deployment_checks.items():
            status_symbol = '✅' if status else '❌'
            print(f"{status_symbol} {check}: {status}")
        
        # Generate Detailed JSON Report
        report = {
            'timestamp': os.getenv('GITHUB_ACTION_REF', 'Local Execution'),
            'project_name': PROJECT_NAME,
            'checks': deployment_checks
        }
        
        with open('deployment_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        # Exit with appropriate status
        sys.exit(0 if all(deployment_checks.values()) else 1)
    
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Error: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"❌ Data Parsing Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    verify_cloudflare_deployment()
