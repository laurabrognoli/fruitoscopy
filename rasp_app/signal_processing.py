import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
import time
import sqlite3 as lite
from signal_processing import *
import scipy.signal as sps
import scipy.optimize as opt
from matplotlib.pylab import savefig
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from database_interactions import *
from machine_learning import *

HOME_PATH  = os.path.dirname(os.path.abspath(__file__))

def mins(array,wl):
    """
    This function receive as input the spectrum and the wavelenghts.
    The return value is the list of the minima.

    The purpose of this function is to find the minima of the

    Specifically:
    @@@@@@@@@@@@@

    :Variables in input:
    ----------
    :param 0: array of the spectrum
    :param 1: list of wavelenghts


    :Return values:
    ----------
    :value 0: List of minimas of the spectrum
    """
    der = np.diff(array)

    prev = 0
    min_vals = []
    for x in range(len(wl)):
        if der[x-1] > 0 and prev < 0:
            min_vals.append(x-1)
        elif der[x-1] == 0 and prev < 0:
            min_vals.append(x-1)
        prev = der[x-1]
    return min_vals

def remove_background(spectrum):
    """
    This function receive as input the spectrum, the wavelenghts, the minima points and the deg to compute the regression line.
    The return value is the label and the normalized spectrum

    The purpose of this function is to normalize the spectrum

    Specifically:
    @@@@@@@@@@@@@

    :Variables in input:
    ----------
    :param 0: array of the spectrum
    :param 1: list of wavelenghts
    :param 2: list of minimas
    :param 3: deg of regression line

    :Return values:
    ----------
    :value 0: Normalized spectrum (nparray)
    :value 0: Label of the spectrum
    """
    #This has been disabled because is not the right approach, the regression line is jost a background line,
    #with m = 0
    '''
    # Compute a regression line for the first sample
    p2 = np.polyfit(wl, spectrum, deg = 1)

    # Calculate the background values
    back_val = []
    for x in wl:
        back_val_current = 0
        for i in range(len(p2)):
            back_val_current += p2[len(p2) - i - 1]*(x**i)
        back_val.append(back_val_current)

    spec_final = spectrum - back_val
    min_val = np.amin(spec_final)
    for i in range(len(spec_final)):
        spec_final[i] -= min_val

    pf = np.poly1d(p2)
    return [spec_final, pf]
    '''
    min_height = min(spectrum)

    background_rem =  np.array(spectrum)
    background_rem -= min_height

    return (background_rem)

def save_plot(array, wl=[]):
    """
    This function receive as input an array.
    The return is nothing.

    The purpose of this function is to create a plot of the values of the array and save it.

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: array of the y elements of a spectrum

    :Return values:
    ----------
    - no return values
    """
    if wl == []:
        wl = range(len(array))
    plt.clf();plt.plot(wl,array,c='black')
    #Uncomment to save csv arrays
    #f=open(HOME_PATH + '/static/spectrum.csv','a')
    #f.write(",".join(map(str, array))+'\n')
    #f.close()
    savefig(HOME_PATH + '/static/spectrum.png', bbox_inches='tight')

def get_image():
    """
    This function receive as input some parameters as a tuple.
    The return value is the image of the spectrum.

    Specifically:
    @@@@@@@@@@@@@

    :Parameters of the tuple:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)

    :Return values:
    ----------
    :value 0: Image of the spectrum
    """
    param = get_params()
    im=Image.open(HOME_PATH + '/source.jpg')
    im=im.rotate(param[4])
    im = im.crop(box=param[:4])
    im.save(HOME_PATH + '/static/processed.jpg')

    #Better not to resize, data is lost or altered too much
    #maxsize = (1000, im.size[0])
    #im = im.resize(maxsize, Image.ANTIALIAS)

    #im.show()
    img_spectrum = im.load()
    return img_spectrum

def get_baseline(img_spectrum):
    """
    This function receive as input the matrix of the pixels of the spectrum image, after being cropped, and some parameters as a tuple.
    The return value is the spectrum.

    The purpose of this function is to calculate the y values of the spectrum from the image

    Specifically:
    @@@@@@@@@@@@@

    :Parameters of the tuple:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)

    :Matrix:
    ----------
    r,g,b = matrix[col, row]
    where "col" is column of the matrix and "row" is the row
    r, g and b are the 3 components, red, green and blue of every pixel of the matrix

    :Return values:
    ----------
    :value 0: List of y elements of the spectrum
    """
    param=get_params()
    rl=np.zeros(param[2]-param[0]);gl=np.zeros(param[2]-param[0]);bl=np.zeros(param[2]-param[0]);
    tot = [[] for x in range(param[2]-param[0])]
    for col in range(param[2]-param[0]):
        count=[0.,0.,0.]

        for row in range(0,param[3]-param[1],1):
            #b,g,r = img_spectrum[row,col]
            r,g,b = img_spectrum[col,row]
            tot[col].append(r+g+b)

    black_line = []
    for elem in tot:
        black_line.append(max(elem))
    return black_line

def process_image():
    """
    I will process the image, taking 1 tuple made of parameters as input.
    The return values will be the label of the sample and the spectrum

    Specifically:
    @@@@@@@@@@@@@

    :Parameters:
    ----------
    :param 0: Left margin of image to crop
    :param 1: Top margin of image to crop
    :param 2: Left margin of image to crop
    :param 3: Bottom margin of image to crop
    :param 4: Degrees to rotate the image (+ is CCW)

    :Return values:
    ----------
    :value 0: Label of the fruit
    :value 1: List of y elements of the spectrum

    """

    #param = (800,1000,2400,1250,5) #left,top,right,bottom, rotate
    param = get_params()
    img_spectrum = get_image()

    black_line = get_baseline(img_spectrum)
    #plt.plot(black_line, color="blue")
    almost_good = sps.savgol_filter(black_line, 51, 3)
    #plt.plot(almost_good, color="red")
    #savefig(HOME_PATH + '/aabbbccc.png', bbox_inches='tight')
    wl = np.array(range(400,801))
    idx = mins(almost_good,wl)

    background_rem = remove_background(almost_good)

    normalized = normalize(background_rem, wl)
    try:
        if(normalized.any() == -1):
            return -1, -1
    except:
        if(normalized == -1):
            get_image()
            return -1, -1
    plt.plot(background_rem)
    #plt.plot(normalized)
    #savefig(HOME_PATH + '/aabbb.png', bbox_inches='tight')
    save_plot(normalized, wl)

    get_label(normalized)
    
    return (0,normalized)

def normalize(array, wl):
    """
    This functions get in input the array that has been calculated by the image
    and then returns the correct array based on the wavelenghts.

    This because the number of the points in the array of the wavelenghts is not
    equal to the number of the points of the spectrum taken from the image.
    (Depends on the number of pixels and the calibration)

    Specifically:
    @@@@@@@@@@@@@

    :Values in input:
    ----------
    :value 0: Array of the y values of the spectrum
    :value 1: Array of x values of the wavelenghts

    :Return values:
    :value 0: The array of the normalized spectrum, Returns -1 if the area
                is wrong and needs to be calibrated

    """
    ##This part cuts the initial array and depending on the wl calibration parameters
    ##in order to take only the part between 400 and 1000 nm

    min_wl = np.amin(wl)
    max_wl = np.amax(wl)
    len_arr = len(array)
    normalized = []
    count = 0
    param = get_spectrum_param()
    diff_param = param[1] - param[0]

    begin = param[0] - diff_param * 0.375
    end = param[1] + diff_param * 0.625

    begin_px = int(begin*len(array)/1000)
    end_px = int(end*len(array)/1000)
    #print(begin_px)

    ##If the area is too little to get the data from all the wl points
    ##minimaze the error making an automatic calibration, returning an error
    ## (Area calibration is done, now the user must calibrate the wl)

    if(begin_px < 0 or end_px > len_arr):
        #print("error")
        dim = get_params()
        if(begin_px < 0 and end_px > len_arr):
            diff_begin = -begin_px
            diff_end = end_px - len_arr
            update_calib_params((dim[0]-diff_begin-10,dim[1],dim[2]+diff_end+10,dim[3],dim[4]))
            #update_spectrum_params(((param[0]-int(diff_begin*len(array)/1000)), param[1]+int(diff_end*len(array)/1000)))
            return -1
        elif(begin_px < 0):
            diff_begin = -begin_px
            update_calib_params((dim[0]-diff_begin-10,dim[1],dim[2],dim[3],dim[4]))
            #update_spectrum_params(((param[0]-int(diff_begin*len(array)/1000)), (param[1])))
            return -1
        elif(end_px > len_arr):
            diff_end = end_px - len_arr
            update_calib_params((dim[0],dim[1],dim[2]+diff_end+10,dim[3],dim[4]))
            #update_spectrum_params(((param[0]), param[1]+int(diff_end*len(array)/1000)))
            return -1

    new_list = array[begin_px:end_px]

    array = new_list
    len_arr = len(array)

    ##To check, because math is not magic and this function worked too easily
    ##Now that the "good spectrum" between the desired wl is saved, a compression
    ##or dilation is needed in order to have a point for every wl nm

    ##This is done by removing the points in excess or adding new points by average

    if(max_wl-min_wl < len_arr):
        to_delete = (max_wl-min_wl)/(len_arr-max_wl+min_wl)
        for i in range(len(array)):
            if int(i%(to_delete+1)) != 0:
                normalized.append(array[i])
            else:
                count +=1
        if(len(normalized) < max_wl-min_wl+1):
            normalized.append(normalized[-1])
    else:
        to_add = (max_wl-min_wl)/(max_wl-min_wl-len_arr)
        for i in range(len(array)):
            if int(i%(to_add-1)) == 0:
                normalized.append((array[i]+array[i-1])/2)
                count +=1
            normalized.append(array[i])
        if(len(normalized)<max_wl-min_wl+1):
            normalized.append(normalized[-1])

    #print(count) #Check how many removed/added
    #print("AAAAAAA: %d" % len(normalized))
    #print("BBBBBBB: %d" % (max_wl-min_wl))
    return np.array(normalized)
