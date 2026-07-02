provider "digitalocean" {
  token             = var.do_token
  spaces_access_id  = var.spaces_access_key
  spaces_secret_key = var.spaces_secret_key
}

# ---------------------------------------------------------------------------
# SSH Key (must already exist in your DO account)
# ---------------------------------------------------------------------------
data "digitalocean_ssh_key" "deploy_key" {
  name = "kamikonn-deploy"
}

# ---------------------------------------------------------------------------
# Droplet
# ---------------------------------------------------------------------------
resource "digitalocean_droplet" "app" {
  name   = "kamikonn-prod"
  region = var.region
  size   = var.droplet_size
  image  = "ubuntu-24-04-x64"

  ssh_keys  = [data.digitalocean_ssh_key.deploy_key.id]
  user_data = file("${path.module}/cloud-init.yaml")

  tags = ["kamikonn", "production"]

  lifecycle {
    prevent_destroy = true
  }
}

# ---------------------------------------------------------------------------
# Firewall
# ---------------------------------------------------------------------------
resource "digitalocean_firewall" "app" {
  name = "kamikonn-prod-firewall"

  droplet_ids = [digitalocean_droplet.app.id]

  # Inbound rules
  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  # Outbound rules (allow all)
  outbound_rule {
    protocol              = "tcp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "all"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "icmp"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}

# ---------------------------------------------------------------------------
# DNS
# ---------------------------------------------------------------------------
resource "digitalocean_domain" "app" {
  name       = var.domain_name
  ip_address = digitalocean_droplet.app.ipv4_address
}

resource "digitalocean_record" "apex" {
  domain = digitalocean_domain.app.name
  type   = "A"
  name   = "@"
  value  = digitalocean_droplet.app.ipv4_address
  ttl    = 300
}

resource "digitalocean_record" "www" {
  domain = digitalocean_domain.app.name
  type   = "CNAME"
  name   = "www"
  value  = "@"
  ttl    = 300
}

# ---------------------------------------------------------------------------
# Spaces (S3-compatible object storage for media)
# ---------------------------------------------------------------------------
resource "digitalocean_spaces_bucket" "media" {
  name   = "kamikonn-media"
  region = var.region
  acl    = "private"
}

resource "digitalocean_spaces_bucket_cors_configuration" "media" {
  bucket = digitalocean_spaces_bucket.media.name
  region = var.region

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["https://${var.domain_name}", "https://www.${var.domain_name}"]
    max_age_seconds = 3000
  }
}

# CDN endpoint for media bucket
resource "digitalocean_cdn" "media" {
  origin = digitalocean_spaces_bucket.media.bucket_domain_name
}

# ---------------------------------------------------------------------------
# Project (groups all resources)
# ---------------------------------------------------------------------------
resource "digitalocean_project" "kamikonn" {
  name        = var.project_name
  description = "KamiKonn academic event discovery platform"
  purpose     = "Web Application"
  environment = "Production"

  resources = [
    digitalocean_droplet.app.urn,
    digitalocean_spaces_bucket.media.urn,
    digitalocean_domain.app.urn,
  ]
}
