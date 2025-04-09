from TelopsToolbox.hcc.readIRCam import read_ircam
from TelopsToolbox.hcc.writeIRCam import write_ircam
import TelopsToolbox.utils.image_processing as ip
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

""" read the first 50 frames of a sequence hcc """
data, header, specialPixel, nonSpecialPixel = read_ircam(r'F:\Telops_Python_Toolbox\PythonTelopsToolbox-1.0.1\PythonTelopsToolbox-1.0.1\Demo Data\Fireworks.hcc', frames=list(
    range(0, 50)))

header_df = pd.DataFrame(header)
frame = data[0]

""" look for a particular header """
numero_header = 0
this_header = header_df.iloc[numero_header]


""" print bad pixels """
BP = specialPixel[0] == 14
BD_2d = ip.form_image(header, BP)
plt.imshow(BD_2d.squeeze(), extent=[0, header['Width'][0], 0, header['Height'][0]])

""" print a frame """
image_2D = ip.form_image(header, frame)
c_lim = ip.image_scaling_limits(frame)
vmin, vmax = c_lim.squeeze()
plt.figure(1)
plt.imshow(image_2D.squeeze(), vmin=vmin, vmax=vmax, cmap='inferno')
plt.colorbar()

""" build an area of interest """
aoi = ip.build_aoi(500-400, 400-300, 400, 300)  # define the ROI
idx_aoi, aoi_out = ip.get_aoi_indices(this_header, aoi)

aoi_data = np.array([frame[idx] for idx in idx_aoi])
aoi_2d = ip.form_image(aoi_out, aoi_data)
c_lim = ip.image_scaling_limits(aoi_data)
vmin, vmax = c_lim.squeeze()
plt.figure(2)
plt.imshow(aoi_2d.squeeze(), vmin=vmin, vmax=vmax, cmap='inferno')
plt.colorbar()

""" temporal profile """
# create the time vector
time = header['POSIXTime'] + header['SubSecondTime']*(10**(-7))
# the posixTime gives the times precise to the second
# and the subsecond time needs to be used to achieve better precision
time = time-header['POSIXTime'][0]-header['SubSecondTime'][0]*(10**(-7))
plt.figure(3)
plt.plot(time, [max(data[i][:])-273.15 for i in range(len(data))])
plt.xlabel('time [s]')
plt.ylabel('temperature [oC]')

""" write .hcc file """
data_EHDRI, header_EHDRI, _, _ = read_ircam(r'F:\Telops_Python_Toolbox\PythonTelopsToolbox-1.0.1\PythonTelopsToolbox-1.0.1\Demo Data\Soldering iron.hcc')
# extract the information about the second EHDRI exposure time
nbrFrames = data_EHDRI.shape[0]
data1 = np.array([data_EHDRI[i] for i in range(nbrFrames) if header_EHDRI['EHDRIExposureIndex'][i] == 1])
header1 = {}
for key in header_EHDRI.keys():
    header1[key] = np.array([header_EHDRI[key][i] for i in range(nbrFrames)
                             if header_EHDRI['EHDRIExposureIndex'][i] == 1], dtype=header_EHDRI[key].dtype)

# write a new hcc with the extracted data
write_ircam(header1, data1, 'new_hcc1.hcc')
