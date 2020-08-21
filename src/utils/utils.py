# Standard library imports
import secrets
# Third library imports
import hashlib
from tinyec import ec
from tinyec import registry as reg
from nummaster.basic import sqrtmod

# Custom imports

def generatePrivateKey(curve_name='secp192r1'):
    """
    Generates an ECC private key in the specified curve.
    :param curve_name: Name of the elliptic curve employed.
    :return: Private EC key.
    """
    curve = reg.get_curve(curve_name)
    privKey = secrets.randbelow(curve.field.n)
    return privKey

def generatePublicKey(curve_name='secp192r1'):
    """
    Generates an ECC public key in the specified curve.
    :param curve_name: Name of the elliptic curve employed.
    :return: A public EC key (EC Point)
    """
    curve = reg.get_curve(curve_name)
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    return pubKey

def generateKeyPair(curve_name='secp192r1'):
    """
    Generates an ECC private and public key in the specified curve.
    :param curve_name: Name of the elliptic curve employed.
    :return: A tuple of private and public EC keys
    """
    curve = reg.get_curve(curve_name)
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    return privKey, pubKey

def compressPoint(point, curve_name='secp192r1'):
    """
    Takes a EC point/public key in the form (x,y) and returns a compressed point in the form (x, even/odd)
    :param Point point: Point object (tinyec library) of the form (x,y).
    :param curve_name: Name of the elliptic curve employed.
    :return: EC Point
    """
    return ec.Point(curve_name, point.x, point.y % 2)

def decompressPoint(point, curve_name='secp192r1'):
    """
    Takes a compressed point of the form  (x, even/odd)
    :param point: Compressed point in the form (x, even/odd)
    :param curve_name: Name of the elliptic curve employed.
    :return: EC Point
    """
    curve = reg.get_curve(curve_name)
    p = curve.field.p
    y = sqrtmod(pow(point.x, 3, p) + curve.a * point.x + curve.b, p)
    if point.y:
        return ec.Point(curve_name, point.x, y)
    else:
        return ec.Point(curve_name, point.x, p - y)

def toStandardFormat(point, curve_name='secp192r1'):
    """
    Takes a public key and returns it in the standard format: compressed, hexed and prefixed with 02 or 03.
    :param point: Point of an elliptic curve.
    :param curve_name: Name of the elliptic curve employed.
    :return: Standard hex representation of EC point.
    """
    return '0' + str(2 + point.y % 2) + str(toHex(compressPoint(point, curve_name), True))

def toHex(input, remove=False):
    """
    Transforms an input to hexadecimal.
    :param input: Any input that can be transformed to hexadecimal.
    :param remove: Boolean to remove "0x" from the output
    :return: An hexadecimal number.
    """
    if remove:
        return hex(input)[2:]
    else:
        return hex(input)

def fromHexToInt(input):
    """
    Transforms hexadecimal to decimal.
    :param input: An hexadecimal number.
    :return: An integer in base 10.
    """
    return int(input, base=16)

def hashToScalar(input, curve_name='secp192r1'):
    """
    Given an input, returns an element in the field defined by the curve.
    :param input: Any hashable input.
    :param curve_name: Name of the elliptic curve employed.
    :return: A number in the finite field defined by the curve.
    """
    curve = reg.get_curve(curve_name)
    p = curve.field.p
    return fromHexToInt(hashlib.sha3_256(input).hexdigest()) % p

def hashToPoint(input, curve_name='secp192r1'):
    """
    A hash function that returns a point of the curve
    :param input: A point of an elliptic curve.
    :param curve_name: Name of the elliptic curve employed.
    :return: A point on the curve.
    """
    curve = reg.get_curve(curve_name)
    scalar = hashToScalar(input, curve_name)
    return scalar * curve.g
