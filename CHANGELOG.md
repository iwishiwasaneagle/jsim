# Changelog

All notable changes to this project will be documented in this file.

## [0.0.13+r2] - 2022-01-26

### Bug Fixes

- Never stored long_term_ds

### Performance

- Reduce number of trials and steps

### Testing

- Cache .tox properly, bump python to 3.10

## [0.0.13] - 2022-01-26

### Bug Fixes

- Updated python version
- Ignore imports (mypy)
- Mock pydantic in docs
- Mypy typing issues
- Added virtualenv back for tox
- Need to install reqs to run jupyter docs
- Specify python version
- Wrap py version in quotes

### Documentation

- CLI flags to make the submodule/subpackage a bit nicer to view
- Package requirements needed for doctest
- Example formatting in HexEnvironment.py

### Features

- New HexEnvironment to enable hexagonal tiled simulations
- Q-Learning hex environment example
- Q-Learning hex environment example completed. Results dubious
- Dev requirements
- Type checking with mypy

### Miscellaneous Tasks

- Add pydantic 1.8.2 to requirements
- Cache tox and pip in CI (#36)
- Bump fonttools from 4.28.4 to 4.28.5 (#34)
- Bump numpy from 1.21.4 to 1.21.5 (#35)
- Bump tox from 3.24.4 to 3.24.5 (#42)
- Bump virtualenv from 20.10.0 to 20.11.1 (#41)
- Bump identify from 2.4.0 to 2.4.1 (#39)
- Bump filelock from 3.4.0 to 3.4.2 (#37)
- Bump platformdirs from 2.4.0 to 2.4.1 (#38)
- Bump identify from 2.4.1 to 2.4.2 (#49)
- Bump pillow from 8.4.0 to 9.0.0 (#47)
- Bump virtualenv from 20.11.1 to 20.13.0 (#46)
- Bump identify from 2.4.2 to 2.4.4 (#51)
- Bump pydantic from 1.8.2 to 1.9.0 (#48)
- Bump codecov/codecov-action from 1 to 2.1.0 (#54)
- Bump pre-commit from 2.16.0 to 2.17.0 (#56)

### Performance

- 1 trial in doctests for HexQLearning Example

### Refactor

- Types and default envs in one block

### Testing

- Code coverage via tox and uploaded to CodeCov
- Tests specific requirements file rather than forcing tox to handle it
- Codecov coverage badge in readme
- Adjusted axial_to_pixel testto use pointy-top rather than flat

## [0.0.11] - 2021-12-16

### Documentation

- Images for docs and readme
- Use banner in docs
- Use docs/_static/banner.png in master branch in readme

### Miscellaneous Tasks

- Clicking readme logo directs to this repo

## [0.0.10] - 2021-12-16

### Bug Fixes

- Pre-commit should not be bundled with the package

### Documentation

- Add bare-minimum install and usage instructions
- Update the way the build system handles versioning (#25)

## [0.0.9] - 2021-12-15

### Bug Fixes

- Push master before tag to ensure CHANGELOG.md is on github when release is crafted
- Cite Lin et al. for the algorithm (#24)

## [0.0.8] - 2021-12-15

### Bug Fixes

- Not having pre-commit in path was causing errors with release.sh script

### Features

- Working linear kernel example of LHC_GW_CONV
- Configure dependabot correctly (#16) (#18)

### Miscellaneous Tasks

- Added scipy
- Added scipy
- Bump fonttools from 4.28.3 to 4.28.4 (#21)
- Bump matplotlib from 3.5.0 to 3.5.1 (#20)
- Bump pre-commit from 2.15.0 to 2.16.0 (#19)
- Bump tomli from 1.2.2 to 2.0.0 (#22)
- Bump distlib from 0.3.3 to 0.3.4 (#23)

### Styling

- Ensure jupyter notebooks are uploaded without output

## [0.0.7] - 2021-12-04

### Bug Fixes

- Pandoc was required for CI doctests and doc building

### Documentation

- Added capability to include jupyter notebooks in docs incl output
- Local Hill Climb and Potential-based navigation as jupyter notebooks

### Refactor

- User defines where env and agent get initialized

## [0.0.6] - 2021-12-04

### Bug Fixes

- Imports where to module, not the actual classes
- Circular dependcy error

### Documentation

- New RTD theme with better layout

## [0.0.5] - 2021-12-03

### Bug Fixes

- Pass psim to env as outlined in docs
- Frozen set of requirements which will help with dependabot security advice

### Features

- Potential function based navigation example
- Policy function to extend for user
- Add functionality to steps, trials, and __init__ as outlined in docs
- Add learn function to the Agent (#5)

### Refactor

- Start_trial renamed to reset (#8)
- Rename sensation to state (#11)
- Adjust architecture as per #12

### Testing

- Run examples as integration test
- Use cache to speed up CI
- Remove windows and macos from CI testing
- Tests if docs still build

## [0.0.4] - 2021-12-01

### Bug Fixes

- Prevent pre-commit from running. Was causing the script to fail. The assumption is that pre-commit has been run already
- Prevent pre-commit from running. Was causing the script to fail. The assumption is that pre-commit has been run already

### Documentation

- Outline the Agent class skeleton alongside docstrings
- Give credit to Richard S. Sutton and Juan Carlos Santamaria
- Enhance descriptions of what the agent does
- Outline the Environment class skeleton alongside docstrings
- Outline the Simulation class skeleton alongside docstrings
- Brief descriptions of what Actiona and Sensation do
- Outline the Agent class skeleton alongside docstrings
- Give credit to Richard S. Sutton and Juan Carlos Santamaria
- Enhance descriptions of what the agent does
- Outline the Environment class skeleton alongside docstrings
- Outline the Simulation class skeleton alongside docstrings
- Brief descriptions of what Actiona and Sensation do
- Update readme with more information

### Miscellaneous Tasks

- Ignore F401 errors in __init__.py
- Add blacken-docs to pre-commit check to ensure good docstrings
- Delete remnents from pyscaffold
- Ignore F401 errors in __init__.py
- Add blacken-docs to pre-commit check to ensure good docstrings
- Delete remnents from pyscaffold
- Ignore F401 errors in __init__.py

### Refactor

- Use `abc` rather than manually raisingin NotImplementedError
- Use `abc` rather than manually raisingin NotImplementedError

### Testing

- Add skeleton for testing of new modules
- Test if the proper methods are abstract via sets
- Only run CI on push in master and dev
- Tox as test requirement
- Add skeleton for testing of new modules
- Test if the proper methods are abstract via sets
- Only run CI on push in master and dev

## [0.0.3] - 2021-11-30

### Documentation

- Update link to changelog

### Testing

- Update testing dependencies

## [0.0.1] - 2021-11-30

### Bug Fixes

- Requirements auto installed when tox is run

### Docs

- Add section on contributing to README.md

### Documentation

- Encode version number into build files

### Feat

- Use git-cliff to automate changelogs

### Features

- Upload wheel and sdist to release

