from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools import tool
import requests
import time

CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

@tool
def solve_any_captcha(
    website_url: str,
    website_key: str,
    captcha_type: str = "ReCaptchaV2TaskProxyLess"
) -> str:
    """Universal CAPTCHA solver supporting multiple types."""
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": captcha_type,
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }

    response = requests.post("https://api.capsolver.com/createTask", json=payload)
    result = response.json()

    if result.get("errorId") != 0:
        return f"Error: {result.get('errorDescription')}"

    task_id = result.get("taskId")

    for _ in range(60):
        time.sleep(2)
        result = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id}
        ).json()

        if result.get("status") == "ready":
            solution = result.get("solution", {})
            return solution.get("gRecaptchaResponse") or solution.get("token")
        if result.get("status") == "failed":
            return f"Failed: {result.get('errorDescription')}"

    return "Timeout"

# CAPTCHA Specialist Agent
captcha_agent = Agent(
    name="CAPTCHA Specialist",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_any_captcha],
    description="Expert at identifying and solving various CAPTCHA types",
    instructions=[
        "Identify the CAPTCHA type from page analysis",
        "Use appropriate solver with correct parameters",
        "Report success or failure clearly"
    ]
)

# Data Extraction Agent
data_agent = Agent(
    name="Data Extractor",
    model=OpenAIChat(id="gpt-4o"),
    description="Extracts and processes data from web pages",
    instructions=[
        "Extract structured data from HTML content",
        "Request CAPTCHA solving when needed",
        "Validate and clean extracted data"
    ]
)

# Create the team
scraping_team = Team(
    name="Web Scraping Team",
    agents=[captcha_agent, data_agent],
    description="Team specialized in web scraping with CAPTCHA handling"
)

if __name__ == "__main__":
    # Example usage
    print("Multi-Agent Team initialized. Ready to handle complex scraping tasks.")
