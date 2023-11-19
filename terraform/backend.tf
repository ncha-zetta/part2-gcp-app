terraform {
  backend "gcs" {
    bucket  = "part2-tfstate-app"
    prefix  = "terraform/state"
  }
}
