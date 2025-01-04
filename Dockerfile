FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]