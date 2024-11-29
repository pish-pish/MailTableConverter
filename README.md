# Pikmin 2 Mail Table Converter by PishPish

A tool to convert mail_table.bin from binary to an editable text format and back to binary.

*Requires Python 3.12+*

### Usage:
1. Locate mail_table.bin (in `user/Koono/mail_table.szs/mail_table.bin`)
2. Drag and drop `mail_table.bin` onto `convert2txt.bat`
3. Edit the outputted `.ini` file
4. Drag and drop the `.ini` file onto `convert2bin.bat`
5. Replace mail_table.bin back into the archive.

## MAIL TABLE INFORMATION
__Message ID__: Corresponding BMG message ID for the mail entry.
__Filename__: Corresponding mail icon filename for the mail entry.

__Flags__:
- Flag 0 is Mail Category,
```
MailCategories:
PokoUnder3000  = 49,
PokoUnder5000  = 50,
PokoUnder8000  = 51,
PokoUnder10000 = 52,
PayDebt        = 53,
SavedLouie     = 54,
AllTreasures   = 55
```

- Flag 1 is Mail ID,

- Flag 2 Sound Type (Character Mail Jingle Sound),
```
SoundTypes:
SHACHO   = 0,
WIFE     = 1,
SON      = 2,
DAUGHTER = 3,
GRANDMA  = 4,
PRESWIFE = 5,
SPAM     = 255
```
