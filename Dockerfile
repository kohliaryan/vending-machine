# Use a lightweight Python base image
FROM python:3.12-slim

# Install uv (The magic part)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Set working directory
WORKDIR /app

# Copy dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies (system-wide inside the container)
RUN uv sync --frozen --no-install-project

# Copy the rest of your application code
COPY . .

# Expose the port
EXPOSE 8000

# Run the app
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]