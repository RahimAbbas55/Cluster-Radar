# Cluster-Radar

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?logo=kubernetes&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Status](https://img.shields.io/badge/status-in%20progress-yellow)

A Kubernetes learning project: a market data feed health/SLA monitor.

## What it does
Workers poll market data feeds and record staleness, latency, and gaps.
The API exposes health metrics per feed source. Postgres stores the
time-series health history.

## Why it exists
This project exists to learn Kubernetes orchestration concepts (Deployments,
Services, HPA, self-healing, observability) using a realistic multi-service
app rather than a toy example.

## Architecture
- `api/` - FastAPI service, exposes feed health endpoints
- `worker/` - polls configured feeds on an interval, writes health records
- Postgres - stores feed health time-series

## Status
Phase 1: local development (Docker Compose), raw k8s manifests next.

## Setup
See docker-compose.yml. Instructions added as services come online.