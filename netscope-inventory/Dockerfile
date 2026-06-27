FROM public.ecr.aws/docker/library/python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Ensure logs are sent directly to the console
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy dependency list first (improves Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the Flask/Gunicorn port
EXPOSE 5000

# Start the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
