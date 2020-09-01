import secrets
from timeit import default_timer as timer

from src.ringCT import sign, verify
from src.utils import utils

def evaluate(args):
    # Define the used keys
    max_size = max(args.ringsizes)
    pair_keys = [utils.generateKeyPair() for i in range(max_size)]
    public_keys = [pair_keys[i][1] for i in range(len(pair_keys))]
    private_keys = [pair_keys[i][0] for i in range(len(pair_keys))]

    total_stimes = []
    total_vtimes = []
    for c in args.curves:
        used_keys = []
        stimes = []
        vtimes = []
        for rs in args.ringsizes:
            keys = public_keys[:rs]
            signer = secrets.randbelow(rs)

            # Eval signature time
            t0 = timer()
            keys, key_image, seed, randon_numbers = sign(keys, signer, private_keys[signer], args.message, c)
            sign_time = t0 - timer()
            stimes.append(sign_time)

            # Eval verify
            t0 = timer()
            verify(keys, key_image, seed, randon_numbers, used_keys, args.message, c)
            verify_time = t0 - timer()
            vtimes.append(verify_time)

        total_stimes.append(stimes)
        total_vtimes.append(vtimes)
    #for b in args.baselines:
        # OpenSSL is dead
        # Pyca proposes cryptography



