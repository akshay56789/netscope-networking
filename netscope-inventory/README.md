# NetScope Inventory

NetScope Inventory is a purposefully built, production-style Flask application designed specifically to be deployed in Microsoft Azure. Its primary purpose is to serve as an educational and testing workload for advanced networking concepts.

While it contains a simple Inventory Management System (Products table), its true value lies in the **Networking Diagnostic Module** which exposes telemetry and request data.

## Features for Azure Networking Demonstrations

- **Health Probes**: `/health` endpoint to test Azure Load Balancer and Application Gateway probe behavior.
- **Route-Based Routing**: `/api/products`, `/api/users`, `/api/orders` endpoints for testing Application Gateway path-based rules.
- **Header Forwarding Inspection**: `/headers` and `/clientip` endpoints to demonstrate how Application Gateway and Nginx forward client IP addresses (`X-Forwarded-For`).
- **SSL Termination**: `/ssltest` validates if traffic arrived via HTTP or HTTPS, showing how App Gateway terminates SSL.
- **Load Balancer Diagnostics**: Server Identity banner dynamically updates to show the Hostname and Private IP of the VM processing the request, perfect for demonstrating round-robin or sticky session routing.
- **Timeouts & WAF Testing**: `/slow` (10s delay) and `/error` (HTTP 500) endpoints allow you to intentionally test Application Gateway timeouts and Web Application Firewall anomaly detection rules.

## Local Development (SQLite)

For ease of local development, the app uses SQLite by default.

1. **Install Python 3.12+**
2. **Clone and Setup Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables:**
   Copy `.env.example` to `.env` and adjust if needed.
   ```bash
   cp .env.example .env
   ```
5. **Initialize Database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```
6. **Run the App:**
   ```bash
   python run.py
   ```
   Access at `http://localhost:5000`

## Azure Deployment (MySQL)

This app is designed to be deployed on an Azure Linux VM (Ubuntu/Debian) running Nginx and Gunicorn, connected to an Azure Database for MySQL Flexible Server.

1. **Configure MySQL Environment Variables:**
   In your `.env` or system environment variables, set:
   ```
   DB_HOST=your-server.mysql.database.azure.com
   DB_PORT=3306
   DB_NAME=netscope_db
   DB_USER=your_user
   DB_PASSWORD=your_password
   ```

2. **Running with Gunicorn (Production):**
   ```bash
   gunicorn -w 4 -b 127.0.0.1:5000 run:app
   ```

3. **Nginx Reverse Proxy Configuration:**
   When running behind Nginx, configure Nginx to forward headers so Flask can accurately read client IPs and SSL status:
   ```nginx
   server {
       listen 80;
       server_name your_domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

## Folder Structure
- `/app` - Core application code.
- `/app/diagnostics` - Networking and request telemetry logic.
- `/app/routes` - Blueprint route controllers.
- `/logs` - Output directory for `app.log` (JSON structured or flat).
