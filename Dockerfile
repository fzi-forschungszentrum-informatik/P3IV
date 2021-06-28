ARG DISTRIBUTION=20.04
FROM ubuntu:${DISTRIBUTION} AS p3iv_deps

ARG ROS_DISTRO=noetic
ARG DEBIAN_FRONTEND=noninteractive

# basics
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    bash-completion \
    build-essential \
    curl \
    git \
    cmake \
    ipython3 \
    keyboard-configuration \
    locales \
    lsb-core \
    nano \
    python-dev \
    software-properties-common \
    sudo \
    wget \
    && locale-gen en_US.UTF-8 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# locale
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    ROS_DISTRO=${ROS_DISTRO}

# install ROS
RUN echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list \
    && curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -

# dependencies for lanelet2
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libboost-all-dev \
    libeigen3-dev \
    libgeographic-dev \
    libpugixml-dev \
    python3-catkin-pkg \
    libboost-python-dev \
    python3-osrf-pycommon \
    python3-catkin-tools \
    ros-$ROS_DISTRO-catkin \
    ros-$ROS_DISTRO-rosbash \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# dependencies for p3iv
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    libcgal-dev \
    pybind11-dev \
    python3-pip \
    libgoogle-glog-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


# create a user
RUN useradd --create-home --groups sudo --shell /bin/bash developer \
    && mkdir -p /etc/sudoers.d \
    && echo "developer ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/developer \
    && chmod 0440 /etc/sudoers.d/developer


# environment, dependencies and entry points
USER developer
ENV HOME /home/developer
WORKDIR /home/developer/workspace

RUN sudo chown -R developer:developer /home/developer \
    && echo "export ROS_HOSTNAME=localhost" >> /home/developer/.bashrc \
    && echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> /home/developer/.bashrc \
    && echo "source /home/developer/workspace/devel/setup.bash" >> /home/developer/.bashrc

# setup workspace, add dependencies
RUN cd /home/developer/workspace \
    && /bin/bash -c "source /home/developer/.bashrc && catkin init && catkin config --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo" \
    && git clone https://github.com/KIT-MRT/mrt_cmake_modules.git /home/developer/workspace/src/mrt_cmake_modules \
    && git clone https://github.com/fzi-forschungszentrum-informatik/Lanelet2.git /home/developer/workspace/src/lanelet2   

# second stage: get the code and build the image
FROM p3iv_deps As p3iv

# bring in the code
COPY --chown=developer:developer . /home/developer/workspace/src/p3iv

# update dependencies
RUN git -C /home/developer/workspace/src/mrt_cmake_modules pull

# build
RUN /bin/bash -c "source /opt/ros/$ROS_DISTRO/setup.bash && catkin build --no-status"

# run tests
RUN cd src/p3iv && pip3 install -r requirements.txt && catkin run_tests