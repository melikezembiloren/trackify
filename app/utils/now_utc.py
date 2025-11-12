from datetime import datetime, timezone

def now_utc():
    return datetime.now(timezone.utc)


class Now:
    @staticmethod
    def now_utc():
        return now_utc()