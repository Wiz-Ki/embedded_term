FROM ubuntu:latest
LABEL authors="ki"

ENTRYPOINT ["top", "-b"]