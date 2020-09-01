import argparse

def parseArgs():
    parser = argparse.ArgumentParser('Test and evaluate Ring Confidential Transactions')
    parser.add_argument('-rs', '--ringsizes', required=True, nargs='*', help="Define the size of the ring.")
    parser.add_argument('-c', '--curves', required=False, nargs='*', help="Elliptic curve to employ.")
    parser.add_argument('-m', '--message', required=False, help="Message to sign.")
    parser.add_argument('-b', '--baselines', required=False, nargs='*', default='',
                        help="List of OpenSSL functions to use as baseline.")
    parser.add_argument('-o', '--output', required=False, help="Destination file to save the output graphics.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArgs()
    curves = ['secp192r1']
    message = 'I voted for Kodos'
    baselines = ['DES']
    output = 'comparative'
    if args.curve is None:
        args.curves = curves
    if args.message is None:
        args.message = message
    if args.baseline is None:
        args.baselines = baselines
    if args.output is None:
        args.output = output
    evaluate(args)

