import matplotlib.pyplot as plt


def plot (x, xlabel, ys, ylabel, ylabels, title, output_name="plot.jpg"):
    """
    It represents received data as a line plot.
    :param x: X axis data
    :param xlabel: X axis label
    :param ys: Y axis data (may contain more than one list of data)
    :param ylabel: Y axis label
    :param ylabels: Y axis labels (one for each list of data)
    :param title: Title for the graph.
    :param output_name: Name to save the plot
    :return:
    """

    line_styles = ['-', '--', '-.', ':']
    # Use Latex fonts
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Get the figure
    f = plt.figure()

    # Plot the data
    for i in range(len(ys)):
        plt.plot(x, ys[i], line_styles[i % len(line_styles)], label=ylabels[i])

    # Set Title and Labels
    plt.title(r'\textbf{' + title + '}')
    plt.xlabel(r'\textbf{' + xlabel + '}')
    plt.ylabel(r'\textbf{' + ylabel + '}')

    # Save figure
    f.savefig(title + '_' + output_name, bbox_inches='tight')