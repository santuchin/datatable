import os

from . import codecs, base

class value:

    def __init__(self, path: str, codec: codecs.codec=None, /) -> None:

        if codec in codecs.defaults:
            self.codec = codecs.defaults[codec]

        else:
            self.codec = codec

        if os.path.exists(path):

            file = open(path, 'rb')
            self.obj = self.codec.decode(base.decode_void(file.read(), base.ASCII))
            file.close()

        else:
            self.obj = self.codec.decode(0)

        self.path = path

    def save(self, /) -> None:

        file = open(self.path, 'wb')
        file.write(base.encode_void(self.codec.encode(self.obj), base.ASCII))
        file.close()
