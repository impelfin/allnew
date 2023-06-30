all : appdep getdep getsvc getpod
restart : delsvc deldep appdep getdep getsvc getpod
appdep:
	kubectl apply -f deployment.yaml
getdep:
	kubectl get deployment
getsvc:
	kubectl get svc -o wide
getpod:
	kubectl get pod -o wide
delsvc:
	kubectl delete svc test 
deldep:
	kubectl delete deployment test 
