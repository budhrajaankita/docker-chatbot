FROM python:3.9

EXPOSE 5051

WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


ADD shrug_command_server.py /app
CMD python shrug_command_server.py