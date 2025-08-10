# Use a Python base image
FROM python:3.9-slim-buster

# Install uv
RUN pip install uv

# Set the working directory in the container
WORKDIR /app/frontend

# Copy the requirements file (assuming frontend also uses the same requirements for gradio)
# It's better to have a separate requirements.txt for frontend if dependencies differ
# For simplicity, I'll assume it uses the main requirements.txt for now.
# In a real-world scenario, you'd have frontend/requirements.txt
COPY requirements.txt /app/requirements.txt
RUN uv pip install --system --no-cache-dir -r /app/requirements.txt

# Copy the frontend application code
COPY . .

# Expose the port Gradio runs on (default is 7860)
EXPOSE 7860

# Command to run the application
CMD ["python", "app.py"]
