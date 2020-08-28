"""
This module contains some covenient methods to get roll decay results from the DB
"""
import pandas as pd

import data
from sqlalchemy import create_engine
from mdldb.mdl_db import MDLDataBase
import signal_lab.mdl_to_evaluation
import rolldecay
import os

sql_template = """
SELECT * from
%s
INNER JOIN run
ON %s.run_id == run.id
    INNER JOIN projects
    ON run.project_number==projects.project_number
        INNER JOIN loading_conditions
        ON (run.loading_condition_id == loading_conditions.id)
            INNER JOIN models
            ON run.model_number == models.model_number
                INNER JOIN ships
                ON models.ship_name == ships.name
        
"""

engine = create_engine('sqlite:///' + data.mdl_db_path)

def load(rolldecay_table_name='rolldecay_direct_improved',sql=None,only_latest_runs=True, limit_score=0.96,
         include_softmooring=False, exclude_table_name=None):


    db = get_db()

    if sql is None:
        sql = sql_template % (rolldecay_table_name, rolldecay_table_name)

    df_rolldecay = pd.read_sql(sql, con=engine, index_col='run_id', )
    df_rolldecay = df_rolldecay.loc[:, ~df_rolldecay.columns.duplicated()]

    mask = df_rolldecay['score'] > limit_score
    df_rolldecay = df_rolldecay.loc[mask]

    if not include_softmooring:
        mask = df_rolldecay['Körfallstyp']!='Rak bana'
        df_rolldecay = df_rolldecay.loc[mask]

    if only_latest_runs:
        by = ['model_number', 'loading_condition_id', 'ship_speed']
        df_rolldecay = df_rolldecay.groupby(by=by).apply(func=get_latest)
        df_rolldecay.drop(columns = by, inplace=True)
        df_rolldecay.reset_index(inplace=True)
        df_rolldecay.set_index('run_id', inplace=True)

    if not exclude_table_name is None:
        df_exclude = pd.read_sql_table(table_name=exclude_table_name,con=engine, index_col='run_id',)
        common_index = list(set(df_rolldecay.index) - set(df_exclude.index))
        df_rolldecay=df_rolldecay.loc[common_index].copy()

    return df_rolldecay

def get_db():
    db = MDLDataBase(engine=engine)
    return db

def get_latest(group):
    """
    Get the latest run in this group:
    """
    s = group.sort_values(by=['date','run_number'], ascending=False).iloc[0]
    s['run_id'] = s.name
    return s

def load_run(db_run, load_temp=True, save_temp=True, save_as_example=False):

    if save_as_example:
        other_save_directory = os.path.join(rolldecay.data_path,'example_data')
    else:
        other_save_directory = None

    ascii_file = db_run.load(load_temp=load_temp, save_temp=save_temp, other_save_directory=other_save_directory)
    df_raw = ascii_file.channels

    df = signal_lab.mdl_to_evaluation.do_transforms(df=df_raw)
    df.rename(columns={'MA/Roll': 'phi'}, inplace=True)

    return df
