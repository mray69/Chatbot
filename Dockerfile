FROM python:3.9-slim

# Install tini
RUN apt-get update && apt-get install -y tini

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application code to the container
COPY . .

# Expose necessary ports
EXPOSE 5000
EXPOSE 5005

# Use tini to manage both processes
CMD ["/usr/bin/tini", "--", "sh", "-c", "flask run --host=0.0.0.0 --port=5000 & rasa run --enable-api --cors '*' --debug"]
