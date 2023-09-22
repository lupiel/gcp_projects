provider "google" {
  project     = "Project ID"
  region      = "us-central-1"
}

resource "google_storage_bucket" "test-bucket-for-state" {
  name        = "<bucket_name>"
  location    = "US"
  uniform_bucket_level_access = true
  force_destroy = true # terraform destroy
}

terraform {
  # select one backend 
  backend "local" {
    path = "terraform/state/terraform.tfstate"
  }
  # backend "gcs" {
  #   bucket  = "<bucket_name>"
  #   prefix  = "terraform/state"
  # }
}


