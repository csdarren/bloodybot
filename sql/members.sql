
CREATE TABLE IF NOT EXISTS public.members
(
    member_id bigint NOT NULL,
    member_name varchar(32) NOT NULL,
    guild_id bigint NOT NULL,
    FOREIGN KEY(guild_id) REFERENCES public.guilds(id),
    CONSTRAINT members_pkey PRIMARY KEY (member_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.members
    OWNER to discord_botuser;
