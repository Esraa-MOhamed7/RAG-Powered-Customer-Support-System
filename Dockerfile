# 1) Use an official Python base image
FROM python:3.11-slim

# 2) Set the working directory inside the container
WORKDIR /app

# 3) Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# 4) Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5) Enviroment Variables 
ENV GROQ_API_KEY=${GROQ_API_KEY}

# 5) Copy the rest of the application code into the container
COPY . .

# 6) Expose the port Flask runs on
EXPOSE 5000

# 7) Command to run the Flask application
CMD ["python", "app.py"]