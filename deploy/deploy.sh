#!/bin/bash

# Deployment script for ChoreChart Django Application
# This script runs the Ansible playbook to deploy the application to AWS EC2

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if ansible is installed
if ! command -v ansible-playbook &> /dev/null; then
    print_error "Ansible is not installed. Please install it first:"
    echo "  pip install ansible"
    exit 1
fi

# Check if inventory file exists and is configured
if [ ! -f "inventory.ini" ]; then
    print_error "inventory.ini file not found!"
    exit 1
fi

# Check if inventory file has been configured (not using placeholder)
if grep -q "YOUR_EC2_PUBLIC_IP" inventory.ini; then
    print_error "Please configure your EC2 instance details in inventory.ini"
    echo "Replace YOUR_EC2_PUBLIC_IP with your actual EC2 public IP address"
    exit 1
fi

# Check if deploy.yml has been configured with actual repo URL
if grep -q "sg40/Chores.git" deploy.yml; then
    print_warning "Using default repository URL. Make sure this is correct or update project_repo in deploy.yml"
fi

print_status "Starting deployment of ChoreChart Django application..."

# Run the ansible playbook
if ansible-playbook deploy.yml "$@"; then
    print_status "Deployment completed successfully!"
    echo ""
    print_status "Your Django application should now be accessible at:"
    
    # Extract the IP address from inventory file
    IP=$(grep ansible_host inventory.ini | sed 's/.*ansible_host=\([0-9.]*\).*/\1/')
    echo "  http://$IP/"
    echo ""
    print_status "To check the status of your services, run:"
    echo "  ansible django_servers -m systemd -a 'name=gunicorn state=started'"
    echo "  ansible django_servers -m systemd -a 'name=nginx state=started'"
else
    print_error "Deployment failed! Check the error messages above."
    echo ""
    print_status "Common troubleshooting steps:"
    echo "1. Verify your EC2 instance is running and accessible"
    echo "2. Check that your SSH key file exists and has correct permissions (chmod 400)"
    echo "3. Ensure your security group allows SSH (port 22) and HTTP (port 80)"
    echo "4. Verify the inventory.ini file has the correct IP address and key path"
    exit 1
fi