build:
	docker build .
run:
	docker run -it --name centos centos:centos7 /bin/bash
exec:
	docker start centos
	docker attach centos
ps:
	docker ps -a
img:
	docker images
rm:
	docker rm -f $$(docker ps -aq)
rmi:
	docker rmi $$(docker images -q)
