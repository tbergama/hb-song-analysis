import pandas as pd
import os

import topic_model
import labels_to_documents
import cluster
import stft
import conf

def map_range(x, ab, cd=(0,1)):
    y = (x-ab[0]) * (cd[1]-cd[0])/(ab[1]-ab[0]) + cd[0]
    return y


if __name__ == "__main__":

    path = conf.model_path

    stft.main()
    cluster.main()
    labels_to_documents.main()

    alpha = [0.9, 0.5, 0.1, 0.01, 0.001]  # alpha vals to sweep
    alpha_fixed = 0.1  # value to fix alpha at when sweeping beta
    beta = [0.9, 0.5, 0.1, 0.01, 0.001]  # beta vals to sweep
    beta_fixed = 0.1  # value to fix beta at when sweeping alpha
    num_topics = [2, 5, 10, 15, 20]  # number of topics to sweep
    runs_per_param = 5  # number of runs per parameterization

    perplexity_df = pd.DataFrame(columns=['alpha', 'beta', 'num_topics''perplexity'])

    for a in alpha:
        for t in num_topics:
            p_sum = 0
            for i in range(runs_per_param):
                print("RUN %d TOPIC MODEL WITH alpha=%f, beta=%f, T=%d" % (i, a, beta_fixed, t))
                topic_model.main(alpha=a, beta=beta_fixed, T=t, W=conf.vocab_size)
                df = pd.read_csv(filepath_or_buffer=path+"perplexity.csv",
                                 header=None)
                p = df.sum()[1] / len(df)  # average per doc perplexity
                p_sum += p  # running total of average per doc perplexity

            p_avg = p_sum/runs_per_param
            perplexity_df = perplexity_df.append({'alpha': a, 'beta': beta_fixed, 'num_topics': t,
                                                  'perplexity': p_avg}, ignore_index=True)
    #os.system('say "I am done with alpha"')

    for b in beta:
        for t in num_topics:
            p_sum = 0
            for i in range(runs_per_param):
                print("RUN %d TOPIC MODEL WITH alpha=%f, beta=%f, T=%d" % (i, alpha_fixed, b, t))
                topic_model.main(alpha=alpha_fixed, beta=b, T=t, W=conf.vocab_size)
                df = pd.read_csv(filepath_or_buffer=path+"perplexity.csv",
                                 header=None)
                p = df.sum()[1] / len(df)
                p_sum += p

            p_avg = p_sum/runs_per_param
            perplexity_df = perplexity_df.append({'alpha': alpha_fixed, 'beta': b, 'num_topics': t,
                                                  'perplexity': p_avg}, ignore_index=True)

    print("Done.")
    perplexity_df.to_csv("./param_sweep_{}_win_{}_ovr_{}_wpd_{}_gtime.csv".format(conf.window_size, int(conf.overlap*100),
                                                                                  conf.words_per_doc, conf.g_time))

    #os.system('say "I am done"')



