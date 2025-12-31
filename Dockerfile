# Using a standard Python 3.11 base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy and install requirements
# This ensures all dependencies (Flask, Transformers, Torch, Gunicorn) are installed.
COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Transformers use subword tokenization, so punkt, wordnet, and stopwords are no longer needed.

# Copy the rest of your application code and models
# This includes your 'app.py' and the 'SA_model' folder.
COPY . .

# Expose the correct port for Hugging Face Spaces
EXPOSE 7860

# Run the application using Gunicorn
# This is the industry standard for serving Flask apps in production.
CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]