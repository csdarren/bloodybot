CREATE TABLE IF NOT EXISTS public.guilds
(
    id bigint NOT NULL,
    name varchar(32) NOT NULL,
    CONSTRAINT guilds_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.guilds
    OWNER to discord_botuser;
