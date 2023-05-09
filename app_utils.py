import os
import json
from itertools import islice
import seaborn as sns
import matplotlib.pyplot as plt


def save_landing_page_dashboard(landing_page):
    """
    Saves the landing page vizualization in the static folder
    :param landing_page: a dictionary containing the landing page information
    :return: None
    """
    folder_name = landing_page['index']
    if not os.path.exists(f'static/{folder_name}'):
        os.mkdir(f'static/{folder_name}')

    local_links = len(landing_page['local_links'])
    nonlocal_links = len(landing_page['nonlocal_links'])
    # plot a pie chart with labels as local and nonlocal links
    colors = sns.color_palette('bright')[0:2]
    plt.pie([local_links, nonlocal_links], labels=['Local Links', 'Nonlocal Links'], colors=colors, autopct='%1.1f%%')
    plt.title('Local vs Nonlocal Links')
    plt.savefig(f'static/{folder_name}/local_vs_nonlocal.png')
    plt.clf()

    # plot a bar chart with keys on the x-axis and values on the y-axis
    if len(landing_page['tag_counts'].keys()) > 10:
        landing_page['tag_counts'] = dict(islice(landing_page['tag_counts'].items(), 0, 10))
    sns.barplot(x=list(landing_page['tag_counts'].keys()), y=list(landing_page['tag_counts'].values()))
    plt.xlabel('Tags')
    plt.ylabel('Count')
    plt.title('Tag Counts')
    plt.savefig(f'static/{folder_name}/tag_counts.png')
    plt.clf()

    # plot a bar chart with keys on the x-axis and values on the y-axis
    if len(landing_page['lang_counts'].keys()) > 10:
        landing_page['lang_counts'] = dict(islice(landing_page['lang_counts'].items(), 0, 10))
    sns.barplot(x=list(landing_page['lang_counts'].keys()), y=list(landing_page['lang_counts'].values()))
    plt.xlabel('Languages')
    plt.ylabel('Count')
    plt.title('Language Counts')
    plt.savefig(f'static/{folder_name}/lang_counts.png')
    plt.clf()

    # visualize the page and the image loading times from the api response
    sns.barplot(x=['Page Load Time', 'Image Load Time'], y=[landing_page['load_page_time'], landing_page['check_imgs_time']])
    sns.boxplot(x=['Page Load Time', 'Image Load Time'], y=[landing_page['load_page_time'], landing_page['check_imgs_time']])
    plt.xlabel('Load Time')
    plt.ylabel('Time (in seconds)')
    plt.title('Page and Image Load Times')
    plt.savefig(f'static/{folder_name}/load_times.png')
    plt.clf()
