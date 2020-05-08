ARG VARIANT=3.8
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

ENV PIP_TARGET=/usr/local/pip-global
ENV PYTHONPATH=${PIP_TARGET}:${PYTHONPATH}
ENV PATH=${PIP_TARGET}/bin:${PATH}
RUN mkdir -p ${PIP_TARGET} \
  && chown vscode:root ${PIP_TARGET} \
  && export SNIPPET="if [ \"\$(stat -c '%U' ${PIP_TARGET})\" != \"vscode\" ]; then chown -R vscode:root ${PIP_TARGET}; fi" \
  && echo "$SNIPPET" | tee -a /root/.bashrc >> /home/vscode/.bashrc \
  && echo "$SNIPPET" | tee -a /root/.zshrc >> /home/vscode/.zshrc
