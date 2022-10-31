FROM ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.3.0}
USER 0
RUN apt-get update && apt-get install -y git
#RUN touch /var/run/docker.sock
#RUN chown 777 /var/run/docker.sock