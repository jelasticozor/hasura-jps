ARG HASURA_VERSION

FROM hasura/graphql-engine:${HASURA_VERSION}.cli-migrations-v3

COPY ./hasura/auth/migrations /hasura-migrations
COPY ./hasura/auth/metadata /hasura-metadata