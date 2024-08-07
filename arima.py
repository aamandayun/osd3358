# arima_forecasting_no_pandas.py

import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Generate synthetic quadratic data
def generate_quadratic_data(n):
	x = np.linspace(0, 50, n)
	y = 0.1 * x**2 + np.cumsum(np.random.rand(n) * 3)
	return x, y

# Test for stationarity
def test_stationarity(timeseries):
	result = adfuller(timeseries, autolag='AIC')
	print('ADF Statistic:', result[0])
	print('p-value:', result[1])
	print('Critical Values:', result[4])
	if result[1] <= 0.05:
		print("The data is stationary")
	else:
		print("The data is not stationary")

# Parameters
n = 100  # Number of data points

# Generate data
x, y = generate_quadratic_data(n)

# Plot the data
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Observed Data')
plt.title('Generated Quadratic Data')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()


print('hello')
# Test stationarity
test_stationarity(y)

# Differencing to make data stationary if needed
y_diff = np.diff(y)
test_stationarity(y_diff)

# Fit ARIMA model
model = ARIMA(y, order=(1, 1, 1))
model_fit = model.fit()

# Print model summary
print(model_fit.summary())

# Forecast
forecast_steps = 10  # Number of periods to forecast
forecast = model_fit.forecast(steps=forecast_steps)

# Print forecasted values
print('Forecasted values:', forecast)

# Generate future x values for plotting
x_future = np.linspace(x[-1], x[-1] + forecast_steps, forecast_steps)

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(x, y, label='Observed Data')
plt.plot(x_future, forecast, color='red', label='Forecast')
plt.title('Forecasting Quadratic Data Using ARIMA')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
plt.show()

