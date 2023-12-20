# coding=utf-8
import pandas as pd


def toExcel(data, className):
    with pd.ExcelWriter(f'{className}.xlsx') as writer:
            for schoolName in data:
                pd.DataFrame(data[schoolName][className]).T.to_excel(writer, schoolName)