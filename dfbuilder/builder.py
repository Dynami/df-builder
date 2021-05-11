import datetime
import numpy as np
import pandas as pd
from dfbuilder.features import Feature


def load_csv_dataframe(  
                        csv_filepath:str, 
                        start_dt:datetime.datetime=None, 
                        end_dt:datetime.datetime=None,  
                        columns=None, 
                        index_col:str='Date'):
    st_data = pd.read_csv(
        csv_filepath,
        #names=[columns],
        index_col=index_col,
        parse_dates=True, 
        header=0
    )

    if columns is not None and len(columns) > 0:
        st_data.columns = columns

    if start_dt is not None:
        st_data = st_data[st_data.index >= start_dt]
    if end_dt is not None:
        st_data = st_data[st_data.index <= end_dt]

    return st_data


def label_data(data:pd.DataFrame, main_column:str='Close', lookback:int=5, lookforward:int=1, custom_labeler=None, in_place:bool=False):
    df = data if in_place else data.copy()
    
    series = df[[main_column]]

    df['y'] = df[[main_column]].shift(-lookforward)

    if( custom_labeler is not None):
        df['y'] = custom_labeler(df)

    return df


def compute_x_features(data:pd.DataFrame, append:bool=False, features:tuple=[]):
    if append:
        out = data.copy()
    else:
        out = pd.DataFrame(dtype=float, index=data.index)

    for feat in features:
        label = feat.alias if feat.alias is not None else feat.name
        d = feat.compute(data)
        #print('>>>>', type(d))
        if(type(d) == pd.DataFrame):
            out[label] = d.squeeze()
        elif(type(d) == pd.Series):
            out[label] = d
        elif(type(d) == tuple):
            for i, v in enumerate(d):
                #print('#####', i, type(v))
                out[label+'_'+str(i)] = v
        

    return out

def inline_x_data(_data:pd.DataFrame, lookback:int, train:bool=True, ylabel:str='y', dropna:bool=False):
    data = _data.copy()
    train = train and ylabel in data.columns
    print('train',train)
    if(train):
        y = data[[ylabel]].values
        data = data.drop(columns=[ylabel])
    
    n_features = data.shape[1]
    out = np.full([data.shape[0], lookback * n_features + (1 if train else 0)], np.NaN)
    for j in range(0, n_features):
        feat = data.iloc[:, j]

        for i in range(0, lookback):
            v = feat.shift(i).values #np_shift(feat, i)
            out[:, (j*lookback)+i] = v
    
    feat_names = []
    for j in range(0, n_features):
        for i in range(0, lookback):
            feat_names.append('feat_%s_%s' % (j+1, i+1))
    
    if(train):
        feat_names.append(ylabel)
        out[:, out.shape[1]-1] = y.reshape((-1))


    #print(out)
    out = pd.DataFrame(out, columns=feat_names, index=data.index)
    if(dropna):
        out.dropna(axis=0, inplace=True)
    
    return out