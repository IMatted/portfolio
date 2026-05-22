FROM python:3
LABEL maintainer="Danish Singh <danishs@uoregon.edu>"
RUN apt-get update -y
RUN apt-get install -y python3-dev build-essential
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN echo 'alias nosetests="pytest"' >> ~/.bashrc
ENTRYPOINT ["python"]
CMD ["flask_brevets.py"]