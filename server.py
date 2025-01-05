import os
from rasa.core.run import serve_application

if __name__ == "__main__":
    serve_application(
        model_directory="models",
        endpoints="endpoints.yml",
        cors="*",
        enable_api=True,
    )
