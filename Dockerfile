# Step 1: Use an official Python base image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to the container
COPY requirements.txt .

# Step 4: Upgrade pip, setuptools, and wheel
RUN pip install --upgrade pip setuptools wheel

# Step 5: Install dependencies
RUN pip install -r requirements.txt

# Step 6: Copy the application code to the container
COPY . .

# Step 7: Expose the port for Flask (Frontend) and Rasa (Backend)
EXPOSE 5000
EXPOSE 5005

# Step 8: Start Flask to serve frontend and Rasa backend
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5000 & rasa run --enable-api --cors '*' --debug"]
