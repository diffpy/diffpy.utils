import importlib.metadata
import json
from copy import copy
from pathlib import Path

import numpy as np
from scipy.optimize import dual_annealing
from scipy.signal import convolve
from xraydb import material_mu

from diffpy.utils.parsers.loaddata import loadData


def _stringify(string_value):
    """Convert None to an empty string.

    Parameters
    ----------
    string_value : str or None
        The value to be converted. If None, an empty string is returned.

    Returns
    -------
    str
        The original string if string_value is not None, otherwise an empty
        string.
    """
    return string_value if string_value is not None else ""


def _load_config(file_path):
    """Load configuration from a .json file.

    Parameters
    ----------
    file_path : Path
        The path to the configuration file.

    Returns
    -------
    config : dict
        The configuration dictionary or {} if the config file does not exist.
    """
    config_file = Path(file_path).resolve()
    if config_file.is_file():
        with open(config_file, "r") as f:
            config = json.load(f)
        return config
    else:
        return {}


def get_user_info(owner_name=None, owner_email=None, owner_orcid=None):
    """Get name, email, and orcid of the owner/user from various sources and
    return it as a metadata dictionary.

    The function looks for the information in json format configuration files
    with the name 'diffpyconfig.json'. These can be in the user's home
    directory and in the current working directory.  The information in the
    config files are combined, with the local config overriding the
    home- directory one.  Values for owner_name, owner_email, and owner_orcid
    may be passed in to the function and these override the values in the
    config files.

    A template for the config file is below.  Create a text file called '
    diffpyconfig.json' in your home directory and copy-paste the template
    into it, editing it with your real information.
    {
      "owner_name": "<your name as you would like it stored with your data>>",
      "owner_email": "<your_associated_email>>@email.com",
      "owner_orcid": "<your_associated_orcid if you would like this stored with your data>>"  # noqa: E501
    }
    You may also store any other global-level information that you would like
    associated with your diffraction data in this file

    Parameters
    ----------
    owner_name : str, optional, default is the value stored in the global or
        local config file. The name of the user who will show as owner in the
        metadata that is stored with the data
    owner_email : str, optional, default is the value stored in the global or
        local config file. The email of the user/owner
    owner_orcid : str, optional, default is the value stored in the global or
        local config file. The ORCID id of the user/owner

    Returns
    -------
    user_info : dict
        The dictionary containing username, email and orcid of the user/owner
        , and any other information stored in the global or local config files.
    """
    runtime_info = {
        "owner_name": owner_name,
        "owner_email": owner_email,
        "owner_orcid": owner_orcid,
    }
    for key, value in copy(runtime_info).items():
        if value is None or value == "":
            del runtime_info[key]
    global_config = _load_config(Path().home() / "diffpyconfig.json")
    local_config = _load_config(Path().cwd() / "diffpyconfig.json")
    user_info = global_config
    user_info.update(local_config)
    user_info.update(runtime_info)
    return user_info


def check_and_build_global_config(skip_config_creation=False):
    """Check for a global diffpu config file in user's home directory and
    creates one if it is missing.

    The file it looks for is called diffpyconfig.json.  This can contain
    anything in json format, but minimally contains information about the
    computer owner.  The information is used when diffpy objects are created
    and saved to files or databases to retain ownership information of
    datasets.  For example, it is used by diffpy.utils.tools.get_user_info().

    If the function finds no config file in the user's home directory it
    interrupts execution and prompts the user for name, email, and orcid
    information.  It then creates the config file with this information
    inside it.

    The function returns True if the file exists and False otherwise.

    If you would like to check for a file but not run the file creation
    workflow you can set the optional argument skip_config_creation to True.

    Parameters
    ----------
    skip_config_creation : bool, optional, default is False.
        The boolean that will override the creation workflow even if no
        config file exists.

    Returns
    -------
    config_exists : bool
        The boolean indicating whether the config file exists.
    """
    config_exists = False
    config_path = Path().home() / "diffpyconfig.json"
    if config_path.is_file():
        config_exists = True
        return config_exists
    if skip_config_creation:
        return config_exists
    intro_text = (
        "No global configuration file was found containing information about "
        "the user to associate with the data.\n By following the prompts "
        "below you can add your name and email to this file on the current "
        "computer and your name will be automatically associated with "
        "subsequent diffpy data by default.\n This is not recommended on a "
        "shared or public computer. You will only have to do that once.\n "
        "For more information, please refer to www.diffpy.org/diffpy.utils/ "
        "examples/toolsexample.html "
    )
    print(intro_text)
    username = input(
        "Please enter the name you would want future work to be credited to: "
    ).strip()
    email = input("Please enter your email: ").strip()
    orcid = input("Please enter your orcid ID if you know it: ").strip()
    config = {
        "owner_name": _stringify(username),
        "owner_email": _stringify(email),
        "owner_orcid": _stringify(orcid),
    }
    if email != "" or orcid != "" or username != "":
        config["owner_orcid"] = _stringify(orcid)
        with open(config_path, "w") as f:
            f.write(json.dumps(config))
        outro_text = (
            f"The config file at {Path().home() / 'diffpyconfig.json'} has "
            f"been created. The values  {config} were entered.\n These values "
            "will be inserted as metadata with your data in apps that use "
            "diffpy.get_user_info(). If you would like to update these values "
            ", either delete the config file and this workflow will rerun "
            "next time you run this program.  Or you may open the config "
            "file in a text editor and manually edit the entries.  For more "
            "information, see: "
            "https://diffpy.github.io/diffpy.utils/examples/tools_example.html"
        )
        print(outro_text)
        config_exists = True
    return config_exists


def get_package_info(package_names, metadata=None):
    """Fetch package version and updates it into (given) metadata.

    Package info stored in metadata as
    {'package_info': {'package_name': 'version_number'}}.

    ----------
    package_name : str or list
        The name of the package(s) to retrieve the version number for.
    metadata : dict
        The dictionary to store the package info. If not provided, a new
        dictionary will be created.

    Returns
    -------
    metadata : dict
        The updated metadata dict with package info inserted.
    """
    if metadata is None:
        metadata = {}
    if isinstance(package_names, str):
        package_names = [package_names]
    package_names.append("diffpy.utils")
    pkg_info = metadata.get("package_info", {})
    for package in package_names:
        pkg_info.update({package: importlib.metadata.version(package)})
    metadata["package_info"] = pkg_info
    return metadata


def get_density_from_cloud(sample_composition, mp_token=""):
    """Function to get material density from the MP or COD database.

    It is not implemented yet.
    """
    raise NotImplementedError(
        "So sorry, density computation from composition is not implemented "
        "right now. "
        "We hope to have this implemented in the next release. "
        "Please rerun specifying a sample mass density."
    )


def compute_mu_using_xraydb(
    sample_composition, energy, sample_mass_density=None, packing_fraction=None
):
    """Compute the attenuation coefficient (mu) using the XrayDB database.

    Computes mu based on the sample composition and energy.
    User should provide a sample mass density or a packing fraction.
    If neither density nor packing fraction is specified,
    or if both are specified, a ValueError will be raised.
    Reference: https://xraypy.github.io/XrayDB/python.html#xraydb.material_mu.

    Parameters
    ----------
    sample_composition : str
        The chemical formula of the material.
    energy : float
        The energy of the incident x-rays in keV.
    sample_mass_density : float, optional, Default is None
        The mass density of the packed powder/sample in g/cm*3.
    packing_fraction : float, optional, Default is None
        The fraction of sample in the capillary (between 0 and 1).
        Specify either sample_mass_density or packing_fraction but not both.

    Returns
    -------
    mu : float
        The attenuation coefficient mu in mm^{-1}.
    """
    if (sample_mass_density is None and packing_fraction is None) or (
        sample_mass_density is not None and packing_fraction is not None
    ):
        raise ValueError(
            "You must specify either sample_mass_density or packing_fraction, "
            "but not both. "
            "Please rerun specifying only one."
        )
    if packing_fraction is not None:
        sample_mass_density = (
            get_density_from_cloud(sample_composition) * packing_fraction
        )
    energy_eV = energy * 1000
    mu = (
        material_mu(
            sample_composition,
            energy_eV,
            density=sample_mass_density,
            kind="total",
        )
        / 10
    )
    return mu


def _top_hat(z, half_slit_width):
    """Create a top-hat function, return 1.0 for values within the specified
    slit width and 0 otherwise."""
    return np.where((z >= -half_slit_width) & (z <= half_slit_width), 1.0, 0.0)


def _model_function(z, diameter, z0, I0, mud, slope):
    """
    Compute the model function with the following steps:
    1. Let dz = z-z0, so that dz is centered at 0
    2. Compute length l that is the effective length for computing intensity
       I = I0 * e^{-mu * l}:
    - For dz within the capillary diameter, l is the chord length of
      the circle at position dz
    - For dz outside this range, l = 0
    3. Apply a linear adjustment to I0 by taking I0 as I0 - slope * z
    """
    min_radius = -diameter / 2
    max_radius = diameter / 2
    dz = z - z0
    length = np.piecewise(
        dz,
        [
            dz < min_radius,
            (min_radius <= dz) & (dz <= max_radius),
            dz > max_radius,
        ],
        [0, lambda dz: 2 * np.sqrt((diameter / 2) ** 2 - dz**2), 0],
    )
    return (I0 - slope * z) * np.exp(-mud / diameter * length)


def _extend_z_and_convolve(z, diameter, half_slit_width, z0, I0, mud, slope):
    """Extend z values and I values for padding (so that we don't have tails in
    convolution), then perform convolution (note that the convolved I values
    are the same as modeled I values if slit width is close to 0)"""
    n_points = len(z)
    z_left_pad = np.linspace(
        z.min() - n_points * (z[1] - z[0]), z.min(), n_points
    )
    z_right_pad = np.linspace(
        z.max(), z.max() + n_points * (z[1] - z[0]), n_points
    )
    z_extended = np.concatenate([z_left_pad, z, z_right_pad])
    I_extended = _model_function(z_extended, diameter, z0, I0, mud, slope)
    kernel = _top_hat(z_extended - z_extended.mean(), half_slit_width)
    I_convolved = I_extended  # this takes care of the case where slit width is close to 0  # noqa: E501
    if kernel.sum() != 0:
        kernel /= kernel.sum()
        I_convolved = convolve(I_extended, kernel, mode="same")
    padding_length = len(z_left_pad)
    return I_convolved[padding_length:-padding_length]


def _objective_function(params, z, observed_data):
    """Compute the objective function for fitting a model to the
    observed/experimental data by minimizing the sum of squared residuals
    between the observed data and the convolved model data."""
    diameter, half_slit_width, z0, I0, mud, slope = params
    convolved_model_data = _extend_z_and_convolve(
        z, diameter, half_slit_width, z0, I0, mud, slope
    )
    residuals = observed_data - convolved_model_data
    return np.sum(residuals**2)


def _compute_single_mud(z_data, I_data):
    """Perform dual annealing optimization and extract the parameters."""
    bounds = [
        (
            1e-5,
            z_data.max() - z_data.min(),
        ),  # diameter: [small positive value, upper bound]
        (
            0,
            (z_data.max() - z_data.min()) / 2,
        ),  # half slit width: [0, upper bound]
        (z_data.min(), z_data.max()),  # z0: [min z, max z]
        (
            1e-5,
            I_data.max(),
        ),  # I0: [small positive value, max observed intensity]
        (1e-5, 20),  # muD: [small positive value, upper bound]
        (-100000, 100000),  # slope: [lower bound, upper bound]
    ]
    result = dual_annealing(_objective_function, bounds, args=(z_data, I_data))
    diameter, half_slit_width, z0, I0, mud, slope = result.x
    convolved_fitted_signal = _extend_z_and_convolve(
        z_data, diameter, half_slit_width, z0, I0, mud, slope
    )
    residuals = I_data - convolved_fitted_signal
    rmse = np.sqrt(np.mean(residuals**2))
    return mud, rmse


def compute_mud(filepath):
    """Compute the best-fit mu*D value from a z-scan file, removing the sample
    holder effect.

    This function loads z-scan data and fits it to a model
    that convolves a top-hat function with I = I0 * e^{-mu * l}.
    The fitting procedure is run multiple times, and we return the best-fit
    parameters based on the lowest rmse.

    The full mathematical details are described in the paper:
    An ad hoc Absorption Correction for Reliable Pair-Distribution Functions
    from Low Energy x-ray Sources, Yucong Chen, Till Schertenleib, Andrew Yang
    , Pascal Schouwink, Wendy L. Queen and Simon J. L. Billinge,
    in preparation.

    Parameters
    ----------
    filepath : str
        The path to the z-scan file.

    Returns
    -------
    mu*D : float
        The best-fit mu*D value.
    """
    z_data, I_data = loadData(filepath, unpack=True)
    best_mud, _ = min(
        (_compute_single_mud(z_data, I_data) for _ in range(20)),
        key=lambda pair: pair[1],
    )
    return best_mud
