import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib.transforms as mtransforms
from .statistics_utils import StatsUtils

class VerifStandard(object):
    """
    Standard verification methods, including:
    1- "Eyeball" verification
    2- Methods for dichotomous (yes/no) forecasts
    3- Methods for multi-category forecasts
    4- Methods for foreasts of continuous variables
    5- Methods for probabilistic forecasts 
    """
    def __init__(self, obs, pred):
        """
        Args:
            obs & pred: a dataframe with columns of station in string (eg ['54511', '57494']),
                 and DatetimeIndex in datetime64[ns] (using pd.to_datetime)
                 and all the missing values are set to np.nan and have checked the validation.
                 obs for observation and pred for prediction/forecast
        """
        self.obs = obs
        self.pred = pred

    def eyeball(self):
        """
        Visualize the forecast/precipitation and observation and look at them side by side and
        use human judgment to discern the forecast errors.
        """
        x = np.arange(0., len(self.obs), 1)
        plt.plot(x, self.obs, 'r', x, self.pred, 'b')
        plt.xlabel('Lead time')
        plt.ylabel('Observation VS Forecast')
        plt.show()

    def tmp_cma(self, threshold):
        """
        calculate the Prediction accuracy(PC) under absolute error within 2℃ and 1℃ according CMA
        for one station.

        Return:
            pc: accuracy
        """
        ts_flags = []
        for i in range(0, len(self.obs)):
            ts_flag = np.nan
            if abs(self.obs[i] - self.pred[i]) < threshold: ts_flag = ('good')
            if abs(self.obs[i] - self.pred[i]) >= threshold: ts_flag = ('bad')
            ts_flags.append(ts_flag)
        pc = ((ts_flags.count('good')) / (ts_flags.count('good') + ts_flags.count('bad')))
        return pc

    def dichotomous(self, scores, threshold, operator):
        """
        calculate Accuracy(PC), Threat score(TS), False alarm ratio(FAR)

        Args:
            obs: observation
            forcast: precipitation/rain forecast/prediction
            scores: the wanted scores, make it available to have flexible option which
                    can be used to decide which scores would be calculated.
        Returns:
            PC: Accuracy
            TS: Threat score
            FAR: False alarm ratio
        """
        ts_flags = []
        for i in range(0, len(self.obs)):
            ts_flag = np.nan
            if operator == 'ge':
                if self.obs[i] >= threshold and self.pred[i] >= threshold: ts_flag = ('NA')
                if self.obs[i] < threshold and self.pred[i] >= threshold: ts_flag = ('NB')
                if self.obs[i] >= threshold and self.pred[i] < threshold: ts_flag = ('NC')
                if self.obs[i] < threshold and self.pred[i] < threshold: ts_flag = ('ND')
            elif operator == 'gt':
                if self.obs[i] > threshold and self.pred[i] > threshold: ts_flag = ('NA')
                if self.obs[i] <= threshold and self.pred[i] > threshold: ts_flag = ('NB')
                if self.obs[i] > threshold and self.pred[i] <= threshold: ts_flag = ('NC')
                if self.obs[i] <= threshold and self.pred[i] <= threshold: ts_flag = ('ND')
            elif operator == 'le':
                if self.obs[i] <= threshold and self.pred[i] <= threshold: ts_flag = ('NA')
                if self.obs[i] > threshold and self.pred[i] <= threshold: ts_flag = ('NB')
                if self.obs[i] <= threshold and self.pred[i] > threshold: ts_flag = ('NC')
                if self.obs[i] > threshold and self.pred[i] > threshold: ts_flag = ('ND')
            elif operator == 'lt':
                if self.obs[i] < threshold and self.pred[i] < threshold: ts_flag = ('NA')
                if self.obs[i] >= threshold and self.pred[i] < threshold: ts_flag = ('NB')
                if self.obs[i] < threshold and self.pred[i] >= threshold: ts_flag = ('NC')
                if self.obs[i] >= threshold and self.pred[i] >= threshold: ts_flag = ('ND')
            ts_flags.append(ts_flag)

        returns = []
        cols = []
        if 'TS' in scores:
            ts = ts_flags.count('NA') \
                 / (ts_flags.count('NA') + ts_flags.count('NB') + ts_flags.count('NC')) * 100
            returns.append(ts)
            cols.append('TS')
        if 'PC' in scores:
            pc = (ts_flags.count('NA') + ts_flags.count('ND')) \
                 / (ts_flags.count('NA') + ts_flags.count('NB') + ts_flags.count('NC')
                    + ts_flags.count('ND')) * 100
            returns.append(pc)
            cols.append('PC')
        if 'FAR' in scores:
            far= ts_flags.count('NB') / (ts_flags.count('NA') + ts_flags.count('NB')) * 100
            returns.append(far)
            cols.append('FAR')
        return returns, cols

    def multicategory(self):
        """
        Methods for verifying multi-category forecasts  also start with a contingency table
        showing the frequency of forecasts and observations in the various bins.
        For example: heavy rain, light rain ...

        """
        pass

    """
    Verifying forecasts of continuous variables measures
    how the values of the forecasts differ from the values of the observations.

    The continuous verification methods and statistics include:
    1) Scatter plot - Plots the forecast values against the observed values.
    2) Box plot - Plot boxes to show the range of data
       falling between the 25th and 75th percentiles, horizontal line inside the box
       showing the median value, and the whiskers showing the complete range of the data.
    3) Mean Error(ME), Multiplicative bias, Mean absolute error(MAE),
       Correlation coefficient(R), Mean squared error(MSE) and Root mean square error(RMSE);
    """
    def continuous_statistic(self, statistics):
        """
        Get the wanted statistics, make it available to have flexible option: statistics which
        can be used to decide which statistic indexes would be calculated.
        """
        temp = []
        cols = []
        utils = StatsUtils(self.pred, self.obs)
        if 'RMSE' in statistics:
            rmse = utils.rmse()
            temp.append(rmse)
            cols.append('RMSE')
        elif 'R' in statistics:
            r = utils.r()
            temp.append(r)
            cols.append('R')
        elif 'ME' in statistics:
            me = utils.me()
            temp.append(me)
            cols.append('ME')
        elif 'Multiplicative bias' in statistics:
            bias_multiplicative = utils.bias_multiplicative()
            temp.append(bias_multiplicative)
            cols.append('Multiplicative bias')
        elif 'MAE' in statistics:
            mae = utils.mae()
            temp.append(mae)
            cols.append('MAE')
        elif 'MSE' in statistics:
            mse = utils.mse()
            temp.append(mse)
            cols.append('MSE')
        return temp, cols

    def continuous_scatter(self):
        """
        Graphs observations and forecasts together
        """
        fig, ax = plt.subplots()
        ax.scatter(self.obs, self.pred)
        line = mlines.Line2D([0, 1], [0, 1])
        transform = ax.transAxes
        line.set_transform(transform)
        ax.add_line(line)
        plt.xlabel('Obervation')
        plt.ylabel('Forecast')
        plt.show()

    def continuous_box(self):
        """
        Graphs observations and forecasts together
        """
        labels = ['Obervation', 'Forecast']
        plt.boxplot([self.obs, self.pred], labels=labels) #, showfliers=False)
        plt.show()

    def probabilistic(self):
        """
        A probabilistic forecast gives a probability of an event occurring,
        with a value between 0 and 1 (or 0 and 100%).
        A set of probabilistic forecasts, pi, is verified using observations that those events
        either occurred (oi=1) or did not occur (oi=0).

        :return:
        """
        pass

class VerifDiagnostic(object):
    """
    Diagnostic, verification methods delve more deeply into the nature of forecast errors, including
    1- Methods for spatial forecasts 
    2- Methods for probabilistic forecasts, including ensemble prediction systems 
    3- Methods for rare events 
    4- Other methods
    """
    pass
