def xy2dataset(*data):#Translates numpy arrays into chart.js datasets
    dataset = []
    if len(data) == 1:
        xy = data[0]
        for i in range(len(xy[:,0])):
            dataset.append({'x':xy[i, 0], 'y':xy[i, 1]})
        return dataset
    elif len(data) == 2:
        x = data[0]
        y = data[1]
        for i in range(len(x)):
            dataset.append({'x':x[i], 'y':y[i]})
        return dataset
    else:
        return False