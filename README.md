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

Pilot HDC was developed by Indoc Research Europe gGmbH ([info@indocresearch.org](mailto:info@indocresearch.org)) in the context of the HealthDataCloud and eBRAIN-Health projects.

The development of the HealthDataCloud open source software was supported by the EBRAINS research infrastructure, funded from the European Union's Horizon 2020 Framework Programme for Research and Innovation under the Specific Grant Agreement No. 945539 (Human Brain Project SGA3) and H2020 Research and Innovation Action Grant Interactive Computing E-Infrastructure for the Human Brain Project ICEI 800858.

The eBRAIN-Health project has received funding from the European Union’s Horizon Europe research and innovation programme under grant agreement No 101058516. Views and opinions expressed are however those of the author(s) only and do not necessarily reflect those of the European Union or other granting authorities. Neither the European Union nor other granting authorities can be held responsible for them.

![HDC-EU-acknowledgement](https://hdc.ebrains.eu/img/HDC-EU-acknowledgement.png)
