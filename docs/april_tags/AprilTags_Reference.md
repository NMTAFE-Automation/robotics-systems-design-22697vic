# AprilTags Reference

## 1. What Are AprilTags?

AprilTags are a type of **visual fiducial marker** — a printed black-and-white square pattern designed to be extremely easy for a computer to detect, identify, and precisely locate in 3D space from a single camera image. They look similar to a QR code at first glance, but they're built for a fundamentally different purpose.

A QR code is optimized to pack in as much *data* as possible (URLs, text, contact info). An AprilTag is optimized for the opposite: it carries a small amount of data (just a unique ID number) but is engineered to be detected reliably at odd angles, in poor lighting, when partially blurred by motion, or when only partly visible — and once detected, it can be used to calculate the exact position and orientation (6 degrees of freedom: x, y, z, roll, pitch, yaw) of the camera relative to the tag, or vice versa.

This is why AprilTags are the go-to fiducial system in robotics: a robot doesn't need to read a URL from a tag, it needs to know *"I am 1.2 meters away from tag #7, and I am facing it at a 15-degree angle."*

**Key components of an AprilTag:**
- A **black border** that the detector locates first (defines the outer boundary/quad)
- An internal **grid of black/white cells** encoding a unique binary ID
- A **white quiet zone** around the tag (space free of other markings) so the detector can distinguish the tag's edge cleanly from its background

## 2. A Short History

| Year | Milestone |
|---|---|
| **2010–2011** | AprilTag created by **Edwin Olson**, then a professor at the University of Michigan, leading the APRIL Robotics Laboratory (**A**utonomy, **P**erception, **R**obotics, **I**nterfaces, and **L**earning). Olson published the foundational paper *"AprilTag: A robust and flexible visual fiducial system"* at ICRA 2011. |
| **Motivation** | Existing fiducial systems at the time (like ARTag) were either proprietary/closed, or not robust enough under real-world lighting, occlusion, and lens distortion for robotics research. Olson designed AprilTag as a fully open, well-documented alternative with a stronger digital coding system. |
| **2016** | **AprilTag 2** released (Wang & Olson, IROS 2016) — a major rewrite focused on faster, more efficient detection suitable for real-time use on modest hardware. |
| **2016–present** | Adopted widely across robotics: ROS/ROS2 ecosystems, the DARPA-style research community, FIRST Robotics Competition (FRC) and FIRST Tech Challenge (FTC), industrial automation, drone localization, and camera calibration workflows. |
| **Today** | Maintained as an open-source project (AprilRobotics/apriltag on GitHub), with active ports and bindings in C, Python, Java, and integrations inside OpenCV's `cv2.aruco` module. |

Edwin Olson has since gone on to found May Mobility (autonomous shuttle company) and previously co-directed autonomous driving research at Toyota Research Institute — AprilTag remains one of his most widely used contributions to the robotics field.

## 3. Tag Families — What the Numbers Mean

AprilTags come in different **families**, each with a name like `tag36h11`. The naming convention encodes two design parameters:

```
tag  36        h11
     ^          ^
     |          └── Minimum Hamming distance between any two valid codes
     └── Number of data bits encoded in the grid
```

- **The first number (e.g. 36)** — the number of bits of data encoded in the tag's internal grid (a 6×6 grid = 36 bits for `tag36h11`).
- **"h" + number (e.g. h11)** — the **minimum Hamming distance** between any two valid tag codes in that family. This measures error tolerance: a higher Hamming distance means more bits would need to be misread before one tag's ID could be mistaken for a different tag's ID, making the family more robust against detection errors — at the cost of needing more pixels to resolve reliably.

| Family | Grid size | Data bits | Hamming distance | Max unique IDs | Robustness | Notes |
|---|---|---|---|---|---|---|
| `tag16h5` | 4×4 | 16 | 5 | 30 | Lower | Simple, decodes at a distance with fewer pixels, but easier to misread |
| `tag25h9` | 5×5 | 25 | 9 | 35 | Medium | Balance point, less commonly used |
| `tag36h10` | 6×6 | 36 | 10 | ~2,320 | High | Similar to 36h11, older revision |
| `tag36h11` | 6×6 | 36 | 11 | **587** | **Highest (of the common families)** | **The de facto robotics standard** — used by ROS, FRC/FTC, and most vision libraries by default |
| `tagStandard41h12` | larger | 41 | 12 | 2,115 | Very high | Bigger grid, needs more resolution to decode |
| `tagStandard52h13` | larger | 52 | 13 | 48,714 | Very high | Large ID space, needs high-resolution imaging |

**Practical rule of thumb:** unless you have a specific reason to choose otherwise (e.g. a sensor that's locked to a specific family, like HuskyLens V1), use `tag36h11`. It's the most widely supported, has excellent error tolerance, and 587 IDs is more than enough for almost any classroom or lab project.

## 4. How AprilTags Are Used in Robotic Applications

**Localization & SLAM ground-truthing**
Fixed tags placed at known positions in an environment act as landmarks. A robot with a camera can compute its own position and orientation relative to each visible tag, effectively solving "where am I?" without GPS — useful indoors or in GPS-denied environments.

**Docking & precision alignment**
A tag mounted on a charging dock or a loading bay lets a robot compute the exact approach angle and distance needed to dock precisely, even from an imperfect starting position. This pattern shows up in autonomous mobile robots, drone landing pads, and (per Nav2 documentation) restaurant service robots aligning to fixed stations.

**Camera and multi-sensor calibration**
Because a tag's physical size and geometry are known exactly, detecting it lets you solve for a camera's intrinsic parameters (focal length, distortion) or the extrinsic transform between a camera and another sensor (e.g. camera-to-LiDAR, camera-to-arm-flange calibration).

**Multi-robot coordination and tracking**
Tags mounted on robots themselves let *other* robots or fixed overhead cameras track their position and identity — common in swarm robotics research and warehouse fleet systems.

**Robotic arm and pick-and-place guidance**
A tag on a workpiece or fixture gives a robotic arm precise pose information for grasping, insertion, or quality-check alignment tasks — used in some fast-food and light-manufacturing robotic arm deployments.

**Competition robotics (FRC/FTC)**
Since 2023, FIRST places AprilTags at known field positions so competition robots can self-localize and align to scoring targets — a widely-used real-world teaching example of tag-based localization in action.

## 5. Uses Beyond Robotics

**Augmented Reality (AR)**
Tags act as trackable anchors for overlaying 3D graphics onto a live camera feed — since the tag gives full 6DOF pose, virtual objects can be rendered as if they're physically attached to the tag's location.

**3D scanning and photogrammetry**
Placing multiple tags around a physical space or object gives a scanning rig fixed, precisely-known reference points, letting software register and align multiple scans/photos into a single accurate 3D model — a workflow used for scanning large studio or industrial spaces.

**Motion capture (as a lightweight alternative to marker-based MoCap)**
Because a single tag gives full pose, arrays of tags can substitute for traditional retroreflective motion-capture markers in some research and prototyping contexts.

**General camera calibration (non-robotics)**
Photographers, VR/AR developers, and computer-vision researchers use tags (or the closely related ArUco/checkerboard patterns) any time a camera's precise optical parameters need to be measured.

**Asset tracking and inventory**
Since each tag ID is unique and cheap to print, tags can label physical objects/bins in a warehouse or lab for a camera-based system to identify and log without needing barcode scanners or RFID hardware.

**Interactive installations, art, and education**
Tags are cheap (just ink and paper) and easy to prototype with, making them popular for interactive exhibits, escape rooms, and teaching computer vision concepts hands-on — exactly the use case for a classroom set like the ones printed for this course.

## 6. AprilTags + HuskyLens

### HuskyLens hardware notes

| HuskyLens model | Supported tag families | Notes |
|---|---|---|
| **HuskyLens V1 (K210, SKU SEN0305)** | **`tag36h11` only** | Confirmed by DFRobot's own FAQ — hardcoded, no family selection available. Detects the tag shape but does **not** decode the tag's built-in binary ID; instead, you manually assign IDs (1, 2, 3...) via the physical learning button, in whatever order you teach the tags. |
| **HuskyLens 2 (K230)** | `tag16h5`, `tag25h9`, `tag36h10`, `tag36h11` (defaults to `tag36h11`) | Newer model — supports selecting the family via its on-device menu/parameter settings, and can decode true tag IDs. |

**Practical implication:** for a HuskyLens V1 project (e.g. Maqueen + micro:bit), always print `tag36h11` tags — it's the only family the sensor can see at all — and remember that the ID reported by HuskyLens is the *learned* sequence number, not the number encoded in the tag's actual pattern.

### Typical HuskyLens V1 + micro:bit workflow (recap)
1. Print `tag36h11` tags (the only compatible family).
2. Set HuskyLens to **Tag Recognition** mode, enable **Learn Multiple**.
3. Physically teach each tag using the learning button — HuskyLens assigns sequential IDs (1, 2, 3...).
4. Read detected tag ID + bounding box over UART from the micro:bit; note this gives 2D position/size only, not full 6DOF pose (HuskyLens V1 does not do pose solving).
