import pandas as pd

import matplotlib.pyplot as plt
%matplotlib inline

from matplotlib import style
style.use('ggplot')

# Idea: Impact of the euro exchange rate on the countries
# most affected at the beginning of the coronavirus pandemic.

exchange_rates = pd.read_csv('/content/drive/MyDrive/mlops/euro-daily-hist_1999_2020.csv')
# The DataFrame has 5699 rows and 40 columns.
# There are many null values.
# Some columns are type float, but the majority is object.

exchange_rates.rename(columns={'[US dollar ]': 'US_dollar',
                               'Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates.rename(columns={'[Brazilian real ]': 'Brazilian_real'},
                      inplace=True)
exchange_rates.rename(columns={'[Indian rupee ]': 'Indian_rupee'},
                      inplace=True)
exchange_rates.rename(columns={'[Mexican peso ]': 'Mexican_peso'},
                      inplace=True)
exchange_rates.rename(columns={'[UK pound sterling ]': 'UK_pound_sterling'},
                      inplace=True)

exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)
exchange_rates.reset_index(drop=True, inplace=True)

## Cleaning data

selected_years = exchange_rates.copy()[(exchange_rates['Time'].dt.year >= 2019)]
currency = selected_years[['Time', 'US_dollar', 'Brazilian_real',
                           'Indian_rupee', 'Mexican_peso', 'UK_pound_sterling']].copy()

currency = currency[currency['US_dollar']         != '-']
currency = currency[currency['Brazilian_real']    != '-']
currency = currency[currency['Indian_rupee']      != '-']
currency = currency[currency['Mexican_peso']      != '-']
currency = currency[currency['UK_pound_sterling'] != '-']

currency['US_dollar']         = currency['US_dollar'].astype(float)
currency['Brazilian_real']    = currency['Brazilian_real'].astype(float)
currency['Indian_rupee']      = currency['Indian_rupee'].astype(float)
currency['Mexican_peso']      = currency['Mexican_peso'].astype(float)
currency['UK_pound_sterling'] = currency['UK_pound_sterling'].astype(float)

## Plot
plt.figure(figsize=(10, 10))

ax1 = plt.subplot(3,2,1)
ax2 = plt.subplot(3,2,2)
ax3 = plt.subplot(3,2,3)
ax4 = plt.subplot(3,2,4)
ax5 = plt.subplot(3,2,5)
ax6 = plt.subplot(3,2,6)

axes = [ax1, ax2, ax3, ax4, ax5, ax6]
countries = ['US_dollar', 'Brazilian_real', 'Indian_rupee',
             'Mexican_peso', 'UK_pound_sterling']

for ax, country in zip(axes, countries):
    ax.plot(currency['Time'], currency[country].rolling(30).mean())

    ax.set_xticklabels(['2019', '', '', '', '2020', '', '', '2021'],
                       fontsize=9)
    ax.grid(alpha=0.5)
    ax.set_yticklabels([])
    ax.tick_params(axis='y', left=False)

## Plot 6
ax6.plot(currency['Time'], currency['US_dollar'].rolling(30).mean(), label='Dollar')
ax6.plot(currency['Time'], currency['Brazilian_real'].rolling(30).mean(), label='Real')
ax6.plot(currency['Time'], currency['Indian_rupee'].rolling(30).mean(), label='Rupee')
ax6.plot(currency['Time'], currency['Mexican_peso'].rolling(30).mean(), label='Peso')
ax6.plot(currency['Time'], currency['UK_pound_sterling'].rolling(30).mean(), label='Pound Sterling')
ax6.legend()

ax6.set_xticklabels(['2019', '', '', '2020', '', '', '', '2021'],
                       fontsize=9)

## Title
ax1.text(0.48, 4.15, 'Euro Exchange Rate at the beginning of COVID-19',
         fontsize=12, weight='bold', transform=ax.transAxes)
ax1.text(0.35, 4.05,
         'How the top 5 countries by death toll were affected. (January 2019 - January 2021)',
         fontsize=10, transform=ax.transAxes)

## Plots legend
ax1.text(0.4, 3.84, 'US - Dollar', fontsize=9, transform=ax.transAxes)
ax2.text(1.82, 3.84, 'Brazil - Real', fontsize=9, transform=ax.transAxes)
ax3.text(0.37, 2.45, 'Indian - Rupee', fontsize=9, transform=ax.transAxes)
ax4.text(1.8, 2.45, 'Mexican - Peso', fontsize=9, transform=ax.transAxes)
ax5.text(0.33, 1.05, 'UK - Pound Sterling', fontsize=9, transform=ax.transAxes)

plt.yscale('log')
ax6.tick_params(axis='y', left=False)
ax6.set_yticklabels([])

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)
plt.show()

# We chose to omit the y-axis from all the graphs as they were on different scales
# and the intention of the graph as a whole is just to
# demonstrate the general increase in the value of the euro.