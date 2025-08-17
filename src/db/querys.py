# INSERT

INSERT_CUSTOM_CHANNEL = """
INSERT INTO custom_channel
(channel_id, guild_id, creator_member_id, create_ts)
VALUES
($1, $2, $3, $4)
ON CONFLICT DO NOTHING;
"""

INSERT_CUSTOM_CHANNEL_MEMBER = """
INSERT INTO custom_channel_member
(channel_id, participant_member_id)
VALUES
($1, $2)
ON CONFLICT DO NOTHING;
"""

# UPDATE

UPDATE_CHANNEL_IS_ACTIVE = """
UPDATE custom_channel
SET is_active = $1, delete_ts = $2
WHERE channel_id = $3;
"""

# SELECT

# Queries for custom_channels with is_active = TRUE attribute
SELECT_CHANNEL_IS_ACTIVE = """
SELECT c.channel_id
FROM custom_channel c
WHERE c.is_active = TRUE;
"""

# Queries a create_ts from a specified channel_id
SELECT_CHANNEL_CREATE_TS = """
SELECT create_ts
FROM custom_channel
WHERE channel_id = $1;
"""

# Queries a creator_member_id of a specified channel_id
SELECT_CHANNEL_CREATOR_MEMBER_ID = """
SELECT creator_member_id
FROM custom_channel
WHERE channel_id = $1;
"""

# Queries all channel_ids from a specified date
SELECT_CHANNEL_DATE = """
SELECT channel_id
FROM custom_channel
WHERE create_ts::date = $1::date;
"""

