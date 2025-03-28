# Use official Python image
FROM python:3.12.3

# Set working directory inside container
WORKDIR /app

# Copy all files to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy asyncpg python-dotenv openai "pydantic[email]" werkzeug PyJWT


# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the app
CMD ["uvicorn", "backend.api.__init__:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
