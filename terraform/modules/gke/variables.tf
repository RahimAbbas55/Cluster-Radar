variable "cluster_name" {
  type        = string
  description = "Name of the GKE cluster"
}

variable "region" {
  type        = string
  description = "GCP region for the cluster"
}

variable "network" {
  type        = string
  description = "VPC network name"
}

variable "subnetwork" {
  type        = string
  description = "VPC subnetwork name"
}

variable "node_count" {
  type        = number
  default     = 1
  description = "Initial number of nodes"
}

variable "machine_type" {
  type        = string
  default     = "e2-medium"
  description = "GCE machine type for nodes"
}