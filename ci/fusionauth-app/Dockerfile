ARG FUSIONAUTH_VERSION

FROM python:3.9-slim AS build

ARG FUSIONAUTH_VERSION

RUN pip install fusionauth-client==${FUSIONAUTH_VERSION}

FROM fusionauth/fusionauth-app:${FUSIONAUTH_VERSION}

COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages