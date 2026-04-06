from __future__ import annotations

import warnings
from datetime import datetime, timedelta
from os import PathLike

import lasio
import numpy as np
import pandas as pd

LABVIEW_EPOCH = pd.Timestamp("1904-01-01 00:00:00", tz="UTC")
DATETIME_OUTPUT_FORMAT = ":%m/%d/%Y  %I:%M:%S %p"


def add_datetime(dt: datetime, delta: timedelta) -> datetime:
    """Return a new datetime offset by the given timedelta."""
    return dt + delta


def now_plus(delta: timedelta) -> datetime:
    """Return the current local datetime plus the given timedelta."""
    return datetime.now() + delta


def add_datetime_curve_to_las(
    input_path: str | PathLike[str],
    output_path: str | PathLike[str],
    time_curve_name: str = "Time",
    datetime_curve_name: str = "DateTime",
    timezone: str | None = "UTC",
) -> str | PathLike[str]:
    """Add a formatted DateTime curve converted from LabVIEW timestamp seconds.

    Invalid time values are coerced to NaT and reported via warning.
    """
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
        errors="coerce",
    )

    invalid_count = int(pd.isna(datetime_series).sum())
    if invalid_count > 0:
        warnings.warn(
            f"{invalid_count} invalid timestamp value(s) were coerced to NaT.",
            RuntimeWarning,
            stacklevel=2,
        )

    # Convert timezone if specified
    if timezone is not None:
        datetime_series = datetime_series.tz_convert(timezone)

    # Convert to string for LAS compatibility
    datetime_str = pd.Series(datetime_series).dt.strftime(DATETIME_OUTPUT_FORMAT)
    datetime_str = datetime_str.where(pd.Series(datetime_series).notna(), "NaT")

    # Append new curve at the end
    las.append_curve(
        datetime_curve_name,
        datetime_str.to_numpy(dtype=object),
        unit="",
        descr=f"Converted from LabVIEW timestamp ({timezone})",
    )

    # Write out new LAS file
    las.write(output_path, version=las.version.VERS.value)

    return output_path