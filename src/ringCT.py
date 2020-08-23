# Standard library imports
import secrets

# Third library imports
from tinyec import registry as reg

# Custom imports
from src.utils import utils


def sign(keys, signer_index, signer_private, message='I voted for Kodos', curve_name='secp192r1'):
    """

    :param keys:
    :param signer_index:
    :param signer_private:
    :param message:
    :param curve_name:
    :return:
    """
    # Curve parameters
    curve = reg.get_curve(curve_name)
    prime_field = curve.field.p

    # Ring signature parameters
    n_keys = len(keys)
    random_numbers = [secrets.randbelow(prime_field) for i in range(n_keys)]
    alpha = secrets.randbelow(prime_field)
    L = [0] * n_keys
    R = [0] * n_keys
    c = [0] * n_keys

    # Compute first element of the ring
    key_image = signer_private * utils.hashToPoint(keys[signer_index])
    L[signer_index] = alpha * curve.g
    R[signer_index] = alpha * utils.hashToPoint(keys[signer_index])
    c[(signer_index + 1) % n_keys] = utils.hashToScalar(str((message, L[signer_index], R[signer_index])), curve_name)

    # Iterate for the rest of elements
    i = (signer_index + 1) % n_keys
    while i != signer_index:
        L[i] = random_numbers[i] * curve.g + c[i] * keys[i]
        R[i] = random_numbers[i] * utils.hashToPoint(keys[i]) + c[i] * key_image
        c[(i + 1) % n_keys] = utils.hashToScalar(str((message, L[i], R[i])), curve_name)
        i = (i + 1) % n_keys

    # Close the ring
    random_numbers[signer_index] = alpha - c[signer_index] * signer_private

    return keys, key_image, c[0], random_numbers


def verify(keys, key_image, seed, random_numbers, used_keys=None, message='I voted for Kodos', curve_name='secp192r1'):
    """

    :param keys:
    :param key_image:
    :param seed:
    :param random_numbers:
    :param used_keys:
    :param message:
    :param curve_name:
    :return:
    """
    # If the key_image was already used the signature is not valid
    if key_image in used_keys:
        return False
    # Curve parameters
    curve = reg.get_curve(curve_name)

    # Ring signature parameters
    n_keys = len(keys)
    L = [0] * n_keys
    R = [0] * n_keys
    c = [0] * n_keys
    c[0] = seed  # Introduce seed

    # Compute first element of the signature
    L[0] = random_numbers[0] * curve.g + c[0] * keys[0]
    R[0] = random_numbers[0] * utils.hashToPoint(keys[0]) + c[0] * key_image
    c[1] = utils.hashToScalar(str((message, L[0], R[0])), curve_name)

    # Compute the rest of the ring elements
    i = 1
    while i < n_keys:
        L[i] = random_numbers[i] * curve.g + c[i] * keys[i]
        R[i] = random_numbers[i] * utils.hashToPoint(keys[i]) + c[i] * key_image
        c[((i + 1) % n_keys)] = utils.hashToScalar(str((message, L[i], R[i])), curve_name)
        i = i + 1

    # Compute final element
    return seed == c[0]