# Standard library imports
import secrets
from timeit import default_timer as timer

# Custom imports
from src.ringCT import sign, verify
from src.utils import utils
from src.plot import plot


def evaluate(args):
    """
    Evaluates the performance of ring signatures (sign and verify algorithms) under
    the different parameters provided in args.
    :param args: Object containing the parameters such as ring size, curves to evaluate
    :return:
    """

    total_stimes = []
    total_vtimes = []
    for c in args.curves:
        # Define the used keys
        max_size = max(args.ringsizes)
        pair_keys = [utils.generateKeyPair(c) for i in range(max_size)]
        public_keys = [pair_keys[i][1] for i in range(len(pair_keys))]
        private_keys = [pair_keys[i][0] for i in range(len(pair_keys))]
        used_keys = []
        stimes = []
        vtimes = []
        for rs in args.ringsizes:
            keys = public_keys[:rs]
            signer = secrets.randbelow(rs)

            # Eval signature time
            t0 = timer()
            keys, key_image, seed, randon_numbers = sign(keys, signer, private_keys[signer], args.message, c)
            sign_time = timer() - t0
            stimes.append(sign_time)

            # Eval verify
            t0 = timer()
            verify(keys, key_image, seed, randon_numbers, used_keys, args.message, c)
            verify_time = timer() - t0
            vtimes.append(verify_time)

        total_stimes.append(stimes)
        total_vtimes.append(vtimes)
    # Plot signing times
    plot(args.ringsizes, 'Ring size', total_stimes, 'Time in seconds',
         args.curves, 'Time to craft a signature', 'graph', save_csv=True)
    # Plot verification times
    plot(args.ringsizes, 'Ring size', total_vtimes, 'Time in seconds',
         args.curves, 'Time to verify a signature', 'graph', save_csv=True)
