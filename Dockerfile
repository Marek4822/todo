FROM python:3.11.4-slim
EXPOSE 2137

COPY . .
RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD ["app.py" ]