from openai import OpenAI
import logging
from typing import List, Dict, Tuple
import json
import requests

def verify_llm_connection(provider: str, api_key: str, llm_model: str) -> Tuple[bool, str, dict]:
    """Tests the LLM connection with a tiny payload and extracts initial limits."""
    if not api_key and provider != "Ollama":
        return False, "API Key missing.", {}

    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=api_key)
            model = llm_model if llm_model else "gpt-4o-mini"
        elif provider == "Groq":
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            model = llm_model if llm_model else "qwen/qwen3.8-27b"
        elif provider == "Ollama":
            client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
            model = llm_model if llm_model else "llama3"
        elif provider == "Anthropic":
            return False, "Use OpenRouter to access Anthropic models with the OpenAI SDK.", {}
        elif provider == "OpenRouter":
            client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
            model = llm_model if llm_model else "anthropic/claude-3-haiku"
        elif provider == "Google Gemini":
            client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            model = llm_model if llm_model else "gemini-1.5-flash"
        elif provider == "HuggingFace":
            client = OpenAI(api_key=api_key, base_url="https://api-inference.huggingface.co/v1/")
            model = llm_model if llm_model else "meta-llama/Meta-Llama-3-8B-Instruct"
        else:
            return False, f"Provider {provider} not fully supported yet.", {}

        raw_response = client.chat.completions.with_raw_response.create(
            model=model,
            messages=[{"role": "user", "content": "Reply OK"}],
            max_tokens=5,
        )
        
        parsed = raw_response.parse()
        text_result = parsed.choices[0].message.content.strip()
        headers = raw_response.headers
        usage_stats = {}
        
        if provider in ["OpenAI", "Groq"]:
            rem_req = headers.get("x-ratelimit-remaining-requests")
            rem_tok = headers.get("x-ratelimit-remaining-tokens")
            if rem_req: usage_stats["remaining_requests"] = rem_req
            if rem_tok: usage_stats["remaining_tokens"] = rem_tok
            usage_stats["type"] = "tokens"
            
        elif provider == "OpenRouter":
            usage_stats = fetch_openrouter_limits(api_key)
            
        elif provider == "HuggingFace":
            rem_req = headers.get("x-ratelimit-remaining")
            if rem_req: usage_stats["remaining_requests"] = rem_req
            usage_stats["type"] = "requests"
            
        elif provider == "Google Gemini":
            usage_stats["type"] = "run_usage"
            
        elif provider == "Ollama":
            usage_stats = {"type": "local", "status": "∞ Infinite"}

        return True, text_result, usage_stats
    except Exception as e:
        return False, str(e), {}


def fetch_openrouter_limits(api_key: str) -> dict:
    """Fetches exact OpenRouter credits via their auth endpoint."""
    try:
        res = requests.get("https://openrouter.ai/api/v1/auth/key", headers={"Authorization": f"Bearer {api_key}"}, timeout=5)
        if res.status_code == 200:
            data = res.json()
            limit = data.get("data", {}).get("limit")
            usage = data.get("data", {}).get("usage")
            if limit is not None and usage is not None:
                remaining = float(limit) - float(usage)
                return {"type": "credits", "remaining": f"${remaining:.4f}"}
    except Exception as e:
        logging.warning(f"Failed to fetch OpenRouter limits: {e}")
    return {}


def generate_payload(
    provider: str, api_key: str, llm_model: str, context: str, system_prompt: str
) -> Tuple[str, dict]:
    """Uses the configured LLM to generate the payload and extracts rate limits/usage."""
    if not api_key and provider != "Ollama":
        logging.error("API key missing for LLM provider.")
        return "Error: API Key missing.", {}

    prompt = ""
    if context:
        prompt = f"Here is the raw data fetched from the endpoints:\n\n{context}\n\nBased on this data, generate the final output strictly following the system instructions."
    else:
        prompt = "Execute your system instructions and generate the final output."

    try:
        if provider == "OpenAI":
            client = OpenAI(api_key=api_key)
            model = llm_model if llm_model else "gpt-4o-mini"
        elif provider == "Groq":
            client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
            model = llm_model if llm_model else "qwen/qwen3.8-27b"
        elif provider == "Ollama":
            client = OpenAI(api_key="ollama", base_url="http://localhost:11434/v1")
            model = llm_model if llm_model else "llama3"
        elif provider == "Anthropic":
            return "Error: Use OpenRouter to access Anthropic models with the OpenAI SDK.", {}
        elif provider == "OpenRouter":
            client = OpenAI(api_key=api_key, base_url="https://openrouter.ai/api/v1")
            model = llm_model if llm_model else "anthropic/claude-3-haiku"
        elif provider == "Google Gemini":
            client = OpenAI(api_key=api_key, base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
            model = llm_model if llm_model else "gemini-1.5-flash"
        elif provider == "HuggingFace":
            client = OpenAI(api_key=api_key, base_url="https://api-inference.huggingface.co/v1/")
            model = llm_model if llm_model else "meta-llama/Meta-Llama-3-8B-Instruct"
        else:
            return f"Error: Provider {provider} not fully supported yet.", {}

        raw_response = client.chat.completions.with_raw_response.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            max_tokens=800,
            temperature=0.7,
        )
        
        parsed = raw_response.parse()
        text_result = parsed.choices[0].message.content.strip()
        headers = raw_response.headers
        
        usage_stats = {}
        
        if provider in ["OpenAI", "Groq"]:
            rem_req = headers.get("x-ratelimit-remaining-requests")
            rem_tok = headers.get("x-ratelimit-remaining-tokens")
            if rem_req: usage_stats["remaining_requests"] = rem_req
            if rem_tok: usage_stats["remaining_tokens"] = rem_tok
            usage_stats["type"] = "tokens"
            
        elif provider == "OpenRouter":
            usage_stats = fetch_openrouter_limits(api_key)
            
        elif provider == "HuggingFace":
            rem_req = headers.get("x-ratelimit-remaining")
            if rem_req: usage_stats["remaining_requests"] = rem_req
            usage_stats["type"] = "requests"
            
        elif provider == "Google Gemini":
            if parsed.usage:
                usage_stats["tokens_used_this_run"] = parsed.usage.total_tokens
            usage_stats["type"] = "run_usage"
            
        elif provider == "Ollama":
            usage_stats = {"type": "local", "status": "∞ Infinite"}

        return text_result, usage_stats
        
    except Exception as e:
        logging.error(f"Error generating LLM payload: {e}")
        return f"Error generating payload: {e}", {}


def generate_with_failover(llm_config: dict, context: str, system_prompt: str, db_update_callback=None) -> Tuple[str, dict]:
    """
    Attempts to generate a payload using the primary provider.
    If it fails 3 consecutive times and auto_failover is enabled,
    it automatically promotes the next verified provider and retries.
    Returns (payload_string, usage_stats_dict).
    """
    providers = llm_config.get("providers", [])
    primary_id = llm_config.get("primary")
    auto_failover = llm_config.get("auto_failover", False)

    if not providers:
        return "Error: No LLM providers configured.", {}

    # Find the primary provider
    primary = next((p for p in providers if p.get("id") == primary_id), None)
    if not primary:
        primary = providers[0]

    MAX_FAILURES = 3

    while primary:
        logging.info(f"Attempting payload generation using primary provider: {primary.get('name')}")
        result, usage = generate_payload(
            provider=primary.get("name"),
            api_key=primary.get("api_key"),
            llm_model=primary.get("model", ""),
            context=context,
            system_prompt=system_prompt
        )

        if not result.startswith("Error"):
            # Success! Reset failure count for this provider if needed
            if primary.get("failures", 0) > 0:
                primary["failures"] = 0
                if db_update_callback:
                    db_update_callback(llm_config)
            return result, usage
        
        # We hit an error
        logging.warning(f"Provider {primary.get('name')} failed: {result}")
        failures = primary.get("failures", 0) + 1
        primary["failures"] = failures

        if auto_failover and failures >= MAX_FAILURES:
            logging.error(f"Provider {primary.get('name')} exceeded max failures ({MAX_FAILURES}). Executing auto-failover.")
            
            # Find next verified provider that isn't the current one and hasn't exceeded max failures
            next_provider = None
            for p in providers:
                if p.get("id") != primary.get("id") and p.get("verified", False) and p.get("failures", 0) < MAX_FAILURES:
                    next_provider = p
                    break
            
            if next_provider:
                logging.info(f"Promoting {next_provider.get('name')} to Primary.")
                llm_config["primary"] = next_provider.get("id")
                primary = next_provider
                if db_update_callback:
                    db_update_callback(llm_config)
                # Loop will continue and try this new primary
                continue
            else:
                logging.error("Auto-failover failed: No other verified providers available.")
                if db_update_callback:
                    db_update_callback(llm_config)
                return f"Error: All verified LLM providers failed. Last error: {result}", {}
        
        # If no failover, or not reached threshold, just update DB and return the error
        if db_update_callback:
            db_update_callback(llm_config)
        return result, {}

    return "Error: Unexpected exit from failover loop.", {}
