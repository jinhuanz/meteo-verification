import numpy as np

class StatsUtils(object):
    """
    give prediction/forecast (predictions) at one station
    and observation (targets) at one station
    calculate the statistics.

    # test:
    pred = [5, 10, 9, 15, 22, 13, 17, 17, 19, 23]
    obs = [-1, 8, 12, 13, 18, 10, 16, 19, 23, 24]
    Mean Error = 0.8
    Multiplicative bias = 1.06
    MAE = 2.8
    MSE = 10
    RMSE = 3.2
    R = 0.914
    """
    def __init__(self, predictions, targets):
        if isinstance(predictions, np.ndarray):
            self.predictions = predictions
        else:
            self.predictions = np.array(predictions)
        if isinstance(targets, np.ndarray):
            self.targets = targets
        else:
            self.targets = np.array(targets)

    def me(self):
        """
        Mean error.
        Range: -âˆž to âˆž. Perfect score: 0.
        """

        return np.mean(self.predictions - self.targets)

    def bias_multiplicative(self):
        """
        Multiplicative bias.
        Range: -âˆž to âˆž. Perfect score: 1.
        Describe the average forecast magnitude compare to the average observed magnitude.
        """

        return np.mean(self.predictions) / np.mean(self.targets)

    def mae(self):
        """
        Mean absolute error.
        Range: 0 to âˆž.  Perfect score: 0.
        """

        return np.mean(np.abs(self.predictions - self.targets))

    def mse(self):
        """
        Mean squared error.
        Range: 0 to âˆž.  Perfect score: 0.
        """

        return np.mean((self.predictions - self.targets) ** 2)

    def rmse(self):
        """
        Root mean square error.
        Range: 0 to âˆž.  Perfect score: 0.
        """

        return np.sqrt(np.mean((self.predictions - self.targets) ** 2))

    def r(self):
        """
        Correlation coefficient.
        Range: -1 to 1.  Perfect score: 1.
        """
        predictions = self.predictions
        targets = self.targets

        mean_p = np.mean(predictions)
        mean_t = np.mean(targets)
        return (np.mean((predictions - mean_p) * (targets - mean_t)))\
               / (np.sqrt(np.mean((predictions - mean_p) ** 2))
                  * np.sqrt(np.mean((targets - mean_t) ** 2)))

