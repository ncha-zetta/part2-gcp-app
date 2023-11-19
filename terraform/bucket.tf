resource "google_storage_bucket" "app_bucket" {
  name          = var.app_bucket_name
  location      = var.region
}