# Agno + CapSolver: Autonomous Multi-Agent CAPTCHA Solving 🚀

[![GitHub stars](https://img.shields.io/github/stars/capsolver/agno-capsolver-integration?style=social)](https://github.com/capsolver/agno-capsolver-integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Agno](https://img.shields.io/badge/Framework-Agno-orange)](https://github.com/agno-agi/agno)

Integrate **CapSolver** with **Agno** to build high-performance, privacy-first autonomous agents that can seamlessly bypass CAPTCHA challenges.

---

## 🌟 Overview

As AI-driven automation becomes more practical in real-world workflows, **Agno** has emerged as a fast and privacy-first framework for building autonomous multi-agent systems. However, CAPTCHAs often block these agents during web scraping or data collection.

**CapSolver** solves this by allowing Agno agents to reliably handle CAPTCHA-protected pages without breaking the automation flow. Together, they enable scalable, hands-off automation for real-world websites.

### Key Benefits
- **Uninterrupted Workflows**: Agents solve challenges autonomously.
- **Privacy-First**: Maintain control over your data with Agno's self-hosted nature.
- **High Performance**: Agno is up to 529x faster than traditional agent frameworks.
- **Multi-CAPTCHA Support**: Handle reCAPTCHA (v2/v3), Cloudflare Turnstile, AWS WAF, and more.

---

## 🛠️ Installation

```bash
pip install agno requests selenium aiohttp
```

---

## 🚀 Quick Start

### 1. Basic CAPTCHA Solver Tool

Define a custom tool for your Agno agent to use CapSolver:

```python
import requests
from agno.tools import tool

CAPSOLVER_API_KEY = "YOUR_CAPSOLVER_API_KEY"

@tool
def solve_recaptcha_v2(website_url: str, website_key: str) -> str:
    """Solves reCAPTCHA v2 challenges using CapSolver."""
    payload = {
        "clientKey": CAPSOLVER_API_KEY,
        "task": {
            "type": "ReCaptchaV2TaskProxyLess",
            "websiteURL": website_url,
            "websiteKey": website_key
        }
    }
    # ... (see main.py for full implementation)
```

### 2. Create an Autonomous Agent

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    name="Web Scraper",
    model=OpenAIChat(id="gpt-4o"),
    tools=[solve_recaptcha_v2],
    instructions=["When encountering a CAPTCHA, use the solve_recaptcha_v2 tool."],
    markdown=True
)

agent.run("Solve the CAPTCHA at https://example.com/demo")
```

---

## 📂 Project Structure

```text
agno-capsolver-integration/
├── examples/
│   ├── multi_agent_team.py    # Specialized agent teams
│   └── token_submission.py    # Selenium/Requests injection
├── main.py                    # Core implementation & demo
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

---

## 💡 Best Practices

1. **Error Handling**: Implement exponential backoff for polling results.
2. **Balance Management**: Use the `check_capsolver_balance` tool to monitor credits.
3. **Async Support**: Use `aiohttp` for non-blocking CAPTCHA solving in high-concurrency environments.

---

## 🔗 Useful Links

- [CapSolver Dashboard](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=agno)
- [Agno Documentation](https://github.com/agno-agi/agno)
- [CapSolver API Docs](https://docs.capsolver.com/)

---

## 🎁 Special Offer

Ready to get started? [Sign up for CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=repo&utm_campaign=agno) and use bonus code **AGNO** for an extra **6% bonus** on your first recharge!

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

<p align="center">
  Built with ❤️ by the CapSolver Community
</p>
