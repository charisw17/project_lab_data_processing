import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D


from resources.constants_and_factors import WT, NAME, C_ABS_Sup_Bn, C_RFU_Cellsusp_Bn, \
    C_RFU_Sup_Bn, RFUperOD_Cellsusp_Bn
from resources.path_util import PATH_DATA_OUT, sanitize_filename


# CORRECT NOMENCLATURE FOR PLOTTING
def make_cursive(text: str) -> str:
    return rf"$\mathit{{{text}}}$"


_gut_1_delta_latex = make_cursive("gut1") +  r"$\Delta$"
BSY = "BSY"
gut1d = "gut1d"
BG10 = "BG10"
BG10_GUT1D = BG10 + gut1d
BG11 = "BG11"
BG11_GUT1D = BG11 + gut1d

# Y-AXIS PLOT LABELS
conc_per_OD = "Concentration [µg/mL] normalized to cell density"
rfu_per_OD = "Relative Fluorescence Units normalized to cell density [RFU/OD]"


def correct_nomenclature_for_legend(strain_name: str) -> str:
    strain_name = BSY + strain_name

    if "dgut1" in strain_name:
        raise ValueError("Please convert dgut1 to gut1d")

    if gut1d in strain_name:
        return strain_name.replace(gut1d, _gut_1_delta_latex)
    return strain_name


def get_idx_of_wt(strain_names: list[str]) -> int:
    for i, name in enumerate(strain_names):
        if WT in name:
            return i

    raise ValueError(f"'{WT}' not found in strain_names.")


def move_to_front(lst, index):
    if 0 <= index < len(lst):
        element = lst.pop(index)
        lst.insert(0, element)
    return lst


def remove_strain_name_prefixes(strain_names: list[str]) -> list[str]:
    result = []
    for i, name in enumerate(strain_names):
        if not "_" in name:
            raise ValueError("Strain names must contain an underscore '_' to separate the prefix from the numbering.")

        prefix, numbering = name.split("_", 1)
        result.append(numbering)

    return result


def create_grouped_boxplot_by_wt_and_name(input_df, target_column: str, y_axis_label: str, figsize=(14, 8), annotate_with_median: bool = False, show_overall_mean: bool = False):
    plot_df = input_df.copy()

    wt_order = [BG10, BG11, BG10_GUT1D, BG11_GUT1D]
    wt_colors = {
        BG10: "#a2c24b",  # green
        BG11: "#e58bad",  # pink
        BG10_GUT1D: "#3594cc",  # blue
        BG11_GUT1D: "#a559aa",  # purple
    }

    unique_wts_in_data = plot_df[WT].unique()
    for wt_val in unique_wts_in_data:
        if 'dgut1' in wt_val:
            raise ValueError(f"Found wild type: {wt_val} - Please convert dgut1 to gut1d")


        if wt_val not in wt_colors:
            raise ValueError(f"Unexpected WT value '{wt_val}' found in data. Please add it to the 'wt_order' list.")

    plot_data = []
    box_colors = []
    box_labels = []
    positions = []

    # Define spacing and calculate positions
    within_group_gap = 1.0  # Adjust for spacing inside a group
    between_group_gap = 2.0  # Adjust for spacing between groups
    current_pos = 0.0

    for wt_val in wt_order:
        wt_subset = plot_df[plot_df[WT] == wt_val]
        if wt_subset.empty:
            continue

        sorted_names = sorted(wt_subset[NAME].unique())
        index_of_wt = get_idx_of_wt(sorted_names)
        move_to_front(sorted_names, index_of_wt)
        names_in_plot = remove_strain_name_prefixes(sorted_names)

        for i, name in enumerate(sorted_names):
            name_subset = wt_subset[wt_subset[NAME] == name]
            # plot_data.append(name_subset[target_column].dropna())
            data_for_plot = name_subset[target_column].dropna()

            if data_for_plot.empty:  # added check for empty data
                print(f"Warning: Skipping group (WT='{wt_val}', NAME='{name}') as it contains no valid data points!")
                continue

            plot_data.append(data_for_plot)
            box_labels.append(names_in_plot[i])
            box_colors.append(wt_colors[wt_val])
            positions.append(current_pos)
            current_pos += within_group_gap

        current_pos += between_group_gap - within_group_gap

    if not plot_data:
        print(f"Warning: No data available to plot for target column '{target_column}'.")
        return

    plt.figure(figsize=figsize)
    ax = plt.gca()

    bp = ax.boxplot(plot_data, patch_artist=True, tick_labels=box_labels, positions=positions)

    if annotate_with_median:
        medians = [float(d.median()) for d in plot_data]
        ymin, ymax = ax.get_ylim()
        offset = 0.02 * (ymax - ymin)
        for x, median in zip(positions, medians):
            ax.text(x, median + offset, f"{median:.3f}", ha='center', va='bottom', fontsize=9)

    for patch, color in zip(bp['boxes'], box_colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    # set color for median line
    for median in bp['medians']:
        median.set_color('black')

    # Add vertical grid lines at each boxplot position
    for pos in positions:
        ax.axvline(x=pos, color='lightgray', linestyle='--', alpha=0.5, zorder=0)

    # Add horizontal line at y=0
    plt.axhline(y=0, color='gray', linestyle='-', linewidth=1)

    # Add shaded area below y=0
    ax.fill_between([min(positions) - 1, max(positions) + 1], y1=0, y2=ax.get_ylim()[0], color='gray', alpha=0.3)

    # Overall mean line across all plotted data
    if show_overall_mean:
        overall_mean = float(pd.concat(plot_data).mean())
        ax.axhline(y=overall_mean, color='red', linestyle=':', linewidth=1.5)
        # optional small label near left axis
        xmin, _ = ax.get_xlim()
        ax.text(xmin, overall_mean, f"Mean={overall_mean:.3f}", va='bottom', ha='left', fontsize=9, color='red')

    # LABELS AND TITLES
    plt.ylabel(f"{y_axis_label} ")
    plt.title(f"{target_column}")
    plt.xticks(rotation=45, ha='right')

    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, alpha=0.7, label=correct_nomenclature_for_legend(wt))
        for wt, color in wt_colors.items() if wt in unique_wts_in_data]
    if show_overall_mean:
        legend_elements.append(Line2D([0], [0], color='red', linestyle=':', linewidth=1.5, label='Overall mean'))
    plt.legend(handles=legend_elements, title="Strain Background", bbox_to_anchor=(0.5, -0.1), loc='upper center', ncol=4)

    ax.margins(x=0.01)
    plt.tight_layout()

    sanitized_filename = sanitize_filename(target_column)
    plt.savefig(PATH_DATA_OUT / f"{sanitized_filename}.svg")

    plt.show()  # displays fig and clears current figure buffer --> need to save first!


if __name__ == "__main__":
    df = pd.read_excel(PATH_DATA_OUT / "outlier_removed_df.xlsx")
    create_grouped_boxplot_by_wt_and_name(df, target_column=C_ABS_Sup_Bn, y_axis_label=conc_per_OD)
    create_grouped_boxplot_by_wt_and_name(df, target_column=C_RFU_Cellsusp_Bn, y_axis_label=conc_per_OD)      #using cell-free calibration for cellsuspension samples is nonsense!
    create_grouped_boxplot_by_wt_and_name(df, target_column=C_RFU_Sup_Bn, y_axis_label=conc_per_OD)

    create_grouped_boxplot_by_wt_and_name(df, target_column=RFUperOD_Cellsusp_Bn, y_axis_label=rfu_per_OD)

