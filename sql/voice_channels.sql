CREATE TABLE IF NOT EXISTS public.voice_channels
(
    channel_id bigint NOT NULL,
    channel_name varchar(25) NOT NULL,
    guild_id bigint NOT NULL,
    FOREIGN KEY(guild_id) REFERENCES public.guilds(id),
    CONSTRAINT voice_channels_pkey PRIMARY KEY (channel_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.voice_channels
    OWNER to discord_botuser;
