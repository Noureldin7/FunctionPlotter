def config(axes):
    axes.grid(True)
    axes.spines['left'].set_position('zero')
    axes.yaxis.tick_left()
    axes.spines['right'].set_color('none')
    axes.spines['bottom'].set_position('zero')
    axes.xaxis.tick_bottom()
    axes.spines['top'].set_color('none')