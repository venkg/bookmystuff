FROM python:3.6.7
COPY . /app
WORKDIR /app
RUN pip install flask 
RUN pip install Tensorflow==1.14.0 
ENTRYPOINT ["python"]
CMD ["app.py"]