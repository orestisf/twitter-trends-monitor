FROM python:3
COPY requirements.txt trends-monitor.py /app/
WORKDIR /app
RUN pip install -r requirements.txt
CMD [ "python", "trends-monitor.py" ]
