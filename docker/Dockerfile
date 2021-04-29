FROM ubuntu:20.04

# update aptitude
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Zurich
RUN apt-get update && apt-get -y --fix-missing upgrade

# install aptitude essentials
RUN apt-get -y install \
    build-essential \
    meson \
    cmake \
    git \
    vim \
    curl \
    wget \
    doxygen \
    clang-format \
    libgsl-dev \
    libeigen3-dev \
    openmpi-bin \
    openmpi-common \
    libhdf5-openmpi-dev \
    libcairo2-dev \
    libcairo-gobject2 \
    python3-dev \
    python3-pip \
    python3-numpy \
    python3-matplotlib \
    python3-pandas \
    python3-scipy \
    python3-xlrd

RUN python3 -m pip install --upgrade pip

CMD ["/bin/bash"]

# add non-root user
RUN useradd -m korali
WORKDIR /home/korali
USER korali

# install korali
RUN git clone https://github.com/cselab/korali.git --recursive
# FIXME: [fabianw@mavt.ethz.ch; 2021-02-18] use `master` branch once merged
RUN (cd korali && git checkout meson && meson setup build --prefix=$HOME/.local --buildtype release --strip -Donednn=false && meson install -C build)
