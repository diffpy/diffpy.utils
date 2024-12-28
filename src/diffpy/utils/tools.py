import importlib.metadata
import json
import warnings
from copy import copy
from pathlib import Path

from xraydb import material_mu


def clean_dict(obj):
    """Remove keys from the dictionary where the corresponding value is None.

    Parameters
    ----------
    obj: dict
        The dictionary to clean. If None, initialize as an empty dictionary.

    Returns
    -------
    dict:
        The cleaned dictionary with keys removed where the value is None.
    """
    obj = obj if obj is not None else {}
    for key, value in copy(obj).items():
        if not value:
            del obj[key]
    return obj


def _stringify(obj):
    """Convert None to an empty string.

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
    """Load configuration from a .json file.

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
    """Get name, email and orcid of the owner/user from various sources and
    return it as a metadata dictionary.

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
    You may also store any other global-level information that you would like associated with your
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
    user_info = global_config
    user_info.update(local_config)
    user_info.update(runtime_info)
    return user_info


def check_and_build_global_config(skip_config_creation=False):
    """Checks for a global diffpu config file in user's home directory and
    creates one if it is missing.

    The file it looks for is called diffpyconfig.json.  This can contain anything in json format, but
    minimally contains information about the computer owner.  The information is used
    when diffpy objects are created and saved to files or databases to retain ownership information
    of datasets.  For example, it is used by diffpy.utils.tools.get_user_info().

    If the function finds no config file in the user's home directory it interrupts execution
    and prompts the user for name, email, and orcid information.  It then creates the config file
    with this information inside it.

    The function returns True if the file exists and False otherwise.

    If you would like to check for a file but not run the file creation workflow you can set
    the optional argument skip_config_creation to True.

    Parameters
    ----------
    skip_config_creation: bool, optional, Default is False
      The bool that will override the creation workflow even if no config file exists.

    Returns
    -------
    bool: True if the file exists and False otherwise.
    """
    config_exists = False
    config_path = Path().home() / "diffpyconfig.json"
    if config_path.is_file():
        config_exists = True
        return config_exists
    if skip_config_creation:
        return config_exists
    intro_text = (
        "No global configuration file was found containing information about the user to "
        "associate with the data.\n By following the prompts below you can add your name "
        "and email to this file on the current "
        "computer and your name will be automatically associated with subsequent diffpy data by default.\n"
        "This is not recommended on a shared or public computer. "
        "You will only have to do that once.\n"
        "For more information, please refer to www.diffpy.org/diffpy.utils/examples/toolsexample.html"
    )
    print(intro_text)
    username = input("Please enter the name you would want future work to be credited to: ").strip()
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
            f"The config file at {Path().home() / 'diffpyconfig.json'} has been created. "
            f"The values  {config} were entered.\n"
            f"These values will be inserted as metadata with your data in apps that use "
            f"diffpy.get_user_info(). If you would like to update these values, either "
            f"delete the config file and this workflow will rerun next time you run this "
            f"program.  Or you may open the config file in a text editor and manually edit the"
            f"entries.  For more information, see: "
            f"https://diffpy.github.io/diffpy.utils/examples/tools_example.html"
        )
        print(outro_text)
        config_exists = True
    return config_exists


def get_package_info(package_names, metadata=None):
    """Fetches package version and updates it into (given) metadata.

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


def compute_mu_using_xraydb(sample_composition, energy, sample_mass_density=None, packing_fraction=None):
    """Compute the attenuation coefficient (mu) using the XrayDB database.

    Computes mu based on the sample composition and energy.
    User should provide a sample mass density or a packing fraction.
    If neither density nor packing fraction is specified, or if both are specified, a ValueError will be raised.
    Reference: https://xraypy.github.io/XrayDB/python.html#xraydb.material_mu.

    Parameters
    ----------
    sample_composition : str
        The chemical formula or the name of the material.
    energy : float
        The energy of the incident x-rays in keV.
    sample_mass_density : float, optional, Default is None
        The mass density of the packed powder/sample in gr/cm^3.
    packing_fraction : float, optional, Default is None
        The fraction of sample in the capillary (between 0 and 1).

    Returns
    -------
    mu : float
        The attenuation coefficient mu in mm^{-1}.
    """
    if (sample_mass_density is None and packing_fraction is None) or (
        sample_mass_density is not None and packing_fraction is not None
    ):
        raise ValueError(
            "You must specify either sample_mass_density or packing_fraction, but not both. "
            "Please rerun specifying only one."
        )
    if sample_mass_density is not None:
        mu = material_mu(sample_composition, energy * 1000, density=sample_mass_density, kind="total") / 10
    else:
        warnings.warn(
            "Warning: Density is set to None if a packing fraction is specified, "
            "which may cause errors for some materials. "
            "We recommend specifying sample mass density for now. "
            "Auto-density calculation is coming soon."
        )
        mu = material_mu(sample_composition, energy * 1000, density=None, kind="total") * packing_fraction / 10
    return mu
