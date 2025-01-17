"""
py script combining aspects from waveform_analysis.ipynb notebook to save data to a numpy array file.
6th December 2024
ntcb
"""

import uproot, numpy as np, matplotlib.pyplot as plt, platform, pandas as pd

# Local imports
from searchdir import searchdir


# Constants
mppc_DIGITIZER_FULL_SCALE_RANGE = 2.5 # Vpp
mppc_DIGITIZER_RESOLUTION       = 12 # bits
digiCounts = 2.**mppc_DIGITIZER_RESOLUTION
verticalScaleFactor = 1.e3*mppc_DIGITIZER_FULL_SCALE_RANGE/digiCounts; # mV/bank
mppc_DIGITIZER_SAMPLE_RATE      = 3200000000 # S/s
horizontalScaleFactor = 1.e9/mppc_DIGITIZER_SAMPLE_RATE #ns/sample


# Functions
def fetch_data(root_file_path:str, channels:list[str]=["00"], verticalScaleFactor=verticalScaleFactor) -> dict:
    
    # Digitizer specs
    mppc_DIGITIZER_FULL_SCALE_RANGE = 2.5 # Vpp
    mppc_DIGITIZER_RESOLUTION       = 12 # bits
    mppc_DIGITIZER_SAMPLE_RATE      = 3200000000 # S/s
    digiCounts = 2.**mppc_DIGITIZER_RESOLUTION
    
    # Find number of entries.
    with uproot.open(root_file_path) as root_file:
        N_entries = root_file["waveform_tree"].num_entries
        print("Number of waveforms per channel:", root_file["waveform_tree"].num_entries)

    if type(channels) != list:
        channels = [channels]
    
    # Fetch all waveforms per channel
    waveforms = {}
    branches = [f"dt5743_wave{ch}" for ch in channels]
    for i in range(0, len(branches)):
        with uproot.open(root_file_path) as root_file:
            print(root_file["waveform_tree"].branches[1])
            waveforms_raw = root_file["waveform_tree"].arrays([branches[i]], library="np", entry_start = 0, entry_stop = N_entries)[branches[i]]
            
            # Manually scale data to drop zero values
            waveforms_raw = waveforms_raw[:, 0:512]
            
            # Apply scale factor from digitizer
            # Correct mislabled channels in B_002
            if "B_002" in root_file_path:
                if channels[i] == "00":
                    waveforms["03"] = waveforms_raw*verticalScaleFactor
                elif channels[i] == "03":
                    waveforms["00"] = waveforms_raw*verticalScaleFactor
                else:
                    waveforms[channels[i]] = waveforms_raw*verticalScaleFactor
            else:
                waveforms[channels[i]] = waveforms_raw*verticalScaleFactor

            # # Mask to drop oversaturated values
            # mask = np.all(waveforms[channels[i]] <= 1500, axis=1)
            # waveforms[channels[i]] = waveforms[channels[i]][mask]

    print("Channels retrieved: ", waveforms.keys())
    return waveforms


# def analyze_data(waveforms, A=None, B=None, j_A=10, j_B=100, auto_window = False):

#     # Initialize arrays with zeroes
#     N_entries = len(waveforms)
#     charge     = np.zeros(N_entries)
#     amplitude  = np.zeros(N_entries)
#     timing     = np.zeros(N_entries)

#     # If no specific time window, integrate charge over entire waveform.
#     if A == None: A = 0
#     if B == None: B = len(waveforms[0])

#     # auto_window will integrate only around the pulse.
#     if auto_window == False: print(f"Integration window: {A} Sa to {B} Sa.")
#     if auto_window == True : print(f"Integration window: j_max-{j_A} to j_max+{j_B}.")

#     # Loop over every waveform and find baseline, amplitude, charge and timing.
#     for i in range(0, N_entries):
#         baseline = np.average(waveforms[i][25:100])
#         j_max = np.argmax(-1.*waveforms[i][A:B])
#         timing[i] = j_max
#         amplitude[i]   = -1.*(waveforms[i][j_max]-baseline)
#         if auto_window == True:
#             A = j_max - j_A
#             B = j_max + j_B
#             if A  <= 0:   A = 0
#             if B  > 1024: B = 1024
#         charge[i]     = -1.*np.sum(waveforms[i][A:B]-baseline)
 
#     return charge, amplitude, timing
    

################# 
# Main analysis #
#################

# Path to data
path_to_dir = "/home/nikolas/Documents/Research/PMT_Testing/Map"

# Search for data files
data_paths:list[str] = searchdir(path_to_dir, ".root")

# Channel to extract
CH = ["00"]

# Fetch data for each data file
waveform_list = []
for i in range(len(data_paths)):
    waveform_list.append(fetch_data(data_paths[i], channels=CH))
    
# Process each datafile independently
i = 0  # Iterator
for waveforms in waveform_list:
    channels = waveforms.keys()
    # # Extract and analyze charges, amplitudes, and timings from the waveforms
    # charges, amplitudes, timings = {}, {}, {}
    # for ch in channels:
    #     charges[ch], amplitudes[ch], timings[ch] = analyze_data(waveforms[ch], A=None, B=None, j_A=10, j_B=100, auto_window = False)
        
    # # Save data to dictionary
    # data = {"amplitude":amplitudes, "charge":charges, "timing":timings}
    
    # # Convert to pandas dataframe
    # data_df = pd.DataFrame(data)
    
    # Save path
    outfile = data_paths[i].split(".")[0] + ".h5"
    
    # # Save dataframe
    # data_df.to_hdf(outfile, key="data")
    
    for channel in channels:
        # Now save the raw waveforms to file for later viewing
        waveforms_df = pd.DataFrame(waveforms[channel])
        waveforms_df.to_hdf(outfile, key=f"Ch{channel[-1]}")
    
    # Iterate
    i += 1
    
