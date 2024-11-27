import binary
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from io import BufferedIOBase


def remove_comment(line: str):
    return line.split("#")[0].strip()


@dataclass
class MailTableData:
    message_id: str
    flags: list[int]
    file_name: str

    def write(self, stream: BufferedIOBase):
        binary.write_u64(stream, int.from_bytes(self.message_id.encode()))

        # write flags
        stream.write(bytes(self.flags))
        # add 1 byte of padding
        binary.write_u8(stream, 0)

        stream.write(self.file_name.encode())
        binary.write_zero_padding(stream, 4)

    @classmethod
    def from_file(cls, stream: BufferedIOBase) -> "MailTableData":
        data = cls("", list(), "")

        data.message_id = binary.read_u64(stream).to_bytes(64).decode().lstrip("\x00")

        # total of 3 byte flags
        for _ in range(3):
            data.flags.append(binary.read_u8(stream))

        # skip 1 byte
        binary.read_u8(stream)

        filename_bytes = list[int]()
        current_byte = binary.read_u8(stream)
        while current_byte != 0:
            filename_bytes.append(current_byte)
            current_byte = binary.read_u8(stream)

        data.file_name = bytes(filename_bytes).decode()

        binary.skip_padding(stream, 4)  # skip 4 bytes of padding

        return data

    def __str__(self) -> str:
        return (
            "{\n"
            f"\t{self.message_id} # Message ID\n"
            f"\t{self.flags} # Flags\n"
            f"\t{self.file_name} # Filename\n"
            "}"
        )


@dataclass
class MailTable:
    entry_count: int
    data: list[MailTableData]

    def write_to_text(self, path: str | Path):
        filepath = Path(path)
        with open(filepath, "w") as f:
            f.write(str(self))

    def write_to_bin(self, path: str | Path):
        filepath = Path(path)
        with open(filepath, "wb") as f:
            entry_count = len(self.data)
            binary.write_u32(f, entry_count)
            for i in range(entry_count):
                self.data[i].write(f)

    @classmethod
    def from_bin(cls, path: str | Path) -> "MailTable":
        filepath = Path(path)

        table = cls(0, list())

        with open(filepath, "rb") as f:
            table.entry_count = binary.read_u32(f)
            for _ in range(table.entry_count):
                table.data.append(MailTableData.from_file(f))

        return table

    @classmethod
    def from_text(cls, path: str | Path) -> "MailTable":
        filepath = Path(path)

        table = cls(0, list())
        with open(filepath, "r") as f:
            line = f.readline()
            while line:
                if line.strip() == "{":
                    message_id = remove_comment(f.readline())
                    print(message_id)

                    flags = remove_comment(f.readline())
                    flags = [int(x) for x in flags.strip("[]").split(",")]

                    filename = remove_comment(f.readline())

                    data = MailTableData(message_id, flags, filename)
                    table.data.append(data)

                    line = f.readline()
                    continue

                line = f.readline()

        return table

    def __str__(self) -> str:
        data = "\n".join([str(data) for data in self.data])
        return "# Mail Table converter by PishPish\n\n" f"{data}"


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", type=str, required=True)
    parser.add_argument("-o", "--output", type=str, required=True)
    parser.add_argument("--converttext", action="store_true")
    parser.add_argument("--convertbin", action="store_true")

    args = parser.parse_args()

    if args.converttext:
        table = MailTable.from_bin(args.input)
        table.write_to_text(args.output)
    elif args.convertbin:
        table = MailTable.from_text(args.input)
        table.write_to_bin(args.output)
