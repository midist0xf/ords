.PHONY: setup deploy build check

setup: node_modules .env
deploy: preflight build push

node_modules:
	npm install

.env:
	cp .env.example .env

preflight:
	@echo "[preflight] Running deployment preflight checks..."
	@node scripts/preflight.js

build:
	npm run build

push:
	@echo "[deploy] Pushing to deployment target..."

validate:
	@echo "[validate] Running post-deployment validation..."
	@node scripts/validate.js