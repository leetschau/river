from . import base
from . import covariance
from . import variance


class PearsonCorrelation(base.Similarity):
    """Online Pearson correlation.

    Example:

        >>> from creme import stats

        >>> x = [0, 0, 0, 1, 1, 1, 1]
        >>> y = [0, 1, 2, 3, 4, 5, 6]

        >>> pearson = stats.PearsonCorrelation()

        >>> for xi, yi in zip(x, y):
        ...     print(pearson.update(xi, yi).get())
        0
        0
        0
        0.774596...
        0.866025...
        0.878310...
        0.866025...

    """

    def __init__(self, ddof=1):
        self.var_x = variance.Variance(ddof=ddof)
        self.var_y = variance.Variance(ddof=ddof)
        self.cov_xy = covariance.Covariance(ddof=ddof)

    def update(self, x, y):
        self.var_x.update(x)
        self.var_y.update(y)
        self.cov_xy.update(x, y)
        return self

    def get(self):
        var_x = self.var_x.get()
        var_y = self.var_y.get()
        if var_x and var_y:
            return self.cov_xy.get() / (var_x * var_y) ** 0.5
        return 0
