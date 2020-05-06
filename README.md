# node-list-licenses

This python script automates aspects of OSS compliance by listing all licenses
from the node.js dependency tree. A file is considered a license if it is at the
repo root and the file name contains "license", "licence", "notice" or
"copying".

## Usage

`./main.py <path-to-repo> [<path-to-config>]`

## Configuration

The configuration file is a json file. It currently accepts only a list of regex
expressions, under the key `excluded`, to exclude a package and its dependencies
from the output. It does not invalidate any other reason why a dependency of an
excluded package may end up in the output.

Internally, the script uses `re.match`. Therefore, remember to use `.*` instead
of `*` for matching anything, or you will have a bad time.

An example config file, excluding jest, eslint and @testing-library can be found
in `default.json`. This is also the default config file if none is passed on the
command line

## Missing LICENSE files

Occasionally, a project may specify its license in the README or in the source
code headers instead. When this occurs, the script will report a warning that
the license file cannot be found. To supply the license, create a file inside
the `licenses` folder with the name `<package-name>@<version>`, replacing any
`/` characters with `_`. The license needs to be resupplied when updating the
package, in case the license changes. The LICENSE file in a repo takes priority
over the `licenses` folder.

## Possible enhancements

* Allow specifying author to CC-BY licensed projects directly
* Allow checking for file names containing keywords but seem to be spurious
* Check for files named by the license name (eg. MIT, MPL, OFL, etc.)
* A better CLI interface
* Check for SPDX and license mismatches

## Disclaimer

THERE IS NO GUARANTEE THAT RUNNING THIS SCRIPT WILL COMPLETELY SATISFY OSS
COMPLIANCE REQUIREMENTS. In particular, the script does not supply the author of
any CC-BY licensed packages. The script may generate extraneous licenses (such
as the license for documentation) or miss non-standard license file names. Also
see warranty disclaimer in `LICENSE`.

## License

MIT, see `LICENSE`. As a clarification, the requirements for including copyright
and permission notices do not apply to the script's output.