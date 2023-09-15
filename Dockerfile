FROM python:3.11-alpine

RUN apk upgrade --available

# Installing Oracle instant client
RUN apk --no-cache add libaio libnsl libc6-compat curl && \
    cd /tmp && \
    curl -o instantclient-basiclite.zip https://download.oracle.com/otn_software/linux/instantclient/1912000/instantclient-basiclite-linux.x64-19.12.0.0.0dbru.zip -SL && \
    unzip instantclient-basiclite.zip && \
    mv instantclient*/ /usr/lib/instantclient && \
    rm instantclient-basiclite.zip && \
    ln -s /usr/lib/instantclient/libclntsh.so.19.1 /usr/lib/libclntsh.so && \
    ln -s /usr/lib/instantclient/libocci.so.19.1 /usr/lib/libocci.so && \
    ln -s /usr/lib/instantclient/libociicus.so /usr/lib/libociicus.so && \
    ln -s /usr/lib/instantclient/libnnz19.so /usr/lib/libnnz19.so && \
    ln -s /usr/lib/libnsl.so.3 /usr/lib/libnsl.so.1 && \
    ln -s /lib/libc.so.6 /usr/lib/libresolv.so.2 && \
    ln -s /lib64/ld-linux-x86-64.so.2 /usr/lib/ld-linux-x86-64.so.2

ENV ORACLE_BASE /usr/lib/instantclient
ENV LD_LIBRARY_PATH /usr/lib/instantclient
ENV TNS_ADMIN /usr/lib/instantclient
ENV ORACLE_HOME /usr/lib/instantclient
RUN apk add dumb-init

# add extra linux package 
RUN apk add --no-cache ca-certificates curl bash coreutils vim nano busybox-extras iputils net-tools

# add gcc compiler support for cx_Oracle recompile problem
RUN apk add --no-cache gcc musl-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install Cython

RUN pip3 install -r requirements.txt

COPY . /app

EXPOSE 5000

# CMD exec /bin/sh -c "trap : TERM INT; (while true; do sleep 1000; done) & wait"
ENTRYPOINT python3 app.py

#docker run --name webapp -p 5000:5000 -v /root/login_flask/Config:/app/Config webapp:latest
