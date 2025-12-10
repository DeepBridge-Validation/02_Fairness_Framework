# Docker Setup

Docker configuration for the Fairness Framework.

## 🚀 Quick Start

### Using Docker

```bash
# Build image
docker build -t fairness-framework -f docker/Dockerfile .

# Run interactive shell
docker run -it fairness-framework /bin/bash

# Run with data mounted
docker run -it -v $(pwd)/data:/app/data fairness-framework
```

### Using Docker Compose

```bash
# Start Jupyter notebook server
docker-compose -f docker/docker-compose.yml up

# Access notebook at: http://localhost:8888

# Run in background
docker-compose -f docker/docker-compose.yml up -d

# Stop
docker-compose -f docker/docker-compose.yml down
```

### Run Experiments

```bash
# Run all experiments
docker-compose -f docker/docker-compose.yml --profile experiments up

# Or run specific experiment
docker run -v $(pwd)/data:/app/data fairness-framework \
    python experiments/scripts/exp1_detection.py
```

## 📋 Services

### fairness-framework
- **Purpose**: Interactive development with Jupyter
- **Ports**: 8888 (Jupyter)
- **Volumes**: data/, experiments/results/, experiments/notebooks/

### experiments (optional)
- **Purpose**: Run experiments in batch mode
- **Profile**: experiments
- **Volumes**: data/, experiments/

## 🔧 Customization

### Environment Variables

Add to `docker-compose.yml`:
```yaml
environment:
  - DATA_PATH=/app/data
  - RESULTS_PATH=/app/experiments/results
```

### Mount Additional Directories

Add to `volumes` in `docker-compose.yml`:
```yaml
volumes:
  - ../src:/app/src
  - ../tests:/app/tests
```

## 🐛 Troubleshooting

### Permission Issues

If you encounter permission issues with mounted volumes:
```bash
# On Linux, run container as your user
docker run -u $(id -u):$(id -g) -v $(pwd)/data:/app/data fairness-framework
```

### Port Already in Use

If port 8888 is in use, change in `docker-compose.yml`:
```yaml
ports:
  - "9999:8888"  # Access at http://localhost:9999
```

### Rebuild After Changes

```bash
# Rebuild image
docker-compose -f docker/docker-compose.yml build

# Force rebuild
docker-compose -f docker/docker-compose.yml build --no-cache
```

## 📦 Image Size Optimization

Current image is based on `python:3.8-slim` (~200MB base).

For smaller image, use `alpine`:
```dockerfile
FROM python:3.8-alpine
# Note: May need additional build dependencies
```

## 🔍 Debugging

```bash
# Check logs
docker-compose -f docker/docker-compose.yml logs

# Follow logs
docker-compose -f docker/docker-compose.yml logs -f

# Enter running container
docker exec -it fairness-framework /bin/bash

# Inspect image
docker run -it fairness-framework ls -la /app
```
