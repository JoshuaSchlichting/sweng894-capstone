FROM python:3.8
SHELL ["/bin/bash", "-c"]
RUN useradd -ms /bin/bash appuser
ENV POETRY_HOME="/opt/poetry"

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python - \
    && chown -R appuser /opt/poetry
USER appuser
WORKDIR /app


ENV PATH="${POETRY_HOME}/bin:$PATH"
ENV PYTHONPATH="$PYTHONPATH:src"
COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev


COPY ./app /app
CMD [ "python", "main.py"]
