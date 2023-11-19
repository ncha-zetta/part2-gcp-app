##############################################
# Main
##############################################

variable "gcp_project" {
  description = "GCP project name"
  default     = "copper-index-405519"
}

variable "region" {
  description = "GCP region"
  default     = "us-east1"
}

variable "commit_sha" {
  description = "Commit hash"
}

##############################################
# App
##############################################

variable "app_bucket_name" {
  description = "App bucket name"
  default     = "part2-app"
}

variable "zip_file" {
  description = "Zip file name"
  default     = "function.zip"
}