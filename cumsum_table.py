# -*- coding: utf-8 -*-
"""
Created on 2020/9/2 下午 09:53
@author: Ivan Y.W.Chiu
"""

import pandas as pd
import numpy as np
import os

df = pd.read_csv(r"./cumsum_temp.csv")

def get_last_n_OOC_count(ci, mode, CL, n=5):
    if len(ci) >= n:
        if mode=="Ci+":
            count = len(np.where(ci[-n:] >= CL))
        else:
            count = len(np.where(ci[-n:] <= CL))
    else:
        if mode=="Ci+":
            count = len(np.where(ci >= CL))
        else:
            count = len(np.where(ci <= CL))

    return count


def get_last_n_OOC_count(df, columns=[("Ci+", "UCL"), ("Ci-", "LCL")], n=5):

    # 先加入時間constrain:

    # 如果時間許可:
    compare_ci_plus = df[columns[0][0]] >= df[columns[0][1]]
    compare_ci_minus = df[columns[1][0]] <= df[columns[1][1]]

    # 如果資料筆數足夠:
    if len(df[columns[0][0]]) > n:
        count_ci_plus = len(np.where(compare_ci_plus[-n:] == True)[0])
        count_ci_minus = -len(np.where(compare_ci_minus[-n:] == True)[0])
    else:  # 若資料筆數不足:
        count_ci_plus = len(np.where(compare_ci_plus == True)[0])
        count_ci_minus = -len(np.where(compare_ci_minus == True)[0])

    get_the_plus_term = count_ci_plus - abs(count_ci_minus)
    if get_the_plus_term > 0:
        results = count_ci_plus
    elif get_the_plus_term < 0:
        results = count_ci_minus
    else:
        results = 0

    # 若時間不許可:
    # 則顯示已經幾天沒有資料

    return pd.Series({"Count_Ci+": count_ci_plus, "Count_Ci-": count_ci_minus, "Result": results}, dtype=int)


gb1 = df.groupby(["Proc_Recipe_Ph", "CSWP_Recipe", "Eqp_ID", "CSWP_Unit"], as_index=False).apply(get_last_n_OOC_count, n=5)

gb2 = gb1.reset_index()
total_table = gb2.pivot_table("Result", index=["Proc_Recipe_Ph", "CSWP_Recipe"], columns=["Eqp_ID", "CSWP_Unit"], fill_value="N/A")