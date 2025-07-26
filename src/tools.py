import logging
from livekit.agents import function_tool, RunContext

import requests

from langchain_community.tools import DuckDuckGoSearchRun

@function_tool()
async def get_weather(
    run_context: RunContext,
    location: str,) -> str:
    """
    Get the current weather for a given location.
    """

    try:
        response = requests.get(
            f"https://wttr.in/{location}?format=3")
        if response.status_code == 200:
            logging.info(f"Weather for {location}: {response.text.strip()}")
            return response.text.strip()
        else:
            logging.error(f"Failed to get weather for {location}: {response.status_code}")
            return f"Could not retrieve weather data for {location}."
    except Exception as e:
        logging.error(f"Error fetching weather data: {e}")
        return f"An error occurred while retrieving weather data for {location}."
    


@function_tool()
async def search_web(
    run_context: RunContext,
    query: str,
) -> str:
    """
    Search the web using DuckDuckGo and return the results.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        if results:
            logging.info(f"Search results for '{query}': {results}")
            return results
        else:
            logging.warning(f"No results found for '{query}'.")
            return "No results found."
    except Exception as e:
        logging.error(f"Error during web search: {e}")
        return "An error occurred while searching the web."
    

@function_tool()
async def translate_text(
    run_context: RunContext,
    text: str,
    target_language: str,
    source_language: str = "en",
) -> str:
    """
    Translates a given text from a source language to a target language.

    Args:
        text: The text to be translated.
        target_language: The language to translate the text into (e.g., 'es' for Spanish, 'fr' for French).
        source_language: The language of the original text (e.g., 'en' for English). Defaults to 'en'.
    """
    logging.info(f"Attempting to translate '{text}' from {source_language} to {target_language}")

    # This tool uses the free MyMemory API.
    # See their documentation here: https://mymemory.translated.net/doc/spec.php
    api_url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"{source_language}|{target_language}"
    }

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)

        data = response.json()

        # Safely access the translated text from the response
        translated_text = data.get("responseData", {}).get("translatedText")
        
        if translated_text:
            logging.info(f"Translation successful: {translated_text}")
            return translated_text
        else:
            # Handle cases where the API gives a 200 response but no translation
            error_details = data.get("responseDetails", "No details provided.")
            logging.warning(f"Translation API did not return a valid translation. Details: {error_details}")
            return f"Could not translate the text. API response: {error_details}"

    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling translation API: {e}")
        return "An error occurred while communicating with the translation service."
    except Exception as e:
        logging.error(f"An unexpected error occurred during translation: {e}")
        return "An unexpected error occurred."
    

