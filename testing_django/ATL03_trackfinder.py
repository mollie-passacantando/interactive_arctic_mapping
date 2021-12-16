

def getTracks(start_date,end_date,target_directory):
    import modules.ATL03_download as dl
    import numpy as np
    import os
    import h5py
        
    print(start_date)
    print(end_date)
    dl.main(start_date,end_date,target_directory)

    ilat = np.empty([3000])
    ilon = np.empty([3000])
    iheights = np.empty([3000])
    idist = np.empty([3000])
    numpoints = 3000

    var = os.listdir('/home/bitnami/htdocs/projects/laserviz/data')
    for i in range(10):
        filename = var[i]
            # for filename in os.listdir('/home/bitnami/htdocs/projects/laserviz/data'):
        if filename.endswith(".h5"):
            fullname = '/home/bitnami/htdocs/projects/laserviz/data/'+filename
            
            f = h5py.File(fullname,'r')
            
            lat = f['gt1r/heights/lat_ph']
            lon = f['gt1r/heights/lon_ph']
            heights = f['gt1r/heights/h_ph']
            dist= f['gt1r/heights/dist_ph_along']
            seglen = f['gt1r/geolocation/segment_length']
            total_dist = sum(seglen)+dist[-1]
            step = len(lat)/numpoints
            dist_corrected = np.linspace(0,int(total_dist),int(len(dist)))/1000

            final_lat = lat[0::int(step)]
            final_lat = final_lat[0:numpoints]
            final_lon = lon[0::int(step)]
            final_lon = final_lon[0:numpoints]
            print(len(final_lat))
            final_height = heights[0::int(step)]
            final_height = final_height[0:numpoints]
            final_dist = dist_corrected[0::int(step)]
            final_dist = final_dist[0:numpoints]
            ilat = np.vstack([ilat,final_lat])
            ilon = np.vstack([ilon,final_lon])
            iheights = np.vstack([iheights,final_height])
            idist = np.vstack([idist,final_dist])
        else:
            continue
    ilat = ilat[1:,:]
    ilon = ilon[1:,:]
    iheights = iheights[1:,:]
    idist = idist[1:,:]
    data = 'successful download!'
    return data,ilat,ilon,iheights,idist



def makeMap(lons=[],lats=[]):
    import numpy as np
    import matplotlib.pyplot as plt
    import jinja2
    import json

    import mpld3
    from mpld3 import plugins, utils
    import cartopy.crs as ccrs


    class HighlightLines(plugins.PluginBase):
        """A plugin to highlight lines on hover"""
        
        JAVASCRIPT = """
        mpld3.register_plugin("linehighlight", LineHighlightPlugin);
        LineHighlightPlugin.prototype = Object.create(mpld3.Plugin.prototype);
        LineHighlightPlugin.prototype.constructor = LineHighlightPlugin;
        LineHighlightPlugin.prototype.requiredProps = ["line_ids"];
        LineHighlightPlugin.prototype.defaultProps = {alpha_bg:0.3, alpha_fg:1.0}
        function LineHighlightPlugin(fig, props){
            mpld3.Plugin.call(this, fig, props);
        };

        LineHighlightPlugin.prototype.draw = function(){
        for(var i=0; i<this.props.line_ids.length; i++){
            var obj = mpld3.get_element(this.props.line_ids[i], this.fig),
                alpha_fg = this.props.alpha_fg;
                alpha_bg = this.props.alpha_bg;
                var line_id = this.props.line_ids[i]
            obj.elements()
                .on("mouseover", function(d, i){
                                d3.select(this).transition().duration(50)
                                .style("stroke-opacity", alpha_fg); })
                .on("mouseout", function(d, i){
                                d3.select(this).transition().duration(200)
                                .style("stroke-opacity", alpha_bg); })
                .on("mousedown",
                          function(d,i){alert("Copy and paste this track ID into the Track Input Box! [ " + line_id + " ]");});             
        }
        };
        """
        
        def __init__(self, lines):
            self.lines = lines
            self.dict_ = {"type": "linehighlight",
                        "line_ids": [utils.get_id(line) for line in lines],
                        "alpha_bg": lines[0].get_alpha(),
                        "alpha_fg": 1.0}
            
    fig, ax = plt.subplots(subplot_kw={'projection':ccrs.NorthPolarStereo()})
    ax.set_extent([-150,150,50,90],crs=ccrs.PlateCarree())
    ax.stock_img()

    if len(lons)>2:
        lines = ax.plot(lons.T,lats.T,transform = ccrs.PlateCarree(),linewidth=5,alpha=.5)
        plugins.connect(fig, HighlightLines(lines))
        track_info = [utils.get_id(line) for line in lines]
    else:
        track_info=[]

    ax.set_xticks([])
    ax.set_xticklabels([])
    ax.set_yticks([])
    ax.set_yticklabels([])

    fig_html = mpld3.fig_to_html(fig)
    
    return fig_html,track_info


def plotchl(dists,heights):
    import matplotlib.pyplot as plt

    import mpld3
    
    
    fig, ax = plt.subplots()
    ax.scatter(dists,heights,s=3,edgecolors='black')
    ax.set_ylim(-20,30)
    ax.set_title('Photon Height relative to the WGS-84 ellipsoid')
    ax.set_ylabel('Height (m)')
    ax.set_xlabel('Distance along track (m)')
    fig_html = mpld3.fig_to_html(fig)
    return fig_html









