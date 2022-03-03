ARG HASURA_VERSION

FROM hasura/graphql-engine:${HASURA_VERSION}.cli-migrations-v3

RUN apt update && apt install -y python3-pip && pip3 install pyyaml==6.0

COPY ./hasura/auth/metadata /hasura-metadata