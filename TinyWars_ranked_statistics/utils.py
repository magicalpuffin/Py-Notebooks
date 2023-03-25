import pandas as pd
from typing import Iterable

def get_co_available_replays(co_name:str, ban_df:pd.DataFrame, replays:Iterable[int]) -> Iterable[int]:
    '''
    Gets list of replays where the CO was available to be picked.
    '''
    available_replays = ban_df[ban_df.index.isin(replays) & 
                               (ban_df['coName'] != co_name)].index.unique()
    return available_replays

def get_co_picked_replays(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int]) -> Iterable[int]:
    '''
    Gets list of replays where the CO was picked.
    '''
    picked_replays = pick_df[pick_df.index.isin(replays) & 
                               (pick_df['coName'] == co_name)].index.unique()
    return picked_replays

def get_co_banned_replays(co_name:str, ban_df:pd.DataFrame, replays:Iterable[int]) -> Iterable[int]:
    '''
    Gets list of replays where the CO was banned.
    '''
    banned_replays = ban_df[ban_df.index.isin(replays) & 
                            (ban_df['coName'] == co_name)].index.unique()
    return banned_replays

def get_co_pick_rate(co_name:str, pick_df:pd.DataFrame, ban_df:pd.DataFrame, replays:Iterable[int]) -> float:
    '''
    Gets the pick rate of a CO when available.
    '''
    picked_replays = get_co_picked_replays(co_name, pick_df, replays)
    available_replays = get_co_available_replays(co_name, ban_df, replays)

    pick_rate = len(picked_replays)/len(available_replays)
    return pick_rate

def get_co_ban_rate(co_name:str, ban_df:pd.DataFrame, replays:Iterable[int]) -> float:
    '''
    Gets the ban rate of a CO.
    '''
    banned_replays = get_co_banned_replays(co_name, ban_df, replays)

    ban_rate = len(banned_replays)/len(replays)
    return ban_rate

def get_co_matchup_total(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int]) -> pd.Series:
    picked_replays = get_co_picked_replays(co_name, pick_df, replays)
    
    co_matchup_total = pick_df.loc[picked_replays, :]['coName'].value_counts()
    co_matchup_total[co_name] = co_matchup_total[co_name] - len(picked_replays)
    co_matchup_total = co_matchup_total.rename("matchupTotal")
    
    return co_matchup_total