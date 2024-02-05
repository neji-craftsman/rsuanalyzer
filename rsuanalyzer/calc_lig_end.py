from typing import Literal, TypedDict

import numpy as np
from scipy.spatial.transform import Rotation as R


def calc_lig_end(
        lig_type: Literal["RR", "RL", "LR", "LL"], theta: float
        ) -> tuple[np.ndarray, R]:
    """
    Calculate x_ac and rot_ac2 of the ligand.
    x_ac is the position vector of point C2 measured from coordinate 
    system A.
    rot_ac2 is the rotation from coordinate system A to C2.

    Args:
    - lig_type (Literal["RR", "RL", "LR", "LL"]): Rotation directions of
    each of the two C-C bonds. "R" means clockwise, "L" means
    counterclockwise.
    - theta (float): Angle in degrees.

    Returns:
    - x_ac (np.ndarray): Position vector of point C2 measured from 
    coordinate system A.
    - rot_ac2 (R): Rotation from coordinate system A to C2.
    """
    # Validate the input.
    if lig_type not in ("RR", "RL", "LR", "LL"):
        raise ValueError(f"Invalid lig_type: {lig_type}")
    if not 0 <= theta <= 90:
        raise ValueError(f"Invalid theta: {theta}")

    vecs_rots = calc_inner_vecs_and_rots(lig_type, theta)

    x_ac_in_system_a = vecs_rots["x_ab_in_system_a"] + \
        vecs_rots["x_bc_in_system_a"]
    rot_ac = vecs_rots["rot_ab1"] * vecs_rots["rot_b1b2"] \
        * vecs_rots["rot_b2c1"] * vecs_rots["rot_c1c2"]

    return x_ac_in_system_a, rot_ac


class InnerVecsAndRots(TypedDict):
    x_ab_in_system_a: np.ndarray
    x_bc_in_system_a: np.ndarray
    rot_ab1: R
    rot_b1b2: R
    rot_b2c1: R
    rot_c1c2: R


def calc_inner_vecs_and_rots(
        lig_type: Literal["RR", "RL", "LR", "LL"], theta: float
        ) -> InnerVecsAndRots:
    """
    Calculate the inner vectors and rotations of the ligand.

    Args:
    - lig_type (Literal["RR", "RL", "LR", "LL"]): Rotation directions of
    each of the two C-C bonds. "R" means clockwise, "L" means
    counterclockwise.
    - theta (float): Angle in degrees.
    
    Returns:
    - InnerVecsAndRots: Inner vectors and rotations of the ligand: 
    dictionary with the following keys:
        - x_ab_in_system_a (np.ndarray): Position vector of point B 
        measured from coordinate system A.
        - x_bc_in_system_a (np.ndarray): Vector from B to C
        measured from coordinate system A.
        - rot_ab1 (R): Rotation from coordinate system A to B1.
        - rot_b1b2 (R): Rotation from B1 to B2.
        - rot_b2c1 (R): Rotation from B2 to C1.
        - rot_c1c2 (R): Rotation from C1 to C2.
    """
    # j and k represent the rotation directions.
    j, k = lig_type_to_signs(lig_type)
    
    x_ab_in_system_a = np.array([1, 0, 0])
    rot_ab1 = R.from_euler('x', j * theta, degrees=True)
    rot_b1b2 = R.from_euler('z', j * 60, degrees=True)
    rot_b2c1 = R.from_euler('x', k * theta, degrees=True)
    x_bc_in_system_a = (rot_ab1 * rot_b1b2).apply([1, 0, 0])

    if lig_type in ("RR", "LL"):
        # If lig_type is RR or LL, rotate 180 degrees around x-axis
        # in order that the z-axis of coordinates C2 protrudes towards 
        # the "Front" face.
        rot_c1c2 = R.from_euler('x', 180, degrees=True)
    else:
        rot_c1c2 = R.from_euler('x', 0, degrees=True)
    
    return {
        "x_ab_in_system_a": x_ab_in_system_a,
        "x_bc_in_system_a": x_bc_in_system_a,
        "rot_ab1": rot_ab1,
        "rot_b1b2": rot_b1b2,
        "rot_b2c1": rot_b2c1,
        "rot_c1c2": rot_c1c2
    }
    

def lig_type_to_signs(
        lig_type: Literal["RR", "RL", "LR", "LL"]) -> tuple[int, int]:
    """
    Convert the conformation ID to the signs of the rotation directions.

    Args:
    - lig_type (Literal["RR", "RL", "LR", "LL"]): Conformation ID of the ligand.

    Returns:
    - tuple[int, int]: Signs of the rotation directions.
    """
    if lig_type == "RR":
        return 1, 1
    elif lig_type == "RL":
        return 1, -1
    elif lig_type == "LR":
        return -1, 1
    elif lig_type == "LL":
        return -1, -1
    else:
        raise ValueError(f"Invalid lig_type: {lig_type}")