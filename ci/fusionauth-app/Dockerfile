ARG FUSIONAUTH_VERSION

FROM fusionauth/fusionauth-app:${FUSIONAUTH_VERSION}

ARG FUSIONAUTH_VERSION

USER root

RUN apt update && apt install -y python3-pip && pip3 install fusionauth-client==${FUSIONAUTH_VERSION}

USER fusionauth