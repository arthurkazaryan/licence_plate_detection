import numpy as np


def from_preds_to_list(preds, model):
    p = np.array(preds)
    lista =[]
    for i in range(len(p)):
        lista.append(np.where(np.amax(p[i])==p[i])[0][0])
    last=[]
    for element in lista:
        last.append(model.data.classes[element])
    return last