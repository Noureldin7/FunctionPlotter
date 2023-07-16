from matplotlib.axes import Axes
def config(axes:Axes,x:tuple=(-1,1),y:tuple=(-1,1)):
    axes.grid(True)
    axes.axhline(y=0,color='k') # Draw x-axis
    axes.axvline(x=0,color='k') # Draw y-axis
    excessx = (x[1]-x[0])/10
    # Set Zoom Level
    axes.set_xlim(x[0]-excessx,x[1]+excessx)
    ymin,ymax = y
    if y[0]<-1000:
        ymin = -1000
    if y[1]>1000:
        ymax = 1000
    axes.set_ylim(ymin-excessx,ymax+excessx)