import requests
import sys

BLOCKCAIN_URL_DOMAIN = 'https://blockchain.info/'
LATEST_BLOCK_URL = BLOCKCAIN_URL_DOMAIN + 'latestblock'
BLOCK_HEIGHT_URL_FORMAT = BLOCKCAIN_URL_DOMAIN + 'block-height/{0}?format=json'
GENESIS_BLOCK_TS_SECONDS = 1231006505


def get_block_timestamp(height: int) -> int:
  response = requests.get(BLOCK_HEIGHT_URL_FORMAT.format(height)).json()
  return response['blocks'][0]['time']


def get_latest_block_height() -> int:
  response = requests.get(LATEST_BLOCK_URL).json()
  return int(response['height'])


def find_block_height(timestamp: int) -> int:
  """Finds the height of the block in the blockchain which has the biggest
  timestamp out of all the blocks whose timestamp is smaller then the input,
  if none exist returns  -1.
  Method uses binary search heuristic.
  """
  if timestamp < GENESIS_BLOCK_TS_SECONDS:
    return -1

  left = 0
  right = get_latest_block_height()

  while left <= right:
    middle = (left + right) // 2
    middle_timestamp = get_block_timestamp(middle)
    if middle_timestamp < timestamp:
      left = middle + 1
    else:
      middle -= 1
      right = middle

  return middle


if __name__ == '__main__':
  input_timestamp: int = int(sys.argv[1])
  block_height: int = find_block_height(input_timestamp)
  print(block_height)
