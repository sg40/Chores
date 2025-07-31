# Ansible Deployment for ChoreChart Django Application

This directory contains Ansible playbooks and configuration files to automate the deployment of the ChoreChart Django application to AWS EC2 instances.

## Prerequisites

1. **AWS EC2 Instance**: You must have an EC2 instance running Ubuntu 22.04 LTS
2. **Ansible**: Install Ansible on your local machine:
   ```bash
   pip install -r deploy/requirements-ansible.txt
   ```
3. **SSH Key**: Have your EC2 instance's SSH key file (.pem) available
4. **Security Groups**: Ensure your EC2 instance's security group allows:
   - SSH (port 22) from your IP
   - HTTP (port 80) from anywhere (0.0.0.0/0)
   - TCP (port 8000) from anywhere (0.0.0.0/0) - for testing

## Setup Instructions

### 1. Configure Inventory

Edit the `inventory.ini` file and replace the placeholder values:

```ini
[django_servers]
ec2-instance ansible_host=YOUR_EC2_PUBLIC_IP ansible_user=ubuntu ansible_ssh_private_key_file=~/path/to/your/django-ec2-key.pem
```

Replace:
- `YOUR_EC2_PUBLIC_IP` with your EC2 instance's public IP address
- `~/path/to/your/django-ec2-key.pem` with the actual path to your SSH key file

### 2. Update Repository URL

Edit `deploy.yml` and update the `project_repo` variable with your actual GitHub repository URL:

```yaml
project_repo: "https://github.com/yourusername/Chores.git"
```

### 3. Set SSH Key Permissions

Ensure your SSH key has the correct permissions:

```bash
chmod 400 ~/path/to/your/django-ec2-key.pem
```

## Deployment

### Run the Complete Deployment

From the `deploy/` directory, run:

```bash
ansible-playbook deploy.yml
```

This will:
1. Update the system packages
2. Install Python, PostgreSQL, Nginx, and other dependencies
3. Clone your Django project from GitHub
4. Set up a Python virtual environment
5. Install Python dependencies
6. Configure PostgreSQL database and user
7. Create production Django settings
8. Run database migrations
9. Collect static files
10. Configure and start Gunicorn service
11. Configure and start Nginx
12. Set proper file permissions

### Run Specific Tasks

You can run specific parts of the deployment using tags (if you add them to the playbook):

```bash
# Example: Only update application code
ansible-playbook deploy.yml --tags "app"

# Example: Only restart services
ansible-playbook deploy.yml --tags "services"
```

### Check Deployment Status

After deployment, you can verify the services are running:

```bash
# Check if services are running
ansible django_servers -m systemd -a "name=gunicorn state=started"
ansible django_servers -m systemd -a "name=nginx state=started"

# Check service status
ansible django_servers -m command -a "systemctl status gunicorn"
ansible django_servers -m command -a "systemctl status nginx"
```

## Post-Deployment

### Access Your Application

After successful deployment, your Django application will be available at:
- `http://YOUR_EC2_PUBLIC_IP/`

### Troubleshooting

If the deployment fails or the application isn't accessible:

1. **Check service logs**:
   ```bash
   ansible django_servers -m command -a "journalctl -u gunicorn -n 50"
   ansible django_servers -m command -a "journalctl -u nginx -n 50"
   ```

2. **Check Nginx error logs**:
   ```bash
   ansible django_servers -m command -a "tail -n 50 /var/log/nginx/error.log"
   ```

3. **Verify file permissions**:
   ```bash
   ansible django_servers -m command -a "ls -la /home/ubuntu/Chores/"
   ansible django_servers -m command -a "ls -la /tmp/gunicorn.sock"
   ```

4. **Test database connection**:
   ```bash
   ansible django_servers -m shell -a "cd /home/ubuntu/Chores && source venv/bin/activate && python manage.py dbshell --settings=ChoreChart.settings_prod"
   ```

### Manual Restart Services

If you need to restart services manually:

```bash
# Restart Gunicorn
ansible django_servers -m systemd -a "name=gunicorn state=restarted" --become

# Restart Nginx
ansible django_servers -m systemd -a "name=nginx state=restarted" --become
```

## File Structure

```
deploy/
├── deploy.yml              # Main Ansible playbook
├── inventory.ini           # Inventory file with server details
├── ansible.cfg            # Ansible configuration
├── README.md              # This file
└── templates/
    ├── django_settings_prod.py.j2  # Production Django settings template
    ├── gunicorn.service.j2         # Gunicorn systemd service template
    └── nginx_django.conf.j2        # Nginx configuration template
```

## Security Considerations

This deployment includes basic security configurations, but for production use consider:

1. **HTTPS**: Set up SSL/TLS certificates using Let's Encrypt
2. **Firewall**: Configure UFW or AWS security groups more restrictively
3. **Secret Key**: Use environment variables for Django SECRET_KEY
4. **Database**: Use AWS RDS instead of local PostgreSQL for better reliability
5. **Monitoring**: Set up logging and monitoring solutions
6. **Backups**: Implement automated database and file backups

## Updating the Application

To update your application after making changes:

1. Push your changes to GitHub
2. Run the playbook again:
   ```bash
   ansible-playbook deploy.yml
   ```

The playbook will pull the latest code and restart services as needed.