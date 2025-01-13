import argparse
import os
import sys

now_dir = os.getcwd()
sys.path.append(now_dir)
from dotenv import load_dotenv
from scipy.io import wavfile

from configs.config import Config
from infer.modules.vc.modules import VC

load_dotenv()

class TTSCModel():
    def __init__(
        self,
        f0up_key,
        index_path,
        f0method,
        model_name,
        index_rate,
        device,
        is_half,
        filter_radius,
        rms_mix_rate,
        protect
    ):
        self.f0up_key = f0up_key
        self.index_path = index_path
        self.f0method = f0method
        self.model_name = model_name
        self.index_rate = index_rate
        self.device = device
        self.is_half = is_half
        self.filter_radius = filter_radius
        self.resample_sr = 48000
        self.rms_mix_rate = rms_mix_rate
        self.protect = protect

        self.config = Config()
        self.config.device = self.device if self.device else self.config.device
        self.config.is_half = self.is_half if self.is_half else self.config.is_half
        self.vc = VC(self.config)
        self.vc.get_vc(self.model_name)

    def __call__(self, input_filepath: str):
        _, wav_opt = self.vc.vc_single(
            0,
            input_filepath,
            self.f0up_key,
            None,
            self.f0method,
            self.index_path,
            None,
            self.index_rate,
            self.filter_radius,
            self.resample_sr,
            self.rms_mix_rate,
            self.protect,
        )
        return wav_opt[1]
