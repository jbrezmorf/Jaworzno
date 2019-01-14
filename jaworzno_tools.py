import re
import pandas as pd
import pyproj
import numpy as np

def float_converter(x):
    """
    Convert values like '<0.01' to the value.
    """
    if type(x) is str:
        try:
            if x[0] == '<':
                x = x[1:]
            return float(x)
        except Exception as e:
            #print(e)
            #print("Except: X{}X".format(x))
            return 0.0
    else:
        return x

def coord_converter(x):
    """
    Convert values from 'deg.xxx°[N,E]', and 'deg°min'sec"[N,E]
    to float degrees.
    """
    
    if type(x) is str:
        x = x.strip()
        m = re.match('(\d*)\.?°(\d*)´(\d*.\d*)\"[NE]', x)
        if m:
            vals = [float_converter(x) for x in m.groups()]
            return vals[0] + vals[1]/60 + vals[2]/3600
        m = re.match('(\d*.\d*)°[NE]', x)
        if m:
            return float_converter(m[1])
    return x
    
    

    
def read_table(file_name, sheet=0, unit_line=True ):
    """
    Read a table from given sheet of given Excel file.
    :param file_name: path to an Excel file
    :param sheet: index of the sheet to load
    :param unit_line: skip the line after header
    return: Pandas data frame with the table data.    
    """
    # Define script names
    aux_to_orig_name = dict(
        # common
        long='longitude',	# degrees
        lat='latitude',		# degrees
        alt='surface altitude',		# m        
        jtsk_x='JTSK x',
        jtsk_y='JTSK y',
        Sa='a-HCH',
        Sb='b-HCH',
        Sc='c-HCH',
        Sd='d-HCH',
        Se='e-HCH',
        # wells
        well='well name',
        d_aquifer='depth aquifer',
        d_water='depth water',
        s_begin='screen begin',        
        s_end='screen end',
        # trees
        cfrc='circumference',
        specie='specie',
        sid='sample code',        
        prev_id='previous code',        
        matrix='matrix')
        
        
        
    
    # Specify convertes for individual types of columns
    converters = {orig: None for aux, orig in aux_to_orig_name.items()}
    for aux in ['cfrc', 'jtsk_x', 'jtsk_y', 'Sa', 'Sb', 'Sc', 'Sd', 'Se']:
        converters[aux_to_orig_name[aux]] = float_converter  
    converters['latitude'] = coord_converter
    converters['longitude'] = coord_converter
    
    df = pd.read_excel(file_name, sheet=sheet, converters=converters, skiprows=0, header=0)
    
    # Drop the units row
    if unit_line:
        df = df.drop(0)
    
    # Rename columns
    orig_to_aux_name = {orig: aux for aux, orig in aux_to_orig_name.items()}
    aux_col_names = [ orig_to_aux_name.get(orig_col, '__') for orig_col in df.columns]
    df.columns = aux_col_names
    if '__' in df.columns:
      df = df.drop('__', axis=1)    
       
    # Generic data fix
    return df


def make_jtsk(df):
    """
    Create columns jtsk_x, jtsk_y from columns long, lat.
    """
    to_jtsk = pyproj.Proj(init='EPSG:5514')
    if 'jtsk_x' not in df.columns:
        jtsk_coords = [ to_jtsk(lo, la) for lo, la in  zip(np.array(df.long), np.array(df.lat)) ]
        x, y = zip(*jtsk_coords)
        df['jtsk_x'] = x
        df['jtsk_y'] = y

    if 'lat' not in df.columns:
        ll = [ to_jtsk(x, y, inveerse=True) for x, y in  zip(np.array(df.jtsk_x), np.array(df.jtsk_y)) ]
        lon, lat = zip(*ll)
        df['long'] = lon
        df['lat'] = lat

    return df



