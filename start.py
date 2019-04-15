import argparse





parser = argparse.ArgumentParser()
parser.add_argument('-u', dest='url', help='URL of Target Website')
parser.add_argument('-c', dest='cookies', help='add cookies')

#save input args
results = parser.parse_args()