output "droplet_ip" {
  description = "Public IPv4 address of the production Droplet"
  value       = digitalocean_droplet.app.ipv4_address
}

output "droplet_id" {
  description = "DigitalOcean Droplet ID"
  value       = digitalocean_droplet.app.id
}

output "media_bucket_name" {
  description = "Spaces media bucket name"
  value       = digitalocean_spaces_bucket.media.name
}

output "media_cdn_endpoint" {
  description = "CDN endpoint for serving media files"
  value       = digitalocean_cdn.media.endpoint
}

output "domain_name" {
  description = "Primary domain"
  value       = digitalocean_domain.app.name
}

output "next_steps" {
  description = "What to do after terraform apply"
  value       = <<-EOT
    Next steps:
    1. SSH into the server: ssh deploy@${digitalocean_droplet.app.ipv4_address}
    2. Create /opt/kamikonn/.env.prod (see .env.example)
    3. Update SPACES_ENDPOINT_URL to: https://${digitalocean_cdn.media.endpoint}
    4. Run: cd /opt/kamikonn && bash nginx/init-letsencrypt.sh
    5. Run: docker compose -f docker-compose.prod.yml up -d
    6. Run: docker compose -f docker-compose.prod.yml exec backend uv run python manage.py migrate
    7. Run: docker compose -f docker-compose.prod.yml exec backend uv run python manage.py seed_data
    8. Add GitHub Actions secrets: DROPLET_HOST=${digitalocean_droplet.app.ipv4_address}
  EOT
}
