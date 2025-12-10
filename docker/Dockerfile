FROM python:3.8-slim

LABEL maintainer="Gustavo Haase <your-email@domain.com>"
LABEL description="Fairness Framework for Machine Learning"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for data and results
RUN mkdir -p data/synthetic data/case_studies experiments/results

# Set Python path
ENV PYTHONPATH=/app:$PYTHONPATH

# Run tests to verify installation (optional, can comment out for faster builds)
# RUN pytest tests/ -v || echo "Warning: Some tests failed"

# Default command: run Python shell
CMD ["python"]

# Alternative: Run Jupyter notebook server
# CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
