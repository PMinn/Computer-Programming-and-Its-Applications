# coding=utf-8
import pandas as pd


def toExcel(data, path='.', className='file'):
    if path.endswith('/'):
        path = path[:-1]
    with pd.ExcelWriter(f'{path}/{className}.xlsx') as writer:
            for schoolName in data:
                pd.DataFrame(data[schoolName][className]).T.to_excel(writer, schoolName)