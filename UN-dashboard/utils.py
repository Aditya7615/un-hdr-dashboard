import json
import os
import re

LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "groq")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
PRIMARY_MODEL = os.environ.get("PRIMARY_LLM_MODEL", "llama-3.3-70b-versatile")
EVAL_MODEL = os.environ.get("EVAL_LLM_MODEL", "llama-3.1-8b-instant")


def is_mock_mode() -> bool:
    return os.environ.get("LLM_MOCK_MODE", "0") == "1"


def get_groq_client():
    from groq import Groq
    return Groq(api_key=GROQ_API_KEY)


def llm_complete(
    prompt: str,
    system_prompt: str = "",
    model: str = PRIMARY_MODEL,
    temperature: float = 0.1,
    max_tokens: int = 4096,
    json_mode: bool = False,
) -> str:
    if is_mock_mode() or not GROQ_API_KEY:
        return _mock_llm_response(prompt)

    client = get_groq_client()
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = dict(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    resp = client.chat.completions.create(**kwargs)
    return resp.choices[0].message.content


def extract_json_from_llm(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}


def _mock_llm_response(prompt: str) -> str:
    if "bullet" in prompt.lower() or "key findings" in prompt.lower():
        return json.dumps({
            "key_findings": [
                "Social capital is critical for community resilience in Serbia",
                "The 2014 floods exposed severe DRR system deficiencies",
                "Serbia faces increasing frequency of natural disasters",
                "Local communities lack capacity for adequate disaster response",
                "Resilience measurement requires multi-capital approach",
                "Trust and volunteerism are key social capital manifestations",
                "Gender and social inclusion remain challenges in DRR",
            ],
            "chapter_summaries": {
                "Executive Summary": "This report examines social capital's role in community resilience to natural disasters in Serbia, focusing on the 2014 floods.",
                "Introduction": "Serbia is increasingly exposed to natural hazards, with floods and earthquakes being most significant threats.",
                "Chapter 1": "Resilience and social capital concepts are explored, linking them to disaster risk reduction and human development.",
                "Chapter 2": "Global and national DRR policy frameworks are analyzed, including the Sendai Framework and SDGs.",
            },
        })
    elif "json" in prompt.lower() and ("key_strengths" in prompt.lower() or "themes" in prompt.lower()):
        return json.dumps({
            "key_strengths": [
                "Strong volunteerism culture in disaster response",
                "Established DRR legal framework",
                "Community-level cooperation during crises",
                "Growing awareness of resilience importance",
            ],
            "key_challenges": [
                "Insufficient DRR financial resources",
                "Weak local capacity for risk planning",
                "Limited inter-municipal coordination",
                "Aging infrastructure vulnerability",
            ],
            "core_numerical_indicators": {
                "HDI value": 0.776,
                "HDI rank": 67,
                "Life expectancy": 75.6,
                "Expected years of schooling": 14.6,
                "Mean years of schooling": 11.2,
                "GNI per capita": 13500,
                "Population": 7058000,
            },
        })
    return json.dumps({"mock": "response"})


def clean_pdf_text(text: str) -> str:
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        line = line.strip()
        if re.match(r'^\d+$', line):
            continue
        if line in ("SOCIAL CAPITAL:", "THE INVISIBLE FACE OF RESILIENCE", "PART 1", "PART 2"):
            continue
        if line.startswith("ANNEX") and len(line) < 30:
            continue
        cleaned.append(line)
    return "\n".join(cleaned)


def normalize_indicator(values: list) -> list:
    if not values:
        return []
    min_v, max_v = min(values), max(values)
    if max_v == min_v:
        return [0.5] * len(values)
    return [(v - min_v) / (max_v - min_v) for v in values]


def reorient_negative(values: list) -> list:
    return [1.0 - v for v in values]


OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "data", "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)
