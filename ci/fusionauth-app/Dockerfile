ARG FUSIONAUTH_VERSION

FROM fusionauth/fusionauth-app:${FUSIONAUTH_VERSION}

RUN apt update && apt install -y python3-pip \
    && pip3 install fusionauth-client==${FUSIONAUTH_VERSION}