# Manual Deployment Instructions

### **Prerequisites**
1. **AWS Account**: Ensure your son has an AWS account with free tier eligibility. The t2.micro instance is free tier eligible for 750 hours/month for the first 12 months.
2. **Django Project**: The Django app should be tested locally and have a `requirements.txt` file listing all dependencies (e.g., `django`, `gunicorn`). Generate it using:
   ```bash
   pip freeze > requirements.txt
   ```
3. **Git Repository (Optional but Recommended)**: Push the Django project to a GitHub repository for easy transfer to the EC2 instance. If not using Git, we’ll cover transferring files via SCP.
4. **Basic Command Line Knowledge**: Familiarity with terminal commands (Linux or macOS) or tools like PuTTY (Windows).
5. **Local Tools**: Ensure Python, pip, and Git are installed on his laptop.

---

### **Step-by-Step Instructions**

#### **Step 1: Set Up an EC2 Instance**
1. **Log in to AWS Management Console**:
   - Go to [AWS Management Console](https://aws.amazon.com/console/) and sign in with your son’s AWS account.
   - Navigate to the **EC2 Dashboard** by searching for “EC2” in the services menu.

2. **Launch a New EC2 Instance**:
   - Click **Launch Instance** → **Launch Instance**.
   - **Name the instance**: Enter a name like `django-app-server`.
   - **Choose an AMI**:
     - Select **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type** (free tier eligible, 64-bit x86).
   - **Choose Instance Type**:
     - Select **t2.micro** (free tier eligible, 1 vCPU, 1 GiB RAM).
   - **Create a Key Pair**:
     - Under **Key pair (login)**, click **Create new key pair**.
     - Name it (e.g., `django-ec2-key`).
     - Choose **RSA** and **.pem** format.
     - Download the `.pem` file and store it securely (e.g., `~/Desktop/django-ec2-key.pem`).
     - Set permissions on the key file (on Linux/macOS):
       ```bash
       chmod 400 ~/Desktop/django-ec2-key.pem
       ```
   - **Configure Network Settings**:
     - Under **Network settings**, click **Edit**.
     - Create a new security group (e.g., `django-sg`) or edit the default.
     - Add rules to allow:
       - **SSH (port 22)**: Source = `My IP` (or `Anywhere` for simplicity, but less secure).
       - **HTTP (port 80)**: Source = `Anywhere` (0.0.0.0/0) to allow public access.
       - **TCP (port 8000)**: Source = `Anywhere` (0.0.0.0/0) to allow public access.
       - Optionally, add **HTTPS (port 443)** for future SSL setup.
   - **Configure Storage**:
     - Accept the default 8 GiB gp2 volume (free tier allows up to 30 GiB).
   - **Launch Instance**:
     - Click **Launch instance**.
     - Go to **Instances** in the EC2 Dashboard, select the instance, and note the **Public IPv4 address** (e.g., `3.123.456.789`).

3. **Connect to the EC2 Instance**:
   - Open a terminal (Linux/macOS) or PuTTY (Windows).
   - Use SSH to connect:
     ```bash
     ssh -i ~/Desktop/django-ec2-key.pem ubuntu@<public-ip>
     ```
     Replace `<public-ip>` with the instance’s public IP (e.g., `ssh -i ~/Desktop/django-ec2-key.pem ubuntu@3.123.456.789`).
   - If prompted, accept the host key by typing `yes`.
   - You should now be logged into the Ubuntu instance.

#### **Step 2: Set Up the EC2 Instance**
1. **Update the System**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

2. **Install Required Software**:
   - Install Python, pip, virtualenv, Nginx, and Git:
     ```bash
     sudo apt install python3 python3-pip python3-venv nginx git -y
     ```

3. **Transfer the Django Project**:
   - **Option 1: Clone from GitHub** (recommended):
     - If the project is in a GitHub repository, clone it:
       ```bash
       git clone https://github.com/<your-username>/<your-repo>.git
       cd <your-repo>
       ```
     - Replace `<your-username>` and `<your-repo>` with the appropriate GitHub details.
   - **Option 2: Transfer via SCP** (if not using Git):
     - From your son’s laptop, zip the project:
       ```bash
       zip -r django_project.zip <project-folder>
       ```
     - Copy it to the EC2 instance:
       ```bash
       scp -i ~/Desktop/django-ec2-key.pem django_project.zip ubuntu@<public-ip>:/home/ubuntu/
       ```
     - On the EC2 instance, unzip:
       ```bash
       cd /home/ubuntu
       sudo apt install unzip -y
       unzip django_project.zip
       cd <project-folder>
       ```

4. **Set Up a Virtual Environment**:
   - Create and activate a virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   - Install project dependencies:
     ```bash
     pip install -r requirements.txt
     ```
     Ensure `gunicorn` is in `requirements.txt`. If not, install it:
     ```bash
     pip install gunicorn
     ```

5. **Configure Django Settings**:
   - Edit the Django `settings.py` file (e.g., `/home/ubuntu/<project-folder>/<project-name>/settings.py`):
     ```python
     ALLOWED_HOSTS = ['<public-ip>', 'localhost', '127.0.0.1']
     DEBUG = False  # Set to False for production
     STATIC_ROOT = '/home/ubuntu/<project-folder>/static'
     ```
     Replace `<public-ip>` with the EC2 instance’s public IP.
   - Collect static files:
     ```bash
     python manage.py collectstatic
     ```
     Answer `yes` if prompted.

#### **Step 3: Install PostgreSQL on Ubuntu**
1. **Update the Package List**:
   - Open a terminal on the Ubuntu laptop.
   - Update the package index:
     ```bash
     sudo apt update
     ```

2. **Install PostgreSQL**:
   - Install PostgreSQL and its client tools:
     ```bash
     sudo apt install postgresql postgresql-contrib -y
     ```
   - This installs PostgreSQL (version 14 for Ubuntu 22.04 by default) and additional utilities.

3. **Verify PostgreSQL Installation**:
   - Check if PostgreSQL is running:
     ```bash
     sudo systemctl status postgresql
     ```
     You should see `active (running)`. If not, start it:
     ```bash
     sudo systemctl start postgresql
     sudo systemctl enable postgresql
     ```
   - Verify the PostgreSQL version:
     ```bash
     psql --version
     ```
     Example output: `psql (PostgreSQL) 14.13`.

4. **Access PostgreSQL**:
   - PostgreSQL creates a default user called `postgres`. Switch to the `postgres` user to manage databases:
     ```bash
     sudo -u postgres psql
     ```
   - You should see the `psql` prompt: `postgres=#`.

#### **Step 4: Create a PostgreSQL Database and User**
1. **Create a Database**:
   - While in the `psql` prompt, create a database for the Django app:
     ```sql
     CREATE DATABASE chores_db;
     ```
     Replace `chores_db` with a name of your choice (e.g., `myapp_db`).

2. **Create a PostgreSQL User**:
   - Create a user with a password:
     ```sql
     CREATE USER chores_user WITH PASSWORD 'secure_password';
     ```
     Replace `chores_user` with a desired username and `secure_password` with a strong password.
   - Grant the user full privileges on the database:
     ```sql
     GRANT ALL PRIVILEGES ON DATABASE chores_db TO chores_user;
     ```
   - Exit the `psql` prompt:
     ```sql
     \q
     ```

3. **Test Database Access**:
   - Verify the user can connect to the database:
     ```bash
     psql -h localhost -U chores_user -d chores_db
     ```
   - Enter the password (`secure_password`) when prompted. If successful, you’ll see the `psql` prompt: `chores_db=>`.
   - Exit with `\q`.


6. **Test the Django Application**:
   - Run the Django development server:
     ```bash
     python manage.py runserver 0.0.0.0:8000
     ```
   - Open a browser and visit `http://<public-ip>:8000`. If it works, stop the server with `Ctrl+C`.

#### **Step 5: Configure Gunicorn**
1. **Test Gunicorn**:
   - From the project directory, with the virtual environment activated:
     ```bash
     gunicorn --bind 0.0.0.0:8000 <project-name>.wsgi:application
     ```
     Replace `<project-name>` with your Django project’s name (e.g., `myproject` if `myproject/wsgi.py` exists).
   - Verify it works by visiting `http://<public-ip>:8000`. Stop with `Ctrl+C`.

2. **Create a Gunicorn Service**:
   - Create a Gunicorn service file:
     ```bash
     sudo nano /etc/systemd/system/gunicorn.service
     ```
   - Add the following, adjusting paths and names:
     ```ini
     [Unit]
     Description=Gunicorn instance for Django app
     After=network.target

     [Service]
     User=ubuntu
     Group=www-data
     WorkingDirectory=/home/ubuntu/<project-folder>
     ExecStart=/home/ubuntu/<project-folder>/venv/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/<project-folder>/gunicorn.sock <project-name>.wsgi:application

     [Install]
     WantedBy=multi-user.target
     ```
     Replace `<project-folder>` and `<project-name>` as needed.
   - Enable and start the service:
     ```bash
     sudo systemctl start gunicorn
     sudo systemctl enable gunicorn
     ```
   - Check status:
     ```bash
     sudo systemctl status gunicorn
     ```

#### **Step 6: Configure Nginx**
1. **Create an Nginx Configuration**:
   - Create a new Nginx config file:
     ```bash
     sudo nano /etc/nginx/sites-available/django
     ```
   - Add the following:
     ```nginx
     server {
         listen 80;
         server_name <public-ip>;

         location = /favicon.ico { access_log off; log_not_found off; }
         location /static/ {
             root /home/ubuntu/<project-folder>;
         }

         location / {
             include proxy_params;
             proxy_pass http://unix:/home/ubuntu/<project-folder>/gunicorn.sock;
         }
     }
     ```
     Replace `<public-ip>` and `<project-folder>` as needed.

2. **Enable the Nginx Configuration**:
   - Create a symbolic link:
     ```bash
     sudo ln -s /etc/nginx/sites-available/django /etc/nginx/sites-enabled
     ```
   - Test the Nginx configuration:
     ```bash
     sudo nginx -t
     ```
   - Restart Nginx:
     ```bash
     sudo systemctl restart nginx
     ```

3. **Change Socket Permisions**:
    ```bash
    sudo chown ubuntu:www-data /home/ubuntu/Chores/gunicorn.sock
    sudo chmod 664 /home/ubuntu/Chores/gunicorn.sock
    sudo chmod g+rx /home/ubuntu/Chores
    sudo chown ubuntu:www-data /home/ubuntu/Chores
    sudo chmod 755 /home/ubuntu
    sudo systemctl restart gunicorn
    ```

4. **Move the socket to a more permissive directory**:
   - Edit the Gunicorn service file:
     ```bash
     sudo nano /etc/systemd/system/gunicorn.service
     ```
   - Change the socket path in the ExecStart line to:
     ```bash
     ExecStart=/home/ubuntu/Chores/venv/bin/gunicorn --workers 3 --bind unix:/tmp/gunicorn.sock <project-name>.wsgi:application
     ```
   - Update the Nginx config to match:
     ```bash
     sudo nano /etc/nginx/sites-available/django
     ```
   - Change the proxy_pass line to:
     ```bash
     proxy_pass http://unix:/tmp/gunicorn.sock;
     ```
   - Reload services:
     ```bash
     sudo systemctl daemon-reload
     sudo systemctl restart gunicorn
     sudo systemctl restart nginx
     ```

    

5. **Verify the Deployment**:
   - Open a browser and visit `http://<public-ip>`. The Django app should be live.
   - If it doesn’t work, check logs:
     ```bash
     sudo systemctl status nginx
     sudo systemctl status gunicorn
     sudo tail -f /var/log/nginx/error.log
     ```

#### **Step 7: Final Notes**
- **Free Tier Limits**: Ensure the instance is t2.micro and storage is under 30 GiB to stay within the free tier. Stop the instance when not in use to save hours:
  ```bash
  sudo halt
  ```
  Restart it from the EC2 Dashboard.
- **Security**: For production, consider:
  - Using an Elastic IP to maintain a static IP.
  - Setting up HTTPS with Let’s Encrypt.
  - Restricting SSH access to specific IPs.
- **Troubleshooting**:
  - If the app doesn’t load, ensure port 80 is open in the security group.
  - Verify `ALLOWED_HOSTS` includes the public IP.
  - Check file permissions for static files:
    ```bash
    sudo chown -R ubuntu:www-data /home/ubuntu/<project-folder>/static
    sudo chmod -R 755 /home/ubuntu/<project-folder>/static
    ```

---

### **Accessing the App**
The Django app will be accessible at `http://<public-ip>`. Share this IP with others to show off the app. For example, if the public IP is `3.123.456.789`, visit `http://3.123.456.789`.

---

### **Additional Learning**
- **Database Setup**: If the app uses a database, consider SQLite for simplicity (stored on the EC2 instance) or AWS RDS Free Tier (e.g., PostgreSQL) for production. Update `settings.py` with database details if using RDS.
- **Scaling**: Explore AWS Elastic Beanstalk for easier management or Auto Scaling for handling traffic spikes.
- **Monitoring**: Use AWS CloudWatch to monitor instance performance.

This process teaches your son about cloud infrastructure, server setup, and web server configuration while keeping costs within the free tier. If he runs into issues, he can check logs or ask for clarification on specific steps. Happy coding![](https://medium.com/%40fahimad/deploy-django-applications-on-aws-ec2-142d968253e3)[](https://www.linkedin.com/pulse/deploy-django-application-ec2-instance-nginx-dtechnologies-cqdif)

