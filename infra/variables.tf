variable "do_token" {
  description = "DigitalOcean personal access token"
  type        = string
  sensitive   = true
}

variable "ssh_key_fingerprint" {
  description = "Fingerprint of the SSH key already uploaded to DigitalOcean (Settings > Security > SSH Keys)"
  type        = string
}

variable "region" {
  description = "DigitalOcean region slug"
  type        = string
  default     = "ams3"
}

variable "droplet_size" {
  description = "Droplet size slug"
  type        = string
  default     = "s-2vcpu-4gb"
}

variable "domain_name" {
  description = "Primary domain name (without www)"
  type        = string
  default     = "kamikonn.rw"
}

variable "spaces_access_key" {
  description = "Spaces access key for media bucket"
  type        = string
  sensitive   = true
}

variable "spaces_secret_key" {
  description = "Spaces secret key for media bucket"
  type        = string
  sensitive   = true
}

variable "project_name" {
  description = "DigitalOcean project name to group resources"
  type        = string
  default     = "KamiKonn"
}
