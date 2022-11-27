FROM python:latest
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY receiver.py ./
COPY sender.py ./
CMD ["python", "-u", "receiver.py"]