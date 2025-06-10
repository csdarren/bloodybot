CREATE TABLE IF NOT EXISTS public.categories
(
    category_id bigint NOT NULL,
    category_name varchar(25) NOT NULL,
    guild_id bigint NOT NULL,
    FOREIGN KEY(guild_id) REFERENCES public.guilds(id),
    CONSTRAINT categories_pkey PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.categories
    OWNER to discord_botuser;
