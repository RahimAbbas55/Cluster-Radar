resource "google_container_cluster" "primary" {
  name     = var.cluster_name
  location = var.region

  # we manage node pools separately, so remove the default one
  remove_default_node_pool = true
  initial_node_count       = 1

  network    = var.network
  subnetwork = var.subnetwork
}