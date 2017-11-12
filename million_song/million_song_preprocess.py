from file_util import *
from midi_util import *



million_song_path = ""
quant = 2





if not os.path.exists(million_song_path+'_valid'):
	validate_data(million_song_path,quant)
if not os.path.exists(million_song_path+'_valid_quantized'):
	quantize_data(million_song_path+'_valid',quant)
if not os.path.exists(classical_raw_path+'_valid_quantized_inputs'):
	save_data(million_song_path+'_valid_quantized',quant)
