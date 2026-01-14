import requests
import time
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools import tool

# Replace with your actual CapSolver API Key
CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

@tool
def solve_recaptcha_v2(website_url: str, website_key: str) -> str:
    """
    Solves reCAPTCHA v2 challenges using CapSolver.

    Args:
        website_url: The URL of the website with reCAPTCHA v2
        website_key: The site key (data-sitekey attribute)

    Returns:
        The g-recaptcha-response token
    """
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }

    response = requests.post("https://api.capsolver.com/createTask", json=payload)
    result = response.json()

    if result.get("errorId") != 0:
        return f"Error: {result.get('errorDescription')}"

    task_id = result.get("taskId")

    # Poll for result
    for attempt in range(60):
        time.sleep(2)
        result = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": CAPSOLVER_API_KEY, "taskId": task_id}
        ).json()

        if result.get("status") == "ready":
            return result["solution"]["gRecaptchaResponse"]
        if result.get("status") == "failed":
            return f"Failed: {result.get('errorDescription')}"

    return "Timeout waiting for solution"

@tool
def solve_turnstile(website_url: str, website_key: str) -> str:
    """
    Solves Cloudflare Turnstile challenges.

    Args:
        website_url: The URL of the website with Turnstile
        website_key: The site key of the Turnstile widget

    Returns:
        The Turnstile token
    """
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "AntiTurnstileTaskProxyLess",
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
            return result["solution"]["token"]
        if result.get("status") == "failed":
            return f"Failed: {result.get('errorDescription')}"

    return "Timeout"

@tool
def check_capsolver_balance() -> str:
    """
    Checks the current CapSolver account balance.

    Returns:
        Current balance information
    """
    response = requests.post(
        "https://api.capsolver.com/getBalance",
        json={"clientKey": CAPSOLVER_API_KEY}
    )
    result = response.json()

    if result.get("errorId") != 0:
        return f"Error: {result.get('errorDescription')}"

    return f"Balance: ${result.get('balance', 0):.4f}"

# Create the Web Scraper Agent
web_scraper_agent = Agent(
    name="Web Scraper Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_recaptcha_v2, solve_turnstile, check_capsolver_balance],
    description="Expert web scraper that handles CAPTCHA challenges automatically",
    instructions=[
        "You are a web scraping specialist with CAPTCHA solving capabilities.",
        "When encountering a CAPTCHA, identify the type and use the appropriate solver.",
        "For reCAPTCHA v2, use solve_recaptcha_v2 with the URL and site key.",
        "For Turnstile, use solve_turnstile with the URL and site key.",
        "Always check the balance before starting large scraping jobs."
    ],
    markdown=True
)

def main():
    print("=" * 60)
    print("Agno + CapSolver Integration Demo")
    print("=" * 60)

    # Task: Solve a reCAPTCHA challenge
    task = """
    I need you to solve a reCAPTCHA v2 challenge.

    Website URL: https://www.google.com/recaptcha/api2/demo
    Site Key: 6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-

    Please solve this CAPTCHA and report the first 50 characters of the token.
    Also check my CapSolver balance before starting.
    """

    response = web_scraper_agent.run(task)
    print("\nAgent Response:")
    print(response.content)

if __name__ == "__main__":
    main()
