CUSTOM_CHANNEL_ENTRY_START= """
INSERT INTO custom_channel
(channel_id, guild_id, member_id, create_time)
VALUES
($1, $2, $3, $4);
"""

SELECT_CHANNEL_ISACTIVE = """
SELECT channel_id
FROM custom_channel
WHERE is_active = TRUE;

"""

SELECT_CHANNEL_MEMBER_ISACTIVE = """
SELECT member_id
FROM custom_channel
WHERE is_active = TRUE
AND channel_id = $1
"""

UPDATE_CHANNEL_ISACTIVE = """
UPDATE custom_channel
SET is_active = $1,
    delete_time = $2
WHERE channel_id = $3;
"""
