FROM tercen/runtime-python39:0.2.2

COPY ./src /operator
COPY ./operator.json /operator/operator.json
COPY ./requirements.txt /operator/requirements.txt


WORKDIR /operator

RUN python3 -m pip install -r ./requirements.txt --force

ENV TERCEN_SERVICE_URI https://tercen.com


ENTRYPOINT [ "python3", "main.py"]
CMD [ "--taskId", "someid", "--serviceUri", "https://tercen.com", "--token", "sometoken"]
