# Use an official Python runtime as the base image
FROM python:3.10.5

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file to the container
COPY requirements.txt .

RUN apt-get update && apt-get install -y postgresql-client

# Install the project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code to the container
COPY . .

# Set an environment variable for PostgreSQL connection (optional)
ENV POSTGRES_HOST=localhost
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=coil_db
# Expose the port your application runs on
EXPOSE 8000

# Run your python script
CMD ["python", "main.py"]