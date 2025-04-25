import os
import numpy as np
from datetime import datetime


def is_timestamp_valid(txt):
    """
    Check if the text is a timestamp in one of the formats:
    2023-07-05 14:45:34.447
    2023-07-05 14:45:34.447 +0200
    """
    try:
        datetime.strptime(txt, "%Y-%m-%d %H:%M:%S.%f")
        return True
    except ValueError:
        try:
            datetime.strptime(txt, "%Y-%m-%d %H:%M:%S.%f %z")
            return True
        except ValueError:
            return False


def is_lsl_mouse_csv_file(fullFname):
    """
    Check if a file is created by the LSL Mouse Recorder
    """

    if not fullFname.endswith(".csv"):
        return False

    with open(fullFname, "r") as f:
        header_lines = [f.readline().strip() for _ in range(2)]
    if len(header_lines) < 2:
        return False

    if header_lines[0] == "" or header_lines[1] == "":
        return False

    # any LSL-mouse file should have a one line header
    # with "software LSL-mouse" as a key-value pair
    # the key-value pairs are separated by a semicolon
    # followed by line with the timestamp formatted as 2023-07-05 14:45:34.447

    # the first line should contain the software version
    header_txt = header_lines[0]
    if len(header_txt) > 1:
        is_lsl_mouse = False
        for key_value in header_txt.split(";"):
            k_v = key_value.split()
            if len(k_v) == 2:
                key, value = k_v
                if "software" in key and (
                    "LSL-mouse" in value or "mouseReMoCo" in value
                ):
                    is_lsl_mouse = True
                    break

    # the second line should contain the timestamp
    header_timestamp = header_lines[1]
    if len(header_timestamp) > 1:
        if not is_timestamp_valid(header_timestamp):
            return False

    return is_lsl_mouse


def is_lsl_mouse_marker_csv_file(fullFname):
    """
    Check if a file is created by the LSL Mouse Recorder
    and contains marker data
    """

    if not is_lsl_mouse_csv_file(fullFname):
        return False

    with open(fullFname, "r") as f:
        first_5_lines = [f.readline().strip() for _ in range(5)]
    if len(first_5_lines) < 5:
        return False

    # after the 2 header lines, there is one (two?) empty line(s)
    for line in first_5_lines[2:]:
        if line.strip() == "":
            continue
        else:
            # the first (non empty) line should contain
            # timestamp_text, timestamp_float, marker_string
            try:
                timestamp_text, timestamp_float, _ = line.split(",")
                datetime.strptime(timestamp_text, "%Y-%m-%d %H:%M:%S.%f")
                float(timestamp_float)
            except Exception:
                return False
    return True


def is_lsl_mouse_mocap_file(fullFname):
    """
    Check if a file is created by the LSL Mouse Recorder
    and contains mocap data
    """

    if not is_lsl_mouse_csv_file(fullFname):
        return False

    with open(fullFname, "r") as f:
        first_5_lines = [f.readline().strip() for _ in range(5)]
    if len(first_5_lines) < 5:
        return False

    # after the 2 header lines, there is one (two?) empty line(s)
    for line in first_5_lines[2:]:
        if line.strip() == "":
            continue
        else:
            # the first (non empty) line should contain
            # timestamp,mouseX,mouseY,mouseInTarget
            try:
                timestamp, mouseX, mouseY, mouseInTarget = line.split(",")
            except Exception:
                return False
            if (
                timestamp == "timestamp"
                and mouseX == "mouseX"
                and mouseY == "mouseY"
                and mouseInTarget == "mouseInTarget"
            ):
                return True
            else:
                return False


def is_lsl_kinect_csv_file(fullFname):
    """
    Check if a file is created by the LSL Kinect Recorder
    """

    # any LSL-kinect file should have a one line header with
    # "Software : LSL_Kinect" as a key-value pair
    # the key-value pairs are separated by a comma
    if fullFname.endswith(".csv"):
        with open(fullFname, "r") as f:
            header = f.readline()
        if len(header) > 1:
            for key_value in header.split(","):
                k_v = key_value.split(":")
                if len(k_v) == 2:
                    key, value = k_v
                    if "Software" in key and "LSL_Kinect" in value:
                        return True
    return False


def is_lsl_kinect_mocap_file(fullFname):
    """
    Check if a file is created by the LSL Kinect Recorder and
    contains mocap data
    """
    if not is_lsl_kinect_csv_file(fullFname):
        return False
    with open(fullFname, "r") as f:
        first_3_lines = [f.readline().strip() for _ in range(3)]
    if len(first_3_lines) < 3:
        return False

    # after the 1 line header lines, there is one (two?) empty line(s)
    for line in first_3_lines[1:]:
        if line.strip() == "":
            continue
        else:
            # the first (non empty) line should contain 'TimeSpan', 'TimeSpan'
            try:
                timestamp, marker, *_ = line.split(",")
            except Exception:
                return False
            if timestamp == "TimeSpan" and marker == "SpineBase_X":
                return True
            else:
                return False


def is_lsl_kinect_marker_file(fullFname):
    """
    Check if a file is created by the LSL Kinect Recorder and
     contains marker data
    """
    if not is_lsl_kinect_csv_file(fullFname):
        return False

    with open(fullFname, "r") as f:
        first_3_lines = [f.readline().strip() for _ in range(3)]
    if len(first_3_lines) < 3:
        return False

    # after the 1 line header lines, there is one (two?) empty line(s)
    for line in first_3_lines[1:]:
        if line.strip() == "":
            continue
        else:
            # the first (non empty) line should contain 'TimeSpan', 'TimeSpan'
            try:
                timestamp, marker, *_ = line.split(",")
            except Exception:
                return False
            if timestamp == "TimeSpan" and marker == "Marker Message":
                return True
            else:
                return False


def is_lsl_mouse_or_kinect_csv_file(fullFname):
    """
    Check if a file is created by the LSL Mouse or LSL Kinect Recorder
    """
    is_lsl_mouse = is_lsl_mouse_csv_file(fullFname)
    is_lsl_kinect = is_lsl_kinect_csv_file(fullFname)

    return is_lsl_mouse or is_lsl_kinect


def check_csv_date(fullFname, msg=""):
    """
    Check the date of a csv file
    The date is extracted from the first timestamp in the file
    """
    # date is set to 1970-01-01 00:00:00 if not found
    # date = datetime.fromtimestamp(0, tz=None)
    # date is set to None if not found
    date = None

    if not fullFname.endswith(".csv"):
        msg += f"{fullFname} is not a csv file."
        return date, msg

    if not is_lsl_mouse_or_kinect_csv_file(fullFname):
        msg += f"{fullFname} is not a LSL Mouse or LSL Kinect file."
        return date, msg

    # The timestamps are always in column 1, after 3-4 lines of header
    # but it can be a string or a float (in milliseconds)
    try:  # read the first line
        data = np.loadtxt(fullFname, skiprows=4, delimiter=",", max_rows=1, dtype=str)
    except ValueError:
        msg += f"Could not read {fullFname}."
        return date, msg

    # check if the file is empty
    if data.size == 0:
        basename = os.path.basename(fullFname)
        msg += f"{basename} is an empty file."
        return date, msg

    # check if we get the expected number of columns (at least 2)
    if data.size < 2:
        basename = os.path.basename(fullFname)
        msg += f"{basename} has less than 2 columns."
        return date, msg

    # Sounds good, we have some data to check
    # we only need the first timestamp
    timestamp = data[0]

    # if the timestamp is a float...
    try:
        timestamp = float(timestamp)
    except ValueError:
        pass
    if isinstance(timestamp, float):
        timestamp = float(timestamp) / 1000  # in seconds
        date = datetime.fromtimestamp(timestamp, tz=None)

    # if the timestamp is a string...
    if isinstance(timestamp, str):
        timestamp_formats = ["%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S.%f %z"]
        for fmt in timestamp_formats:
            try:
                date = datetime.strptime(timestamp, fmt)
                break
            except ValueError:
                pass

    if date is None:
        basename = os.path.basename(fullFname)
        msg += f"Could not extract a date from {basename}."

    return date, msg
