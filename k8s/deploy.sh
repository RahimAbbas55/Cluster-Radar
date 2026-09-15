#!/bin/bash
set -e

echo "Applying namespace, secrets, and config..."
kubectl apply -f k8s/manifests/namespace.yaml
kubectl apply -f k8s/manifests/secret.yaml
kubectl apply -f k8s/manifests/configmap.yaml

echo "Deploying Postgres..."
kubectl apply -f k8s/manifests/postgres-pvc.yaml
kubectl apply -f k8s/manifests/postgres-deployment.yaml
kubectl apply -f k8s/manifests/postgres-service.yaml

echo "Waiting for Postgres to be ready..."
kubectl wait --for=condition=ready pod -l app=postgres -n cluster-radar --timeout=60s

echo "Building and loading images..."
docker build -t cluster-radar-api:local ./api
docker build -t cluster-radar-worker:local ./worker
kind load docker-image cluster-radar-api:local --name cluster-radar
kind load docker-image cluster-radar-worker:local --name cluster-radar

echo "Deploying API and worker..."
kubectl apply -f k8s/manifests/api-deployment.yaml
kubectl apply -f k8s/manifests/api-service.yaml
kubectl apply -f k8s/manifests/worker-deployment.yaml

echo "Done. Check status with: kubectl get pods -n cluster-radar"