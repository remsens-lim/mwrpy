"""Module for LWP offset correction"""
import numpy as np
import pandas as pd

from mwrpy.atmos import find_lwcl_free

Fill_Value_Float = -999.0


def correct_lwp_offset(
    lev1: dict, lwp_org: np.ndarray, index: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """This function corrects Lwp offset using the
    2min standard deviation of the 31.4 GHz channel and IR temperature

    Args:
        lev1: Level 1 data.
        lwp_org: Lwp array.
        index: Index to use.

    Examples:
        >>> from mwrpy.level2.lwp_offset import correct_lwp_offset
        >>> correct_lwp_offset(lev1, lwp, index, 'site_name')
    """

    if "elevation_angle" in lev1:
        elevation_angle = lev1["elevation_angle"][:]
    else:
        elevation_angle = 90 - lev1["zenith_angle"][:]

    lwcl_i, _ = find_lwcl_free(lev1, index)
    lwp = np.copy(lwp_org)
    lwp[(lwcl_i != 0) | (lwp > 0.04) | (elevation_angle[index] < 89.0)] = np.nan
    time = lev1["time"][index]
    if max(time) > 25:
        lwp_df = pd.DataFrame({"Lwp": lwp}, index=pd.to_datetime(time, unit="s"))
    else:
        lwp_df = pd.DataFrame({"Lwp": lwp}, index=pd.to_datetime(time, unit="h"))
    lwp_std = lwp_df.rolling("2min", center=True, min_periods=10).std()
    lwp_max = lwp_std.rolling("20min", center=True, min_periods=100).max()
    lwp_df[lwp_max > 0.002] = np.nan
    lwp_offset = lwp_df.rolling("20min", center=True, min_periods=100).mean()

    lwp_offset = lwp_offset.interpolate(method="linear")
    lwp_offset = lwp_offset.fillna(method="bfill")
    lwp_offset["Lwp"][np.isnan(lwp_offset["Lwp"])] = 0
    lwp_org -= lwp_offset["Lwp"].values

    return lwp_org, lwp_offset["Lwp"].values
