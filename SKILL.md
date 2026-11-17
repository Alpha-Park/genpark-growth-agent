---
name: genpark-growth-agent
description: Omnichannel marketing and SEO automation engine.
---
# genpark-growth-agent

An open-source GenPark alternative to anlah AI: CanMarket.

Give this agent your brand guidelines. It continuously monitors trending topics, drafts SEO-optimized blog posts, schedules tweets, and suggests ad copy adjustments—all orchestrated locally without a costly subscription.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.
