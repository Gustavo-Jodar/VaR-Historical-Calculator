FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the application code into the container
COPY app /app

# Create the uploads directory inside the container
RUN mkdir -p /app/uploads

# Install dependencies
RUN pip install flask flask-restx werkzeug numpy pandas

# Expose port 5000 for the Flask application
EXPOSE 5000

# Set the command to run the Flask application
CMD ["python3", "main.py"]
