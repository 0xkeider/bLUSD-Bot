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

DISCORD_TOKEN     = os.getenv('DISCORD_API_KEY')
ALCHEMY_API_KEY   = os.getenv('ALCHEMY_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')

bLUSD_CONTRACT_ADDRESS       = '0xB9D7DdDca9a4AC480991865EfEf82E01273F79C3'
CHICKENBOND_CONTRACT_ADDRESS = '0x57619FE9C539f890b19c61812226F9703ce37137'

CURVE_API_URL     = 'https://api.curve.fi/api/getPools/ethereum/factory-crypto'
ALCHEMY_API_URL   = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"
ETHERSCAN_API_URL = f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress={bLUSD_CONTRACT_ADDRESS}&apikey={ETHERSCAN_API_KEY}"

web3 = Web3(Web3.HTTPProvider(ALCHEMY_API_URL))

abi = [{"inputs":[{"components":[{"internalType":"address","name":"bondNFTAddress","type":"address"},{"internalType":"address","name":"lusdTokenAddress","type":"address"},{"internalType":"address","name":"curvePoolAddress","type":"address"},{"internalType":"address","name":"curveBasePoolAddress","type":"address"},{"internalType":"address","name":"bammSPVaultAddress","type":"address"},{"internalType":"address","name":"yearnCurveVaultAddress","type":"address"},{"internalType":"address","name":"yearnRegistryAddress","type":"address"},{"internalType":"address","name":"yearnGovernanceAddress","type":"address"},{"internalType":"address","name":"bLUSDTokenAddress","type":"address"},{"internalType":"address","name":"curveLiquidityGaugeAddress","type":"address"}],"internalType":"struct ChickenBondManager.ExternalAdresses","name":"_externalContractAddresses","type":"tuple"},{"components":[{"internalType":"uint256","name":"targetAverageAgeSeconds","type":"uint256"},{"internalType":"uint256","name":"initialAccrualParameter","type":"uint256"},{"internalType":"uint256","name":"minimumAccrualParameter","type":"uint256"},{"internalType":"uint256","name":"accrualAdjustmentRate","type":"uint256"},{"internalType":"uint256","name":"accrualAdjustmentPeriodSeconds","type":"uint256"},{"internalType":"uint256","name":"chickenInAMMFee","type":"uint256"},{"internalType":"uint256","name":"curveDepositDydxThreshold","type":"uint256"},{"internalType":"uint256","name":"curveWithdrawalDxdyThreshold","type":"uint256"},{"internalType":"uint256","name":"bootstrapPeriodChickenIn","type":"uint256"},{"internalType":"uint256","name":"bootstrapPeriodRedeem","type":"uint256"},{"internalType":"uint256","name":"bootstrapPeriodShift","type":"uint256"},{"internalType":"uint256","name":"shifterDelay","type":"uint256"},{"internalType":"uint256","name":"shifterWindow","type":"uint256"},{"internalType":"uint256","name":"minBLUSDSupply","type":"uint256"},{"internalType":"uint256","name":"minBondAmount","type":"uint256"},{"internalType":"uint256","name":"nftRandomnessDivisor","type":"uint256"},{"internalType":"uint256","name":"redemptionFeeBeta","type":"uint256"},{"internalType":"uint256","name":"redemptionFeeMinuteDecayFactor","type":"uint256"}],"internalType":"struct ChickenBondManager.Params","name":"_params","type":"tuple"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"accrualParameter","type":"uint256"}],"name":"AccrualParameterUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"redeemer","type":"address"},{"indexed":False,"internalType":"uint256","name":"bLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"minLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"lusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"yTokens","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"redemptionFee","type":"uint256"}],"name":"BLUSDRedeemed","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_baseRedemptionRate","type":"uint256"}],"name":"BaseRedemptionRateUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"bonder","type":"address"},{"indexed":False,"internalType":"uint256","name":"bondId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"principalLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"minLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"withdrawnLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint80","name":"bondFinalHalfDna","type":"uint80"}],"name":"BondCancelled","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"bonder","type":"address"},{"indexed":False,"internalType":"uint256","name":"bondId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"lusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"bLusdAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"lusdSurplus","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"chickenInFeeAmount","type":"uint256"},{"indexed":False,"internalType":"bool","name":"migration","type":"bool"},{"indexed":False,"internalType":"uint80","name":"bondFinalHalfDna","type":"uint80"}],"name":"BondClaimed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"bonder","type":"address"},{"indexed":False,"internalType":"uint256","name":"bondId","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"amount","type":"uint256"},{"indexed":False,"internalType":"uint80","name":"bondInitialHalfDna","type":"uint80"}],"name":"BondCreated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"_lastRedemptionFeeOpTime","type":"uint256"}],"name":"LastRedemptionTimeUpdated","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint256","name":"previousPermanentLUSD","type":"uint256"}],"name":"MigrationTriggered","type":"event"},{"inputs":[],"name":"BETA","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BOOTSTRAP_PERIOD_CHICKEN_IN","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BOOTSTRAP_PERIOD_REDEEM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"BOOTSTRAP_PERIOD_SHIFT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"CHICKEN_IN_AMM_FEE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"DECIMAL_PRECISION","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"INDEX_OF_LUSD_TOKEN_IN_CURVE_POOL","outputs":[{"internalType":"int128","name":"","type":"int128"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MINUTE_DECAY_FACTOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_BLUSD_SUPPLY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"MIN_BOND_AMOUNT","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"NFT_RANDOMNESS_DIVISOR","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SECONDS_IN_ONE_MINUTE","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SHIFTER_DELAY","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"SHIFTER_WINDOW","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bammLUSDValue","type":"uint256"}],"name":"_calcSystemBackingRatioFromBAMMValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"accrualAdjustmentMultiplier","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"accrualAdjustmentPeriodCount","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"accrualAdjustmentPeriodSeconds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"accrualParameter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"activateMigration","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"bLUSDToken","outputs":[{"internalType":"contract IBLUSDToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bammSPVault","outputs":[{"internalType":"contract IBAMM","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"baseRedemptionRate","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"bondNFT","outputs":[{"internalType":"contract IBondNFT","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"}],"name":"calcAccruedBLUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"}],"name":"calcBondBLUSDCap","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_fractionOfBLUSDToRedeem","type":"uint256"}],"name":"calcRedemptionFeePercentage","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"calcSystemBackingRatio","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"calcTotalLUSDValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"calcTotalYearnCurveVaultShareValue","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"calcUpdatedAccrualParameter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"}],"name":"chickenIn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"},{"internalType":"uint256","name":"_minLUSD","type":"uint256"}],"name":"chickenOut","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"countChickenIn","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"countChickenOut","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_lusdAmount","type":"uint256"}],"name":"createBond","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"createBondWithPermit","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"curveBasePool","outputs":[{"internalType":"contract ICurvePool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"curveDepositLUSD3CRVExchangeRateThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"curveLiquidityGauge","outputs":[{"internalType":"contract ICurveLiquidityGaugeV5","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"curvePool","outputs":[{"internalType":"contract ICurvePool","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"curveWithdrawal3CRVLUSDExchangeRateThreshold","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"deploymentTimestamp","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"firstChickenInTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAcquiredLUSDInCurve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getAcquiredLUSDInSP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getBAMMLUSDDebt","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"}],"name":"getBondData","outputs":[{"internalType":"uint256","name":"lusdAmount","type":"uint256"},{"internalType":"uint64","name":"claimedBLUSD","type":"uint64"},{"internalType":"uint64","name":"startTime","type":"uint64"},{"internalType":"uint64","name":"endTime","type":"uint64"},{"internalType":"uint8","name":"status","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getLUSDInBAMMSPVault","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bondID","type":"uint256"}],"name":"getLUSDToAcquire","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOpenBondCount","outputs":[{"internalType":"uint256","name":"openBondCount","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwnedLUSDInCurve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getOwnedLUSDInSP","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPendingLUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getPermanentLUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalAcquiredLUSD","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTotalLUSDInCurve","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getTreasury","outputs":[{"internalType":"uint256","name":"_pendingLUSD","type":"uint256"},{"internalType":"uint256","name":"_totalAcquiredLUSD","type":"uint256"},{"internalType":"uint256","name":"_permanentLUSD","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastRedemptionTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lastShifterCountdownStartTime","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"lusdToken","outputs":[{"internalType":"contract ILUSDToken","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"migration","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"minimumAccrualParameter","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"_bLUSDToRedeem","type":"uint256"},{"internalType":"uint256","name":"_minLUSDFromBAMMSPVault","type":"uint256"}],"name":"redeem","outputs":[{"internalType":"uint256","name":"","type":"uint256"},{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_lusdAmount","type":"uint256"}],"name":"sendFeeShare","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxLUSDToShift","type":"uint256"}],"name":"shiftLUSDFromCurveToSP","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_maxLUSDToShift","type":"uint256"}],"name":"shiftLUSDFromSPToCurve","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"startShifterCountdown","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"targetAverageAgeSeconds","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalWeightedStartTimes","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"yTokensHeldByCBM","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"yearnCurveVault","outputs":[{"internalType":"contract IYearnVault","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"yearnGovernanceAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"yearnRegistry","outputs":[{"internalType":"contract IYearnRegistry","name":"","type":"address"}],"stateMutability":"view","type":"function"}]

contract = web3.eth.contract(address=CHICKENBOND_CONTRACT_ADDRESS, abi=abi)

# Logging Config
logging.basicConfig(
    level=logging.INFO,
    format='{asctime} [{levelname:<8}] {message}',
    datefmt="%d %b %Y %H:%M:%S %z",
    style='{',
    filemode='w'
)

def call_API(api_name, API_URL):
    try:
        logging.info(f"Requesting {api_name} API...")
        response = requests.get(
            API_URL,
            timeout=5
        )
        logging.info('Request Complete.')
        return response.json()
    except requests.exceptions.RequestException as e:
        # If there is any exception raised while making the request, log the error and return None
        logging.error(f"Error while requesting {api_name} API: {e}")
        return None

def get_usd_price(curve_data, pool_id, token):
    pool_data = curve_data['data']['poolData'][pool_id]
    for coins in pool_data['underlyingCoins']:
        coin_data = coins
        if coin_data['symbol'] == token:
            usdPrice = coin_data['usdPrice']
            return usdPrice

def get_reserve_bucket():
    try:
        logging.info(f"Requesting Alchemy API...")
        reserveBucketRaw = contract.functions.getTotalAcquiredLUSD().call()
        reserveBucket = Web3.fromWei(int(reserveBucketRaw), 'ether')
        logging.info('Request Complete.')
        return reserveBucket
    except ValueError:
        # Handle errors when the value passed to Web3.fromWei is not a valid integer
        logging.error("Error converting value to integer")
        return None
    except Exception as e:
        # Catch any other exceptions and log the error
        logging.error("Web3 call failed: {}".format(e))
        return None

def main():

    # Broadcast version number
    logging.info('Script Built on 30/12/2022')

    # Connect to Discord
    client = discord.Client(intents=discord.Intents.default())
    @client.event
    async def on_ready():
        if not loop.is_running():
            loop.start()
        logging.info('Logged in as {0.user}'.format(client))
        logging.info(f"Connected to Web3: {web3.isConnected()}")

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

            reserveBucketSupply = get_reserve_bucket()

            logging.info(f"LUSD = ${round(LUSD_usdPrice, 4)} | bLUSD = ${round(bLUSD_usdPrice, 4)} = {round(bLUSD_LUSDPrice, 4)} LUSD")
            logging.info(f"Reserve bucket: {millify(reserveBucketSupply, precision=2)} LUSD | Circulating supply: {millify(bLUSD_supply, precision=2)}")

            floorPrice = reserveBucketSupply/bLUSD_supply

            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{round(floorPrice, 3)} LUSD Floor 🚀"))

            # Update nickname in every connected guild
            total_guilds = 0
            for guild in client.guilds:
                nickname = f"{round(bLUSD_LUSDPrice, 4)} LUSD"
                await client.get_guild(guild.id).me.edit(nick=nickname)
                total_guilds += 1
            logging.info(f"Updating activity, watching {total_guilds} guild(s)")
            
        except TypeError as e:
            # Handle errors when a variable is None or has the wrong type
            logging.error("TypeError occurred: {}".format(e))
        except KeyError as e:
            # Handle errors when a dictionary key is not found
            logging.error("KeyError occurred: {}".format(e))
        except ZeroDivisionError as e:
            # Handle errors when division by zero occurs
            logging.error("ZeroDivisionError occurred: {}".format(e))
        except Exception as e:
            # Catch any other exceptions and log the error
            logging.error("Error occurred: {}".format(e))

    client.run(DISCORD_TOKEN)

if __name__ == "__main__":
    main()