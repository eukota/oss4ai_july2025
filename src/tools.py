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
    

@function_tool()
async def wikipedia_summary(
    run_context: RunContext,
    query: str,
) -> str:
    """
    Provides a brief summary of a Wikipedia article for a given query.

    Args:
        query: The topic to search for on Wikipedia.
    """
    logging.info(f"Fetching Wikipedia summary for: {query}")
    try:
        # The 'wikipedia' library automatically handles searching and disambiguation.
        # 'auto_suggest=True' helps find the right page even with typos.
        # 'sentences=3' keeps the summary concise.
        summary = wikipedia.summary(query, sentences=3, auto_suggest=True)
        return summary
    except wikipedia.exceptions.PageError:
        logging.warning(f"Wikipedia page not found for query: {query}")
        return f"Sorry, I couldn't find a Wikipedia page for '{query}'."
    except wikipedia.exceptions.DisambiguationError as e:
        logging.info(f"Disambiguation needed for query: {query}. Options: {e.options[:3]}")
        # Return the top 3 suggestions to the user/agent
        return f"That query is ambiguous. Did you mean: {', '.join(e.options[:3])}?"
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching from Wikipedia: {e}")
        return "An error occurred while trying to get a Wikipedia summary."


# Tool 3: Random Joke Generator
@function_tool()
async def get_random_joke(
    run_context: RunContext,
) -> str:
    """
    Fetches a random joke from a public API.
    """
    logging.info("Fetching a random joke.")
    # This API provides jokes in a two-part format (setup and punchline).
    api_url = "https://official-joke-api.appspot.com/random_joke"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        joke = f"{data['setup']} - {data['punchline']}"
        return joke
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling joke API: {e}")
        return "Sorry, I couldn't fetch a joke right now."
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching a joke: {e}")
        return "An unexpected error occurred."


# Tool 4: Safe Calculator
@function_tool()
async def calculate(
    run_context: RunContext,
    expression: str,
) -> str:
    """
    Safely evaluates a mathematical expression.

    Args:
        expression: The mathematical string to evaluate (e.g., "5 * (3 + 1)").
    """
    logging.info(f"Calculating expression: {expression}")
    try:
        # asteval is a robust library for safely evaluating Python expressions.
        # It prevents the execution of malicious code.
        aeval = asteval.Astraeval()
        result = aeval.eval(expression)
        return f"The result of '{expression}' is {result}."
    except Exception as e:
        logging.error(f"Error evaluating expression '{expression}': {e}")
        return f"I couldn't calculate that. Please check if it's a valid mathematical expression."
