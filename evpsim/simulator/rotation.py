import numpy as np


class LocalFrame:
    def __init__(self, x0_axis: np.ndarray, x1_axis: np.ndarray):
        self._rot_matrix = np.zeros((3, 3))

        self._rot_matrix[:, 0] = x0_axis / np.linalg.norm(x0_axis)
        self._rot_matrix[:, 1] = x1_axis / np.linalg.norm(x1_axis)
        self._rot_matrix[:, 2] = np.cross(
            self._rot_matrix[:, 0], self._rot_matrix[:, 1])

        self._inverse_rot_matrix = self._rot_matrix.T

    def rotate_tensor2_to_material(self, x: np.ndarray) -> np.ndarray:
        return self._inverse_rot_matrix @ x @ self._rot_matrix

    def rotate_tensor2_from_material(self, x: np.ndarray) -> np.ndarray:
        return self._rot_matrix @ x @ self._inverse_rot_matrix

    def rotate_tensor4_from_material(self, x: np.ndarray) -> np.ndarray:

        rot_left = np.einsum(
            "ik,jl->ijkl", self._rot_matrix, self._rot_matrix)

        rot_right = np.einsum(
            "ik,jl->ijkl", self._inverse_rot_matrix, self._inverse_rot_matrix)

        tmp = np.einsum("ijkl,klmn->ijmn", rot_left, x)
        return np.einsum("ijkl,klmn->ijmn", tmp, rot_right)
