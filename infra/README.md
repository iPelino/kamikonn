# KamiKonn Infrastructure

Terraform configuration for provisioning the KamiKonn production environment on DigitalOcean.

## Resources provisioned

| Resource | Details |
|---|---|
| Droplet | Ubuntu 24.04, s-2vcpu-4gb (2 vCPU / 4 GB), AMS3 |
| Firewall | Inbound: 22, 80, 443 only. Outbound: all |
| DNS | `kamikonn.rw` A record + `www` CNAME |
| Spaces bucket | `kamikonn-media` (private, with CORS for GET/HEAD) |
| CDN | Edge endpoint in front of the media bucket |
| Project | Groups all DO resources under "KamiKonn" |
| cloud-init | Installs Docker, creates deploy user, hardens SSH |

State is stored remotely in a DigitalOcean Spaces bucket (`kamikonn-tf-state`).

---

## Prerequisites

1. **Terraform >= 1.6** — install from https://developer.hashicorp.com/terraform/install
2. **DigitalOcean personal access token** — create at https://cloud.digitalocean.com/account/api/tokens
3. **Spaces access key + secret key** — generate at https://cloud.digitalocean.com/account/api/spaces
4. **SSH key uploaded to DigitalOcean** — must be named `kamikonn-deploy` in DO (Settings > Security > SSH Keys). The key you upload is the one that will be installed on the Droplet and in the deploy user's `authorized_keys`.

---

## One-time bootstrap: create the state bucket

The Terraform backend requires the `kamikonn-tf-state` Spaces bucket to exist **before** you run `terraform init`. This is a chicken-and-egg situation: Terraform cannot create the bucket it needs to store its own state.

Create it manually once:

1. Go to https://cloud.digitalocean.com/spaces
2. Create a new Space: name `kamikonn-tf-state`, region `AMS3`, access `Private`

You only need to do this once. All subsequent state changes are managed by Terraform.

---

## Usage

### 1. Copy and fill in variables

```bash
cd infra/
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars with real values — this file is gitignored
```

### 2. Initialize

Pass Spaces credentials as backend config (not stored in state):

```bash
terraform init \
  -backend-config="access_key=<spaces_access_key>" \
  -backend-config="secret_key=<spaces_secret_key>"
```

Or use the Makefile shortcut (reads from environment variables):

```bash
export SPACES_ACCESS_KEY=your_key
export SPACES_SECRET_KEY=your_secret
make terraform-init
```

### 3. Plan

```bash
terraform plan
# or:
make terraform-plan
```

Review the output carefully before applying.

### 4. Apply

```bash
terraform apply
# or:
make terraform-apply
```

Type `yes` when prompted. After apply completes, the `next_steps` output will print the exact commands to run on the new server.

### 5. Destroy

```bash
terraform destroy
```

> **Warning:** The `digitalocean_droplet.app` resource has `lifecycle { prevent_destroy = true }`.
> You must remove or comment out that block before `terraform destroy` will succeed.
> This is intentional to prevent accidental deletion of production data.

---

## After apply: GitHub Actions secrets

Set the following secrets in your GitHub repository (Settings > Secrets and variables > Actions):

| Secret | Value |
|---|---|
| `DROPLET_HOST` | The IP printed in the `droplet_ip` output |
| `DROPLET_USER` | `deploy` |
| `DROPLET_SSH_KEY` | Private key corresponding to the `kamikonn-deploy` key uploaded to DO |

---

## Notes

- The `ssh_key_fingerprint` variable is accepted by `variables.tf` for documentation and future use, but the Droplet currently references the SSH key by the `data.digitalocean_ssh_key.deploy_key` data source (looked up by the name `kamikonn-deploy`). If you prefer to use the fingerprint directly, replace the data source lookup with `data "digitalocean_ssh_key" "deploy_key" { fingerprint = var.ssh_key_fingerprint }`.
- `terraform.tfvars` is listed in `.gitignore` and must never be committed. It contains your DO token and Spaces keys.
- The `.terraform.lock.hcl` file is also gitignored here because provider binaries differ between developer machines and CI environments. Re-run `terraform init` after cloning.
