import os

from mwrpy import lev1_to_nc
from mwrpy.level2.lev2_collocated import generate_lev2_multi, generate_lev2_single
from mwrpy.level2.write_lev2_nc import lev2_to_nc

PACKAGE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = f"{PACKAGE_DIR}/data/hyytiala"
COEFFICIENTS_DIR = f"{PACKAGE_DIR}/../mwrpy/site_config/"
DATE = "2023-04-06"


def test_level2_processing():
    lev1_file = "temp_file1.nc"
    lev2_file = "temp_file2.nc"
    temp_file = "temp_file3.nc"
    hum_file = "temp_file4.nc"

    site = "hyytiala"

    lev1_to_nc("1C01", DATA_DIR, site, lev1_file)

    # mwr-single
    lev2_to_nc("2I01", lev1_file, lev2_file, site=site)
    lev2_to_nc("2I02", lev1_file, lev2_file, site=site)
    lev2_to_nc("2P01", lev1_file, lev2_file, site=site)
    lev2_to_nc("2P03", lev1_file, hum_file, site=site)

    generate_lev2_single(site, lev1_file, lev2_file)

    # mwr-multi
    lev2_to_nc("2P02", lev1_file, temp_file, site=site)
    lev2_to_nc(
        "2P04", lev1_file, lev2_file, site=site, temp_file=temp_file, hum_file=hum_file
    )
    lev2_to_nc(
        "2P07", lev1_file, lev2_file, site=site, temp_file=temp_file, hum_file=hum_file
    )
    lev2_to_nc(
        "2P08", lev1_file, lev2_file, site=site, temp_file=temp_file, hum_file=hum_file
    )

    generate_lev2_multi(site, lev1_file, lev2_file)

    for file in (lev1_file, lev2_file, temp_file, hum_file):
        if os.path.exists(file):
            try:
                os.remove(file)
            except PermissionError:
                pass
