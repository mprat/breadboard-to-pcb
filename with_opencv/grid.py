from __future__ import division
import cv2
import numpy as np
import matplotlib.pylab as lab
from scipy.ndimage.filters import gaussian_filter
from blob_params import SBD_HOLES

def show(img):
    cv2.imshow('foo', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def rotmat(angle):
    return np.matrix([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])

class BreadboardGrid:
    """
    Abstract class for different kinds of breadboard grids
    """

    def align(self, pt):
        """
        Return (row, col) of the closest point on the grid to pt (given in pixel coords) or None if there is none (e.g. out of bounds)
        """
        raise NotImplementedError

    def draw_fit(self, pt):
        raise NotImplementedError

class ThreeDOFGrid(BreadboardGrid):
    """
    A breadboard grid which has rotational and xy translational freedom, aligned using opencv
    """
    def __init__(self, img):
        """
        get the grid from an opencv2 image object
        """
        self.img = img

        sbd_params = cv2.SimpleBlobDetector_Params()
        for (k, v) in SBD_HOLES.iteritems():
            setattr(sbd_params, k, v)
        sbd = cv2.SimpleBlobDetector(sbd_params)
        keypoints = sbd.detect(img)

        blobs = img.copy()
        for kp in keypoints:
            cv2.circle(blobs, tuple([int(coord) for coord in kp.pt]), 4, 255, 4)

        ###### Identifying the grid spacing #####
        # What we do here is find the distances between all the detected holes in the image. The actual spacing between pins should be the minimum distance observed between holes.

        dists = np.zeros((len(keypoints),len(keypoints)))
        kps = [np.array(p.pt) for p in keypoints]
        for j, pj in enumerate(kps):
            for k, pk in enumerate(kps):
                dists[j,k] = np.linalg.norm(pj - pk)
        upper = np.triu(dists)
        flat = np.array([x for x in upper.reshape((-1,1)) if x > 1])
        n_dist, bins = np.histogram(flat, range=(0,100), bins=400)
        min_spacing = bins[lab.find(np.diff(gaussian_filter(n_dist, 2)) < 0)[0]+1]
        cond = np.where((upper >= min_spacing - 1) * (upper <= min_spacing + 1), 1, 0)
        neighbors = []
        for j, row in enumerate(cond):
            for k, el in enumerate(row):
                if el:
                    # print j, k, keypoints[j].pt, keypoints[k].pt
                    neighbors.append([j, k, keypoints[j].pt, keypoints[k].pt])

        # Draw lines between grid neighbors
        lines = blobs.copy()
        for n in neighbors:
            cv2.line(lines, tuple(map(int, n[2])), tuple(map(int, n[3])), 255)

        # Identify the angle of the grid
        # We find the angle of the grid by looking at the orientation of the lines between adjacent holes in the grid

        angles = np.array([np.arctan2(n[3][1] - n[2][1], n[3][0] - n[2][0]) for n in neighbors])
        angle_step = 0.5
        n_ang, bins = np.histogram((angles % np.pi) * 180 / np.pi, range=(0,180), bins=180./angle_step)


        kernel = np.tile(np.hstack([lab.normpdf(np.array(range(int(45./angle_step))), 0, 10./angle_step), lab.normpdf(np.array(range(int(45./angle_step))), 45./angle_step, 10./angle_step)]), 2)

        angle_fits = np.zeros(int(45./angle_step))
        for t in range(len(angle_fits)):
            angle_fits[t] = np.correlate(np.roll(kernel, t), n_ang)
        grid_angle = (np.argmax(angle_fits) * angle_step + angle_step/2) * np.pi/180
        print grid_angle, grid_angle*180/np.pi

        # Translation of the grid
        # Now we have the spacing and orientation of the grid, so let's find its translation as well. First, let's undo the rotation:
        R = rotmat(-grid_angle)
        kps_rot = [np.array(R * np.reshape(k, (2,-1))) for k in kps]
        # Next, we can find the phase of the x and y position of the grid using mod
        x_mod = [k[0][0] % min_spacing for k in kps_rot]
        y_mod = [k[1][0] % min_spacing for k in kps_rot]
        n_x, bins = np.histogram(x_mod, range=(0,min_spacing), bins=(min_spacing))
        n_y, bins = np.histogram(y_mod, range=(0,min_spacing), bins=(min_spacing))

        grid_orig = np.reshape([np.argmax(gaussian_filter(n_x, 2))+0.5, np.argmax(gaussian_filter(n_y,2))+0.5], (2,-1))

        self.grid_orig = grid_orig
        self.grid_angle = grid_angle
        self.grid_spacing = min_spacing

        # Draw the result
        # self.draw_fit()

    def draw_fit(self):
        Ri = rotmat(self.grid_angle)
        X, Y = lab.meshgrid(range(-50, 50), range(-50, 50))
        X, Y = X * self.grid_spacing + self.grid_orig[0], Y * self.grid_spacing + self.grid_orig[1]
        inferred_grid_pts = np.hstack([np.reshape(X, (-1,1)), np.reshape(Y, (-1,1))])
        inferred_grid_pts = [Ri * np.reshape(p,(-1,1)) for p in inferred_grid_pts]

        with_grid = self.img.copy()
        for p in inferred_grid_pts:
            cv2.circle(with_grid, tuple(p), 4, 200, 4)
        show(with_grid)

    def align(self, pt):
        row, col = self.pt2grid(pt)
        row, col = int(round(row)), int(round(col))
        return row, col

    def pt2grid(self, pt):
        R = rotmat(-self.grid_angle)
        pt_rot = R * np.reshape(pt, (2,1))
        col = (pt_rot[0] - self.grid_orig[0]) / self.grid_spacing
        row = (pt_rot[1] - self.grid_orig[1]) / self.grid_spacing
        return (row, col)

    def grid2pt(self, rc):
        row, col = rc
        pt_rot = np.array([col * self.grid_spacing + self.grid_orig[0], row * self.grid_spacing + self.grid_orig[1]]).reshape((2,1))
        Ri = rotmat(self.grid_angle)
        return Ri * pt_rot

if __name__ == '__main__':
    """
    Generate a grid, then randomly select some points and find their nearest grid locations
    """
    img = cv2.imread('../imgs/breadboard_35.jpg', 0)
    g = ThreeDOFGrid(img)
    x = np.random.random_integers(200,500,30)
    y = np.random.random_integers(200,500,30)
    with_lines = img.copy()
    for i in range(len(x)):
        pt = [x[i], y[i]]
        grid_pt = g.grid2pt(g.align(pt))
        cv2.line(with_lines, tuple(pt), tuple(grid_pt), 255, 2)
        cv2.circle(with_lines, tuple(grid_pt), 3, 0, 2)
    show(with_lines)






