import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
from astropy.coordinates import SkyCoord
from astropy import units as u
import itertools

groups = pd.read_csv(r'.\groups.tsv',delimiter='\t')
gl=groups.dropna()

mwithf = gl.mean_mu[gl.features == 1]
mwoutf = gl.mean_mu[gl.features == 0]

#print(mwithf.mean(),mwoutf.mean())

#print(stats.shapiro(mwithf).pvalue, end=" ")
#print(stats.shapiro(mwoutf).pvalue, end=" ")
#print(stats.fligner(mwithf,mwoutf).pvalue, end=" ")
#print(stats.f_oneway(mwithf,mwoutf).pvalue)

glg=pd.read_csv(r'.\galaxies_morphology.tsv', delimiter='\t')
gli=pd.read_csv(r'.\isolated_galaxies.tsv', delimiter='\t')

#glg.plot(y='n',kind='hist')
#gli.plot(y='n',kind='hist')
#plt.show()

#print(glg[glg.n>2].value_counts().sum()/glg.value_counts().sum(), end=" ")
#print(gli[gli.n>2].value_counts().sum()/gli.value_counts().sum(), end=" ")
#print(stats.ks_2samp(glg.n, gli.n, alternative='two-sided', method='auto').pvalue)

gla=glg.groupby('Group').agg({'n':'mean','T':'mean'}).sort_index().rename(columns={'n':'mean_n','T':'mean_T'})
glc=gl.merge(gla,how='inner',left_on='Group',right_on='Group')

#glc.plot(x='mean_mu', y='mean_n', kind='scatter')
#glc.plot(x='mean_mu', y='mean_T', kind='scatter')
#plt.show()

#print(stats.shapiro(glc.mean_mu).pvalue, end=" ")
#print(stats.shapiro(glc.mean_n).pvalue, end=" ")
#print(stats.shapiro(glc.mean_T).pvalue, end=" ")
#print(stats.pearsonr(glc.mean_mu,glc.mean_n).pvalue, end=" ")
#print(stats.pearsonr(glc.mean_mu,glc.mean_T).pvalue, end=" ")

glco = pd.read_csv(r'.\galaxies_coordinates.tsv',delimiter='\t')

rdict={}
daadict={}
glistdict = {}
rtetadict = {}
for i in glco.Group.unique():
    glist = list([])
    glmed = list([])
    rtetalist = np.array([])
    daa = FlatLambdaCDM(H0=67.74, Om0=0.3089).angular_diameter_distance(groups[groups.Group==i].z.iloc[0]).to(u.kpc)
    daadict[i] = daa
    for j in range(glco.shape[0]):
        if glco.loc[j, 'Group'] == i:
            glist.append(glco.loc[j, 'Name'])
    glistdict[i]=glist
    for k in itertools.combinations(glistdict[i], 2):
        p1,p2 = k
        ra1 = glco[glco.Name == p1].RA.iloc[0]
        dec1 = glco[glco.Name == p1].DEC.iloc[0]
        ra2 = glco[glco.Name == p2].RA.iloc[0]
        dec2 = glco[glco.Name == p2].DEC.iloc[0]
        teta = ((SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree, frame="fk5")).separation(SkyCoord(ra=ra2 * u.degree, dec=dec2 * u.degree, frame="fk5"))).to(u.rad)
        r = (teta*daadict[i]).value
        rtetalist = np.append(rtetalist, r)
    rtetadict[i]=np.median(rtetalist)

gfinal = groups
gfinal['R'] = gfinal['Group'].map(rtetadict)
gfinal.dropna(inplace=True)
gfinal.plot(x='R', y='mean_mu', kind='scatter')
plt.show()
print(gfinal[gfinal.Group == 'HCG 2'].R[1], end=" ")
print(stats.shapiro(gfinal.R).pvalue, end=" ")
print(stats.shapiro(gfinal.mean_mu).pvalue, end=" ")
print(stats.pearsonr(gfinal.mean_mu, gfinal.R).pvalue, end=" ")
