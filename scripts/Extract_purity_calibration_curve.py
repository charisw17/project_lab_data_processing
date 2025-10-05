from dataclasses import dataclass

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

from resources.path_util import PATH_DATA_OUT


class ExtractConcentrationData:
    X = np.array([10000, 5000, 2500, 1000, 500, 250])
    Y = np.array([15.778, 8.327, 4.605, 2.367, 1.568, 1.312])


@dataclass(frozen=True)
class LinRegResult:
    slope: float
    intercept: float
    r_squared: float
    x: np.array
    y: np.array


def print_lin_reg_result(lin_reg: LinRegResult, name: str = ""):
    print(f"{name} K: {lin_reg.slope:.4f}, D: {lin_reg.intercept:.4f}, R²: {lin_reg.r_squared:.4f}")


def calc_linear_regression(x, y) -> LinRegResult:
    slope, intercept, rvalue, _, _ = linregress(x, y)
    r_squared = rvalue ** 2
    return LinRegResult(slope, intercept, r_squared, x, y)


def sample_cal_data(calibration_data: LinRegResult, x_sample: np.array) -> np.array:
    return calibration_data.slope * x_sample + calibration_data.intercept


def plot_lin_reg_result(lin_reg: LinRegResult, y_fit: np.array):
    plt.scatter(lin_reg.x, lin_reg.y, label='Data', color='blue')
    plt.plot(lin_reg.x, y_fit, label="Fit", color='red')
    plt.xlabel("Weighed-In Extract Concentration [µg/mL]")
    plt.ylabel("Measured Betanin Concentration [µg/mL]")
    plt.title("Betanin Content in Beet Root Extract")
    plt.text(0.05, 0.95, f"y = {lin_reg.slope:.4f}x + {lin_reg.intercept:.4}\nR² = {lin_reg.r_squared:.4f}",
             transform=plt.gca().transAxes, fontsize=12, verticalalignment='top')
    plt.legend()
    plt.grid(True)
    plt.savefig(PATH_DATA_OUT / "purity_calibration_curve.png")
    plt.show()


if __name__ == '__main__':
    extract_purity_result = calc_linear_regression(ExtractConcentrationData.X, ExtractConcentrationData.Y)
    print_lin_reg_result(extract_purity_result, "Betanin in Beet Root Extract")

    y_fit = sample_cal_data(extract_purity_result, ExtractConcentrationData.X)
    plot_lin_reg_result(extract_purity_result, y_fit)

extract_purity_result = calc_linear_regression(ExtractConcentrationData.X, ExtractConcentrationData.Y)
BETANIN_PURITY_FACTOR = extract_purity_result.slope
