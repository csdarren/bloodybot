# INSERT

INSERT_BOT_GUILDS = """
INSERT INTO guilds
(id, name)
VALUES
($1, $2)
ON CONFLICT DO NOTHING;
"""

INSERT_GUILD_CATEGORY = """
INSERT INTO categories
(category_id, category_name, guild_id)
VALUES
($1, $2, $3)
ON CONFLICT DO NOTHING;
"""

INSERT_GUILD_VOICE_CHANNEL = """
INSERT INTO voice_channels
(channel_id, channel_name, guild_id)
VALUES
($1, $2, $3)
ON CONFLICT DO NOTHING;
"""

INSERT_GUILD_TEXT_CHANNEL = """
INSERT INTO text_channels
(channel_id, channel_name, guild_id)
VALUES
($1, $2, $3)
ON CONFLICT DO NOTHING;
"""

INSERT_GUILD_MEMBER = """
INSERT INTO members
(member_id, member_name, guild_id)
VALUES
($1, $2, $3)
ON CONFLICT DO NOTHING;
"""



INSERT_CUSTOM_CHANNEL = """
INSERT INTO custom_channel
(channel_id, guild_id, member_id, create_time)
VALUES
($1, $2, $3, $4);
"""

INSERT_CUSTOM_CHANNEL_PARTICIPANTS = """
INSERT INTO custom_channel_participants
(channel_id, member_id)
VALUES
($1, $2);
"""

# UPDATE

UPDATE_CHANNEL_ISACTIVE = """
UPDATE custom_channel
SET is_active = $1,
delete_time = $2
WHERE channel_id = $3;
"""

# SELECT

SELECT_CHANNEL_ISACTIVE = """
SELECT channel_id
FROM custom_channel
WHERE is_active = TRUE;
"""

SELECT_CHANNEL_MEMBER_ISACTIVE = """
SELECT member_id
FROM custom_channel
WHERE is_active = TRUE
AND channel_id = $1;
"""

SELECT_CHANNEL_PARTICIPANTS = """
SELECT member_id
FROM custom_channel_participants
WHERE channel_id = $1;
"""

SELECT_CHANNELS_TIMESTAMP = """
SELECT channel_id
FROM custom_channel
WHERE create_time::date = $1::date
"""

