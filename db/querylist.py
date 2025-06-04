INSERT_CUSTOM_CHANNEL = """
INSERT INTO custom_channel
(reporter, ts, member, create_ts, delete_ts, num_hours, active, notes)
VALUES
($1, $2, $3, $4, $5, $6, $7, $8)
"""
