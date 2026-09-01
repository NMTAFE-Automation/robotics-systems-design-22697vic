# Using SCP to Transfer Files Between Your PC and a Raspberry Pi

**A quick-reference guide for TAFE students working with Raspberry Pi in robotics projects**

Scenario used throughout this guide:

- **Local machine** = your PC (Windows/Mac/Linux with a terminal)
- **Remote machine** = your Raspberry Pi board, IP address `192.168.1.50`, username `pi`

---

## 1. Why We Use SCP (Brief)

**SCP** (Secure Copy Protocol) lets you copy files and folders between two computers over a network connection, encrypted using SSH. Instead of pulling out a USB drive every time you need to move a file, you can send it directly over Wi-Fi or Ethernet with one command.

In robotics work, this matters because the Raspberry Pi is usually running "headless" (no monitor/keyboard attached) and controlling motors, sensors, or a ROS2 node in real time. SCP lets you:

- Push updated Python/C++ scripts or ROS2 packages from your PC straight onto the robot.
- Pull log files, sensor data, or camera captures off the robot for analysis on your PC.
- Do all of this securely, since SCP travels over an encrypted SSH connection — important on shared lab or workshop networks.

In short: SCP is the fastest, most reliable way to keep code and data in sync between your development PC and the Pi controlling your robot.

---

## 2. Copy a Local File to a Remote Server

**Syntax:**

```bash
scp <local_file> <username>@<remote_ip>:<remote_path>
```

**Example:** Copy a Python control script from your PC to the Pi's home folder.

```bash
scp motor_control.py pi@192.168.1.50:/home/pi/
```

You will be prompted for the Pi's password (or it will connect automatically if you've set up SSH keys). Once done, `motor_control.py` will appear in `/home/pi/` on the Raspberry Pi.

---

## 3. Copy a Remote File to Your Local Machine

**Syntax:**

```bash
scp <username>@<remote_ip>:<remote_path> <local_destination>
```

**Example:** Copy a sensor log file from the Pi back to your PC's current folder.

```bash
scp pi@192.168.1.50:/home/pi/logs/imu_data.csv .
```

The `.` at the end means "save it in my current folder." You could also specify a full path, e.g. `C:\Users\Student\Downloads\` on Windows or `~/Downloads/` on Mac/Linux.

---

## 4. Copy an Entire Folder (Recursively)

To copy a whole folder (including all its files and subfolders), add the `-r` (recursive) flag.

### 4a. Local to Remote

**Example:** Copy your entire ROS2 package folder from your PC onto the Pi.

```bash
scp -r ~/ros2_ws/src/my_robot_pkg pi@192.168.1.50:/home/pi/ros2_ws/src/
```

This copies `my_robot_pkg` and everything inside it onto the Raspberry Pi.

### 4b. Remote to Local

**Example:** Copy a folder of camera images captured by the Pi back to your PC for review.

```bash
scp -r pi@192.168.1.50:/home/pi/captures ./captures_backup
```

This downloads the entire `captures` folder from the Pi and saves it locally as `captures_backup`.

---

## 5. Common and Useful Options

| Option | What it does |
|---|---|
| `-r` | Recursive — copies an entire folder and its contents |
| `-P <port>` | Specifies a custom SSH port (default is 22) — note this is a **capital** P |
| `-i <keyfile>` | Uses a specific SSH private key file for authentication |
| `-v` | Verbose mode — shows detailed connection/debug info, useful for troubleshooting |
| `-C` | Compresses data during transfer — speeds up large transfers over slow Wi-Fi |
| `-p` | Preserves original file modification times, access times, and permissions |

**Example combining options:** Copy a folder using a custom SSH port and a specific key file.

```bash
scp -r -P 2222 -i ~/.ssh/id_rsa ~/robot_code pi@192.168.1.50:/home/pi/
```

---

## 6. Important Things to Remember

- **Order matters:** the source comes first, the destination second — always think "from → to."
- **Colon `:` marks the remote side.** No colon = local path. A colon after the hostname = remote path.
- **SSH must be enabled** on the Raspberry Pi (`sudo raspi-config` → Interface Options → SSH) before SCP will work.
- **Both devices must be on the same network** (or otherwise reachable), and you need the Pi's correct IP address (find it with `hostname -I` on the Pi).
- **Use `-r` for folders** — forgetting it is one of the most common beginner errors and will cause SCP to fail on a directory.
- **Watch your paths** — a trailing slash on the source folder (e.g. `my_folder/`) copies the *contents* of the folder, while no trailing slash copies the folder itself. Test on non-critical files first if unsure.
- **SSH keys save time:** setting up passwordless SSH key authentication avoids typing a password every time — very handy when scripting repeated transfers.
- **Double-check destination paths exist** on the target machine; SCP will not automatically create missing parent directories.
- **For very large or frequently-synced projects**, consider `rsync` instead of `scp` — it only transfers changed data, which is faster for repeated deployments to the robot.
