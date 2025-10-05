import enum

# Table Headers
WELL = "Well"
DWP = "DWP"
NAME = "Strain Name"
OLDNAME = "Original Name"
ID = "Well-ID"
WT = "WT"
CELLSUSP_DF = "Cellsuspension DilutionFactor"
CELLSUSP_OD = "Cellsuspension OD600"
CELLSUSP_RFU_Bn = "Cellsuspension RFU_(537,601)"
CELLSUSP_RFU_Bl = "Cellsuspension RFU_(390,460)"
CELLSUSP_RFU_Bx = "Cellsuspension RFU_(470,551)"
CELLSUSP_ABS_Bn = "Cellsuspension Abs_536 nm"
CELLSUSP_ABS_Bl = "Cellsuspension Abs_424"
SUP_DF = "Supernatant DilutionFactor"
SUP_OD = "Supernatant OD600"
SUP_RFU_Bn = "Supernatant RFU_(537,601)"
SUP_RFU_Bl = "Supernatant RFU_(390,460)"
SUP_RFU_Bx = "Supernatant RFU_(470,551)"
SUP_ABS_Bn = "Supernatant Abs_536 nm"
SUP_ABS_Bl = "Supernatant Abs_424"

STERILE = "\(sterile\)"

metadata_cols = [WELL, DWP, NAME, OLDNAME, ID, WT]
cellsusp_data_cols = [CELLSUSP_OD, CELLSUSP_RFU_Bn, CELLSUSP_RFU_Bl, CELLSUSP_RFU_Bx, CELLSUSP_ABS_Bn,
                      CELLSUSP_ABS_Bl]  # excl. DF
sup_data_cols = [SUP_OD, SUP_RFU_Bn, SUP_RFU_Bl, SUP_RFU_Bx, SUP_ABS_Bn, SUP_ABS_Bl]  # excl. DF
all_data_cols = [CELLSUSP_DF] + cellsusp_data_cols + [SUP_DF] + sup_data_cols


_betanin_concentration = "Betanin Concentration"
_cell_susp = "Cell Suspension"
# C_ABS_Cellsusp_Bn = f"{_betanin_concentration} in {_cell_susp} via Abs [µg/mL] (NONSENSE! MEASURES CELL DENSITY)"
C_ABS_Cellsusp_Bl = f"Betalamic Acid Concentration in {_cell_susp} via Abs [µg/mL]"
C_RFU_Cellsusp_Bn = f"{_betanin_concentration} in {_cell_susp} via RFU [µg/mL]"
# C_RFU_Cellsusp_Bl = f"Betalamic Acid Concentration in {_cell_susp} via RFU [µg/mL] (NONSENSE! NO BL STANDARD!)"

C_ABS_Sup_Bn = f"{_betanin_concentration} in Supernatant via Abs [µg/mL]"
C_ABS_Sup_Bl = "Betalamic Acid Concentration in Supernatant via Abs [µg/mL]"
C_RFU_Sup_Bn = f"{_betanin_concentration} in Supernatant via RFU [µg/mL]"

CONCENTRATION_RESULT_COLS = [C_ABS_Cellsusp_Bl, C_RFU_Cellsusp_Bn, C_ABS_Sup_Bn, C_ABS_Sup_Bl, C_RFU_Sup_Bn]

# C_RFU_Sup_Bl = "Betalamic Acid Concentration in Supernatant via RFU [µg/mL] (NONSENSE! NO BL STANDARD!)"


MG_TO_UG_FACTOR = 1000

# Extinction Coefficients [L/(mol*cm)]
EXTINCTION_COEFF_BL = 24000  # Betalamic Acid
EXTINCTION_COEFF_BN = 65000  # Betanin
EXTINCTION_COEFF_BD = 54000  # Betanidin

# Molecular Weights [g/mol]
MW_BL = 211.2  # Betalamic Acid
MW_BN = 550.5  # Betanin
MW_BD = 388.3  # Betanidin

# Pathlength [cm]
PATHLENGTH = 0.594  # for 200µL Volume in MTP, measured without pathlength correction.

# Gain 100:
LIN_REG_K_BN = 2.43
LIN_REG_D_BN = 702.31

PLATE_READER_THRESHOLD = 0.1


class Compound(enum.Enum):
    BETANINE = "Betanin"
    BETALAMIC_ACID = "Betalamic Acid"
    BETANIDIN = "Betanidin"


COMPOUND_COEFFS = {
    Compound.BETANINE: (EXTINCTION_COEFF_BN, MW_BN),
    Compound.BETALAMIC_ACID: (EXTINCTION_COEFF_BL, MW_BL),
    Compound.BETANIDIN: (EXTINCTION_COEFF_BD, MW_BD)
}
