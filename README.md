# Workspace Service

[![Python](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://www.python.org/)

Provides APIs to help manage workspace resources such as Guacamole.

## Getting Started

### Prerequisites

This project is using [Poetry](https://python-poetry.org/docs/#installation) to handle the dependencies. Installtion instruction for poetry can be found at https://python-poetry.org/docs/#installation

### Installation & Quick Start

1. Clone the project.

       git clone https://github.com/PilotDataPlatform/workspace.git

2. Install dependencies.

       poetry install

3. Add environment variables into `.env`. Use `.env.schema` as a reference.

4. Run application.

       poetry run python start.py

### Startup using Docker

This project can also be started using [Docker](https://www.docker.com/get-started/).

1. To build and start the service within the Docker container, run:

       docker compose up


## Contribution

You can contribute the project in following ways:

* Report a bug.
* Suggest a feature.
* Open a pull request for fixing issues or adding functionality. Please consider
  using [pre-commit](https://pre-commit.com) in this case.

## Acknowledgements
The development of the HealthDataCloud open source software was supported by the EBRAINS research infrastructure, funded from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3) and H2020 Research and Innovation Action Grant Interactive Computing E-Infrastructure for the Human Brain Project ICEI 800858.
