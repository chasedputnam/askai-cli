import io
import os

import click

from openai_client import build_openai_client
from log_response import LogResponse


@click.command()
@click.argument("source", type=click.File("rt", encoding="utf-8"))
@click.option("-t", "--token", default="", help="OpenAI API token")
@click.option(
    "-m", "--model", default="gpt-3.5-turbo", help="OpenAI model option. (i.e. gpt-3.5-turbo)"
)
@click.option("-f", "--folder", default="", help="Conversation log storage folder")
def cli(source: io.TextIOWrapper, token: str, model: str, file: str):
    """Create response log file to append into"""
    log = LogResponse(path=file)
    log.create_rotating_chat_logger()
    """Start interactive shell session for OpenAI completion API."""
    client = build_openai_client(token=get_token(token), api_url=get_openai_api_url())
    while True:
        prompt = input("Prompt: ")
        log.print_and_log(prompt)
        service = check_prompt_prefix_for_service(prompt)
        if service == "google":
            print("Google Bard does not have an API endpoint available for use yet.")
        else:
            response = client.generate_response(prompt, model)
            log.print_and_log("Openai:")
            log.print_and_log(response)
            log.print_and_log("--------")


def check_prompt_prefix_for_service(prompt):
    openai_keywords = ["chatgpt","hey chatgpt","openai","hey openai"]
    google_keywords = ["bard","hey bard","google","hey google"]
    stripped_prompt = prompt.strip(prompt, "Prompt: ").lower()
    for keyword in openai_keywords:
        if stripped_prompt.startswith(keyword):
            return "openai"
    for keyword in google_keywords:
        if stripped_prompt.startswith(keyword):
            return "google"
    return ""


def get_openai_api_url() -> str:
    return os.environ.get("ASKAI_OPENAI_API_URL", "https://api.openai.com/v1/completions")


def get_log_path(path: str) -> str:
    if not path:
        path = os.environ.get("ASKAI_LOG_FOLDER", "")
    if not path:
        raise click.exceptions.UsageError(
           message=(
               "Either --folder (-f) option or ASKAI_LOG_FOLDER environment variable must be provided"
           )
        )


def get_token(token: str) -> str:
    if not token:
        token = os.environ.get("ASKAI_OPENAI_API_TOKEN", "")
    if not token:
        raise click.exceptions.UsageError(
            message=(
                "Either --token (-t)  option or ASKAI_OPENAI_API_TOKEN environment variable must be provided"
            )
        )
    return token


if __name__ == "__main__":
    cli()
