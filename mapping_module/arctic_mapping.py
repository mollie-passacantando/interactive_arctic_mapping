## Best to place this in a modules folder under your project home directory
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









