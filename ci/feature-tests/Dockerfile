ARG PYTHON_VERSION
ARG HASURA_CLI_VERSION

FROM python:${PYTHON_VERSION}-slim AS build

ARG FAAS_CLI_VERSION

COPY ./requirements.txt .

RUN apt update && apt install -y gcc wget git curl \
  && curl -sSL https://github.com/openfaas/faas-cli/releases/download/${FAAS_CLI_VERSION}/faas-cli --output /usr/local/bin/faas-cli \
  && chmod u+x /usr/local/bin/faas-cli \
  && pip install --no-cache-dir -r requirements.txt

FROM hasura/graphql-engine:${HASURA_CLI_VERSION}.cli-migrations-v3 AS hasura-migrations

FROM python:${PYTHON_VERSION}

COPY --from=build /usr/local/bin/faas-cli /usr/local/bin/faas-cli
COPY --from=build /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages
COPY --from=build /usr/local/bin /usr/local/bin
COPY --from=hasura-migrations /bin/hasura-cli /usr/local/bin/hasura
# this copy is necessary as long as we clone behave's git repo
COPY --from=build /src /src

WORKDIR /app