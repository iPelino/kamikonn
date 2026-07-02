terraform {
  required_version = ">= 1.6"

  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }

  backend "s3" {
    # DigitalOcean Spaces as Terraform state backend
    # Initialize with:
    #   terraform init \
    #     -backend-config="access_key=<spaces_access_key>" \
    #     -backend-config="secret_key=<spaces_secret_key>"
    endpoint                    = "https://ams3.digitaloceanspaces.com"
    bucket                      = "kamikonn-tf-state"
    key                         = "kamikonn/terraform.tfstate"
    region                      = "us-east-1" # required field, ignored by Spaces
    skip_credentials_validation = true
    skip_metadata_api_check     = true
    skip_region_validation      = true
    force_path_style            = true
  }
}
