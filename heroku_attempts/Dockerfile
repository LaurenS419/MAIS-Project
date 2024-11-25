# Use an official PyTorch runtime as the base image
FROM python:3.11-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file first (to leverage Docker caching)
COPY webapp/requirements.txt /app/requirements.txt

# Install dependencies (this will be cached unless requirements.txt changes)
RUN pip install --timeout=5000 --no-cache-dir -r requirements.txt

# Copy the rest of the app into the container
COPY webapp /app

# Expose the port the app will run on
EXPOSE 5000

# Define the command to run the app using Gunicorn
CMD ["gunicorn", "app:app"]
