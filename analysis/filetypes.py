from enum import Enum

TAB = "\t"
SPACE = " "
COMMA = ","
NEW_LINE = "\n"


class FileType(Enum):
    TEXT_FILE = 1
    LINES_FILE = 2
    QTFTM_FILE = 3
    CSV_FILE = 4

    def title(self):
        return str.replace(self.name, "_", " ").title()


class FileFormat(Enum):
    FTB_FIXED_SHOTS = 1
    FTB_ESTIMATED_SHOTS = 2
    FREQUENCY_ONLY = 3
    DELIMITER = 4

    def title(self):
        return str.replace(self.name, "_", " ").title()


class ExportType:
    def __init__(self, ext, formats):
        ## type: (string, Enum#) -> object
        self.extension = ext  # (string) Extension of the type
        self.formats = formats  # (FileFormat[]) List of valid formats


# Dictionary of Valid Export File Types
# FileType ::-> ExportType
EXPORT_FILE_TYPES = {FileType.TEXT_FILE: ExportType(".txt", [FileFormat.FREQUENCY_ONLY, FileFormat.DELIMITER]),
                     FileType.LINES_FILE: ExportType(".lines", [FileFormat.FREQUENCY_ONLY, FileFormat.DELIMITER]),
                     FileType.QTFTM_FILE: ExportType(".ftb",
                                                     [FileFormat.FTB_ESTIMATED_SHOTS, FileFormat.FTB_FIXED_SHOTS]),
                     FileType.CSV_FILE: ExportType(".csv",
                                                   [FileFormat.FREQUENCY_ONLY, FileFormat.DELIMITER])}
