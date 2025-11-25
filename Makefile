# Makefile para proyecto CI/CD

# Variables
IMAGE_NAME=cocha
IMAGE_VERSION=1.0.5
STACK_NAME=doraemon
# ⚠️ IMPORTANTE: Reemplaza con tu usuario de GitHub
GITHUB_USER=Silvert05

# Construcción local de la imagen
build:
	docker build -t $(IMAGE_NAME):$(IMAGE_VERSION) .

# Etiquetar para GHCR
tag:
	docker tag $(IMAGE_NAME):$(IMAGE_VERSION) ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME):$(IMAGE_VERSION)

# Push a GitHub Container Registry
push: tag
	docker push ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME):$(IMAGE_VERSION)

# Desplegar con Docker Stack
deploy:
	docker stack deploy --with-registry-auth -c stack.yml $(STACK_NAME)

# Remover el stack
rm:
	docker stack rm $(STACK_NAME)

# Ver servicios del stack
ps:
	docker stack ps $(STACK_NAME)

# Ver logs del servicio
logs:
	docker service logs -f $(STACK_NAME)_pgcocha

# Ejecutar tests localmente
test:
	pytest tests/ -v

# Construir y ejecutar localmente
run: build
	docker run -p 5000:5000 $(IMAGE_NAME):$(IMAGE_VERSION)

# Limpiar imágenes locales
clean:
	docker rmi $(IMAGE_NAME):$(IMAGE_VERSION) || true
	docker rmi ghcr.io/$(GITHUB_USER)/$(IMAGE_NAME):$(IMAGE_VERSION) || true

# Ayuda
help:
	@echo "Comandos disponibles:"
	@echo "  make build   - Construir imagen Docker localmente"
	@echo "  make tag     - Etiquetar imagen para GHCR"
	@echo "  make push    - Subir imagen a GHCR"
	@echo "  make deploy  - Desplegar stack en Docker Swarm"
	@echo "  make rm      - Eliminar stack"
	@echo "  make ps      - Ver estado de servicios"
	@echo "  make logs    - Ver logs del servicio"
	@echo "  make test    - Ejecutar tests"
	@echo "  make run     - Ejecutar contenedor localmente"
	@echo "  make clean   - Limpiar imágenes locales"

.PHONY: build tag push deploy rm ps logs test run clean help