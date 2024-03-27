# Makefile
SHELL = /bin/bash

# Styling
.PHONY: style
style:
	black .
	flake8
