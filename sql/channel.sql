-- Base channel table. Defines all channels, regardless of type
CREATE TABLE IF NOT EXISTS public.custom_channel
(
    channel_id bigint NOT NULL,
    guild_id bigint NOT NULL,
    creator_member_id bigint NOT NULL,
    create_ts timestamp with time zone NOT NULL,
    delete_ts timestamp with time zone DEFAULT NULL,
    is_active boolean NOT NULL DEFAULT true,
    CONSTRAINT custom_channel_pkey PRIMARY KEY (channel_id)
);

CREATE TABLE IF NOT EXISTS public.custom_channel_member
(
    channel_id bigint NOT NULL,
    participant_member_id bigint NOT NULL,
    CONSTRAINT custom_channel_member_pkey PRIMARY KEY (channel_id, participant_member_id),
    FOREIGN KEY(channel_id) REFERENCES custom_channel(channel_id)
);

-- Alter all tables to ensure they belong to discord_botuser
ALTER TABLE IF EXISTS public.custom_channel
    OWNER to discord_botuser;
ALTER TABLE IF EXISTS public.custom_channel_member
    OWNER to discord_botuser;
