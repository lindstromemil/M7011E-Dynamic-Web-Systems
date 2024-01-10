# Use an official Python runtime as a base image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r src/internal/requirements.txt

EXPOSE 5000

# Specify the command to run on container start
CMD ["python", "app.py"]