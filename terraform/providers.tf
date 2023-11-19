provider "google" {
  project = var.gcp_project
  region  = var.region
}

data "google_client_config" "default" {}
