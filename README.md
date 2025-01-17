# digitizer_analysis
Python implimentation to analyze PMT data using root digitizer data files.

## searchdir.py
Helper script to search directory for root data files. Keep in same directory as `waveform_extraction.py`.

## waveform_extraction.py
Extracts data from `.root` files from the digitizer. By default, this will store the data in hdf files with as a pandas object. Data files are large, but convinent for use.

- Update parameter: `path_to_dir` to the relevent directory with the `.root` files for extraction.

## digitizer.ipynb
Main analysis notebook. First version is repurposed from a previous notebook used for analyzing muon data (some remnents of the old version still apparent). 

- Plotting uses backend `Agg` -> No interactive plotting, must save the figures to disk. This speeds up the process when trying to visualize many waveforms.
