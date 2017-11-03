from file_util import *
from midi_util import *
# from main import *
from model import *


classical_raw_path = "/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/raw_data/classical"
jazz_raw_path = "/Users/sjayakum/Desktop/csci599/StyleNet/surajs_implementation/raw_data/jazz"
quant = 2





if not os.path.exists(classical_raw_path+'_valid'):
	validate_data(classical_raw_path,quant)
if not os.path.exists(jazz_raw_path+'_valid'):
	validate_data(jazz_raw_path,quant)
if not os.path.exists(classical_raw_path+'_valid_quantized'):
	quantize_data(classical_raw_path+'_valid',quant)
if not os.path.exists(jazz_raw_path+'_valid_quantized'):
	quantize_data(jazz_raw_path+'_valid',quant)

if not os.path.exists(classical_raw_path+'_valid_quantized_inputs'):
	save_data(classical_raw_path+'_valid_quantized',quant)
if not os.path.exists(jazz_raw_path+'_valid_quantized_inputs'):
	save_data(jazz_raw_path+'_valid_quantized',quant)







data_for_model = "./data_for_model"
if not os.path.exists(data_for_model):
        os.makedirs(data_for_model)


jazz_file_names = []
classical_file_names = []

for i, filename in enumerate(os.listdir(classical_raw_path+'_valid_quantized_inputs')):
    classical_file_names.append(filename)

for i, filename in enumerate(os.listdir(jazz_raw_path+'_valid_quantized_inputs')):
    jazz_file_names.append(filename) 

import random

random.shuffle(classical_file_names)
random.shuffle(jazz_file_names)

train_count,valid_count = int(0.7*len(classical_file_names)),int(0.15*len(classical_file_names))

train_classical_filenames = classical_file_names[:train_count]
valid_classical_filenames = classical_file_names[train_count:train_count+valid_count]
test_classical_filenames = classical_file_names[train_count+valid_count:]



train_count,valid_count = int(0.7*len(jazz_file_names)),int(0.15*len(jazz_file_names))

train_jazz_filenames = jazz_file_names[:train_count]
valid_jazz_filenames = jazz_file_names[train_count:train_count+valid_count]
test_jazz_filenames = jazz_file_names[train_count+valid_count:]

from shutil import copyfile

if not os.path.exists(data_for_model+'/inputs'):
    os.makedirs(data_for_model+'/inputs')
    os.makedirs(data_for_model+'/inputs/classical')
    os.makedirs(data_for_model+'/inputs/jazz')

    for each_file in train_classical_filenames:
        copyfile(classical_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/inputs/classical/'+each_file)
    for each_file in train_jazz_filenames:
        copyfile(jazz_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/inputs/jazz/'+each_file)

if not os.path.exists(data_for_model+'/velocities'):
    os.makedirs(data_for_model+'/velocities')
    os.makedirs(data_for_model+'/velocities/classical')
    os.makedirs(data_for_model+'/velocities/jazz')

    for each_file in train_classical_filenames:
		copyfile(classical_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/velocities/classical/'+each_file)
    for each_file in train_jazz_filenames:
        copyfile(jazz_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/velocities/jazz/'+each_file)

        
if not os.path.exists(data_for_model+'/test'):
    os.makedirs(data_for_model+'/test')
    os.makedirs(data_for_model+'/test/inputs/classical')
    os.makedirs(data_for_model+'/test/inputs/jazz')
    os.makedirs(data_for_model+'/test/velocities/classical')
    os.makedirs(data_for_model+'/test/velocities/jazz')

    for each_file in test_classical_filenames:
    	copyfile(classical_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/test/inputs/classical/'+each_file)
        copyfile(classical_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/test/velocities/classical/'+each_file)

    for each_file in test_jazz_filenames:
        copyfile(jazz_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/test/inputs/jazz/'+each_file)
        copyfile(jazz_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/test/velocities/jazz/'+each_file)
 
        
if not os.path.exists(data_for_model+'/eval'):
    os.makedirs(data_for_model+'/eval')
    os.makedirs(data_for_model+'/eval/inputs/classical')
    os.makedirs(data_for_model+'/eval/inputs/jazz')
    os.makedirs(data_for_model+'/eval/velocities/classical')
    os.makedirs(data_for_model+'/eval/velocities/jazz')

    for each_file in valid_classical_filenames:
        copyfile(classical_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/eval/inputs/classical/'+each_file)
        copyfile(classical_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/eval/velocities/classical/'+each_file)

    for each_file in valid_jazz_filenames:
        copyfile(jazz_raw_path+'_valid_quantized_inputs/'+each_file,data_for_model+'/eval/inputs/jazz/'+each_file)
        copyfile(jazz_raw_path+'_valid_quantized_velocities/'+each_file,data_for_model+'/eval/velocities/jazz/'+each_file)






    
current_run_cnt = '0'
data_dir = "./"
data_set = "data_for_model"
runs_dir = "./"
bi = True
forward_only = False #keep false for training, True for forward pass only
load_model = None
load_last = None



def setup_dir():

    print('[*] Setting up directory...')

    main_path = runs_dir
    current_run = os.path.join(main_path, current_run_cnt)

    files_path = data_dir
    files_path = os.path.join(files_path, data_set)

    x_path = os.path.join(files_path, 'inputs')
    y_path = os.path.join(files_path, 'velocities')
    eval_path = os.path.join(files_path, 'eval')

    model_path = os.path.join(current_run, 'model')
    logs_path = os.path.join(current_run, 'tmp')
    png_path = os.path.join(current_run, 'png')
    pred_path = os.path.join(current_run, 'predictions')

    if not os.path.exists(current_run):
        os.makedirs(current_run)
    if not os.path.exists(logs_path):
        os.makedirs(logs_path)
    if not os.path.exists(model_path):
        os.makedirs(model_path)
    if not os.path.exists(png_path):
        os.makedirs(png_path)
    if not os.path.exists(pred_path):
        os.makedirs(pred_path)

    dirs = {
            'main_path': main_path,
            'current_run': current_run,
            'model_path': model_path,
            'logs_path': logs_path,
            'png_path': png_path,
            'eval_path': eval_path,
            'pred_path': pred_path,
            'x_path': x_path,
            'y_path': y_path
        }


    return dirs

def load_training_data(x_path, y_path, genre):
    X_data = []
    Y_data = []
    names = []
    print('[*] Loading data...')

    x_path = os.path.join(x_path, genre)
    y_path = os.path.join(y_path, genre)

    for i, filename in enumerate(os.listdir(x_path)):
        if filename.split('.')[-1] == 'npy':
            names.append(filename)

    for i, filename in enumerate(names):
        abs_x_path = os.path.join(x_path,filename)
        abs_y_path = os.path.join(y_path,filename)
        loaded_x = np.load(abs_x_path)

        X_data.append(loaded_x)

        loaded_y = np.load(abs_y_path)
        loaded_y = loaded_y/127
        Y_data.append(loaded_y)
        assert X_data[i].shape[0] == Y_data[i].shape[0]


    return X_data, Y_data

def prepare_data():
    dirs = setup_dir()
    data = {}
    data["classical"] = {}
    data["jazz"] = {}

    c_train_X , c_train_Y = load_training_data(dirs['x_path'], dirs['y_path'], "classical")

    data["classical"]["X"] = c_train_X
    data["classical"]["Y"] = c_train_Y

    j_train_X , j_train_Y = load_training_data(dirs['x_path'], dirs['y_path'], "jazz")

    data["jazz"]["X"] = j_train_X
    data["jazz"]["Y"] = j_train_Y
    return dirs, data



dirs, data = prepare_data()

network  = GenreLSTM(dirs, input_size=176, mini=True, bi=bi)
network.prepare_model()

if not forward_only:
    if load_model:
        loaded_epoch = load_model.split('.')[0]
        loaded_epoch = loaded_epoch.split('-')[-1]
        loaded_epoch = loaded_epoch[1:]
        print("[*] Loading " + load_model + " and continuing from " + loaded_epoch + ".")
        loaded_epoch = int(loaded_epoch)
        network.train(data, model=load_model, starting_epoch=loaded_epoch+1)
    else:
        network.train(data)
else:
    network.load(load_model)


