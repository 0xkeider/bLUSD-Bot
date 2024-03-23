# bLUSD Price Bot

A Discord sidebar bot to display real-time market data for bLUSD.

## Requirements

1. Discord API Key - [Discord Developer Portal](https://discord.com/developers/applications/)

2. Etherscan API Key - [Etherscan API](https://etherscan.io/apis)

3. Alchemy API Key - [Alchemy API](https://www.alchemy.com/)

## Installation

1. Install dependencies:

```python
pip install -r requirements.txt
```

2. Create a `.env` file in the root folder and paste your API keys:

```bash
DISCORD_API_KEY=
ETHERSCAN_API_KEY=
ALCHEMY_API_KEY=
```

3. Run `main.py`.

## Configuration

The bot updates the price every 60 seconds by default. To change this, modify the interval
```python
@tasks.loop(seconds=60)
```
You can use the properties `seconds`, `minutes` and `hours`.