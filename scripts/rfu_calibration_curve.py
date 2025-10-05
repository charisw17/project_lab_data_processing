from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from resources.path_util import PATH_DATA_OUT


class RFUGain100Data:
    X = np.array([10000, 1000, 100, 10, 1.0])
    Y = np.array([24919, 3822, 836, 468, 449])


class RFUGain80Data:
    X = np.array([10000, 1000, 100, 10, 1.0]),  # Extract Concentration [µg/mL]
    Y = np.array([26667, 4000, 900, 500, 480])  # Change DATA!!!


@dataclass(frozen=True)
class LinRegResult:
    slope: float
    intercept: float
    r_squared: float
    x: np.array
    y: np.array


def print_lin_reg_result(lin_reg: LinRegResult, name: str = ""):
    print(f"{name} K: {lin_reg.slope:.2f}, D: {lin_reg.intercept:.2f}, R²: {lin_reg.r_squared:.4f}")


def calc_linear_regression(x, y) -> LinRegResult:
    slope, intercept, rvalue, _, _ = linregress(x, y)
    r_squared = rvalue ** 2
    return LinRegResult(slope, intercept, r_squared, x, y)


def sample_cal_data(calibration_data: LinRegResult, x_sample: np.array) -> np.array:
    return calibration_data.slope * x_sample + calibration_data.intercept


def plot_lin_reg_result(lin_reg: LinRegResult, y_fit: np.array):
    plt.scatter(lin_reg.x, lin_reg.y, label='Data', color='blue')
    plt.plot(lin_reg.x, y_fit, label="Fit", color='red')
    plt.xlabel("Weighed-In Concentration [µg/mL]")
    plt.ylabel("RFU Betanin (537, 601)")
    plt.title("Calibration Curve of Betanin Fluorescence")
    plt.text(0.05, 0.95, f"y = {lin_reg.slope:.2f}x + {lin_reg.intercept:.2f}\nR² = {lin_reg.r_squared:.4f}",
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
    plt.legend()
    plt.grid(True)
    plt.savefig(PATH_DATA_OUT / "rfu_calibration_curve.png")
    plt.show()


if __name__ == '__main__':
    gain_100_result = calc_linear_regression(RFUGain100Data.X, RFUGain100Data.Y)
    print_lin_reg_result(gain_100_result, "Gain 100")

    # gain_80_result = calc_linear_regression(RFUGain80Data.X, RFUGain80Data.Y)
    # print_lin_reg_result(gain_80_result, "Gain 80")

    y_fit = sample_cal_data(gain_100_result, RFUGain100Data.X)
    plot_lin_reg_result(gain_100_result, y_fit)
