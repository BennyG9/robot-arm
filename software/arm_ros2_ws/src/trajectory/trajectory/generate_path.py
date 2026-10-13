import numpy as np

def linear_path(pos1, pos2, res):

    n = int(res * np.linalg.norm(np.array(pos1)-np.array(pos2)))

    path = np.array(
        [
            np.linspace(pos1[0], pos2[0], n, endpoint=True),
            np.linspace(pos1[1], pos2[1], n, endpoint=True),
            np.linspace(pos1[2], pos2[2], n, endpoint=True),
        ]
    )

    return path