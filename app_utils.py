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

    # plot a bar chart with keys on the x-axis and values on the y-axis
    if len(landing_page['tag_counts'].keys()) > 10:
        landing_page['tag_counts'] = dict(islice(landing_page['tag_counts'].items(), 0, 10))
    sns.barplot(x=list(landing_page['tag_counts'].keys()), y=list(landing_page['tag_counts'].values()))
    plt.xlabel('Tags')
    plt.ylabel('Count')
    plt.title('Tag Counts')
    plt.savefig(f'static/{folder_name}/tag_counts.png')

    # plot a bar chart with keys on the x-axis and values on the y-axis
    if len(landing_page['lang_counts'].keys()) > 10:
        landing_page['lang_counts'] = dict(islice(landing_page['lang_counts'].items(), 0, 10))
    sns.barplot(x=list(landing_page['lang_counts'].keys()), y=list(landing_page['lang_counts'].values()))
    plt.xlabel('Languages')
    plt.ylabel('Count')
    plt.title('Language Counts')
    plt.savefig(f'static/{folder_name}/lang_counts.png')
