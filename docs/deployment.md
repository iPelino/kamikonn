# KamiKonn Deployment Runbook

This document covers end-to-end provisioning and deployment of KamiKonn on DigitalOcean.

---

## 1. Provision the Droplet

- **Image:** Ubuntu 24.04 LTS (x64)
- **Size:** 4 GB RAM / 2 vCPUs (Basic, AMS3 region)
- **Options:** Enable backups, add your SSH public key during provisioning
- **Firewall:** Allow inbound TCP 22, 80, 443 only

---

## 2. Initial Server Setup

SSH in as root, then run:

```bash
# Update system
apt update && apt upgrade -y

# Create a deploy user
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy

# Install Docker (official script)
curl -fsSL https://get.docker.com | sh
usermod -aG docker deploy

# Verify Docker Compose v2 is bundled
docker compose version

# Install Git
apt install -y git

# Install rclone (for Spaces backups)
curl https://rclone.org/install.sh | bash
```

Switch to the deploy user for all subsequent steps:

```bash
su - deploy
```

---

## 3. Clone the Repository

```bash
sudo mkdir -p /opt/kamikonn
sudo chown deploy:deploy /opt/kamikonn
git clone https://github.com/iPelino/kamikonn.git /opt/kamikonn
cd /opt/kamikonn
```

---

## 4. Create `.env.prod`

```bash
cp .env.example .env.prod
nano .env.prod
```

Fill in every variable. Required variables:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | 50+ character random secret |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `kamikonn.rw,www.kamikonn.rw` |
| `POSTGRES_DB` | `kamikonn` |
| `POSTGRES_USER` | `kamikonn_user` |
| `POSTGRES_PASSWORD` | Strong random password |
| `POSTGRES_HOST` | `db` (Docker service name) |
| `POSTGRES_PORT` | `5432` |
| `REDIS_URL` | `redis://redis:6379/0` |
| `DJANGO_CORS_ALLOWED_ORIGINS` | `https://kamikonn.rw` |
| `GOOGLE_CLIENT_ID` | From Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | From Google Cloud Console |
| `DEFAULT_FROM_EMAIL` | `noreply@kamikonn.rw` |
| `EMAIL_HOST` | SMTP host (e.g. smtp.sendgrid.net) |
| `EMAIL_HOST_USER` | SMTP username |
| `EMAIL_HOST_PASSWORD` | SMTP password / API key |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `DO_SPACES_KEY` | DigitalOcean Spaces access key |
| `DO_SPACES_SECRET` | DigitalOcean Spaces secret |
| `DO_SPACES_BUCKET` | `kamikonn-media` |
| `DO_SPACES_REGION` | `ams3` |
| `DO_SPACES_ENDPOINT` | `https://ams3.digitaloceanspaces.com` |

---

## 5. Configure rclone for Spaces Backups

```bash
rclone config
# Name the remote: spaces
# Type: s3
# Provider: DigitalOcean Spaces
# Access key: <DO_SPACES_KEY>
# Secret key: <DO_SPACES_SECRET>
# Endpoint: ams3.digitaloceanspaces.com
# Leave everything else as default
```

Verify the remote works:

```bash
rclone ls spaces:kamikonn-media/
```

---

## 6. Obtain SSL Certificate

Run the init script once before starting all containers (it temporarily starts nginx in HTTP-only mode):

```bash
cd /opt/kamikonn
chmod +x init-letsencrypt.sh
./init-letsencrypt.sh
```

Follow prompts to enter your domain and email address.

---

## 7. Start All Services

```bash
cd /opt/kamikonn
docker compose -f docker-compose.prod.yml up -d
```

Check that every container is healthy:

```bash
docker compose -f docker-compose.prod.yml ps
```

Expected services: `db`, `redis`, `backend`, `celery`, `celery-beat`, `nginx`, `certbot`.

---

## 8. Run Seed Data

```bash
docker compose -f docker-compose.prod.yml exec backend \
  uv run python manage.py seed_data
```

This populates universities, categories, and any fixture data defined in the management command.

---

## 9. Add GitHub Actions Secrets

In GitHub: **Repository Settings > Secrets and variables > Actions > New repository secret**.

| Secret name | Value |
|---|---|
| `DROPLET_HOST` | Droplet public IP or `kamikonn.rw` |
| `DROPLET_USER` | `deploy` |
| `DROPLET_SSH_KEY` | Contents of `~/.ssh/id_rsa` (deploy user's private key) |

After adding secrets, trigger a test deploy from **Actions > Deploy to Production > Run workflow**.

---

## 10. Set Up Automated Backups (Cron)

Make the script executable and add a cron job for the deploy user:

```bash
chmod +x /opt/kamikonn/scripts/backup_db.sh

crontab -e
# Add this line (runs at 02:00 every day):
0 2 * * * POSTGRES_HOST=localhost POSTGRES_USER=kamikonn_user POSTGRES_DB=kamikonn /opt/kamikonn/scripts/backup_db.sh >> /var/log/kamikonn-backup.log 2>&1
```

> The script reads `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_DB`, and `POSTGRES_PASSWORD` from environment.
> Set `PGPASSWORD` or use a `.pgpass` file to avoid interactive prompts.

---

## 11. Uptime Monitoring

Use [UptimeRobot](https://uptimerobot.com) (free tier):

1. Create a free account at https://uptimerobot.com
2. Add a new monitor: **HTTP(s)**, URL `https://kamikonn.rw/api/health/`
3. Set interval to **5 minutes**
4. Add an alert contact (email or Slack) for downtime notifications

---

## Rollback Procedure

If a deployment causes issues:

```bash
cd /opt/kamikonn
git log --oneline -5          # Find the last good commit hash
git checkout <commit-hash>
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d
```

---

## Useful Commands

```bash
# View live logs for all services
docker compose -f docker-compose.prod.yml logs -f

# View backend logs only
docker compose -f docker-compose.prod.yml logs -f backend

# Open a Django shell
docker compose -f docker-compose.prod.yml exec backend uv run python manage.py shell

# Apply migrations manually
docker compose -f docker-compose.prod.yml exec backend uv run python manage.py migrate --no-input
```
