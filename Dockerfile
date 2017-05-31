FROM alpine

RUN apk update \
    && apk add git py2-pip tar xz build-base python-dev jpeg-dev zlib-dev py-numpy \
    && pip install pillow lmdb protobuf \
    && git clone https://github.com/CorcovadoMing/DataLoader.git /root/data-loader

ENTRYPOINT ["python", "/root/data-loader/main.py"]
