import os
from fabric import Connection

expected_env_variables = [
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY",
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET",
    "DJANGO_SECRET_KEY",
]
for expected_env_variable in expected_env_variables:
    if expected_env_variable not in os.environ:
        raise Exception(f"Please export a {expected_env_variable} environment variable")

connection = Connection("user@server")
with connection.cd("/filepath_to_repo"):
    connection.run(
        "export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY="
        f"{os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']}"
        " && export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET="
        f"{os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET']}"
        " && export DJANGO_SECRET_KEY="
        f"'{os.environ['DJANGO_SECRET_KEY']}'"
        " && sh deploy/deploy.sh"
    )
print("=========== Deployed ============")
