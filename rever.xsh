$PROJECT = 'diffpy.utils'
$ACTIVITIES = [
              'tag',  # Creates a tag for the new version number
              'push_tag',  # Pushes the tag up to the $TAG_REMOTE
              'pypi',  # Sends the package to pypi
              'ghrelease'  # Creates a Github release entry for the new tag
               ]
$PUSH_TAG_REMOTE = 'git@github.com:diffpy/diffpy.utils.git'  # Repo to push tags to
$GITHUB_ORG = 'diffpy'  # Github org for Github releases and conda-forge
$GITHUB_REPO = 'diffpy.utils'  # Github repo for Github releases  and conda-forge
$GHRELEASE_PREPEND = """See [CHANGELOG.md](CHANGELOG.md) for detailed release notes.

The release is also available at [PyPI](https://pypi.org/project/diffpy.pdffit2/) and [Conda](https://anaconda.org/conda-forge/diffpy.pdffit2).
"""  # release message
