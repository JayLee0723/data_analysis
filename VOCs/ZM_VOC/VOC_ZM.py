# -*- coding: utf-8 -*-
"""
Created on Mon Nov 21 12:17:50 2022

@author: ajay0
"""


from pandas import ExcelWriter

import numpy as np
import pandas as pd
from datetime import datetime as dtm
from pandas import date_range, DataFrame
from pathlib import Path



df_all = pd.read_csv(r"C:\Users\ajay0\Desktop\期中報告\csv\忠明\忠明0401-0131.csv",parse_dates=['TIME']).set_index('TIME')
df_all = df_all.loc[~df_all.index.duplicated()].reindex(pd.date_range(*df_all.index[[0,-1]],freq='1h'))

df_index = pd.read_csv(r"C:\Users\ajay0\Desktop\期中報告\csv\忠明\VOC_tool.csv").set_index('SPECIES')
ext = pd.read_csv(r"C:\Users\ajay0\Desktop\期中報告\csv\忠明\2022大表數據 - Optical.csv",parse_dates=['Time']).set_index('Time').reindex(df_all.index)['ext']


####補時間
season = {
			'spr_2022' : (dtm(2022,4,1),dtm(2022,5,27,23)),
			'sum_2022' : (dtm(2022,5,28),dtm(2022,8,31,23)),
			'sum-aut_2022' : (dtm(2022,9,1),dtm(2022,10,8,23)),
			'aut_2022' : (dtm(2022,10,9),dtm(2022,12,15,23)),
			'win_2022' : (dtm(2022,12,16),dtm(2022,12,31,23)),
	
	}





for _sea, _time in season.items():
	
	path_dt = Path(f'data_{_sea}')
	path_dt.mkdir(exist_ok=True)
	path_plot_dt = path_dt/'plot_dt'
	path_plot_dt.mkdir(exist_ok=True)
	path_plot_dt_bar = path_dt/'plot_dt_bar'
	path_plot_dt_bar.mkdir(exist_ok=True)

	
	f = ExcelWriter(path_dt/f'VOC_{_sea}.xlsx')
	
	print(_sea)
	start, end = _time
	all_time_indx = pd.date_range(start,end,freq='1h')
	all_time_indx.name = 'TIME'
	
	df = df_all.reindex(all_time_indx).copy()	
	ext_sea = ext.reindex(all_time_indx).copy()
	
	clean_indx = ext_sea.where(ext_sea<=ext_sea.quantile(0.1)).dropna().index
	event_indx = ext_sea.where(ext_sea>=ext_sea.quantile(0.9)).dropna().index
	
	#### process
	OFP = df[df_index.keys()]*df_index.loc['MW',:]/48*df_index.loc['MIR',:]
	SOAP = df[df_index.keys()]*df_index.loc['MW',:]/24.5*df_index.loc['SOAP',:]/100*0.054
	LOH = df[df_index.keys()]*df_index.loc['MW',:]/24.5/df_index.loc['MW',:]*0.602*df_index.loc['KOH',:]

	## mean dataframe process
	dt_type = {
				"Conc" : df,
				"OFP" : OFP,
				"SOAP" : SOAP,
				"LOH" : LOH,
		}
	
	
	for _type, _df in dt_type.items():
		df_mean = pd.DataFrame(index=all_time_indx)
	
		df_mean['alkane_total'] = _df[['Ethane','Propane','Isobutane','n-Butane','Cyclopentane','Isopentane','n-Pentane','2,2-Dimethylbutane','2,3-Dimethylbutane'
								 ,'2-Methylpentane','3-Methylpentane','n-Hexane','Methylcyclopentane','2,4-Dimethylpentane','Cyclohexane','2-Methylhexane'
								 ,'2-Methylhexane','3-Methylheptane','2,2,4-Trimethylpentane','n-Heptane','Methylcyclohexane','2,3,4-Trimethylpentane'
								 ,'2-Methylheptane','3-Methylhexane','n-Octane','n-Nonane','n-Decane','n-Undecane']].sum(axis=1,min_count=1)
		
		df_mean['alkene_total'] = _df[['Ethylene','Propylene','t-2-Butene','1-Butene','cis-2-Butene','t-2-Pentene','1-Pentene','cis-2-Pentene'
								 ,'isoprene']].sum(axis=1,min_count=1)
		
		df_mean['alkyne_total'] = _df[['Acetylene']].sum(axis=1,min_count=1)
		
		df_mean['aromatic_total'] = _df[['Benzene','Toluene','Ethylbenzene','m,p-Xylene','Styrene','o-Xylene','Isopropylbenzene','n-Propylbenzene'
								   ,'m-Ethyltoluene','p-Ethyltoluene','1,3,5-Trimethylbenzene','o-Ethyltoluene','1,2,4-Trimethylbenzene'
								   ,'1,2,3-Trimethylbenzene','m-Diethylbenzene','p-Diethylbenzene']].sum(axis=1,min_count=1)
		
		df_mean['Total'] = _df[['Ethane','Propane','Isobutane','n-Butane','Cyclopentane','Isopentane','n-Pentane','2,2-Dimethylbutane','2,3-Dimethylbutane'
								 ,'2-Methylpentane','3-Methylpentane','n-Hexane','Methylcyclopentane','2,4-Dimethylpentane','Cyclohexane','2-Methylhexane'
								 ,'2-Methylhexane','3-Methylheptane','2,2,4-Trimethylpentane','n-Heptane','Methylcyclohexane','2,3,4-Trimethylpentane'
								 ,'2-Methylheptane','3-Methylhexane','n-Octane','n-Nonane','n-Decane','n-Undecane','Ethylene','Propylene','t-2-Butene','1-Butene','cis-2-Butene','t-2-Pentene','1-Pentene','cis-2-Pentene'
								  ,'isoprene','Acetylene','Benzene','Toluene','Ethylbenzene','m,p-Xylene','Styrene','o-Xylene','Isopropylbenzene','n-Propylbenzene'
								        ,'m-Ethyltoluene','p-Ethyltoluene','1,3,5-Trimethylbenzene','o-Ethyltoluene','1,2,4-Trimethylbenzene'
										   ,'1,2,3-Trimethylbenzene','m-Diethylbenzene','p-Diethylbenzene']].sum(axis=1,min_count=1)
		
		
		## classify
		df_mean_clean = df_mean.loc[clean_indx].reindex(all_time_indx).copy()
		df_mean_event = df_mean.loc[event_indx].reindex(all_time_indx).copy()
		
		_df_clean = _df.loc[clean_indx].reindex(all_time_indx)
		_df_event = _df.loc[event_indx].reindex(all_time_indx)

		## plot data table
		concat_lst=[df_mean.mean(),df_mean_clean.mean(),df_mean_event.mean(),
					df_mean.std(),df_mean_clean.std(),df_mean_event.std(),	
					]
		
		plot_data = pd.concat(concat_lst,axis=1)
		plot_data.columns = ['total_mean','clean_mean','event_mean','total_std','clean_std','event_std',]
		plot_data.index.name = 'species'
		
		## plot data bar
		plot_data_bar = pd.DataFrame()
		_df_sort = _df.mean().dropna().sort_values()[-10:]
		_df_sort_std = _df.std().dropna().sort_values()[-10:]
		_df_clean_sort = _df_clean.mean().dropna().sort_values()[-10:]
		_df_clean_sort_std = _df_clean.std().dropna().sort_values()[-10:]
		_df_event_sort = _df_event.mean().dropna().sort_values()[-10:]
		_df_event_sort_std = _df_event.std().dropna().sort_values()[-10:]
		
		plot_data_bar['total_species'] = _df_sort.index
		plot_data_bar['total_conc'] = _df_sort.values
		plot_data_bar['total_std'] = _df_sort_std.values
		plot_data_bar['clean_species'] = _df_clean_sort.index
		plot_data_bar['cleanl_conc'] = _df_clean_sort.values
		plot_data_bar['cleanl_std'] = _df_clean_sort_std.values
		plot_data_bar['event_species'] = _df_event_sort.index
		plot_data_bar['event_conc'] = _df_event_sort.values
		plot_data_bar['event_std'] = _df_event_sort_std.values

		
		## output data
		_df.to_excel(f,sheet_name=f'{_type}')
		df_mean.to_excel(f,sheet_name=f'{_type}_mean')		
		_df_clean.to_excel(f,sheet_name=f'{_type}_clen')
		df_mean_clean.to_excel(f,sheet_name=f'{_type}_mean_clean')	
		_df_event.to_excel(f,sheet_name=f'{_type}_event')
		df_mean_event.to_excel(f,sheet_name=f'{_type}_mean_event')	
		
		plot_data.to_csv(path_plot_dt/f'plot_data_{_type}_{_sea}.csv')
		plot_data_bar.to_csv(path_plot_dt_bar/f'plot_data_bar_{_type}_{_sea}.csv')


	f.close()
















