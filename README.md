# RVC Project TTSC Component by LCC

## What is this for?
Uses [RVC-project](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI) apply AI-powered voice changers to speech. You may used your trained RVC models with this. 

## Setup

Please refer to the [their docs](https://github.com/RVC-Project/Retrieval-based-Voice-Conversion-WebUI/blob/main/docs/en/README.en.md) for the latest installation instructions for your os and hardware. Below is a modified version (for NVidia GPUs) specific for this project at the time of writing. It doesn't cover everything from their install guide. The main thing is to set this up in the right environment.

**This component has been tested with NVidia GPUs.** I can't ensure this will work with non-CUDA cards.

Please ensure you have [CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) (for NVidia GPUs) installed. You may also need to edit your path variables to ensure it's tools can be found.

If working in WSL, ensure you are using WSL2. You may need to additionally install the driver's in WSL as well.

The model needs to be in this projects `models` directory. Please put the folder generated under `logs` from the RVC-project associated with your model in here similar to how it was generated in the original RVC project. Also copy the associated weights from `assets/weights` from the RVC-project into the `assets/weights` in this project.

### Windows
1. Ensure you have CUDA setup properly
2. Create and activate the virtual environment. Find the command to install the correct pytorch packages for your system from [their website](https://pytorch.org/get-started/locally/).
```
conda create -n jaison-comp-ttsc-rvc-project python=3.10 cudatoolkit ffmpeg -c nvidia -y
conda activate jaison-comp-ttsc-rvc-project
# install command for pytorch like: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```
3. Download the required assets. **Ensure you have Git LFS enabled**.
```
python download_models.py
```

### Unix
1. Ensure you have CUDA setup properly
2. Create and activate the virtual environment. Make sure you are using Python 3.10 (dependencies won't work otherwise)
```
sudo apt install python3.10 python3.10-venv python3.10-dev # if you need python3.10
python3.10 -m venv venv
source venv/bin/activate
```
3. Install the remaining dependencies. Find the command to install the correct pytorch packages for your system from [their website](https://pytorch.org/get-started/locally/).
```
# install command for pytorch like: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
pip install -r requirements.txt
```
4. Download the required assets. **Ensure you have Git LFS enabled**.
```
python download_models.py
```

## Configuration
You need to edit `config.json` found in the root with information about your model. Namely, you need to change the `model_name`, the rest of the configuration should work for most systems.

## Customizing voice
Train AI voice conversion models using [RVC-PROJECT](https://github.com/limitcantcode/Retrieval-based-Voice-Conversion-WebUI). You can find a translation of their docs under the `/docs/` directory. 

Follow the instructions to setup the project, run the web UI, and train a model with you desired voice. **YOU WILL NEED TO BE ABLE TO RUN CUDA TO TRAIN A VOICE**.

It is recommended you have a GPU with at least 8GB of dedicated VRAM (not shared or combined with system RAM). If you encounter `CUDA out of memory` errors or something similar, try training smaller models. An RTX 3070 with 8GB or VRAM could only train a v1 model with pitch at 40k sample rate, using both rvmpe_gpu and rvmpe, on a batch size of 1 with no caching. You want to just train a model (be patient after clicking the button, it can take a couple minutes to kick in) and you may ignore training a feature index. If you still have trouble training due to memory, you can swap the pretrained base models from `f0X40k.pth` to just `X40k.pth` where X is either `D` or `G` accordingly.

## Testing
Assuming you are in the right virtual environment and are in the root directory:
```
python ./src/main.py --port=5000
```
If it runs, it should be fine.

## Related stuff
Project J.A.I.son: https://github.com/limitcantcode/jaison-core

Join the community Discord: https://discord.gg/Z8yyEzHsYM
