FROM python:3.5.3
MAINTAINER Your Name "woka@alterra.id"
RUN mkdir -p /demo
COPY . /demo
RUN pip install -r /demo/requirements.txt
WORKDIR /demo
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
