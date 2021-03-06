import pandas as pd
from utils import *
import database


def process_trr():
    df = database.download('trr_trr_refresh')

    # convert columns to integers
    df['beat'] = to_int(df['beat'])
    df['officer_birth_year'] = to_int(df['officer_birth_year'])
    df['officer_age'] = to_int(df['officer_age'])
    df['subject_birth_year'] = to_int(df['subject_birth_year'])
    df['subject_age'] = to_int(df['subject_age'])

    # convert columns to booleans
    to_bool(df, 'officer_on_duty')
    to_bool(df, 'officer_injured')
    to_bool(df, 'officer_in_uniform')
    to_bool(df, 'subject_armed')
    to_bool(df, 'subject_injured')
    to_bool(df, 'subject_alleged_injury')
    to_bool(df, 'notify_oemc')
    to_bool(df, 'notify_district_sergeant')
    to_bool(df, 'notify_op_command')
    to_bool(df, 'notify_det_division')

    # reconcile races of subject and officer
    reconcile_race(df, 'subject_race')
    reconcile_race(df, 'officer_race')

    # convert to datetime
    process_timestamp(df, 'trr_datetime')
    process_timestamp(df, 'trr_created')

    # remove redacted
    df['officer_appointed_date'].replace('REDACTED', None, inplace=True)
    # convert to dates
    df['officer_appointed_date'] = pd.to_datetime(df['officer_appointed_date'])
    # convert back to string
    df['officer_appointed_date'] = df['officer_appointed_date'].dt.strftime('%Y-%m-%d')

    # capitalize first name
    df['officer_first_name'] = df['officer_first_name'].str.title()
    # capitalize last name
    df['officer_last_name'] = df['officer_last_name'].str.title()
    # extract suffix from last name
    process_suffix(df, 'officer_last_name', 'officer_suffix_name')

    # cleanup subject gender
    df['subject_gender'].replace('MALE', 'M', inplace=True)
    df['subject_gender'].replace('FEMALE', 'F', inplace=True)

    # cleanup subject birth year
    df['subject_birth_year'] = to_int(df['subject_birth_year'])
    df['subject_birth_year'] = df['subject_birth_year'].apply(reconcile_subject_birth_year)

    # cleanup indoor or outdoor
    df['indoor_or_outdoor'].replace('OUTDOOR', 'Outdoor', inplace=True)
    df['indoor_or_outdoor'].replace('INDOOR', 'Indoor', inplace=True)

    # convert locations and streets to capital case
    df['street'] = df['street'].str.title()
    df['location'] = df['location'].str.title()
    # formatting of locations
    df['location'].replace('Cha Parking Lot / Grounds', 'Cha Parking Lot/Grounds', inplace=True)
    df['location'].replace('Cha Hallway / Stairwell / Elevator', 'Cha Hallway/Stairwell/Elevator', inplace=True)
    df['location'].replace('Church / Synagogue / Place Of Worship', 'Church/Synagogue/Place Of Worship', inplace=True)
    df['location'].replace('College / University - Grounds', 'College/University Grounds', inplace=True)
    df['location'].replace('Cta Parking Lot / Garage / Other Property', 'Cta Garage / Other Property', inplace=True)
    df['location'].replace('School - Private Building', 'School, Private, Building', inplace=True)
    df['location'].replace('School - Private Grounds', 'School, Private, Grounds', inplace=True)
    df['location'].replace('School - Public Building', 'School, Public, Building', inplace=True)
    df['location'].replace('School - Public Grounds', 'School, Public, Grounds', inplace=True)
    df['location'].replace('Medical / Dental Office', 'Medical/Dental Office', inplace=True)
    df['location'].replace('Hospital Building / Grounds', 'Hospital Building/Grounds', inplace=True)
    df['location'].replace('Hotel / Motel', 'Hotel/Motel', inplace=True)
    df['location'].replace('Highway / Expressway', 'Highway/Expressway', inplace=True)
    df['location'].replace('Lakefront / Waterfront / Riverbank', 'Lakefront/Waterfront/Riverbank', inplace=True)
    df['location'].replace('Movie House / Theater', 'Movie House/Theater', inplace=True)
    df['location'].replace('Nursing / Retirement Home', 'Nursing Home/Retirement Home', inplace=True)
    df['location'].replace('Vehicle - Commercial', 'Vehicle-Commercial', inplace=True)
    df['location'].replace('Vehicle - Other Ride Share Service (Lyft, Uber, Etc.)', 'Vehicle - Other Ride Service', inplace=True)
    df['location'].replace('Vacant Lot / Land', 'Vacant Lot/Land', inplace=True)
    df['location'].replace('Tavern / Liquor Store', 'Tavern/Liquor Store', inplace=True)
    df['location'].replace('Parking Lot / Garage (Non Residential)', 'Parking Lot/Garage(Non.Resid.)', inplace=True)
    df['location'].replace('Police Facility / Vehicle Parking Lot', 'Police Facility/Veh Parking Lot', inplace=True)
    df['location'].replace('Sports Arena / Stadium', 'Sports Arena/Stadium', inplace=True)
    df['location'].replace('Residence - Garage', 'Residence-Garage', inplace=True)
    df['location'].replace('Residence - Porch / Hallway', 'Residence Porch/Hallway', inplace=True)
    df['location'].replace('Residence - Yard (Front / Back)', 'Residential Yard (Front/Back)', inplace=True)
    df['location'].replace('Factory / Manufacturing Building', 'Factory/Manufacturing Building', inplace=True)
    df['location'].replace('Government Building / Property', 'Government Building/Property', inplace=True)
    df['location'].replace('Other (Specify)', 'Other', inplace=True)
    df['location'].replace('Other Railroad Property / Train Depot', 'Other Railroad Prop / Train Depot', inplace=True)
    df['location'].replace('Airport Parking Lot', 'Parking Lot/Garage(Non.Resid.)', inplace=True)

    return df


def process_trrstatus():
    df = database.download('trr_trrstatus_refresh')

    # convert officer birth year to int
    df['officer_birth_year'] = to_int(df['officer_birth_year'])

    # convert to datetime
    process_timestamp(df, 'status_datetime')
    # remove redacted
    df['officer_appointed_date'].replace('REDACTED', None, inplace=True)
    # convert to dates
    df['officer_appointed_date'] = pd.to_datetime(df['officer_appointed_date'])
    # convert back to string
    df['officer_appointed_date'] = df['officer_appointed_date'].dt.strftime('%Y-%m-%d')

    df['officer_first_name'] = df['officer_first_name'].str.title()
    df['officer_last_name'] = df['officer_last_name'].str.title()
    # extract suffix from last name
    process_suffix(df, 'officer_last_name', 'officer_suffix_name')

    # reconcile officer races
    reconcile_race(df, 'officer_race')

    return df


def process_weapondischarge():
    df = database.download('trr_weapondischarge_refresh')
    to_bool(df, 'firearm_reloaded')
    to_bool(df, 'sight_used')

    df = df.rename(columns={'trr_report_id': 'trr_id'})
    cols = [
        'weapon_type',
        'weapon_type_description',
        'firearm_make',
        'firearm_model',
        'firearm_barrel_length',
        'firearm_caliber',
        'total_number_of_shots',
        'firearm_reloaded',
        'number_of_cartridge_reloaded',
        'handgun_worn_type',
        'handgun_drawn_type',
        'method_used_to_reload',
        'sight_used',
        'protective_cover_used',
        'discharge_distance',
        'object_struck_of_discharge',
        'discharge_position',
        'trr_id'
    ]

    df = df[cols]
    return df


def process_actionresponse():
    df = database.download('trr_actionresponse_refresh')
    df = df.rename(columns={'trr_report_id': 'trr_id'})
    cols = ['person', 'resistance_type', 'action', 'other_description', 'trr_id']
    df = df[cols]
    return df


def process_charge():
    df = database.download('trr_charge_refresh')
    df = df.rename(columns={'trr_report_id': 'trr_id'})
    cols = ['statute', 'description', 'subject_no', 'trr_id']
    df = df[cols]
    return df


def process_subjectweapon():
    df = database.download('trr_subjectweapon_refresh')
    df = df.rename(columns={'trr_report_id': 'trr_id'})
    cols = ['weapon_type', 'firearm_caliber', 'weapon_description', 'trr_id']
    df = df[cols]
    return df
