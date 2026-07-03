#!/usr/bin/env bash
# KamiKonn database backup script
# Dumps the PostgreSQL database and uploads to DigitalOcean Spaces
# Requires: pg_dump, rclone configured with remote named 'spaces'
# Usage: ./scripts/backup_db.sh
# Cron: 0 2 * * * /opt/kamikonn/scripts/backup_db.sh >> /var/log/kamikonn-backup.log 2>&1

set -euo pipefail

DATESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
BACKUP_DIR="/tmp/kamikonn_backups"
BACKUP_FILE="${BACKUP_DIR}/kamikonn_${DATESTAMP}.sql.gz"
SPACES_PATH="spaces:kamikonn-media/backups/"
RETENTION_DAYS=30

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Starting backup: ${BACKUP_FILE}"

pg_dump \
    --host "${POSTGRES_HOST:-localhost}" \
    --port "${POSTGRES_PORT:-5432}" \
    --username "${POSTGRES_USER:-kamikonn_user}" \
    --dbname "${POSTGRES_DB:-kamikonn}" \
    --no-password \
    | gzip > "${BACKUP_FILE}"

echo "[$(date)] Upload to Spaces: ${SPACES_PATH}"
rclone copy "${BACKUP_FILE}" "${SPACES_PATH}"

echo "[$(date)] Cleaning up local backups older than ${RETENTION_DAYS} days"
find "${BACKUP_DIR}" -name "*.sql.gz" -mtime +${RETENTION_DAYS} -delete

echo "[$(date)] Backup complete: kamikonn_${DATESTAMP}.sql.gz"
