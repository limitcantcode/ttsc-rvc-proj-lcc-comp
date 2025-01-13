# RVC Project TTSC Component by LCC

## What is this for?
Uses [RVC-project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) apply AI-powered voice changers to speech. You may used your trained RVC models with this. 

## Setup

Please refer to the [their docs](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/en/README.en.md) for the latest installation instructions for your os and hardware. Below is a modified verion (for NVidia GPUs) specific for this project at the time of writing. It doesn't cover everything from their install guide. The main thing is to set this up in the right environment.

**This component has been tested with NVidia GPUs.** I can't ensure this will work with non-CUDA cards.

Please ensure you have [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (for NVidia GPUs) installed. You may also need to edit your path variables to ensure it's tools can be found.

If working in WSL, ensure you are using WSL2. You may need to additionally install the driver's in WSL as well.

The model needs to be in this projects `models` directory. Please put the folder generated under `logs` from the RVC-project associated with your model in here. Also copy the associated weights from `assets/weights` from the RVC-project into the `assets/weights` in this project.

### Windows
1. Ensure you have CUDA setup properly
2. Create and activate the virtual environment. Replace the `pytorch-cuda` version with the latest version before the version stated on your CUDA (found using command `nvidia-smi`). For example, I'm using `CUDA 12.6`, but the latest `pytorch-cuda` is for `CUDA 12.4`, so use `pytorch-cuda==12.4`
```
conda create -n jaison-comp-ttsc-rvc-project python=3.10 pytorch-cuda=12.4 pytorch cudatoolkit -c pytorch -c nvidia -y
conda activate jaison-comp-ttsc-rvc-project
pip install -r requirements.txt
```
3. Download the required assets. **Ensure you have Git LFS enabled**.
```
python download_models.py
```
4. Install `ffmpeg` if you haven't already. You can simply download these files and put it in this project's root:

- [ffmpeg](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffmpeg.exe)
- [ffprobe](https://huggingface.co/lj1995/VoiceConversionWebUI/blob/main/ffprobe.exe)

### Unix
1. Ensure you have CUDA setup properly
2. Create and activate the virtual environment. Make sure you are using Python 3.10 (No guaruntee this will work for later versions)
```
python -m venv venv
source venv/bin/activate
```
3. Install the remaining dependencies. Find the command to install the correct pytorch packages for your system from [their website](https://pytorch.org/get-started/locally/).
```
pip install ...(stuff for pytorch)
pip install -r requirements.txt
```

## Configuration
You need to edit `config.json` found in the root with information about your model. Namely, you need to change the `model_name`, the rest of the configuration should work for most systems.

## Testing
Assuming you are in the right virtual environment and are in the root directory:
```
python ./src/main.py --port=5000
```
If it runs, it should be fine.

## Related stuff
Project J.A.I.son: https://github.com/limitcantcode/jaison-core
Join the community Discord: https://discord.gg/Z8yyEzHsYM
