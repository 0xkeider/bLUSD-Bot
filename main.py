import os
import json
import logging

from dotenv import load_dotenv
import requests
import discord
from discord.ext import commands, tasks
from web3 import Web3
from millify import millify

load_dotenv()

ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
DISCORD_TOKEN     = os.getenv('DISCORD_API_KEY')

bLUSD_CONTRACT_ADDRESS = '0xB9D7DdDca9a4AC480991865EfEf82E01273F79C3'

CURVE_API_URL     = 'https://api.curve.fi/api/getPools/ethereum/factory-crypto'
ETHERSCAN_API_URL = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={bLUSD_CONTRACT_ADDRESS}&apikey={ETHERSCAN_API_KEY}"

# Logging Config
logging.basicConfig(
    level=logging.INFO,
    format='{asctime} [{levelname:<8}] {message}',
    datefmt="%d %b %Y %H:%M:%S %z",
    style='{',
    filemode='w'
)

def call_API(api_name, API_URL):
    logging.info(f"Requesting {api_name} API...")
    response = requests.get(
        API_URL,
        timeout=5
    )
    logging.info('Request Complete')
    return response.json()

def get_usd_price(curve_data, pool_id, token):
    pool_data = curve_data['data']['poolData'][pool_id]
    for coins in pool_data['underlyingCoins']:
        coin_data = coins
        if coin_data['symbol'] == token:
            usdPrice = coin_data['usdPrice']
            return usdPrice

def main():

    # Broadcast version number
    logging.info('Script Built on 22/10/2022')

    # Connect to Discord
    client = discord.Client(intents=discord.Intents.default())
    @client.event
    async def on_ready():
        if not loop.is_running():
            loop.start()
        logging.info('Logged in as {0.user}'.format(client))

    # Update activity every minute
    @tasks.loop(seconds=60)
    async def loop():
        try:
            curve_json = call_API('Curve', CURVE_API_URL)
            LUSD_usdPrice = get_usd_price(curve_json, 134, 'LUSD')
            bLUSD_usdPrice = get_usd_price(curve_json, 134, 'bLUSD')
            bLUSD_LUSDPrice = bLUSD_usdPrice/LUSD_usdPrice

            etherscan_json = call_API('Etherscan', ETHERSCAN_API_URL)
            bLUSD_supply = Web3.fromWei(int(etherscan_json['result']), 'ether')

            logging.info(f"Current prices: LUSD = ${round(LUSD_usdPrice, 4)}, bLUSD = ${round(bLUSD_usdPrice, 4)} | {millify(bLUSD_supply)} bLUSD circulating")

            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{millify(bLUSD_supply)} circulating"))

            # Update nickname in every connected guild
            total_guilds = 0
            for guild in client.guilds:
                nickname = f"{round(bLUSD_LUSDPrice, 4)} LUSD"
                await client.get_guild(guild.id).me.edit(nick=nickname)
                total_guilds += 1
            logging.info(f"Updating activity, watching {total_guilds} guild(s)")
        except:
            logging.error("Error occurred, loop not executed")

    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()