import pandas as pd
import os


def get_excels_for_merge(xls_dir):
    xls = []
    for root, dirs, files in os.walk(xls_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.xls':
                xls.append(os.path.join(root,file))
    return xls
# 读取目录下的所有excel文件路径，返回列表


def merge_to_excel(xls):
    dfs = []
    for fn in xls:
        dfs.append(pd.read_excel(fn))
    df = pd.concat(dfs)
    df.to_excel('result_all2.xls', index=False)


xls = get_excels_for_merge('D:\\360che\\results_new')
merge_to_excel(xls)
