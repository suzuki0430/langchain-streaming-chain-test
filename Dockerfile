# Use the official Python image with the specified version
FROM python:3.11.6-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Run bash
CMD ["/bin/bash"]
