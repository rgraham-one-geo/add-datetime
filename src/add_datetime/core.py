import lasio
import numpy as np
import pandas as pd

LABVIEW_EPOCH = pd.Timestamp("1904-01-01 00:00:00", tz="UTC")

def add_datetime_curve_to_las(
    input_path,
    output_path,
    time_curve_name="Time",
    timezone="UTC"
):
    # Read LAS file
    las = lasio.read(input_path)

    # Ensure the Time curve exists
    if time_curve_name not in las.curves.keys():
        raise ValueError(f"Curve '{time_curve_name}' not found in LAS file")

    # Extract raw time values
    raw_time = np.asarray(las[time_curve_name], dtype=float)

    # Convert LabVIEW timestamp → UTC datetime
    datetime_series = pd.to_datetime(
        raw_time,
        unit="s",
        origin=LABVIEW_EPOCH,
        utc=True,
        errors="coerce"
    )

    # Convert timezone if specified
    if timezone is not None:
        datetime_series = datetime_series.dt.tz_convert(timezone)

    # Convert to string for LAS compatibility
    datetime_str = datetime_series.astype("datetime64[ns]").astype(str)

    # Append new curve at the end
    las.append_curve(
        "DateTime",
        datetime_str,
        unit="",
        descr=f"Converted from LabVIEW timestamp ({timezone})"
    )

    # Write out new LAS file
    las.write(output_path, version=las.version.VERS.value)

    return output_path