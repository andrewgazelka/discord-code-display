# Start from a minimal Python environment
FROM python:3.12-slim

# Create the working directory inside the container
WORKDIR /app

# Copy in just the files needed to install dependencies first
COPY pyproject.toml uv.lock ./

# Install uv itself
RUN pip install --no-cache-dir uv

# Use uv to pip-install the dependencies
# This ensures they're installed in a way that Python can find them
RUN uv pip install --system .

# Now copy in the rest of your app's source code
COPY . .

# (Optional) Expose a port if you're running a web server
# EXPOSE 8000

# Finally, define the command that starts your app
CMD ["python", "hello.py"]