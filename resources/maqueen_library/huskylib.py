"""
Author: John Robertson (GitHub: Robbo-lab)
License: GNU
"""
from microbit import i2c, sleep, running_time
import struct

HUSKYLENS_ADDR = 0x32       # Default HuskyLens I2C address
HEADER = b"\x55\xAA"
DEVICE_ID = 0x11
CMD_REQUEST_ALL = 0x20      # Summary frame containing counts
CMD_ALGORITHM = 0x2D        # Switch algorithm (data = alg bytes)

class Block:
    """
    Container for a HuskyLens detection bounding box.
    Uses __slots__ to minimise memory usage on the micro:bit.
    """
    __slots__ = ("x","y","w","h","ID")
    def __init__(self, x, y, w, h, ID):
        """Represent a HuskyLens detection bounding box."""
        self.x, self.y, self.w, self.h, self.ID = x, y, w, h, ID
    def __repr__(self):
        """Provides a readable representation for debugging."""
        return "Block(x=%s,y=%s,w=%s,h=%s,ID=%s)" % (self.x,self.y,self.w,self.h,self.ID)

class HuskyLens:
    def __init__(self, address=HUSKYLENS_ADDR):
        """Prepare the HuskyLens for I2C communication and tag detection."""
        self.address = address
        # I2C initialise
        try:
            i2c.init(freq=100000)  # Standard mode, can be changed if processor struggles
        except Exception:
            pass

        # Set algorithm to Tag Recognition (Note: also set on-camera alongwith I2C protocol)
        self._write_command(CMD_ALGORITHM, b"\x05\x00")
        sleep(50)

    # Private library helpers not used by the adapter
    def _checksum(self, payload):
        """Calculate a simple checksum byte for the provided payload."""
        total = 0
        for b in payload:
            total += b
        return bytes([total & 0xFF])

    def _write(self, b):
        """Send raw bytes over I2C to the HuskyLens."""
        i2c.write(self.address, b)

    def _write_with_checksum(self, body):
        """Write a full command frame with header and checksum."""
        frame = HEADER + body + self._checksum(HEADER + body)
        self._write(frame)

    def _write_command(self, command, data=b""):
        """Send a command byte plus optional payload."""
        length = len(data)
        body = bytes([DEVICE_ID, length, command]) + data
        self._write_with_checksum(body)

    def _read(self, n):
        """Attempt to read `n` bytes, returning empty bytes on failure."""
        try:
            return i2c.read(self.address, n)
        except Exception:
            return b""

    # Public API methods used by the Adapter
    def algorithm_tag_recognition(self):
        """Ensure the HuskyLens is in tag recognition mode."""
        self._write_command(CMD_ALGORITHM, b"\x05\x00")
        sleep(20)

    def request_blocks(self):
        """Ask the HuskyLens to provide block data in the next read."""
        self._write_command(CMD_REQUEST_ALL)

    def read_blocks(self, max_blocks=5, timeout_ms=150):
        """
        Returns a list of Block().
        Reads a reasonable upper bound box limit and parses any blocks found into bytes.
        """
        deadline = running_time() + timeout_ms
        buf = b""  # Stashes raw bytes read from HuskyLens until a frame can be parsed
        max_bytes = max(1, max_blocks) * 16  # rough upper bound per block
        while running_time() < deadline and len(buf) < max_bytes:
            part = self._read(32)
            if part:
                buf += part
                continue
            # No data, wait...
            sleep(5)

        print("HuskyLens buffer bytes:", len(buf))
        print("HuskyLens raw:"," ".join("%02X" % b for b in buf[:32]),"... total", len(buf))
        blocks = []
        i = 0
        while i + 6 <= len(buf):
            # Look for frame header, advancing one byte at a time if misaligned
            if buf[i:i+2] != HEADER:
                i += 1
                continue
            
            # Minimum fixed header bytes (e.g. device,len,cmd,checksum)
            if i + 5 > len(buf):
                break

            frame_device = buf[i+2]          # The HuskyLens device
            payload_len = buf[i+3]           # Payload byte count
            command_id = buf[i+4]            # Command describing the payload contents
            frame_end = i + 5 + payload_len  # Checksum byte index

            # Bail if payload still incomplete in the buffer
            if frame_end >= len(buf):
                break

            # Validate checksum, check image is not corrupt or to be skipped
            payload = buf[i+5:frame_end] 
            checksum = buf[frame_end]        # checksum byte at end of frame
            computed_checksum = (sum(buf[i:i+5+payload_len]) & 0xFF)

            if checksum != computed_checksum:
                print("Checksum mismatch cmd=0x%02X exp=%02X got=%02X" % (command_id, computed_checksum, checksum))
                i = frame_end + 1
                continue
            print("Frame cmd=0x%02X len=%d device=0x%02X" % (command_id, payload_len, frame_device))
            if command_id in (0x2A,):
                # Tag/frame data: convert fields into Block objects
                # Example payload b'\x20\x01\x58\x00\x30\x00\x40\x00\x05\x00' -> Block(x=288,y=88,w=48,h=64,ID=5)
                if len(payload) >= 10:
                    try:
                        x = payload[0] | (payload[1] << 8)
                        y = payload[2] | (payload[3] << 8)
                        w = payload[4] | (payload[5] << 8)
                        h = payload[6] | (payload[7] << 8)
                        ID = payload[8] | (payload[9] << 8)
                        if ID > 0 and w > 0 and h > 0:
                            block = Block(x,y,w,h,ID)
                            print("HuskyLens block:", block)
                            blocks.append(block)
                            if len(blocks) >= max_blocks:
                                break
                    except Exception as exc:
                        print("Block parse error:", exc)
            i = frame_end + 1
        return blocks