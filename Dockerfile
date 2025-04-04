FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install all required dependencies, including Flask, Gunicorn, Flask-SQLAlchemy, and Flask-WTF
RUN pip install flask gunicorn flask-sqlalchemy flask-wtf

# Copy application files into the container
COPY . .

# Expose the port Gunicorn will listen on (5000)
EXPOSE 5000

# Start the Flask application using Gunicorn
CMD ["gunicorn", "--log-level", "debug", "--preload", "-w", "1", "-b", "0.0.0.0:5000", "app:app"]
# Note: The app variable in the CMD command should be replaced with the actual name of your Flask app module if it's different.
# For example, if your Flask app is in a file named 'myapp.py', you would use "myapp:app" instead of "app:app".
