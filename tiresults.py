#!/usr/bin/python3.4
"""
Created on Thu Jun  7 12:17:55 2018

@author: obal
"""

import pandas as pd

def get_duals(instance, anEq):
    duals={}
    for index in anEq:
        try:
            duals[index]=abs(instance.dual[anEq[index]])
        except KeyError:
            pass
    return duals

def get_rc(instance, aVar):
    rc={}
    for index in aVar:
        try:
            rc[index]=abs(instance.rc[aVar[index]])
        except KeyError:
            pass
    return rc
    
def clean_df(df):
    df[df < 1e-12] = 0
    df.replace(0, pd.np.nan, inplace=True)
    df.dropna(thresh=1, inplace=True)
    df.replace(pd.np.nan, 0, inplace=True)


def mi_df(dict_level, dict_duals, index):
    level='LEVEL'
    dual='DUAL'
    if dict_level and dict_duals:
        s1 = pd.Series(dict_level, name=level).rename_axis(index, axis=0)
        s2 = pd.Series(dict_duals, name=dual).rename_axis(index, axis=0)
        df=pd.concat([s1, s2],axis=1)
    else:
        multi_index = pd.MultiIndex(levels=[[] for x in range(len(index))],
                                labels=[[] for x in range(len(index))],
                                names=index)
        df = pd.DataFrame(index=multi_index, columns=[level, dual])
    return df

def df2csv(df,index_order,fl_name):
    clean_df(df)
    df = df.loc[:, (df != 0).any(axis=0)]
    
    if df.index.names != index_order:
        i=''
        j=''
        for n in range(len(index_order)):
            if index_order[n] != df.index.names[n]:
                i=index_order[n]
                j=df.index.names[n]
                df = df.swaplevel(i,j,axis=0)
    
    return df.to_csv(fl_name + '.csv', encoding='utf8', index=True, header=True)