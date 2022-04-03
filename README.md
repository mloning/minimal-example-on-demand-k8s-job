# Minimal example for running on-demand K8s job using FastAPI

## Getting started

* Install Python requirements (see `environment.yml`)
* Install minikube (<https://minikube.sigs.k8s.io/docs/start/>)
* Launch minikube cluster (<https://kubernetes.io/docs/tutorials/hello-minikube/>)

## Run

* Run API: `uvicorn main:app --reload`
* To see root page, run: `open http://127.0.0.1:8000`.
* Try out "run_job" POST request on docs page: `http://127.0.0.1:8000/docs`
* Run `kubectl get jobs` and `kubectl get pods` to see created job and associated pods.
* Run `kubectl logs <pod-name>` to see logs for given pod.

## Clean up

* `kubectl delete <resource> <name>`, e.g. `kubectl job <job-name>`
* `minikube stop`
* `minikube delete`
