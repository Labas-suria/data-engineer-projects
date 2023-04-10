From python:3

ARG aws_default_region
ARG aws_access_key_id
ARG aws_secret_access_key

ENV AWS_DEFAULT_REGION=$aws_default_region
ENV AWS_ACCESS_KEY_ID=$aws_access_key_id
ENV AWS_SECRET_ACCESS_KEY=$aws_secret_access_key

COPY . .

RUN pip install -r requirements.txt

CMD python main.py
