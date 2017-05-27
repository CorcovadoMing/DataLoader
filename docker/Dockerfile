FROM alpine

RUN apk update \
    && apk add py2-pip tar xz build-base python-dev jpeg-dev zlib-dev py-numpy \
    && pip install pillow lmdb protobuf
