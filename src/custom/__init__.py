from dotenv import load_dotenv
load_dotenv()

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
import wave
from datetime import datetime
import numpy as np
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

from jaison_grpc.common import STTComponentRequest, T2TComponentRequest, TTSGComponentRequest, TTSCComponentRequest
async def request_unpacker(request_iterator):
    async for request_o in request_iterator:
        match request_o:
            case STTComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case T2TComponentRequest():
                yield request_o.system_input, request_o.user_input
            case TTSGComponentRequest():
                yield request_o.content
            case TTSCComponentRequest():
                yield request_o.audio, request_o.sample_rate, request_o.sample_width, request_o.channels
            case _:
                raise Exception(f"Unknown request type: {type(request_o)}")

def process_audio(audio_bytes, sample_rate, sample_width, channels):
    if sample_width == 1:
        audio_array = np.frombuffer(audio_bytes, dtype=np.int8)
    elif sample_width == 2:
        audio_array = np.frombuffer(audio_bytes, dtype=np.int16)

    if channels == 2:
        audio_array = (audio_array.reshape([int(audio_array.shape[0]/2), 2])/2).sum(1)

    audio_array = np.interp(np.arange(0, len(audio_array), float(sample_rate)/16000), np.arange(0, len(audio_array)), audio_array)
    audio_array = audio_array.flatten().astype(np.float32)

    if sample_width == 1:
        audio_array = audio_array / 64
    elif sample_width == 2:
        audio_array = audio_array / 32768
    audio_b, sr = ttsc_model(audio=audio_array)

    return audio_b, sr, sample_width, channels

# For voice changers
async def start_ttsc(request_iterator):
    
    global ttsc_model
    audio_buffer = b''
    sample_rate, sample_width, channels = 48000, 2, 1
    async for chunk_audio, chunk_sample_rate, chunk_sample_width, chunk_channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        audio_buffer += chunk_audio
        sample_rate, sample_width, channels = chunk_sample_rate, chunk_sample_width, chunk_channels
        # if len(audio_buffer) > 0.25 * sample_rate * sample_width * channels:
        #     yield process_audio(audio_buffer, sample_rate, sample_width, channels)
        #     audio_buffer = b''
        
    if len(audio_buffer) > 0:
        yield process_audio(audio_buffer, sample_rate, sample_width, channels)

# For speech-to-text models
async def start_stt(request_iterator) -> str:
    for audio, sample_rate, sample_width, channels in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For text generation models
async def start_t2t(request_iterator) -> str:
    for system_input, user_input in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError

# For text-to-speech generation
async def start_ttsg(request_iterator) -> str:
    for text in request_unpacker(request_iterator): # receiving chunks of info through a stream
        raise NotImplementedError
