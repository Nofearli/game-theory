"""Kalman filters (book Ch. 2 / 2.3)."""
from __future__ import annotations

import numpy as np


class KalmanFilter:
    """Generic linear Kalman filter with known input:

        X^- = A X + B U ;  P^- = A P A^T + Q
        K   = P^- H^T (H P^- H^T + R)^-1
        X   = X^- + K (Z - H X^-) ;  P = (I - K H) P^-
    """

    def __init__(self, A, B, H, Q, R, x0, P0):
        self.A = np.atleast_2d(A).astype(float)
        self.B = np.atleast_2d(B).astype(float) if B is not None else None
        self.H = np.atleast_2d(H).astype(float)
        self.Q = np.atleast_2d(Q).astype(float)
        self.R = np.atleast_2d(R).astype(float)
        self.x = np.asarray(x0, float).reshape(-1, 1)
        self.P = np.atleast_2d(P0).astype(float)

    def predict(self, u=None):
        self.x = self.A @ self.x
        if self.B is not None and u is not None:
            self.x = self.x + self.B @ np.asarray(u, float).reshape(-1, 1)
        self.P = self.A @ self.P @ self.A.T + self.Q
        return self.x.ravel()

    def update(self, z):
        z = np.asarray(z, float).reshape(-1, 1)
        S = self.H @ self.P @ self.H.T + self.R
        K = self.P @ self.H.T @ np.linalg.inv(S)
        self.x = self.x + K @ (z - self.H @ self.x)
        I = np.eye(self.P.shape[0])
        self.P = (I - K @ self.H) @ self.P
        return self.x.ravel()


def constant_velocity_filter(dt, q_acc, r_meas, x0, y0, vx0=0.0, vy0=0.0, P0=None):
    """Constant-velocity model: state [x, y, vx, vy], B = 0 (book 2.3, game version).

    q_acc : process noise on acceleration (scalar)
    r_meas: measurement noise variance (scalar)
    """
    A = np.array([[1, 0, dt, 0],
                  [0, 1, 0, dt],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]], float)
    q = q_acc * np.array([[dt ** 4 / 4, 0, dt ** 3 / 2, 0],
                          [0, dt ** 4 / 4, 0, dt ** 3 / 2],
                          [dt ** 3 / 2, 0, dt ** 2, 0],
                          [0, dt ** 3 / 2, 0, dt ** 2]], float)
    H = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], float)
    R = np.eye(2) * r_meas
    x0 = np.array([x0, y0, vx0, vy0], float)
    P0 = np.eye(4) * 10.0 if P0 is None else P0
    return KalmanFilter(A, None, H, q, R, x0, P0)
