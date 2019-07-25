import numpy as np
import pandas as pd
import yfinance as yf
#used to grab the stock prices, with IEX api
import pandas_datareader as pdr
from datetime import datetime
#to visualize the results
import matplotlib.pyplot as plt
import seaborn
import time
import os.path
yf.pdr_override()

#select start date for correlation window as well as list of tickers

start_date = '2019-01-01'
end_date = '2019-07-16'
symbols_list = ["TERRNT-B.ST","TE5.F","SAMPO.HE","SAND.ST","SCA-A.ST","SCA-B.ST","SCHO.CO","SEB-A.ST","SEB-C.ST","SECU-B.ST","SHB-A.ST","SHB-B.ST","SIM.CO","SKA-B.ST","SKF-A.ST","SKF-B.ST","SOBI.ST","SPNO.CO","SSAB-A.ST","SSAB-B.ST","SSABAH.HE","SSABBH.HE","STE-A.ST","STE-R.ST","STEAV.HE","STERV.HE","STG.CO","SWEC-A.ST","SWEC-B.ST","SWED-A.ST","SWMA.ST","SYDB.CO","TEL2-A.ST","TEL2-B.ST","TELIA.ST","TELIA1.HE","THULE.ST","TIETO.HE","TIETOS.ST","TIGO-SDB.ST","TOP.CO","TREL-B.ST","TRYG.CO","RBREW.CO","RESURS.ST","RILBA.CO","ROCK-A.CO","ROCK-B.CO","SAA1V.HE","SAAB-B.ST","SAGA-A.ST","SAGA-B.ST","SAGA-D.ST","SAGA-PREF.ST","NOLA-B.ST","NOVO-B.CO","NYF.ST","NZYM-B.CO","ORI.ST","ORNAV.HE","ORNBV.HE","ORSTED.CO","OSSR.CO","OUT1V.HE","PEAB-B.ST","PNDORA.CO","PNDX-B.ST","RATO-A.ST","RATO-B.ST","NDA-DK.CO","NDA-FI.HE","NDA-SE.ST","NENT-A.ST","NENT-B.ST","NESTE.HE","NET-B.ST","NETC.CO","NIBE-B.ST","NLFSK.CO","NOBI.ST","NOKIA.HE","LUN.CO","LUND-B.ST","LUPE.ST","MAERSK-A.CO","MAERSK-B.CO","MAREL.IC","METSA.HE","METSB.HE","METSO.HE","MTG-A.ST","MTG-B.ST","MTRS.ST","NCC-A.ST","NCC-B.ST","JYSK.CO","KBHL.CO","KCR.HE","KEMIRA.HE","KESKOA.HE","KESKOB.HE","KIND-SDB.ST","KINV-A.ST","KINV-B.ST","KLED.ST","KLOV-A.ST","KLOV-B.ST","KLOV-PREF.ST","KNEBV.HE","KOJAMO.HE","LATO-B.ST","LIFCO-B.ST","LOOM-B.ST","LUMI.ST","HUH1V.HE","HUSQ-A.ST","HUSQ-B.ST","ICA.ST","INDT.ST","INDU-A.ST","INDU-C.ST","INTRUM.ST","INVE-A.ST","INVE-B.ST","ISS.CO","JDAN.CO","JM.ST","FSKRS.HE","G4S.CO","GEN.CO","GETI-B.ST","GN.CO","HEMF.ST","HEMF-PREF.ST","HEXA-B.ST","HM-B.ST","HOLM-A.ST","HOLM-B.ST","HPOL-B.ST","HUFV-A.ST","HUFV-C.ST","FIA1S.HE","FLS.CO","FOI-B.ST","FORTUM.HE","DSV.CO","EKTA-B.ST","ELISA.HE","ELUX-A.ST","ELUX-B.ST","EPI-A.ST","EPI-B.ST","ERIC-A.ST","ERIC-B.ST","ESSITY-A.ST","ESSITY-B.ST","EVO.ST","FABG.ST","DNA.HE","DOM.ST","DRLCO.CO","CTY1S.HE","DANSKE.CO","DEMANT.CO","DFDS.CO","CARL-A.CO","CARL-B.CO","CAST.ST","CGCBV.HE","CHR.CO","COLO-B.CO","ARION-SDB.ST","ARJO-B.ST","ASSA-B.ST","ATCO-A.ST","ATCO-B.ST","ATRLJ-B.ST","ATT.ST","AXFO.ST","AZA.ST","AZN.ST","BALD-B.ST","BEIJ-B.ST","BETS-B.ST","BILL.ST","BOL.ST","BONAV-A.ST","BONAV-B.ST","BRAV.ST","8TRA.ST","AAK.ST","ABB.ST","ADDT-B.ST","AF-B.ST","ALFA.ST","ALIV-SDB.ST","ALK-B.CO","ALMB.CO","AM1.HE","AM1S.ST","AMBU-B.CO","AMEAS.HE","ARION.IC","TTALO.HE","TYRES.HE","UPM.HE","UPONOR.HE","VALMT.HE","VITR.ST","VNE-SDB.ST","VOLV-A.ST","VOLV-B.ST","VWS.CO","WALL-B.ST","WIHL.ST","WRT1V.HE","YIT.HE"]

symbols=[]

if (not os.path.isfile("last_data.csv")):
    for ticker in symbols_list: 
        print(ticker)
        r = pdr.get_data_yahoo(ticker, start=start_date, end=end_date)
        # add a symbol column
        r['Symbol'] = ticker
        symbols.append(r)

    df = pd.concat(symbols)
    df = df.reset_index()
    df = df[['Date', 'Close', 'Symbol']]

    df_pivot = df.pivot('Date','Symbol','Close').reset_index()
    df_pivot.to_csv("last_data.csv")
else:
    df_pivot = pd.read_csv("last_data.csv")

corr_df = df_pivot.corr(method='pearson')
corr_df.head().reset_index()
del corr_df.index.name

#generate plot
#corr_df[np.abs(corr_df)<.90] = 0
#corr_df[np.abs(corr_df)==1.0] = 0

#corr_df = corr_df.dropna(axis='columns')
#corr_df = corr_df.dropna(axis='rows')

#Highest influencers
print(corr_df.sum(axis = 0, skipna = True).reset_index().sort_values(by = [0]))

#Telia correlation matrix
corr_df = corr_df[['SAMPO.HE']].sort_values(by=['SAMPO.HE'],ascending=False)

print(corr_df)
mask = np.zeros_like(corr_df)
mask[np.triu_indices_from(mask)] = True
plt.figure(figsize=(216,216))

seaborn.heatmap(corr_df, cmap='RdYlGn', vmax=1.0, vmin=-1.0 , mask = mask, linewidths=2.5)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()