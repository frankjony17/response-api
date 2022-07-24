
FROM lnx-python3-centos:3.6.8

ARG build_date
ARG vcs_ref
ARG VERSAO=1.0.0b9
ARG BOM_PATH="/docker/fks"

# hadolint ignore=DL3033
RUN yum install -y gcc gcc-c++ make cmake && yum clean all
ENV CMAKE_C_COMPILER=/usr/bin/gcc CMAKE_CXX_COMPILER=/usr/bin/g++ MODE=prod
# hadolint ignore=DL3033
RUN yum install -y python36-devel boost-devel libXext libSM libXrender && yum clean all

COPY dist/response_api-${VERSAO}-py3-none-any.whl /
# hadolint ignore=DL3013
RUN pip3 --no-cache-dir install --upgrade pip
# hadolint ignore=DL3013
RUN pip3 --no-cache-dir install response_api-${VERSAO}-py3-none-any.whl
RUN rm -fr /response_api-${VERSAO}-py3-none-any.whl

RUN mkdir -p /prometheus

ENV VERSAO=$VERSAO \
    MODE=prod \
    prometheus_multiproc_dir=/prometheus

EXPOSE 9000

WORKDIR /usr/local/lib/python3.6/site-packages/response_api
# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/
COPY response_api/config ./config
# Run gunicorn
ENTRYPOINT ["gunicorn", "-c", "config/gunicorn.py", "main:app"]