help: ## Список команд
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

docker_compose := docker compose
NODE_CONTAINER_NAME := node

up: ## Старт контейнеров
	$(docker_compose) up -d

static: ## Статическая сборка node
	$(docker_compose) run --rm "$(NODE_CONTAINER_NAME)" npm run build

down: ## Остановка контейнеров
	$(docker_compose) down

restart: ## Рестарт контейнеров
	$(docker_compose) restart

i: ## Установка / обновление зависимостей
	$(docker_compose) run --rm "$(NODE_CONTAINER_NAME)" npm install

build: ## Поднять контейнеры и собрать образ
	$(docker_compose) up -d --build 

logs: ## Список логов всех контейнеров
	$(docker_compose) logs -f

npm: ## Позволяет выполнять команды в node контейнере (make npm command="npm install")
	$(docker_compose) run --rm "$(NODE_CONTAINER_NAME)" $(command)

	