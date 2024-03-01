# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 16:24:26 2024

@author: mdelm

An example of data extraction and visualization from a CSV file 
using Python:
    - builtin functions: lists, set, lambda, map, filter, zip
    - list and dictionary comprehensions


"""

import csv
import sys

import matplotlib.pyplot as plt


#%%

def read_csv(path):
    """
    
    Reads a CSV file with Python builtin functions
    

    Parameters
    ----------
    path : Path to the CSV file of interest

    Returns
    -------
    data : Dictionary that contains the data from the CSV file

    """
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = next(reader)
        data = []
        for row in reader:
            iterable = zip(header, row)
            data_dict = {key: value for key, value in iterable}
            data.append(data_dict)
        return data
    

#%%

def get_value_data(components, key, order=1, asc=-1):
    """

    Parameters
    ----------
    components : Dictionary with the data retrieved from a given csv file
    key : A dictionary's key to look up for
    order : 0 for the key's values and 1 for its frequency on the data
    asc : 1 for ascending, -1 for descending

    Returns
    -------
    values_data : a nested list with the distinct values and their frequency

    """
    
    if order!=1 and order!=0:
        print('Posición de ordenamiento mal indicada')
        sys.exit()
        
    if asc!=1 and asc!=-1:
        print('Orden mal indicado')
        sys.exit()
    
    values = []
    values_data = []
    
    for item in components:
        values.append(item[key])
    
    values = list(set(values))
    
    for i in range(len(values)):
        result = list(filter(lambda item: item[key] == values[i], components))
        values_data.append([values[i], len(result)])
        
    values_data = sorted(values_data, key=lambda x: asc*x[order])
        
    return values_data


#%%

def get_average_price_per_feature(components, key, order=2, asc=-1):
    """

    Parameters
    ----------
    components : Dictionary with the data retrieved from a given csv file
    key : A dictionary's key to look up for
    order : 0 for the key's value, 1 for its frequency on the data and
            2 for its price
    asc : 1 for ascending, -1 for descending

    Returns
    -------
    values_data : a nested list with the distinct values, their average price and their frequency

    """
    
    if order<0 or order>2:
        print('Posición de ordenamiento mal indicada')
        sys.exit()
        
    if asc!=1 and asc!=-1:
        print('Orden mal indicado')
        sys.exit()
    
    suppliers = []
    suppliers_data = []
    
    for item in components:
        suppliers.append(item[key])
    
    suppliers = list(set(suppliers))
    
    for i in range(len(suppliers)):
        result = list(filter(lambda item: item[key] == suppliers[i], components))
        prices = list(map(lambda item: item['Price'], result))
        prices = [float(i) for i in range(len(prices))]
        suppliers_data.append([suppliers[i], len(result), sum(prices)/len(prices)])
        
    suppliers_data = sorted(suppliers_data, key=lambda x: asc*x[order])
    
    suppliers_data = [suppliers_data[i] for i in range(len(suppliers_data)) \
                      if suppliers_data[i][order]!=0]
        
    return suppliers_data


#%% 

def generate_chart(data, reference, title, pos):
    """
    
    Parameters
    ----------
    data: nested list of attributes, amount  and prices
    reference: Label for the X axis
    title: Label for the Y axis
    Pos: 1 for quantity, 2 for price
    """
    
    data_labels = []
    data_values = []
    
    # Label filtering    
    for i in range(len(data)):
        label = data[i][0].strip()
        if len(label)>1: # Fields like "-" won't be considered
            data_labels.append(label)
            data_values.append(data[i][pos])
    
    # Ploting figures
    if len(data_values)>14:
        n_plots = int(len(data_values)/14)
        
        for a in range(n_plots):
            plt.figure(dpi=1200)
            rem = 14*a+13 if a<n_plots-1 else len(data_values)-1
            plt.barh(data_labels[14*a:rem], data_values[14*a:rem])
            plt.xlabel(title + f" - Part {a+1}")
            plt.ylabel(reference)
    
    else:
        plt.figure(dpi=1200)
        plt.barh(data_labels, data_values)
        plt.xlabel(title)
        plt.ylabel(reference)


def generate_charts(data, reference, title1, title2):
    """
    
    Parameters
    ----------
    data: nested list of attributes, amount  and prices
    reference: Label for the X axis
    title1: Label for the Y axis. Must be related with amounts
    title2: Label for the Y axis. Must be related with prices
    
    """
    
    data_nums = []
    data_labels = []
    data_values = []  
    
    for i in range(len(data)):
        label = data[i][0].strip()
        if len(label)>1: 
            data_labels.append(label)
            data_nums.append(data[i][1])
            data_values.append(data[i][2])
       
    if len(data_values)>14:
        n_plots = int(len(data_values)/14)
        
        for a in range(int(len(data_values)/14)):
            plt.figure(dpi=1200)
            rem = 14*a+13 if a<n_plots-1 else len(data_values)-1
            plt.barh(data_labels[14*a:rem], data_nums[14*a:rem])
            plt.xlabel(title1 + f" - Part {a+1}")
            plt.ylabel(reference)
    
        for a in range(int(len(data_values)/14)):
            plt.figure(dpi=1200)
            rem = 14*a+13 if a<n_plots-1 else len(data_values)-1
            plt.barh(data_labels[14*a:rem], data_values[14*a:rem])
            plt.xlabel(title2 + f" - Part {a+1}")
            plt.ylabel(reference)

    else:            

        plt.figure(dpi=1200)
        plt.barh(data_labels, data_values)
        plt.xlabel(title1)
        plt.ylabel(reference)
        
        plt.figure(dpi=1200)
        plt.barh(data_labels, data_nums)
        plt.xlabel(title2)
        plt.ylabel(reference)
    
    
#%%

if __name__ == '__main__':
    
    data_adc_dac = read_csv('data/adcs_dacs___special_purpose.csv')
    
    suppliers = get_value_data(data_adc_dac, 'Supplier')
    suppliers_avg_price = get_average_price_per_feature(data_adc_dac, 'Supplier')
    generate_charts(suppliers_avg_price, 'Company', 'Average product price', 'Product quantity available')
    
    suppliers_dev_package = get_value_data(data_adc_dac, 'Supplier Device Package')
    generate_chart(suppliers_dev_package, 'Package', 'Products per package', 1)
    
    suppliers_package_price = get_average_price_per_feature(data_adc_dac, 'Supplier Device Package')
    generate_chart(suppliers_package_price, 'Package', 'Average product price', 2)
    
    res_bits = get_value_data(data_adc_dac, 'Resolution (Bits)', order=0, asc=1)
    generate_chart(res_bits, 'Resolution', 'Products per resolution', 1)
    
    res_bits_price = get_average_price_per_feature(data_adc_dac, 'Resolution (Bits)')
    generate_chart(res_bits_price, 'Bits', 'Average price per resolution', 2)
    
    sampling = get_value_data(data_adc_dac, 'Sampling Rate (Per Second)', order=0, asc=1)
    generate_chart(sampling, 'Sampling speed', 'Products per sampling speed', 1)
    