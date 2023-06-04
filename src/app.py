import numpy as np
import dash_script

data = np.load('spec4000.npz')
wavelength = np.load('wavelength.npz')['arr_0']

spectra = data['spectra']
n = spectra.shape[0]

n2_ha = data['log_NII_Ha']
o3_hb = data['log_OIII_Hb']

lines_to_mask = ['OII_doublet', 'OIII (5007)', 'H_alpha']
lines_waves = [3728.5, 5008.2, 6564.6]
masking_windows = [10,7,8]
masked_spectra = np.zeros_like(spectra)
for i in range(n):
    masked_spectra[i,:] = spectra[i,:]
    for l in range(len(lines_to_mask)):
        # np.searchsorted is used to find the indices of the masking window edges
        i1, i2 = np.searchsorted(wavelength, (lines_waves[l]-masking_windows[l], lines_waves[l]+masking_windows[l]))
        x0, x1 = wavelength[i1-1], wavelength[i2+1]
        y0, y1 = spectra[i,i1-1], spectra[i,i2+1]
        # the emission line region is replaces by linearly interpolating the underlying continuum
        masked_spectra[i,i1:i2] = np.interp(wavelength[i1:i2], [x0,x1], [y0,y1])
        # the below if statement is to prevent masking absoprtion lines
        if np.average(masked_spectra[i,i1:i2]) > np.average(spectra[i,i1:i2]):
                masked_spectra[i,i1:i2] = spectra[i,i1:i2]

# This dictionary is used to tell the dash function which wavelengths to zoom in on and show in subplots titled by the keys.
# The values must be a list/array of size len(x), so if you want to use the same value for each point, you can simply do [value]*number of points
zoom = {}
for l in range(len(lines_to_mask)):
     zoom.update({lines_to_mask[l]: [lines_waves[l]]*n})

app = dash_script.dash_plot_spectra(x={'n2_ha': n2_ha}, y={'o3_hb': o3_hb}, xlim=[-1.5,1], ylim=[-1.2,1], color_code={'redshift': data['z']}, cmap='Inferno', kao_lines=True, \
                                    spectra=[spectra, masked_spectra], wavelength=wavelength, spec_colors=['rgba(0,0,0,0.5)','rgba(256,0,0,0.5)'],\
                                    spec_names=['Observed', 'masked'],\
                                    zoom=zoom, zoom_windows=[15,15,15],\
                                    zoom_extras = [{'OII_doublet flux': spectra[:,np.searchsorted(wavelength, lines_waves[0])]},
                                                   {'OIII(5007) flux': spectra[:,np.searchsorted(wavelength, lines_waves[1])-1]},
                                                   {'H_alpha flux': spectra[:,np.searchsorted(wavelength, lines_waves[2])-1]}])

server = app.server
if __name__ == '__main__':
    app.run_server(debug=True)