'''
Supported component type entrypoints

- Implement the specific entrypoint associated with your component type
- You can leave the others unimplemented

To support streaming, your implementation should be a generator: https://wiki.python.org/moin/Generators
You may also simply return the final result
'''

import logging
import json
import os
from scipy.io import wavfile
from datetime import datetime
from .model import TTSCModel
with open(os.path.join(os.getcwd(),"config.json")) as f:
    model_config = json.load(f)
ttsc_model = TTSCModel(
    model_config['f0up_key'],
    model_config['index_path'],
    model_config['f0method'],
    model_config['model_name'],
    model_config['index_rate'],
    model_config['device'],
    model_config['is_half'],
    model_config['filter_radius'],
    model_config['rms_mix_rate'],
    model_config['protect']
)

# For speech-to-text models
def start_stt(audio: bytes) -> str:
    raise NotImplementedError

# For text generation models
def start_t2t(system_prompt: str, user_input: str) -> str:
    raise NotImplementedError

# For text-to-speech generation
def start_ttsg(text: str) -> bytes:
    raise NotImplementedError

# For voice changers
def start_ttsc(audio: bytes) -> bytes:
    global ttsc_model
    working_file_path = os.path.join(os.getcwd(),os.getenv("working_dir"),f"{int(datetime.now().timestamp()*1000)}.wav")
    wavfile.write(working_file_path, 48000, audio)
    audio = ttsc_model(working_file_path)
    try:
        os.remove(working_file_path)
    except Exception as err:
        logging.error(f"Failed to remove working file: {working_file_path}")
        logging.error(err)
    return audio
