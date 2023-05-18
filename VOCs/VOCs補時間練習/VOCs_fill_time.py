

from pathlib import Path
import pandas as pd
from datetime import datetime as dtm, timedelta as dtmdt
# read

df = pd.read_csv(r'VOCs監測數據(台大環工_東海測站_PA61)20220623-20230410.csv', 
				 skiprows=[1],
				 parse_dates={'time' : ['StartTime']},
				).set_index('time')

df = df.apply( pd.to_numeric, errors='coerce' ).copy()



df_mean = df.resample('1h').mean()

tm_index = pd.date_range( '2022-04-01', '2023-04-10 2300', freq='1h' )
df_mean_index = df_mean.reindex(tm_index)


# calculate

with (Path() / 'TH.csv').open('r', encoding='utf-8', errors='ignore') as f:
	df_tool = pd.read_csv(f, index_col='SPECIES')


####創建四個空的dataframe，並且時間符合tm_index
df_conc = pd.DataFrame(index=tm_index)
df_OFP  = pd.DataFrame(index=tm_index)
df_SOAP = pd.DataFrame(index=tm_index)
df_LOH  = pd.DataFrame(index=tm_index)

for _ky, _col in df_mean_index.items():

	if _ky not in df_tool.keys(): continue
	

	_par = df_tool[_ky].copy()
	_MW, _MIR, _SOAP, _KOH = _par.loc['MW'], _par.loc['MIR'], _par.loc['SOAP'], _par.loc['KOH']

	_df_MW = ( _col * _MW ).copy()

	df_conc[_ky]  = _col
	df_OFP[_ky]   = _df_MW/48 * _MIR
	df_SOAP[_ky]  = _df_MW/24.5 * _SOAP / 100*0.054
	df_LOH[_ky]   = _df_MW/24.5/_MW * 0.602 *_KOH



Path('data').mkdir(exist_ok=True, parents=True)

df_conc.to_csv( Path('data')/'voc0410.csv' )
df_OFP.to_csv( Path('data')/'OFP0410.csv' )
df_SOAP.to_csv( Path('data')/'SOAP0410.csv' )
df_LOH.to_csv( Path('data')/'LOH0410.csv' )



# appdx
## day
# df_day = df_conc.between_time('07:00','18:00')

# ## night
# df_ngt = df_conc.between_time('19:00','05:00')

