import pandas as pd
from sectionproperties.pre.library import steel_sections as steel
import sectionproperties.pre.geometry as geom
import pathlib


def create_sp_section(section_record: pd.Series) -> geom.Geometry:
    """
    Returns a section from section_record
    """
    HSS_DIMS = {"b": "B", "d": "Ht", "t": "tdes", "r_out": None}
    W_DIMS = {"b": "bf", "d": "d", "t_f": "tf", "t_w": "tw", "r": None}
    section = None
    if section_record.Type == "HSS":
        d = section_record[HSS_DIMS['d']]
        b = section_record[HSS_DIMS['b']]
        t = section_record[HSS_DIMS['t']]
        r_out = 2 * t
        section = steel.rectangular_hollow_section(d=d, b=b, t=t, r_out=r_out, n_r=12)
    elif section_record.Type == "W":
        d = section_record[W_DIMS['d']]
        b = section_record[W_DIMS['b']]
        t_f = section_record[W_DIMS['t_f']]
        t_w = section_record[W_DIMS['t_w']]
        k = section_record['kdes']
        r = k - t_f
        section = steel.i_section(d=d, b=b, t_f=t_f, t_w=t_w, r=r, n_r = 12)
    else:
        print(f"Section name of {section_record.Type} is not implemented yet.")
    return section
            

def load_aisc_db(units = 'si') -> pd.DataFrame:
    """
    Returns a DataFrame of the AISC database table contained in the file.
    """
    if units.lower() == 'si':
        si_file_name = pathlib.Path(__file__).parent / 'aisc_db_si.csv'
        return pd.read_csv(si_file_name)
    elif units.lower() == 'us':
        us_file_name = pathlib.Path(__file__).parent / 'aisc_db_us.csv'
        return pd.read_csv(us_file_name)
    else:
        print("Acceptable units are either 'us' or 'si'")
        
        
def sections_by_type(aisc_db: pd.DataFrame, section_type: str) -> pd.DataFrame:
    """
    Returns df with sections of that type
    """
    return aisc_db.loc[aisc_db.Type == section_type]


def values_greater_than(aisc_db: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Returns filtered df a
    """
    sub_df = aisc_db.copy()
    for key, value in kwargs.items():
        sub_df = sub_df.loc[sub_df[key] >= value]
        if sub_df.empty:
            print(f"No records match all of the parameters: {kwargs}")
    return sub_df


def values_less_than(aisc_db: pd.DataFrame, **kwargs) -> pd.DataFrame:
    """
    Returns filtered
    """
    sub_df = aisc_db.copy()
    for key, value in kwargs.items():
        sub_df = sub_df.loc[sub_df[key] <= value]
        if sub_df.empty:
            print(f"No records match all of the parameters: {kwargs}")
    return sub_df


def sort_by_weight(aisc_db: pd.DataFrame) -> pd.DataFrame:
    """
    Returns sorted df
    """
    aisc_db = aisc_db.sort_values("W")
    return aisc_db