FROM alpine

RUN apk update \
    && apk add git py2-pip tar xz build-base python-dev jpeg-dev zlib-dev py-numpy \
    && pip install pillow lmdb protobuf

RUN mkdir -p /root/data-loader
ADD * /root/data-loader/

ENTRYPOINT ["python", "/root/data-loader/main.py"]
