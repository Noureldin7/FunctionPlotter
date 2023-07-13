from matplotlib.axes import Axes
def config(axes:Axes,x:tuple=(-1,1),y:tuple=(-1,1)):
    axes.grid(True)
    axes.axhline(y=0,color='k')
    axes.axvline(x=0,color='k')
    excessx = (x[1]-x[0])/10
    axes.set_xlim(x[0]-excessx,x[1]+excessx)
    if y[0]>1000:
        y[0] = 1000
    if y[1]<-1000:
        y[1] = -1000
    axes.set_ylim(y[0]-excessx,y[1]+excessx)