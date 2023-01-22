FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

COPY source ./source

# Put your own Dockfile commands here
RUN apt-get update && apt-get install -y \
    python3-pip libgl1 libglib2.0-0 libsm6 libxrender1 libxext6


RUN apt-get update \
  && apt-get -y install build-essential \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/* \
  && wget https://github.com/Kitware/CMake/releases/download/v3.24.1/cmake-3.24.1-Linux-x86_64.sh \
      -q -O /tmp/cmake-install.sh \
      && chmod u+x /tmp/cmake-install.sh \
      && mkdir /opt/cmake-3.24.1 \
      && /tmp/cmake-install.sh --skip-license --prefix=/opt/cmake-3.24.1 \
      && rm /tmp/cmake-install.sh \
      && ln -s /opt/cmake-3.24.1/bin/* /usr/local/bin


RUN pip install opencv-python apriltag keyboard pynetworktables

CMD python3 --version