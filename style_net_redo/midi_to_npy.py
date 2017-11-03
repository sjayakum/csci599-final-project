
#first lets extract only piano from the midi


#FIRST LETS VALIDATE MIDI FILES
#WE ARE GOING TO KEEP ONLY THOSE FILES THAT ARE VALID AND SKIP THE REMAINING AUDIO FILES

import os
import logging
import numpy as np

from mido import MidiFile
from midi_util import *


def step1_quantize_data(path, quant):

    total_midi_files =0
    processed_midi_files =0

    output_path = None

    for root,dir,files in os.walk(path):
        for each_file in files:
            #check if its midi
            if each_file.split('.')[-1] == 'mid' or each_file.split('.')[-1] == 'MID':
                total_midi_files+=1
                logging.info("Processing - ",each_file)
                absolute_path = os.path.join(root,each_file)
                try:
                    midi_file= MidiFile(absolute_path)
                except:
                    logging.info("BAD MIDI FILE - ",each_file)

                mid = quantize(MidiFile(os.path.join(root, each_file)), quant)
                if not mid:
                    logging.info("Unable to quantize ",each_file)
                    continue

                midi_file.save(os.path.join(output_path, each_file))
                processed_midi_files +=1


def step2_get_velocities(path,quant):

    #NOTE THIS PATH IS AFTER YOU WHAT YOU SAVE IN STEP-1 PATH


    array_outs = None #some path
    veloctiy_outs = None #some path

    for root,dirs,files in os.walk(path):

        for each_file in files:
            if each_file.split('.')[-1] == 'mid' or each_file.split('.')[-1] == 'MID':
                mid = MidiFile(os.path.join(root, each_file))
                array, velocity_array = midi_to_array_one_hot(mid, quant)
                np.save(array_outs+each_file.split('.')[-1]+'.npy', array)
                np.save(veloctiy_outs+each_file.split('.')[-1]+'.npy', velocity_array)



