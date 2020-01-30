FROM python:3.6.7
RUN pip install flask 
RUN pip install Tensorflow==1.14.0
RUN pip install -U flask-cors 
RUN useradd -ms /bin/bash admin
COPY . /app
WORKDIR /app
RUN chown -R admin:admin /app
RUN chmod 777 /app
USER admin
ENTRYPOINT ["python"]
CMD ["app.py"]