FROM python:3.9-buster AS production-environment

WORKDIR /usr/src/app

ENV TZ=America/Toronto

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    apt-get update && \
    apt-get install -y libsasl2-dev python-dev libldap2-dev libssl-dev vim-tiny less && \
    ln -s /usr/bin/vim.tiny /usr/bin/vim && \
    rm -rf /var/lib/apt/lists/*

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev --no-root --no-interaction
COPY . .

FROM production-environment AS workspace-image

CMD ["python", "run.py"]

FROM production-environment AS development-environment

RUN poetry install --no-root --no-interaction
