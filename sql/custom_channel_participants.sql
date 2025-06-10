CREATE TABLE IF NOT EXISTS public.custom_channel_participants
(
    id bigserial PRIMARY KEY NOT NULL,
    channel_id bigint NOT NULL,
    user_id bigint NOT NULL,
    joined_at timestamp with time zone NOT NULL,
    FOREIGN KEY(channel_id) REFERENCES public.custom_channel(channel_id),
    UNIQUE (channel_id, user_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.custom_channel_participants
    OWNER to discord_botuser;
