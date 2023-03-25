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
    '''
    Gets the count of total matchups against other CO.
    '''
    picked_replays = get_co_picked_replays(co_name, pick_df, replays)
    
    co_matchup_total = pick_df.loc[picked_replays, :]['coName'].value_counts()
    # Correct for mirror matchups
    co_matchup_total[co_name] = co_matchup_total[co_name] - len(picked_replays)
    co_matchup_total = co_matchup_total.rename("matchupTotal")
    
    return co_matchup_total


def get_co_matchup_loss(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int], replay_df:pd.DataFrame) -> pd.Series:
    '''
    Gets the count of lost matchups against other CO.
    '''
    picked_replays = get_co_picked_replays(co_name, pick_df, replays)

    picked_replay_df = replay_df.loc[picked_replays, :]
    co_matchup_loss = picked_replay_df[picked_replay_df['winnerCoName'] != co_name]['winnerCoName'].value_counts()
    co_matchup_loss = co_matchup_loss.rename("matchupLoss")

    return co_matchup_loss

def get_co_matchup_win(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int], replay_df:pd.DataFrame) -> pd.Series:
    '''
    Gets the count of won matchups against other CO.
    '''
    # Uses the total matches and losses to find wins.
    co_matchup_total = get_co_matchup_total(co_name, pick_df, replays)
    co_matchup_loss = get_co_matchup_loss(co_name, pick_df, replays, replay_df)

    co_matchup_win = co_matchup_total - co_matchup_loss
    
    # Mirror matches set to 50% win rate
    # Matchups with no loss result in na, corrected to 100% win rate
    co_matchup_win[co_name] = co_matchup_total[co_name]/2
    co_matchup_win[co_matchup_win.isna()] = co_matchup_total[co_matchup_win.isna()]
    
    co_matchup_win = co_matchup_win.rename("matchupWin")

    return co_matchup_win

def get_co_matchup_win_rate(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int], replay_df:pd.DataFrame) -> pd.Series:
    '''
    Gets the win rate of matchups against other CO.
    '''
    co_matchup_total = get_co_matchup_total(co_name, pick_df, replays)
    co_matchup_win = get_co_matchup_win(co_name, pick_df, replays, replay_df)

    co_matchup_winrate = co_matchup_win / co_matchup_total
    co_matchup_winrate = co_matchup_winrate.rename("matchupWinRate")
    
    return co_matchup_winrate

def get_co_matchup_table(co_name:str, pick_df:pd.DataFrame, replays:Iterable[int], replay_df:pd.DataFrame) -> pd.DataFrame:    
    co_matchup_win = get_co_matchup_win(co_name, pick_df, replays, replay_df)
    co_matchup_total = get_co_matchup_total(co_name, pick_df,replays)
    co_matchup_win_rate = get_co_matchup_win_rate(co_name, pick_df, replays, replay_df)

    co_matchup_table = pd.concat([co_matchup_win, co_matchup_total, co_matchup_win_rate], axis=1)
    co_matchup_table.index = co_matchup_table.index.rename(co_name)
    co_matchup_table = co_matchup_table.sort_values(['matchupTotal'], ascending= False)
    
    return co_matchup_table