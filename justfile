# List recipes
default:
    @just --list

# Install Python and Node dependencies
install:
    uv sync
    npm install

# Run the dev server, rebuilding styles and reloading the browser on change
run port="8001": install
    #!/usr/bin/env bash
    trap 'kill 0' EXIT
    npm run watch &
    uv run manage.py runserver 0.0.0.0:{{port}}
