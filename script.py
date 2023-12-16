import datetime as dt
import pandas as pd

def get_excel_serial_date(datetime_in):
    secs_per_day = 60 * 60 * 24
    excel_start_date = dt.datetime(1899, 12, 30)  # Note not 31st Dec but 30th!
    offset = datetime_in - excel_start_date
    return float(offset.days) + (float(offset.seconds) / secs_per_day)

fp = '...filepath....'
fn_in = '...fn_in...'
fn_out = '...fn_out...'

df = pd.read_csv(
    f"{fp}/{fn_in}",
    header=0,
    dtype={
        'account': str,
        'state': str,
        'postedOn': str,
        'payee': str,
        'usage': str,
        'category': str,
        'tags': str,
        'notes': str,
        'amount': str,
        'action': str,
        'security': str,
        'description': str,
        'quantity': str,
        'price': str,
        'commission': str,
        },
    parse_dates=['postedOn'],
    date_format={'postedOn': '%d/%m/%Y'}
    )


def fill_splits(df, max_recurse=6, recurse_count = 0):
    
    recurse_count += 1

    idx = df[df['account'].isna()].index
    fill_values = df.loc[idx-1, ['account', 'postedOn', 'payee', 'tags', 'notes']]
    fill_values['notes'] = fill_values['notes'].fillna('') + "," + \
        fill_values['postedOn'].dt.strftime('%Y-%m-%d') + ",--SPLIT--"
    fill_values['fill_idx'] = fill_values.index + 1
    fill_values.set_index('fill_idx', inplace=True)
    fill_values.dropna(subset=['account'], inplace=True)
    df.update(fill_values)

    if not(df.loc[df['account'].isna(), ['account']].empty) and recurse_count < max_recurse:
        fill_splits(df, recurse_count=recurse_count)

fill_splits(df)

df.to_csv(
    f"{fp}/{fn_out}",
    index=False,
    date_format='%m/%d/%Y'
)