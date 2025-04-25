import pyxdf


def print_streams_types_and_names(fullFname_or_streams):
    """Print the names and types of all streams in the xdf file
    or in the streams list"""

    if isinstance(fullFname_or_streams, str):
        xdf_data, header = pyxdf.load_xdf(
            filename=fullFname_or_streams, verbose=False
        )
    elif (
        isinstance(fullFname_or_streams, list)
        and all(
            isinstance(x, dict) for x in fullFname_or_streams
        )
        and all(
            "info" in x for x in fullFname_or_streams
        )
    ):
        xdf_data = fullFname_or_streams
    else:
        msg = "Must be a filename or a list of streams."
        raise ValueError(f"{fullFname_or_streams}. {msg}")

    for i in range(len(xdf_data)):
        stream = xdf_data[i]
        s_type = stream["info"]["type"][0]
        s_name = stream["info"]["name"][0]
        print(f"Stream {i}: {s_type}, {s_name}")


def get_stream(xdf_data, searched_stream_type, searched_stream_names):
    """Get the stream of type 'searched_stream_type' with name in
    'searched_stream_names' in the xdf_data"""

    if not isinstance(
        searched_stream_names, list
    ):  # if we get a string (only one name)
        searched_stream_names = [searched_stream_names]

    found_streams = []
    for stream in xdf_data:
        stream_type = stream["info"]["type"][0]
        if searched_stream_type == stream_type:
            stream_name = stream["info"]["name"][0]
            for searched_stream_name in searched_stream_names:
                if searched_stream_name == stream_name:
                    found_streams.append(stream)

    if not found_streams:
        # this happens classically (e.g., before vs after eventIDE)
        # => do not log
        msg = (
            f" Stream not found. Searched in "
            f"[{searched_stream_type}:{searched_stream_names}]."
        )
        # logging.warning(msg)
        # print(msg)
        return None

    if len(found_streams) > 1:
        found_streams_names = [
            stream["info"]["name"][0]
            for stream in found_streams
        ]
        msg = (
            f"Found multiple streams: "
            f"[{searched_stream_type},{found_streams_names}]."
        )
        raise ValueError(msg)

    return found_streams[0]


def get_kinect_channel(kinect_mocap, channel_name):
    """Get one channel from the kinect mocap by its name"""
    channel_index = -1
    nb_channels = len(
        kinect_mocap["info"]["desc"][0]["channels"][0]["channel"]
    )
    for i in range(nb_channels):
        current_name = (
            kinect_mocap["info"]["desc"][0]["channels"][0]
            ["channel"][i]["label"][0]
        )
        if current_name == channel_name:
            channel_index = i
            break
    if channel_index == -1:
        raise ValueError(
            f"Joint {channel_name} not found in the kinect mocap data"
        )

    channel_data = kinect_mocap["time_series"][:, channel_index]

    return channel_data


def get_kinect_channel_index(kinect_mocap, channel_name):
    """Get the index of one channel from the kinect mocap by its name"""
    channel_index = -1
    nb_channels = len(
        kinect_mocap["info"]["desc"][0]["channels"][0]["channel"]
    )
    for i in range(nb_channels):
        current_name = (
            kinect_mocap["info"]["desc"][0]["channels"][0]
            ["channel"][i]["label"][0]
        )
        if current_name == channel_name:
            channel_index = i
            break
    if channel_index == -1:
        raise ValueError(
            f"Joint {channel_name} not found in the kinect mocap data"
        )

    return channel_index


def get_kinect_channel_data(kinect_mocap, channel_name):
    """Get one channel from the kinect mocap by its name"""
    channel_index = get_kinect_channel_index(kinect_mocap, channel_name)
    channel_data = kinect_mocap["time_series"][:, channel_index]
    return channel_data
