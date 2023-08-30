# use some sensible default shell settings
SHELL := /bin/bash
$(VERBOSE).SILENT:
.DEFAULT_GOAL := help

##@ Entry Points
.PHONY: cli
cli: 
	echo "Running MVDAM Docker instance..."
	docker-compose 