terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_compute_network" "vpc" {
  name                    = "cluster-radar-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "cluster-radar-subnet"
  ip_cidr_range = "10.10.0.0/24"
  region        = var.region
  network       = google_compute_network.vpc.id
}

module "gke" {
  source = "./modules/gke"

  cluster_name = "cluster-radar"
  region       = var.region
  network      = google_compute_network.vpc.name
  subnetwork   = google_compute_subnetwork.subnet.name
}