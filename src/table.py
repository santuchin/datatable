import typing
import os

from . import codecs, base, rows

class table:

    def __init__(self, path: str, /, **columns: typing.Dict[str, codecs.codec]) -> None:

        if os.path.exists(path):

            file = open(path, 'rb')
            raw = file.read()
            file.close()

            if b'' == raw:
                self.__data = []
            
            else:

                self.__data = raw.split(b'\x00')

                if 1 == len(self.__data):

                    self.__data[0] = base.encode_void(
                        base.decode_void(self.__data[0], base.CHARMAP) - 1,
                        base.CHARMAP
                    )

        else:
            self.__data = []

        for key in columns:
            
            if columns[key] in codecs.defaults:
                columns[key] = codecs.defaults[columns[key]]

        self.path = path
        self.columns = columns
        self.length = len(columns)

    def __len__(self, /) -> int:
        return len(self.__data)

    def __iter__(self, /) -> typing.Generator[tuple[typing.Any, ...], None, None]:

        for index in range(len(self.__data)):
            yield self.__decode(self.__data[index])


    def __encode(self, row: tuple, /) -> bytes:

        return base.encode_void(rows.encode(list(map(
                lambda codec, obj: codec.encode(obj),
                self.columns.values(), row)
                )),
            base.CHARMAP
        )

    def __decode(self, row: bytes, /) -> tuple[typing.Any]:

        return tuple(map(
            lambda codec, obj: codec.decode(obj),
            self.columns.values(),
            rows.decode(base.decode_void(row, base.CHARMAP), self.length)
        ))

    def save(self, /) -> None:
        
        file = open(self.path, 'wb')

        if 1 == len(self.__data):

            file.write(base.encode_void(
                base.decode_void(self.__data[0], base.CHARMAP) + 1,
                base.CHARMAP
            ))

        else:
            file.write(b'\x00'.join(self.__data))
                
        file.close()
    
    def where(self, /, **keys: typing.Dict[str, typing.Any]) -> typing.Generator[int, None, None]:

        columns = tuple(self.columns.keys())

        for index in range(len(self.__data)):

            row = rows.decode(base.decode_void(self.__data[index], base.CHARMAP), self.length)

            for key in keys:

                if self.columns[key].decode(row[columns.index(key)]) != keys[key]:
                    break

            else:
                yield index

    def add(self, /, **row: typing.Dict[str, typing.Any]) -> None:
        self.__data.append(self.__encode((row[column] for column in self.columns)))

    def get(self, index: int, /) -> tuple:
        return self.__decode(self.__data[index])

    def set(self, index: int, /, **keys: typing.Dict[str, typing.Any]) -> None:

        columns = tuple(self.columns.keys())

        row = rows.decode(base.decode_void(self.__data[index], base.CHARMAP), len(columns))

        for key, value in keys.items():
            row[columns.index(key)] = self.columns[key].encode(value)

        self.__data[index] = base.encode_void(rows.encode(row), base.CHARMAP)

    def insert(self, index: int, /, **row: typing.Dict[str, typing.Any]) -> None:
        self.__data.insert(index, self.__encode((row[column] for column in self.columns)))

    def pop(self, index: int, /) -> None:
        self.__data.pop(index)
