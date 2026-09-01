"""
Author: John Robertson (GitHub: Robbo-lab)
License: GNU
"""
import utime
from huskylib import HuskyLens

class HuskyAdapter:
    """
    Adapter for HuskyLens to return learned tag IDs (integers).
    Ensures algorithm is Tag Recognition and adds simple retry/backoff.
    """
    def __init__(self, empty_notify_every=15):
        """Initialise the adapter with timing for empty reads."""
        self.hl = HuskyLens()
        self._notify_every = max(1, int(empty_notify_every))
        self._empty_reads = 0
        self._last_ids = []

    def get_tag_ids(self, attempts=3, wait_ms=80):
        """
        Read tag IDs from HuskyLens with retries.

        Args:
            attempts: Number of read attempts before giving up.
            wait_ms: Wait between attempts to avoid hammering I2C.
        Returns:
            list[int]: IDs returned by the latest successful read, or [].
        """
        ids = []
        for _ in range(max(1, attempts)):
            try:
                self.hl.algorithm_tag_recognition()
                self.hl.request_blocks()
                blocks = self.hl.read_blocks(timeout_ms=150)
            except Exception as e:
                print("HuskyAdapter: read failed ->", e)
                utime.sleep_ms(wait_ms)
                continue
            ids = [b.ID for b in blocks if getattr(b, "ID", 0) > 0]
            if ids:
                break
            utime.sleep_ms(wait_ms)

        if ids:
            self._empty_reads = 0
            self._last_ids = list(ids)
        else:
            self._empty_reads += 1
            if (self._empty_reads % self._notify_every) == 0:
                print("HuskyAdapter: still waiting for a tag...")
        return ids

    def last_successful_ids(self):
        """Return a copy of the most recent successful ID list."""
        return list(self._last_ids)