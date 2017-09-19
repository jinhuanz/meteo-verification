import os
import pandas as pd
from .verif_methods import VerifStandard

def verif(stations, obs, pred, **kwargs):
    """
    commit the verification case by case.

    Args:
            stations:  a list of stations, eg ['54511']; eg ['54511', '57494']
            obs & pred: a dataframe with columns of station in string (eg ['54511', '57494']),
                 and DatetimeIndex in datetime64[ns] (using pd.to_datetime)
                 and all the missing values are set to np.nan and have checked the validation.
                 obs for observation and pred for prediction/forecast
    """
    flag_eyeball = False
    flag_tmp_cma = False
    flag_dichotomous = False
    flag_cont_stats = False
    flag_cont_scatter = False
    flag_cont_box = False

    if 'Eyeball' in kwargs:
        if  kwargs['Eyeball'] == True:
            flag_eyeball = True
    if 'TMP_CMA' in kwargs:
        if kwargs['TMP_CMA'] == True:
            flag_tmp_cma = True
            verifs_tmp_cma = pd.DataFrame()
            if 'TMP_CMA_output' in kwargs:
                tmp_cma_output = kwargs['TMP_CMA_output']
            else:
                print('output name for TMP_CMA is not set, using the default: ""')
                tmp_cma_output = ""
    if 'Dichotomous' in kwargs:
        if kwargs['Dichotomous'] == True:
            if 'threshold' in kwargs and 'operator' in kwargs:
                threshold = kwargs['threshold']
                operator = kwargs['operator']
                flag_dichotomous = True
            else:
                print("Threshold and operater to create the Dichotomous needed, "
                      "for example: heat event tmp>=35, using:"
                      "verif(stations, obs, pred, Dichotomous=True, scores = ['TS', 'PC'], "
                      "threshold=35, operator='ge'),"
                      "skip this verification")
            if flag_dichotomous:
                if 'scores' in kwargs:
                    scores = kwargs['scores']
                else:
                    print("The scores are not set, using default: scores=['TS', 'PC'].")
                    scores = ['TS', 'PC']
                if 'Dichotomous_output' in kwargs:
                    dichotomous_output = kwargs['Dichotomous_output']
                else:
                    print('output name for Dichotomous is not set, using the default: ""')
                    dichotomous_output = ""
                verifs_dichotomous = pd.DataFrame()
    if 'CONT_Stats' in kwargs:
        if kwargs['CONT_Stats'] == True:
            flag_cont_stats = True
            verifs_cont_stats = pd.DataFrame()
            if "statistics" in kwargs:
                statistics = kwargs["statistics"]
            else:
                print("The statistics are not set, using default: "
                      "statisticss=['RMSE'].")
                statistics = ['RMSE']
            if "CONT_Stats_output" in kwargs:
                cont_stats_output = kwargs['CONT_Stats_output']
            else:
                cont_stats_output = ''
    if 'CONT_Scatter' in kwargs:
        if kwargs['CONT_Scatter'] == True:
            flag_cont_scatter = True
    if 'CONT_Box' in kwargs:
        if kwargs['CONT_Box'] == True:
            flag_cont_box = True

    # station information
    verif_path = os.path.split(os.path.dirname(__file__))[0]
    stas = pd.read_csv(os.path.join(verif_path, "verif/data/stations.csv"))
    stas['station'] = [str(x) for x in stas['station']]

    sta_num = 0
    summary = pd.DataFrame()
    verifs_tmp_cma_temp = []
    verifs_dichotomous_temp = []
    verifs_cont_stats_temp = []
    for station in stations:
        # get (obs, pred) pairs at the one station
        if station not in obs.columns:
            print("observations do not have station %s" % (station))
            continue
        elif station not in pred.columns:
            print("predictions do not have station %s" % (station))
            continue
        obs_i = obs[[station]]
        pred_i = pred[[station]]
        recs = pd.merge(obs_i, pred_i, left_index=True, right_index=True,
                        suffixes=('_obs', '_prediction'))
        recs = recs.dropna(how='any')
        obs_col = '%s_obs' % str(station)
        forecast_col = '%s_prediction' % str(station)
        if len(recs[obs_col]) < 1:
            print("station(%s) do not have pair sample, do nothing." % (station))
            continue
        verification = VerifStandard(recs[obs_col], recs[forecast_col])

        # Eyrball
        if flag_eyeball:
            verification.eyeball()
        # CMA temperature verification
        if flag_tmp_cma:
            cols_tmp_cma = ['station', 'PC(<=2℃)', 'PC(<=1℃)']
            temp = [station]
            temp.append(verification.tmp_cma(2))
            temp.append(verification.tmp_cma(1))
            verifs_tmp_cma_temp.append(temp)
        # Dichotomous
        if flag_dichotomous:
            cols_dichotomous = ['station']
            temp = [station]
            s, c = verification.dichotomous(scores, threshold, operator)
            temp.extend(s)
            cols_dichotomous.extend(c)
            verifs_dichotomous_temp.append(temp)
        # Continuous statistics
        if flag_cont_stats:
            cols_cont_stats = ['station']
            temp = [station]
            s, c = verification.continuous_statistic(statistics)
            temp.extend(s)
            cols_cont_stats.extend(c)
            verifs_cont_stats_temp.append(temp)
        # Continuous scatter
        if flag_cont_scatter:
            verification.continuous_scatter()
        # Continuous box
        if flag_cont_box:
            verification.continuous_box()
        # collect (obs, pred) pairs of all stations to summary
        recs = recs.rename(columns={forecast_col: 'forecast', obs_col: 'obs'})
        summary = summary.append(recs)
        sta_num += 1
    if flag_tmp_cma:
        verifs_tmp_cma = pd.DataFrame(verifs_tmp_cma_temp, columns=cols_tmp_cma)
    if flag_dichotomous:
        verifs_dichotomous =pd.DataFrame(verifs_dichotomous_temp, columns=cols_dichotomous)
    if flag_cont_stats:
        verifs_cont_stats =pd.DataFrame(verifs_cont_stats_temp, columns=cols_cont_stats)

    # CMA temperature verification
    if flag_tmp_cma:
        results = pd.merge(verifs_tmp_cma, stas, on="station", how='inner')
        results.to_csv("verif_temperature_accuracy_cma_%s.csv" % (tmp_cma_output), index=False)
    # Dichotomous
    if flag_dichotomous:
        results = pd.merge(verifs_dichotomous, stas, on="station", how='inner')
        results.to_csv("verif_dichotomous_%s_%s_%s.csv" % (dichotomous_output, operator, threshold),
                                  index=False)
    # Continuous statistics
    if flag_cont_stats:
        results = pd.merge(verifs_cont_stats, stas, on="station", how='inner')
        results.to_csv("verif_continuous_%s.csv" % (cont_stats_output), index=False)

    if sta_num >= 2:
        verification = VerifStandard(summary['obs'], summary['forecast'])
        # Eyrball
        if flag_eyeball:
            print("the obs-forecast figure of the %s stations:" % (sta_num))
            verification.eyeball()
        # CMA temperature
        if flag_tmp_cma:
            cols = ['PC(<=2℃)', 'PC(<=1℃)']
            temp = []
            temp.append(verification.tmp_cma(2))
            temp.append(verification.tmp_cma(1))
            print("The verification scores for all the %s stations:" % (sta_num))
            print(pd.DataFrame([temp], columns=cols))
        # Dichotomous
        if flag_dichotomous:
            temp, cols = verification.dichotomous(scores, threshold, operator)
            print("The verification scores for all the %s stations:" % (sta_num))
            print(pd.DataFrame([temp], columns=cols))
        # Continuous statistics
        if flag_cont_stats:
            temp, cols = verification.continuous_statistic(statistics)
            print("The verification summary for all the %s stations:" % (sta_num))
            print(pd.DataFrame([temp], columns=cols))
        # Continuous scatter
        if flag_cont_scatter:
            print("the obs-forecast figure of the %s stations:" % (sta_num))
            verification.continuous_scatter()
        # Continuous box
        if flag_cont_box:
            print("the obs-forecast figure of the %s stations:" % (sta_num))
            verification.continuous_box()

