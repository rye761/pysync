# Pysync Syncs Lyrics and Produces an LRC file using spleeter, whisper, and text similarity.

## Usage

Pysync can be used using the command line. Setup the environment using conda and make sure that `whisper` and `spleeter` are installed. Then you can use this via the command line, providing an mp3 of the song and text file with lyrics you want to sync. The program will produce a .lrc file with timestamps which can be used by various lyric display programs.

`python pysync` - This will start the app in GUI Mode. When doing multiple jobs, it's also faster as it won't have to load each library again and again

`python pysync [-h] [--output_file OUTPUT_FILE] music lyrics` - it will just do it's job using the console. No GUI here. Libs are loaded for each job.

## Installation

Install [Anaconda3](https://www.anaconda.com/download) and open the Anaconda Prompt.

1. Move to your Projects directory. (You can switch drive letters by just entering e.g. `F:` and hitting enter for the drive letter F.)
2. Create an environment: `conda create --name lyrics python=3.7.16`
3. Activate the environment: `conda activate lyrics`
4. Install `whisper` and `spleeter`: `pip install spleeter openai-whisper pyqt5 pykakasi`
5. Download [ffmpeg](https://ffmpeg.org/download.html) and put the ffmpeg.exe into your project directory within Anaconda (Seems like having it in PATH doesn't work on windows...)

Now you're good to go, just execute it from within Anaconda Prompt. Every time you close the Anaconda Prompt you should repeat step 1 and 3 before executing the script.

## Make GPU compatible

If you're not really lucky the code will most likely not use your GPU but your GPU instead. That can be quite slow. Getting the GPU to work was also quite a hassle. I've got a NVidia RTX 4090 so it had to be possible and after some hours it worked. If you've got a AMD GPU and don't know what you're doing, you're out of luck. Sorry. If you got a NVidia GPU that doesn't support CUDA 11.3 you can try using a lower version and hope it's still compatible. In that case you have to replace **cudatoolkit=11.3**, **torch==1.12.1+cu113** and **--extra-index-url https://download.pytorch.org/whl/cu113** with the other version where e.g. **CUDA 10.2** is **cu102**.

The following dependencies may differ from the needs of your other projects, so they will only be installed in the Anaconda Environment.

- First you've got to install the CUDA Toolkit, Never Toolkits are definitely not compatible so be sure to use 11.3 or lower:`conda install -c anaconda cudatoolkit=11.3`
- You'll also need Cudnn, so here it is: `conda install -c anaconda cudnn`
- To be able to check your installed version you can use `nvidia-smi` or install `conda install -c nvidia cuda-nvcc` and execute `nvcc --version`. I recommend using the second way. If the returned version differs to the the one selected and installed there may be an error that happend, but in my case it was just because I've installed a later version on my computer globally. So it may still work nontheless.
- Lastly you need the correct torch version so the longest process will also use your GPU anything later that 1.12.1 does not support CUDA 11.3 so it's out of question. Anything lower that 1.12.0 is not supported by **whisper** so it's out of question too. I recommend using the following version: `pip install torch==1.12.1+cu113 torchaudio torchvision --extra-index-url https://download.pytorch.org/whl/cu113`

`
# Credits

- Core Version from [Rye761](https://github.com/rye761/pysync)
- Extended Version by [DragonSkills99](https://github.com/DragonSkills99/pysync)