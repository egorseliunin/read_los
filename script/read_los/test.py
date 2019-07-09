#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:34:36 2019

@author: eseliuni
"""
import os

def get_coordinate_from_line(coordinate, line):
    """
    Returns a value of a coordinate from a line
    """
    for word in line.split(","):
        if str(coordinate)+"=" in word:
            if coordinate == "phi":
                return float(word[word.index("=")+1:])
            else:
                return float(word[word.index("=")+1:-1])
            
def get_los(full_path):
    """
    Reads the file *.coordinate from diaggeom with line of sight (LOS) of a
    diagnostic. Returns a dictionary with keys:
        name: short name of the diagnostic
        description: full name of the diagnostic
        signals: contains the name of each channel and its LOS
    """
    # Split the text to the lines
    with open(full_path, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    los_diag = {"name": lines[0].split()[0],
                "description": lines[0][
                             lines[0].index("(")+1:lines[0].index(")")
                             ],
                "signals":{}
    }
    
    # Combine lines to the blocks, corresponding specific channel
    phrase = "(Line of sight)"  # a phrase, that indicates the beginning of the block
    signals_line_idx = [ii for ii in range(len(lines)) if phrase in lines[ii]]
    signals_line_idx.append(len(lines))

    signal_blocks_idx = [(signals_line_idx[ii], signals_line_idx[ii+1]) for ii in range(len(signals_line_idx)-1)[:-1]]
    signal_blocks_idx.append((signals_line_idx[-2], signals_line_idx[-1]))
    
    # obtain R, z and phi for each block
    for (ii, jj) in signal_blocks_idx:
        los = {}
        phrase = "From"
        block = lines[ii:jj]
        line_idx = [ll for ll in range(len(block)) if phrase in block[ll]]
        for idx in line_idx:
            R = [get_coordinate_from_line("R", block[idx]), get_coordinate_from_line("R", block[idx+1])]
            z = [get_coordinate_from_line("z", block[idx]), get_coordinate_from_line("z", block[idx+1])]
            phi = [get_coordinate_from_line("phi", block[idx]), get_coordinate_from_line("phi", block[idx+1])]
            
            if block[idx].split()[0] == phrase:
                los.update({"0":{"R": R, "z":z, "phi":phi}})
            else:
                los.update({block[idx].split()[0]:{"R": R, "z":z, "phi":phi}})
        los_diag["signals"].update({lines[ii].split()[0]:los})
        
    file.close()
    return los_diag

if __name__ == "__main__":
    working_dir = os.getcwd()
    examples_dir = "../../files/"
    path = os.path.join(working_dir, examples_dir)
    file_name = 'diaggeom_Interf.coords'
    los_diag = get_los(os.path.join(path, file_name))
    

        
        
        