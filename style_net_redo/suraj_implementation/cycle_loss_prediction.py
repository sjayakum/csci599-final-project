import numpy as np
from model import GenreLSTM
import mido
import midi_util
from mido import MidiFile
import tensorflow as tf

from file_util import *
from midi_util import *
from model import *


dirs = {
            'main_path': '/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/data_for_model',
            'current_run': 8,
            'model_path':'/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation'
        }
network  = GenreLSTM(dirs, input_size=176, mini=True, bi=True)
network.prepare_model()
network.load("a", path="/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/0/model/model-e14.ckpt")



jazz_input = "/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/data_for_model/test/inputs/jazz/It'sAlmostLikeBeingInLove.mid.npy"

jazz_velocities = "/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/data_for_model/test/velocities/jazz/It'sAlmostLikeBeingInLove.mid.npy"

c_error, c_out, j_out, e_out, out_list = network.predict(jazz_input, jazz_velocities)

mid = MidiFile("/Users/sjayakum/Desktop/cycle_style_net/It'sAlmostLikeBeingInLove.mid")#SOURCE SONG
classical = midi_util.stylify(mid, c_out[-1], 2) #model output
classical.save("/Users/sjayakum/Desktop/cycle_style_net/generated/classical_It'sAlmostLikeBeingInLove.mid")#style transfered song
save_data('/Users/sjayakum/Desktop/cycle_style_net/generated/',2)


classical_input = "/Users/sjayakum/Desktop/cycle_style_net/generated_inputs/classical_It'sAlmostLikeBeingInLove.mid.npy"

classical_velocities = "/Users/sjayakum/Desktop/cycle_style_net/generated_velocities/classical_It'sAlmostLikeBeingInLove.mid.npy"

c_error, c_out, j_out, e_out, out_list = network.predict(classical_input, classical_velocities)

mid = MidiFile("/Users/sjayakum/Desktop/cycle_style_net/generated/classical_It'sAlmostLikeBeingInLove.mid")#SOURCE SONG
jazz_regen = midi_util.stylify(mid, j_out[-1], 2) #model output
jazz_regen.save("/Users/sjayakum/Desktop/cycle_style_net/re-generated/jazz_It'sAlmostLikeBeingInLove.mid")#style transfered song
save_data('/Users/sjayakum/Desktop/cycle_style_net/regenerated/',2)
