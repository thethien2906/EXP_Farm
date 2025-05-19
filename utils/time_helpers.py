def seconds_to_human_readable(seconds):
    """
    Convert seconds to human-readable format like 2h 15m 30s
    :param seconds: total seconds
    :return: str: Formatted time string
    """
    hours = seconds // 3600
    seconds = seconds % 3600
    minutes = seconds // 60
    seconds = seconds % 60

    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:
        parts.append(f"{seconds}s")

    return ' '.join(parts)

def minutes_to_seconds(minutes):
    """

    :param minutes: Number of minutes
    :return: Total seconds
    """
    return minutes * 60


