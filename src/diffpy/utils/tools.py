import importlib.metadata
import json
from copy import copy
from pathlib import Path

from xraydb import material_mu


def _stringify(obj):
    """
    Convert None to an empty string.

    Parameters
    ----------
    obj: str
        The object to convert. If None, return an empty string.

    Returns
    -------
    str or None:
        The converted string if obj is not None, otherwise an empty string.
    """
    return obj if obj is not None else ""


def _load_config(file_path):
    """
    Load configuration from a .json file.

    Parameters
    ----------
    file_path: Path
        The path to the configuration file.

    Returns
    -------
    dict:
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
    """
    Get name, email and orcid of the owner/user from various sources and return it as a metadata dictionary

    The function looks for the information in json format configuration files with the name 'diffpyconfig.json'.
    These can be in the user's home directory and in the current working directory.  The information in the
    config files are combined, with the local config overriding the home-directory one.  Values for
    owner_name, owner_email, and owner_orcid may be passed in to the function and these override the values
    in the config files.

    A template for the config file is below.  Create a text file called 'diffpyconfig.json' in your home directory
    and copy-paste the template into it, editing it with your real information.
    {
      "owner_name": "<your name as you would like it stored with your data>>",
      "owner_email": "<your_associated_email>>@email.com",
      "owner_orcid": "<your_associated_orcid if you would like this stored with your data>>"
    }
    You may also store any other gloabl-level information that you would like associated with your
    diffraction data in this file

    Parameters
    ----------
    owner_name: string, optional, default is the value stored in the global or local config file.
        The name of the user who will show as owner in the metadata that is stored with the data
    owner_email: string, optional, default is the value stored in the global or local config file.
        The email of the user/owner
    owner_orcid:  string, optional, default is the value stored in the global or local config file.
        The ORCID id of the user/owner

    Returns
    -------
    dict:
        The dictionary containing username, email and orcid of the user/owner, and any other information
        stored in the global or local config files.

    """
    runtime_info = {"owner_name": owner_name, "owner_email": owner_email, "owner_orcid": owner_orcid}
    for key, value in copy(runtime_info).items():
        if value is None or value == "":
            del runtime_info[key]
    global_config = _load_config(Path().home() / "diffpyconfig.json")
    local_config = _load_config(Path().cwd() / "diffpyconfig.json")
    # if global_config is None and local_config is None:
    #     print(
    #         "No global configuration file was found containing "
    #         "information about the user to associate with the data.\n"
    #         "By following the prompts below you can add your name and email to this file on the current "
    #         "computer and your name will be automatically associated with subsequent diffpy data by default.\n"
    #         "This is not recommended on a shared or public computer. "
    #         "You will only have to do that once.\n"
    #         "For more information, please refer to www.diffpy.org/diffpy.utils/examples/toolsexample.html"
    #     )
    user_info = global_config
    user_info.update(local_config)
    user_info.update(runtime_info)
    return user_info


def get_package_info(package_names, metadata=None):
    """
    Fetches package version and updates it into (given) metadata.

    Package info stored in metadata as {'package_info': {'package_name': 'version_number'}}.

    ----------
    package_name : str or list
        The name of the package(s) to retrieve the version number for.
    metadata : dict
        The dictionary to store the package info. If not provided, a new dictionary will be created.

    Returns
    -------
    dict:
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


def compute_mu_using_xraydb(sample_composition, energy, density=None, packing_fraction=1):
    """Compute the attenuation coefficient (mu) using the XrayDB database.

    This function calculates mu based on the sample composition and energy.
    If density is not provided, a standard reference density (e.g., 0.987 g/cm^3 for H2O) is used.
    User can provide either a measured density or an estimated packing fraction (with a standard density).
    It is recommended to specify the density, especially for materials like ZrO2, where it can vary.
    Reference: https://xraypy.github.io/XrayDB/python.html#xraydb.material_mu

    Parameters
    ----------
    sample_composition: str
        The chemical formula or the name of the material
    energy: float
        The energy in eV
    density: float, optional, Default is None
        The mass density of the packed powder/sample in gr/cm^3. If None, a standard density from XrayDB is used.
    packing_fraction: float, optional, Default is 1
        The fraction of sample in the capillary (between 0 and 1)

    Returns
    -------
    the attenuation coefficient mu in mm^{-1}
    """
    mu = material_mu(sample_composition, energy, density=density, kind="total") * packing_fraction / 10
    return mu
