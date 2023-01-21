
def encode(numbers: list[int], /) -> int:
    
    length = len(numbers)

    number = 0
    bit = 0
    
    while any(numbers):

        for i in range(length):

            number |= (1 & numbers[i]) << bit
            numbers[i] >>= 1
            bit += 1

    return number

def decode(number: int, length: int, /) -> list[int]:

    array = [0] * length
    bit = 0
    
    while number:

        for i in range(length):
            
            array[i] |= (1 & number) << bit
            number >>= 1
        
        bit += 1
    
    return array

