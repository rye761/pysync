import argparse
import separate
import sync
import os

def cli():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("music", type=str, help="Audio file containing complete track")
    parser.add_argument("lyrics", type=str, help="File containing song lyrics to be synced")
    parser.add_argument("--output_file", type=str, default=None, help="Output file name, defaults to name_of_mp3.lrc")

    args = parser.parse_args().__dict__

    filename = os.path.basename(args['music'])

    if args['output_file']:
        output_file = args['output_file']
    else:
        output_file = filename[0:filename.find('.')] + '.lrc'

    temp_file = separate.separated_vocals(args['music'])
    vocal_file_name = temp_file.name + '/' + filename[0:filename.find('.')] + '/vocals.wav'

    print(vocal_file_name)

    segments = sync.get_segments(vocal_file_name)

    file = open(args['lyrics'], 'r')
    full_lyrics = file.read()
    file.close()

    temp_file.cleanup()

    file = open(output_file, 'w')
    file.writelines(sync.sync_segments(full_lyrics, segments))
    file.close()

cli()