# coding=utf-8
import matplotlib.pyplot as plt
import numpy as np

def barPlot(output, data, tick, figsize=None, colors=None, total_width=0.8, single_width=1):
    # 設定中文字體
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
    plt.rcParams['axes.unicode_minus'] = False
    
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    if figsize is None:
        plt.figure()
    else:
        plt.figure(figsize=figsize)
    n_bars = len(data)
    bar_width = total_width / n_bars
    bars = []
    for i, (name, values) in enumerate(data.items()):
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
        bar = plt.bar(np.arange(len(values)) + x_offset, values, width=bar_width * single_width, tick_label=tick, label=name, color=colors[i % len(colors)])
        bars.append(bar)
    for bar in bars:
        plt.bar_label(bar, fmt='%.0f', label_type='edge')
    plt.legend(loc='best')
    plt.savefig(output, dpi=300)