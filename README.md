# bLUSD Price Bot

## Requirements

1. Discord API Key - [Discord Developer Portal](https://discord.com/developers/applications/)

2. Etherscan API Key - [Etherscan API](https://etherscan.io/apis)

3. Alchemy API Key - [Alchemy API](https://www.alchemy.com/)

## Initial Setup

1. Create a `.env` file and insert your API keys.

```
DISCORD_API_KEY=
ETHERSCAN_API_KEY=
ALCHEMY_API_KEY=
```

2. Run `main.py`.


## Configuration

The bot updates the price every 60 seconds by default. To change this, modify the interval
```
@tasks.loop(seconds=60)
```
You can use the properties `seconds`, `minutes` and `hours`.