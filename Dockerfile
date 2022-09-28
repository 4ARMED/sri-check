FROM python:3

WORKDIR /app
COPY . ${WORKDIR}
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT [ "./sri-check" ]