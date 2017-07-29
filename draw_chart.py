from bokeh.plotting import figure, output_file, show
from bokeh.io import export_png

# prepare some data
x = ["7.13", "7.14", "7.15", "7.16", "7.17"]
y = [12, 7, 24, 4, 15]
# create a new plot with a title and axis labels
p = figure(title="simple line example", plot_width=500, plot_height=400, x_axis_type = "auto",x_axis_label='日期', y_axis_label='bug 数量')
# add a line renderer with legend and line thickness
p.line(x, y, legend="Temp.", line_width=2)
p.circle(x, y, fill_color="white", size=8)
export_png(p, filename="test.png")

