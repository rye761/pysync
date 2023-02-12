# Pysync Syncs Lyrics and Produces an LRC file using spleeter, whisper, and text similarity.

## Usage

Pysync can be used using the command line. Setup the environment using conda and make sure that `whisper` and `spleeter` are installed. Then you can use this via the command line, providing an mp3 of the song and text file with lyrics you want to sync. The program will produce a .lrc file with timestamps which can be used by various lyric display programs.

`python pysync [-h] [--output_file OUTPUT_FILE] music lyrics`