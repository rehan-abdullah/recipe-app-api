FROM python:3.7-alpine
LABEL maintainer="rehanabdullah <m.rehan.abdullah@gmail.com>"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt

# Dependencies that are not removed during installation
RUN apk add --update --no-cache postgresql-client jpeg-dev

# Dependencies that are removed during installation
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# For static and media files
# -p flag, make all sub-dirs
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
# Give created user ownership of /vol/ dir
# -R flag, recursively adds sub-dirs to ownership
RUN chown -R user:user /vol/
# Gives user full access to web dir. Other users can read and execute from the dir
RUN chown -R 755 /vol/web
USER user