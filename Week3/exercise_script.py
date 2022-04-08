import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches


# generate matplotlib handles to create a legend of the features we put in our map.
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


plt.ion()

# ---------------------------------------------------------------------------------------------------------------------
#import practical 3b files, counties and wards

# in this section, write the script to load the counties and ward data 
# and transform to a UTM projection
# check crs

counties = gpd.read_file('data_files/counties.shp')
wards = gpd.read_file('data_files/NI_wards.shp')
print(counties.head())
print(wards.head())

counties=counties.to_crs(epsg=2157)
wards=wards.to_crs(epsg=2157)

counties.crs
wards.crs

#complete a spatial join of wards and counties
#now the population column is in both wards AND join files 

join =gpd.sjoin(wards, counties, how='inner', lsuffix='left', rsuffix='right')
join

join['Population'].sum()

join.groupby(['CountyName'])['Population'].sum() 

join.groupby(['CountyName', 'Ward'])['Population'].sum()

myCRS = ccrs.UTM(29)


# ---------------------------------------------------------------------------------------------------------------------

# create a crs using ccrs.UTM(29) that corresponds to our CRS
myCRS = ccrs.UTM(29)

# create a figure of size 10x10 (representing the page size in inches
fig, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

# add gridlines below
gridlines = ax.gridlines(draw_labels=True,
                         xlocs=[-8, -7.5, -7, -6.5, -6, -5.5],
                         ylocs=[54, 54.5, 55, 55.5])
gridlines.right_labels = False
gridlines.bottom_labels = False

# to make a nice colorbar that stays in line with our map, use these lines:
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

# plot the ward data into our axis, using
ward_plot = wards.plot(column='Population', ax=ax, vmin=1000, vmax=8000, cmap='viridis',
                       legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})

#plot the county outlines on the axis
county_outlines = ShapelyFeature(counties['geometry'], myCRS, edgecolor='r', facecolor='none')

ax.add_feature(county_outlines)
#define the county handles by refering back to the function at the top
county_handles = generate_handles([''], ['none'], edge='r')

#add county handles to to the legend
ax.legend(county_handles, ['County Boundaries'], fontsize=12, loc='upper left', framealpha=1)

# save the figure
# fig.savefig('sample_map.png', dpi=300, bbox_inches='tight')
