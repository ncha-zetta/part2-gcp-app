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

##############################################
# App
##############################################

variable "app_bucket_name" {
  description = "App bucket name"
  default     = "part2-app"
}
