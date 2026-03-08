# Job Monitor Worker

A Dockerized automation worker that monitors job APIs and sends alerts to Slack, Discord, and Telegram.

## Features
- Multi-API ingestion (Rise + ArbeitNow)
- Job normalization pipeline
- PostgreSQL deduplication
- Multi-channel notifications
- Docker containerized worker
- Environment-based configuration

## Stack
Python  
Docker  
PostgreSQL  
REST APIs

## Deployment
Runs as a containerized background worker.