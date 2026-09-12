from microbit import i2c, sleep, running_time

HUSKYLENS_V1_ADDR = 0x32
HEADER = b"\x55\xAA"
DEVICE_ID = 0x11
CMD_REQUEST_ALL = 0x20
CMD_ALGORITHM = 0x2D


class Block:
    __slots__ = ("x", "y", "w", "h", "ID")

    def __init__(self, x, y, w, h, ID):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.ID = ID


class HuskyLensV1:
    def __init__(self, address=HUSKYLENS_V1_ADDR):
        self.address = address
        try:
            i2c.init(freq=100000)
        except Exception:
            pass
        self._write_command(CMD_ALGORITHM, b"\x05\x00")
        sleep(50)

    def _checksum(self, payload):
        total = 0
        for b in payload:
            total += b
        return bytes([total & 255])

    def _write(self, data):
        i2c.write(self.address, data)

    def _write_with_checksum(self, body):
        frame = HEADER + body + self._checksum(HEADER + body)
        self._write(frame)

    def _write_command(self, command, data=b""):
        self._write_with_checksum(bytes([DEVICE_ID, len(data), command]) + data)

    def _read(self, count):
        try:
            return i2c.read(self.address, count)
        except Exception:
            return b""

    def knock(self):
        return True

    def switch_algorithm(self, algorithm_name):
        if algorithm_name != "tag_recognition":
            return False
        self.algorithm_tag_recognition()
        return True

    def algorithm_tag_recognition(self):
        self._write_command(CMD_ALGORITHM, b"\x05\x00")
        sleep(20)

    def request_blocks(self):
        self._write_command(CMD_REQUEST_ALL)

    def read_blocks(self, max_blocks=5, timeout_ms=150):
        deadline = running_time() + timeout_ms
        buf = b""
        max_bytes = max(1, max_blocks) * 16
        while running_time() < deadline and len(buf) < max_bytes:
            part = self._read(32)
            if part:
                buf += part
            else:
                sleep(5)

        blocks = []
        i = 0
        while i + 6 <= len(buf):
            if buf[i:i + 2] != HEADER:
                i += 1
                continue
            if i + 5 > len(buf):
                break
            payload_len = buf[i + 3]
            command_id = buf[i + 4]
            frame_end = i + 5 + payload_len
            if frame_end >= len(buf):
                break
            payload = buf[i + 5:frame_end]
            if buf[frame_end] != (sum(buf[i:frame_end]) & 255):
                i = frame_end + 1
                continue
            if command_id == 0x2A and len(payload) >= 10:
                x = payload[0] | (payload[1] << 8)
                y = payload[2] | (payload[3] << 8)
                w = payload[4] | (payload[5] << 8)
                h = payload[6] | (payload[7] << 8)
                ID = payload[8] | (payload[9] << 8)
                if ID > 0 and w > 0 and h > 0:
                    blocks.append(Block(x, y, w, h, ID))
                    if len(blocks) >= max_blocks:
                        break
            i = frame_end + 1
        return blocks

    def get_result(self):
        self.algorithm_tag_recognition()
        self.request_blocks()
        blocks = self.read_blocks()
        return {
            "camera_version": 1,
            "algorithm": "tag_recognition",
            "ids": [block.ID for block in blocks],
            "blocks": blocks,
            "count": len(blocks),
        }

    def get_tag_ids(self):
        return self.get_result()["ids"]

    def get_object(self, object_id=None):
        blocks = self.get_result()["blocks"]
        if object_id is None:
            return blocks[0] if blocks else None
        for block in blocks:
            if block.ID == object_id:
                return block
