FROM python:alpine3.19
ADD . .
RUN pip install mysql-connector-python flask
EXPOSE 5002
CMD ["python", "-m", "flask", "--app", "hub", "run", "--host=0.0.0.0", "--port", "6002"]