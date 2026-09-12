import utime
from huskylens import HuskyLensV1


class HuskyAdapter:
    def __init__(self, version=1, empty_notify_every=15, debug=False):
        self.version = version
        self.debug = bool(debug)
        self._notify_every = max(1, int(empty_notify_every))
        self._empty_reads = 0
        self._last_ids = []
        self.hl = self._select_backend(version)

    def _select_backend(self, version):
        if version in (1, 2, "auto"):
            return HuskyLensV1()
        raise ValueError("version must be 1, 2, or 'auto'")

    def get_tag_ids(self, attempts=3, wait_ms=80):
        ids = []
        for _ in range(max(1, attempts)):
            try:
                ids = list(self.hl.get_tag_ids())
            except Exception:
                utime.sleep_ms(wait_ms)
                continue
            if ids:
                self._empty_reads = 0
                self._last_ids = ids
                return ids
            utime.sleep_ms(wait_ms)
        self._empty_reads += 1
        return ids

    def get_result(self, attempts=3, wait_ms=80):
        for _ in range(max(1, attempts)):
            try:
                result = self.hl.get_result()
            except Exception:
                utime.sleep_ms(wait_ms)
                continue
            if result:
                return result
            utime.sleep_ms(wait_ms)
        return {"camera_version": 0, "algorithm": "unknown", "ids": [], "blocks": [], "count": 0}

    def get_object(self, object_id=None, attempts=3, wait_ms=80):
        for _ in range(max(1, attempts)):
            try:
                obj = self.hl.get_object(object_id=object_id)
            except Exception:
                utime.sleep_ms(wait_ms)
                continue
            if obj is not None:
                return obj
            utime.sleep_ms(wait_ms)

    def last_successful_ids(self):
        return list(self._last_ids)
