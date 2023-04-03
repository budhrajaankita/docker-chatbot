FROM python:3.9

EXPOSE 5052

WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD email_server.py /app
CMD python email_server.py