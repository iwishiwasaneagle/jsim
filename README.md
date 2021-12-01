# jSim

[![CI](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CI.yml/badge.svg)](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CI.yml)
[![CD](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CD.yml/badge.svg)](https://github.com/iwishiwasaneagle/jsim/actions/workflows/CD.yml)

Simulation environment for SAR research.

## Description

SAR is a unique design problem for path planning with little exposure to research. The search planning is highly dependent on the environment, and what it contains. Many papers use Probability Distribution Maps (PDMs) to inform the algorithms to make better paths since less time taken to find a missing person means higher chance of survivability.

This simulation environment is built to accommodate my research into this topic but anyone interested is more than welcome to help me build it.

## Making Changes & Contributing

This project uses `pre-commit`, please make sure to install it before making any changes:

```bash
pip install pre-commit
cd demo-project
pre-commit install
```

It is a good idea to update the hooks to the latest version:

```bash
pre-commit autoupdate
```

## References

- Architecture heavily inspired by [http://incompleteideas.net/RLinterface/RLI-Cplusplus.html](http://incompleteideas.net/RLinterface/RLI-Cplusplus.html)
