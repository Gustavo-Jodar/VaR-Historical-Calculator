# Value at Risk - Calculator API

This is a Python3 Flask-based API that calculates the Value at Risk (VaR) from historical data provided as CSV files.

## Value at Risk (VaR)

Value at Risk (VaR) is a statistical measure used to assess the potential loss in value of an asset or portfolio over a defined time period for a given confidence interval. This API calculates VaR using historical data based on percentiles of past profits and losses (pnl).

## Routes

This API was documented using [Swagger](https://swagger.io/). Once running, it exposes the following routes:

##### 1. `/trade/var`
- Calculates the VaR for a single trade.

##### 2. `/portfolio/var`
- Calculates the VaR for a portfolio of trades.

##### 3. `/portfolio/varPerTrade`
- Calculates VaR for each trade in the portfolio.

## Requirements

- **Python 3**
- **Libraries:**
  - `Flask`
  - `Flask-RESTX`
  - `Werkzeug`
  - `numpy`
  - `pandas`
  - `requests`

To install the dependencies, run:

```bash
pip3 install flask flask-restx werkzeug requests numpy pandas
```

## Run the API
```bash
cd VaR-App/app
python3 main.py
```

## Or run it using Docker
```bash
cd VaR-App/

sudo docker build -t var_calculator_app .

sudo docker run -p 5000:5000 var_calculator_app
```

The API will be available at: 
http://localhost:5000/ 

## Testing the application
 - Make sure that the API is running at http://localhost:5000, then run:

#### Testing with Docker:
```bash
cd VaR-App/

sudo docker build -t var_calculator_tester_app -f Dockerfile-test .

sudo docker run --network=host var_calculator_tester_app
```
#### Or run:
```bash
cd VaR-App/app
python3 test.py
```
