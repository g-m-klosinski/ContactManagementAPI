Contact Management API
======================

A single-user database with contacts exposed via HTTP

Quick Start
-----------

You can launch the server with
[UV manager](https://docs.astral.sh/uv/) as follows:

1. Clone this repository and `cd` into it

1. Synchronize environment with `uv sync`

1. Start the server:
   ```
   uv run uvicorn myapi.main:app --host 0.0.0.0 --port 8000
   ```

1. Open your browser and go to `http://localhost:8000/docs` to see
   the API documentation


Motivation
----------

The project comes from
https://www.upgrad.com/blog/backend-projects/
list. The name there is "Simple Contact Management API".

ℹ️ The site may redirect you to your locale and report
"page not found". In this case, access it through a search
engine, typing e.g. "20 backend projects".