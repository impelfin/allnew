# step 1 : Base Images
FROM python:3.9

# step 2 : Package Install
RUN apt -y update && apt -y upgrade && apt -y install git net-tools vim

# step 3 : Specify a working directory
WORKDIR '/root'

# step 4 : Config file copy
COPY .bashrc .
COPY .exrc .
COPY hello.py .
RUN pip install bottle

# step 5 : open port
EXPOSE 8000

# step 6 : Execution Program
CMD ["python", "hello.py"]
