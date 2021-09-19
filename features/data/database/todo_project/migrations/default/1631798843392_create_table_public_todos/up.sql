CREATE TABLE "public"."todos" (
    "id" uuid NOT NULL DEFAULT uuid_generate_v4(),
    "title" varchar NOT NULL,
    "description" text NOT NULL,
    "state" text NOT NULL DEFAULT 'NEW',
    FOREIGN KEY ("state") REFERENCES "public"."states" ("state") ON UPDATE RESTRICT ON DELETE RESTRICT,
    PRIMARY KEY ("id") , UNIQUE ("id")
);
