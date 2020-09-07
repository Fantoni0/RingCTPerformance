# Standard library imports
import csv

# Third library imports
import matplotlib.pyplot as plt


def plot (x, xlabel, ys, ylabel, ylabels, title, output_name="plot", save_csv=False):
    """
    It represents received data as a line plot.
    :param x: X axis data.
    :param xlabel: X axis label.
    :param ys: Y axis data (may contain more than one list of data).
    :param ylabel: Y axis label
    :param ylabels: Y axis labels (one for each list of data).
    :param title: Title for the graph.
    :param output_name: Name to save the plot.
    :param save_csv: Optional parameter to save data to a csv file.
    :return:
    """
    line_styles = ['o-', 'v--', '*-.', '+:']
    # Use Latex fonts
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')

    # Get the figure
    f = plt.figure()

    # Set tics
    plt.xticks(x)
    # Plot the data
    for i in range(len(ys)):
        plt.plot(x, ys[i], line_styles[i % len(line_styles)], label=ylabels[i])

    # Set Title and Labels
    plt.title(r'\textbf{' + title + '}')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # plt.xlabel(r'\textbf{' + xlabel + '}')
    # plt.ylabel(r'\textbf{' + ylabel + '}')

    # Plot legend
    plt.legend(loc="upper left")

    # Save figure
    f.savefig('imgs/' + title + '_' + output_name + '.pdf', bbox_inches='tight')

    # Save data to csv
    if save_csv:
        with open('data/' + title + '_data.csv', mode='w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(["ring_size"]+ylabels)
            for i, xi in enumerate(x):
                row = [xi]
                for j in range(len(ys)):
                    row += [ys[j][i]]
                writer.writerow(row)


