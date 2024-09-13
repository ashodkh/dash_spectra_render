import numpy as np
import pylab as plt
import pickle
plt.rcParams.update({'font.size': 26})
from sklearn.preprocessing import StandardScaler
import matplotlib.gridspec as gridspec
import umap
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import matplotlib
import dash_script
from dash import html, dcc, Input, Output, Dash
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

lines = ["HBETA", "OIII_5007", "HALPHA", "NII_6584"]
lines_names = [r'H$\beta$', r'[OIII] $\lambda$5007', r'H$\alpha$', r'[NII] $\lambda$6584']
lines_waves = [4862.7, 5008.2, 6564.6, 6585.3]  

embeddings_x = np.load('./data_for_umap_dash/umap_x.npy')
embeddings_y = np.load('./data_for_umap_dash/umap_y.npy')
color_coding = np.load('./data_for_umap_dash/color_coding.npy')
rest_frame_spectra = np.concatenate((np.load('./data_for_umap_dash/rest_frame_spectra1.npy'),np.load('./data_for_umap_dash/rest_frame_spectra2.npy')), axis=0)
fluxes = np.load('./data_for_umap_dash/fluxes.npy')
wavelength = np.load('./data_for_umap_dash/wavelength.npy')
bin_centers = np.load('./data_for_umap_dash/bin_centers.npy')
h_beta_ews = np.load('./data_for_umap_dash/h_beta_ews.npy')
oiii_ews = np.load('./data_for_umap_dash/oiii_ews.npy')
h_alpha_ews = np.load('./data_for_umap_dash/h_alpha_ews.npy')
nii_ews = np.load('./data_for_umap_dash/nii_ews.npy')

l = 2
bpt_lines = [0,1,2,3]
zooms = np.zeros([fluxes.shape[0],len(bpt_lines)])

for i,ll in enumerate(bpt_lines):
    zooms[:,i] = lines_waves[ll]#*(1+z[6])

app = dash_script.dash_plot_spectra(x={'Continuum UMAP axis 1': embeddings_x}, y={'Continuum UMAP axis 2':embeddings_y},\
                                    color_code={'H_alpha EW': np.clip(h_alpha_ews,a_min=0,a_max=20)},\
                                    spectra=[rest_frame_spectra, fluxes], spec_colors=['rgba(0,256,100,0.5)', 'rgba(256,165,0,1)'],\
                                    spec_names=['Observed Spectrum', 'Masked Continuum'], wavelength=[wavelength, bin_centers],\
                                    kao_lines=False,\
                                    zoom={'1':zooms[:,0],'2':zooms[:,1],'3':zooms[:,2],'4':zooms[:,3]}, zoom_windows=[15,15,15,15],\
                                    zoom_extras = [{'H_beta EW': h_beta_ews},\
                                                {'[OIII] EW': oiii_ews},\
                                                {'H_alpha EW': h_alpha_ews},\
                                                {'[NII] EW': nii_ews}])
server = app.server                                                
if __name__ == '__main__':
    app.run_server(debug=True)