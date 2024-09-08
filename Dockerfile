FROM python:alpine3.20
RUN apk add --no-cache gcc musl-dev mariadb-dev pkgconfig
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 8000
CMD ["python", "manage.py", "runserver"]