FROM python:3.10
ARG requirement

WORKDIR /django_shop

# Copy project files to the working directory
COPY . /django_shop/

#RUN apt-get update && apt-get install -y \
#    python3.8-dev \

# Install Python dependencies
RUN pip install -r /django_shop/requirements.txt


COPY ./entrypoint.py /django_shop/

RUN chmod +x /django_shop/entrypoint.py
CMD ["python", "/django_shop/entrypoint.py"]

# for build image use these structure
# sudo docker build --build-arg requirement_file=production.txt --no-cache -t eclaim_production:latest -f Dockerfile .
