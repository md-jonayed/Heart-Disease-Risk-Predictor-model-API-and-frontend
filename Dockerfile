# Use a lightweight official Python runtime
FROM python:3.11-slim-buster

# Set environment variables for non-interactive commands
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# --- Copy Dependencies and Install Packages ---

# Copy only the requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# --- Copy Application Files ---

# Copy the rest of the application files and directories
COPY app.py .
COPY frontend.py .
COPY heart.csv .
COPY index.html .
COPY Model/ Model/
COPY schema/ schema/

# --- Expose Ports ---

# Expose the ports used by FastAPI (8000) and Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# --- Define Entrypoint and Run Command ---

# Default command: Run the FastAPI backend
# We use Uvicorn directly to serve the application defined in app.py
# The host 0.0.0.0 is essential for the application to be accessible outside the container.
# set the port to 8000 as per your configuration.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

# --- Alternative Startup: Streamlit Frontend ---
# To run the Streamlit frontend instead, you can override the CMD when running the container.
# The command to run the Streamlit app would be:
# docker run ... heart-prediction-app streamlit run frontend.py --server.port 8501 --server.enableCORS true