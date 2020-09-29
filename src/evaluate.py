# Standard library imports
import secrets
from timeit import default_timer as timer
import os

# Custom imports
from src.ringCT import sign, verify
from src.utils import utils
from src.plot import plot

# Third party library
from joblib import Parallel, delayed


def auxSign(index, parameters, signatures):
    """
    Auxiliary function to parallelize the generation of ring signatures.
    :param index: Index used to access signatures.
    :param parameters: Parameters of the ring signature.
    :param signatures: List of crafted signatures. Data structure used to store generated signatures.
    :return:
    """
    # Create and store signature
    signatures[index] = sign(parameters[0],  # List of public keys
                             parameters[1],  # Signer index
                             parameters[2],  # Signer's private key
                             parameters[3],  # Message to sign
                             parameters[4])  # Curve used
    return signatures


def auxVerify(index, parameters, signatures, used_keys):
    """
    Auxiliary function to parallelize the verification of ring signatures.
    :param index: Index used to access signatures.
    :param parameters: Parameters of the ring signature.
    :param signatures: List of signatures to verify. Data structure used to store generated signatures.
    :param used_keys: List of already used keys.
    :return: {True, False}
    """
    return verify(signatures[index][0],  # List of public keys
                  signatures[index][1],  # Key image
                  signatures[index][2],  # Seed
                  signatures[index][3],  # List of random numbers
                  used_keys,
                  parameters[3],  # Message
                  parameters[4])  # Curve used


def evaluate(args):
    """
    Evaluates the performance of ring signatures (sign and verify algorithms) under
    the different parameters provided in args.
    :param args: Object containing the parameters such as ring size, curves to evaluate
    :return:
    """

    total_stimes = []
    total_vtimes = []
    num_cpus = os.cpu_count()
    for c in args.curves:
        # Define the used keys
        max_size = max(args.ringsizes)
        pair_keys = [utils.generateKeyPair(c) for _ in range(max_size)]
        public_keys = [pair_keys[i][1] for i in range(len(pair_keys))]
        private_keys = [pair_keys[i][0] for i in range(len(pair_keys))]
        used_keys = []
        stimes = []
        vtimes = []
        for rs in args.ringsizes:
            keys = public_keys[:rs]
            signer = secrets.randbelow(rs)

            # Simulate signatures and verifications
            it = 64  # Number of signatures crafted/verified in parallel
            parameters = keys, signer, private_keys[signer], args.message, c
            signatures = [None for _ in range(it)]

            # Sign
            t0 = timer()
            signatures = Parallel(n_jobs=num_cpus)(delayed(auxSign)(i, parameters, signatures) for i in range(it))
            sign_time = timer() - t0
            stimes.append(sign_time / it)

            # Each parallel job returns a different list.
            # We get a matrix with elements in the diagonal.
            # We apply list comprehension to get a single non-empty list.
            signatures = [signatures[i][i] for i in range(it)]

            # Verify
            t0 = timer()
            Parallel(n_jobs=num_cpus)(delayed(auxVerify)(i, parameters, signatures, used_keys) for i in range(it))
            verify_time = timer() - t0
            vtimes.append(verify_time / it)

        total_stimes.append(stimes)
        total_vtimes.append(vtimes)
    # Plot signing times
    plot(args.ringsizes, 'Ring size', total_stimes, 'Time in seconds',
         args.curves, 'Time to craft a signature', 'graph', save_csv=True)
    # Plot verification times
    plot(args.ringsizes, 'Ring size', total_vtimes, 'Time in seconds',
         args.curves, 'Time to verify a signature', 'graph', save_csv=True)
