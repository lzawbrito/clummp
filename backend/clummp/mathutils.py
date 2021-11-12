import numpy as np 
import matplotlib.pyplot as plt

def get_level_curves(f, n_levels):
    levels = np.linspace(np.min(f) + 0.01, np.max(f), n_levels)

    cnt = plt.contour(x, y, f, levels)
    # Obtain the level curves for this function 
    paths = [coll.get_paths() for coll in cnt.collections]

    vertices = []
    for path in paths: 
        try:
            vertices.append(path[0].vertices)
        except IndexError:
            continue 

    plt.clf()
    return vertices
    

def test_function(x, y):    
    return x ** 2 + y ** 2

x = np.arange(-10, 10, 0.1)
y = np.arange(-10, 10, 0.1)

x, y = np.meshgrid(x, y)

f = test_function(x, y)

vertices = get_level_curves(f, 10)

x, y = np.transpose(vertices[1])
plt.scatter(x, y)

plt.show()