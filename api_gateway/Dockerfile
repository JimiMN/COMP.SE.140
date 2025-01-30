FROM python:3.10-alpine

# Set the working directory inside the container
WORKDIR /app

# Install necessary dependencies for building packages
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev openssl-dev python3-dev

# Copy the requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy the rest of the app code into the container
COPY app.py /app/

# Expose the port Flask will run on
EXPOSE 8197

# Command to run the Flask app
CMD ["python", "app.py"]
