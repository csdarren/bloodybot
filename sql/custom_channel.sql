

-- CREATE custom_channel TABLE --
-- Table: public.custom_channel

-- DROP TABLE IF EXISTS public.custom_channel;

CREATE TABLE IF NOT EXISTS public.custom_channel
(
    channel_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    member_id bigint NOT NULL,
    create_time timestamp with time zone NOT NULL,
    delete_time timestamp with time zone,
    is_active boolean NOT NULL DEFAULT true,
    CONSTRAINT create_channel_pkey PRIMARY KEY (channel_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.custom_channel
    OWNER to discord_botuser;
