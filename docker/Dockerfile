# Use official Python image
FROM python:3.12.3

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "backend.api.__init__:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
