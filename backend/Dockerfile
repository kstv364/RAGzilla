# Use a Python base image
FROM python:3.9-slim-buster

# Install uv
RUN pip install uv

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies using uv
COPY requirements.txt .
RUN uv pip install --system --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
