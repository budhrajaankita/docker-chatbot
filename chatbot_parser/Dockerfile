FROM python:3.9

EXPOSE 5050

WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

ADD chatbot_parser.py /app
CMD python chatbot_parser.py