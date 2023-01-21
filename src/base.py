CHARMAP = bytes(range(1, 256))
ASCII = b'\x00' + CHARMAP


def encode(number: int, symbols: str, /) -> str:

    base = len(symbols)
    
    if base > number:
        return symbols[number]
    
    else:
        return encode(number // base, symbols) + symbols[number % base]

def decode(number: str, symbols: str, /) -> int:

    if 1 == len(number):
        return symbols.index(number)
    
    else:
        return decode(number[:-1], symbols) * len(symbols) + symbols.index(number[-1])


def encode_void(number: int, symbols: bytes, /) -> bytes:

    base = len(symbols)
    
    if base > number:
        return symbols[number - 1: number]
    
    else:
        div, mod = divmod(number - 1, base)
        return symbols[mod:mod + 1] + encode_void(div, symbols)

def decode_void(number: bytes, symbols: bytes, /) -> int:
    
    if b'' == number:
        return 0
   
    else:
        return 1 + symbols.index(number[0]) + decode_void(number[1:], symbols) * len(symbols)

