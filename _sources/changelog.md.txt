# Changelog

All notable changes to this project will be documented in this file.

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

