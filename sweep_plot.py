import pickle as pkl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    filename = "/Users/thomasbergamaschi/Code/hb-song-analysis/param_sweep_1024_win_50_ovr_32_wpd_3_gtime.csv"
    sweep_df = pd.read_csv(filename)

    #beta_df = sweep_df.loc[sweep_df['alpha'] == 0.001]
    #alpha_df = sweep_df.loc[sweep_df['beta'] == 0.001]

    alpha_df = sweep_df.loc[0:((len(sweep_df)/2)-1)]
    beta_df = sweep_df.loc[len(sweep_df)/2:len(sweep_df)]

    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))

    for topic in [2, 5, 10]: #20, 50, 100]:
        alphas = alpha_df.loc[alpha_df['num_topics'] == topic].sort_values(by='alpha')
        betas = beta_df.loc[beta_df['num_topics'] == topic].sort_values(by='beta')

        ax[0].plot(alphas['alpha'],
                   alphas['perplexity'],
                   label="%d topics" % topic, marker="+")

        ax[1].plot(betas['beta'],
                 betas['perplexity'],
                 label="%d topics" % topic, marker="+")

    ax[0].set_title("Alpha=[0.001, 0.01, 0.1, 0.5, 0.9]\nwith Beta=0.1")
    ax[0].set_xscale('log')
    ax[0].set_xlabel('Alpha')
    #ax[0].set_yscale('log')
    ax[0].set_ylabel('Perplexity')
    ax[0].legend(loc=1)

    ax[1].set_title("Beta=[0.001, 0.01, 0.1, 0.5, 0.9]\nAlpha=0.1")
    ax[1].set_xscale('log')
    ax[1].set_xlabel('Beta')
    #ax[1].set_yscale('log')
    ax[1].set_ylabel('Perplexity')
    ax[1].legend(loc=1)

    plt.show()

