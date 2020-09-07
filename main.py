# Standard library imports
import argparse

# Custom library imports
from src.evaluate import evaluate


def parseArgs():
    """
    Parses received arguments using argparse.
    :return:
    """
    parser = argparse.ArgumentParser('Test and evaluate Ring Confidential Transactions')
    parser.add_argument('-rs', '--ringsizes', required=True, nargs='*', type=int, help="Define the size of the ring.")
    parser.add_argument('-c', '--curves', required=False, nargs='*', help="Elliptic curve to employ.")
    parser.add_argument('-m', '--message', required=False, help="Message to sign.")
    parser.add_argument('-o', '--output', required=False, help="Destination file to save the output graphics.")
    return parser.parse_args()


"""
    Reads and parses the arguments.
    Calls the evaluation function.    
"""
if __name__ == '__main__':
    args = parseArgs()
    curves = ['secp192r1']
    message = 'I voted for Kodos'
    output = 'comparative'
    if args.curves is None:
        args.curves = curves
    if args.message is None:
        args.message = message
    if args.output is None:
        args.output = output
    evaluate(args)
