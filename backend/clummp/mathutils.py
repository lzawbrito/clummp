import numpy as np 
import matplotlib.pyplot as plt


def get_level_curves(f, n_levels, padding=0.001, show_plot=False, normalize=True):
    f = np.array(f)
    if normalize: 
        f = (1 / (np.max(f) - np.min(f))) * f + np.min(f)
    levels = np.linspace(np.min(f) + padding, np.max(f) - padding, n_levels)
    
    x = np.arange(0, len(f[0]), 1)
    y = np.arange(0, len(f), 1)

    x, y = np.meshgrid(x, y)

    cnt = plt.contour(x, y, f, levels)

    # Obtain the level curves for this function 
    paths = [coll.get_paths() for coll in cnt.collections]
    labelled_paths = []
    for i in range(0, len(paths)):
        labelled_paths.append({'value': levels[i], 'paths': paths[i]})
    
    if show_plot:
        plt.show()

    plt.clf()
    plt.close()
    return labelled_paths
    

def get_n_paths(f, n_levels, padding=0.001):
    return [(p['value'], len(p['paths'])) for p in get_level_curves(f, n_levels, padding=padding)]


def get_com(vertices):
    """
    vertices: (x, y)
    """
    vertices = np.array(vertices)
    return (np.sum(vertices[0]) / len(vertices[0]), np.sum(vertices[1]) / len(vertices[1]))


def get_com_distance(vert1, vert2):
    c1 = get_com(vert1)
    c2 = get_com(vert2)
    dc = np.array(c1) - np.array(c2)
    return np.sqrt(np.dot(dc, dc))


def get_steepness(vert1, vert2):
    c = get_com(vert1)
    vert1 = np.transpose(vert1)
    vert2 = np.transpose(vert2)
    
    total_dist1 = 0
    n_vertices1 = 0
    for v in vert1:
        dr = np.array(v) - np.array(c)
        total_dist1 += np.sqrt(np.dot(dr, dr))
        n_vertices1 += 1

    total_dist2 = 0
    n_vertices2 = 0
    for v in vert2:
        dr = np.array(v) - np.array(c)
        total_dist2 += np.sqrt(np.dot(dr, dr))
        n_vertices2 += 1
    
    avg_dist1 = total_dist1 / n_vertices1
    avg_dist2 = total_dist2 / n_vertices2

    return avg_dist2 - avg_dist1


def dist(a, b): 
    a = np.array(a) 
    b = np.array(b)
    return norm(a - b)


def norm(a): 
    a = np.array(a)
    return np.sqrt(np.dot(a, a))


if __name__ == '__main__':
    def test_function(x, y):    
        return np.exp(- (x - 1) ** 2 - y ** 2) + np.exp(- (x + 1) ** 2 - y ** 2)


    x = np.arange(-10, 10, 0.1)
    y = np.arange(-10, 10, 0.1)

    x, y = np.meshgrid(x, y)
    f = test_function(x, y)


    # f = fits.getdata('/home/lzawbrito/PythonProjects/clummp/testdata/acisf15117N002_full_img2.fits')

    paths = get_level_curves(f, 10, show_plot=True)

    print('COM: ', get_com(np.transpose(paths[-1]['paths'][0].vertices)))

    path1 = np.transpose(paths[-1]['paths'][0].vertices)
    path2 = np.transpose(paths[-1]['paths'][1].vertices)

    print('COM distance: ', get_com_distance(path1, path2))


    path1 = np.transpose(paths[-2]['paths'][0].vertices)
    path2 = np.transpose(paths[-3]['paths'][0].vertices)
    print('Steepness:', get_steepness(path1, path2))


