FROM fedora:36

LABEL description Robot Framework in docker

# Set the reports directory environment variable
ENV ROBOT_REPORTS_DIR /opt/robotframework/reports

# Set the tests directory environment variable
ENV ROBOT_TASKS_DIR /opt/robotframework/tasks

# Set the working directory environment variable
ENV ROBOT_WORK_DIR /opt/robotframework/temp

# Setup X Window Virtual Framebuffer
ENV SCREEN_COLOUR_DEPTH 24
ENV SCREEN_HEIGHT 1080
ENV SCREEN_WIDTH 1920

# Setup the timezone to use, defaults to UTC
ENV TZ UTC

# Set number of threads for parallel execution
# By default, no parallelisation
ENV ROBOT_THREADS 1

# Define the default user who'll run the tests
ENV ROBOT_UID 1000
ENV ROBOT_GID 1000

# Dependency versions
ENV CHROMIUM_VERSION 105.0
ENV FIREFOX_VERSION 106.0
ENV GECKO_DRIVER_VERSION v0.30.0
ENV XVFB_VERSION 1.20

# Prepare binaries to be executed
COPY ./shell/chromedriver.sh /opt/robotframework/bin/chromedriver
COPY ./shell/chromium-browser.sh /opt/robotframework/bin/chromium-browser
COPY ./shell/init.sh /opt/robotframework/bin/

#In Fedora DNF package manager , increase the parallel downloads to 10
RUN sudo cat /etc/dnf/dnf.conf

RUN sudo echo "max_parallel_downloads=10" | cat /etc/dnf/dnf.conf

# Install system dependencies
# RUN dnf upgrade -y --refresh \
#     && dnf install -y \
#     chromedriver-${CHROMIUM_VERSION}* \
#     chromium-${CHROMIUM_VERSION}* \
#     firefox-${FIREFOX_VERSION}* \
#     npm \
#     nodejs \
#     python3-pip \
#     tzdata \
#     xorg-x11-server-Xvfb-${XVFB_VERSION}* \
#     && dnf clean all

RUN dnf upgrade -y --refresh \
    && dnf install -y \
    npm \
    nodejs \
    python3-pip \
    tzdata \
    xorg-x11-server-Xvfb-${XVFB_VERSION}* \
    && dnf clean all

ADD https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh miniconda3.sh
RUN /bin/bash miniconda3.sh -b -p /conda && rm miniconda3.sh && echo export PATH=/conda/bin:$PATH >>.bashrc

# FIXME: below is a workaround, as the path is ignored
# RUN mv /usr/lib64/chromium-browser/chromium-browser /usr/lib64/chromium-browser/chromium-browser-original \
#     && ln -sfv /opt/robotframework/bin/chromium-browser /usr/lib64/chromium-browser/chromium-browser

# FROM alpine:3.14
WORKDIR .

COPY . .

#ENV TINI_VERSION v0.18.0
#ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
#RUN chmod +x /tini



ENV PATH="/conda/bin:${PATH}"


## ADD CONDA PATH TO LINUX PATH
ENV PATH /opt/conda/bin:$PATH

## COPY ENV REQUIREMENTS FILES
COPY conda.yml /tmp/conda.yml

#RUN . /root/.bashrc && \
#/root/anaconda3/bin/conda init bash

## CREATE CONDA ENVIRONMENT USING YML FILE
RUN conda env create -f /tmp/conda.yml python=3.8

#RUN conda activate conda_robot_framework

## ADD CONDA ENV PATH TO LINUX PATH
ENV PATH /opt/conda/envs/conda_robot_framework/bin:$PATH
ENV CONDA_DEFAULT_ENV conda_robot_framework

# Gecko drivers
# RUN dnf install -y \
#     wget \
#     # Download Gecko drivers directly from the GitHub repository
#     && wget -q "https://github.com/mozilla/geckodriver/releases/download/$GECKO_DRIVER_VERSION/geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz" \
#     && tar xzf geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
#     && mkdir -p /opt/robotframework/drivers/ \
#     && mv geckodriver /opt/robotframework/drivers/geckodriver \
#     && rm geckodriver-$GECKO_DRIVER_VERSION-linux64.tar.gz \
#     && dnf remove -y \
#     wget \
#     && dnf clean all

## MAKE ALL BELOW RUN COMMANDS USE THE NEW CONDA ENVIRONMENT
CMD ["app/shell/init.sh"]
#SHELL ["conda", "run", "-n", "conda_robot_framework", "/bin/bash", "-c"]

#RUN pwd

#EXPOSE 5003
# The code to run when container is started:
ENTRYPOINT ["conda", "run", "-n", "conda_robot_framework", "python", "/code/main.py"]

CMD tail -f /dev/null

