$PROJECT = 'diffpy.utils'
$ACTIVITIES = [
              'changelog', # Create a CHANGELOG.rst using news directory
              'tag',  # Creates a tag for the new version number
              'push_tag',  # Pushes the tag up to the $TAG_REMOTE
              'ghrelease',  # Creates a Github release entry for the new tag
              'pypi',  # Sends the package to pypi
               ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$CHANGELOG_IGNORE = ['TEMPLATE.rst']
$PUSH_TAG_REMOTE = 'git@github.com:diffpy/diffpy.utils.git'  # Repo to push tags to
$GITHUB_ORG = 'diffpy'  # Github org for Github releases and conda-forge
$GITHUB_REPO = 'diffpy.utils'  # Github repo for Github releases  and conda-forge
$GHRELEASE_PREPEND = """See [CHANGELOG.rst](CHANGELOG.rst) for detailed release notes.

The release is also available at [PyPI](https://pypi.org/project/diffpy.utils/) and [Conda](https://anaconda.org/conda-forge/diffpy.utils).
"""  # release message
