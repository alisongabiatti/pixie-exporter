TAG:=1.0.5
cluster:='[your_cluster_name]'
image:="alisongabiatti/sli-services-exporter:${TAG}"

@PHONY: deploy
deploy:
	@cd ./k8s \
	&& kustomize edit set image ${image} \
	&& cd ..
	kustomize build k8s/. | kubectl apply --context ${cluster} -n monit -f -

@PHONY: docker-build
docker-build:
	docker build . --platform linux/amd64 -t ${image}

@PHONY: docker-push
docker-push:
	@echo "Pushing image ${image}"
	docker push ${image}

@PHONY: deploy-all
deploy-all: docker-build docker-push deploy

@PHONY: run
run:
	docker-compose up --force-recreate  --build
