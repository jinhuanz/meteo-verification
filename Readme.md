# Forecast verification

Verif is a python package that lets you verify the quality of weather forecasts for one or several
point locations and spatial region. It can also compare forecasts from different forecasting systems
by changing observation to other forecast.

The verifications include:
look at the forecast and observations side by side;
plot the forecast values against the observed values using scatter or boxplot;
calculate Mean absolute error,  Root mean square error, Correlation coefficient as well as other statistics;
calculate scores for dichotomous (yes/no) events;
... ...

The program reads files with observations and forecasts in a specific format:
1- pure data of pbs and pred with the same length
[1, 2, 3, 4]
2- one or several stations with datetime of obs as well as pred
| Date     | 54511 | 58362 | 58562 | 58370  |
| -------  |:-----:| -----:| -----:| -----: |
| 1/3/2017 | 15.1  | 12.2  | 15.3  | 12.5   |
| 2/3/2017 | 14.4  | 14.7  | 15.9  | 13.4   |

In the case that there are several stations, this module will remove missing value and pair (obs,pred) accoding to the datetime,
output the scores of each staiton in *csv and print the scores for all stations as one on screen.

## Installation

Download source 
and run `python setup.py install`

## Usage

Please check tutorial.

## Knowlege

Would add other verification methods later.
