from spleeter.separator import Separator
import tempfile

def separated_vocals(filename):
    # Use spleeter to separate into files in a temporary directory, and return a reference to the directory
    separator = Separator('spleeter:2stems')
    temp_dir = tempfile.TemporaryDirectory()
    separator.separate_to_file(filename, temp_dir.name)
    return temp_dir