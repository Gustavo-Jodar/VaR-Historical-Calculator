from flask import Flask
from flask_restx import Api, Resource, reqparse
from werkzeug.datastructures import FileStorage
import os
from VaR import VaR

# Initialize Flask and Flask-RESTX app
app = Flask(__name__)
api = Api(
    app, 
    version="1.0", 
    title="Value at Risk Calculator - API",
    description="This API calculates the VaR from historical values for statistical measure."
)

# Define the namespace for organizing endpoints
trade_ns = api.namespace("trade", description="Operations for calculating the VaR of a single trade.")
portfolio_ns = api.namespace("portfolio", description="Operations for calculating the VaR of a portfolio.")

parser = reqparse.RequestParser()
# File upload parser for Swagger
parser.add_argument(
    'file', 
    location='files', 
    type=FileStorage, 
    required=True, 
    help="Upload the file"
)
# Confidence level parser for Swagger
parser.add_argument(
    'confidence_level',
    type=float, 
    required=True, 
    help="Confidence level for VaR"
)

# Utility function to validate the uploaded file
def validate_file(file):
    if file.filename == '':
        api.abort(400, "File must have a valid name")
    if file.filename.rsplit('.', 1)[1].lower() != 'csv':
        api.abort(400, "File type not allowed")
    # Save file to the uploads directory if validation is passed
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)
    return file_path

# Utility function to validate confidence level
def validate_confidence_level(confidence_level):
    if not (0 < confidence_level < 1):
        api.abort(400, "Confidence level must be greater than 0 and smaller than 1.")
    return

# Endpoint - /trade/var -> Calculates VaR for one single trade
@trade_ns.route('/var')
class TradeVaR(Resource):
    @trade_ns.expect(parser)
    def post(self):
        """Upload a file and insert the confidence level to calculate VaR for a single trade"""
        args = parser.parse_args()
        file = args['file']
        confidence_level = args['confidence_level']

        # Validate file and confidence level
        file_path = validate_file(file)
        validate_confidence_level(confidence_level)

        # Calculate VaR
        var_calculator = VaR(api, file_path)
        var = var_calculator.get_var(confidence_level)

        return {"Calculated Value at Risk": var}, 201

# Endpoint - /portifolio/var -> Calculates VaR for one a portfolio
@portfolio_ns.route('/var')
class PortfolioVaR(Resource):
    @portfolio_ns.expect(parser)
    def post(self):
        """Upload a file and insert the confidence level to calculate the VaR of the portfolio"""
        args = parser.parse_args()
        file = args['file']
        confidence_level = args['confidence_level']

        # Validate file and confidence level
        file_path = validate_file(file)
        validate_confidence_level(confidence_level)

        # Calculate portfolio VaR
        var_calculator = VaR(api, file_path)
        var = var_calculator.get_var(confidence_level)

        return {"Calculated Value at Risk": var}, 201

# Endpoint - /portifolio/varPerTrade -> Calculates VaR for every trade in a portfolio
@portfolio_ns.route('/varPerTrade')
class PortfolioVaRPerTrade(Resource):
    @portfolio_ns.expect(parser)
    def post(self):
        """Upload a file and insert the confidence level to calculate VaR for each trade in the portfolio"""
        args = parser.parse_args()
        file = args['file']
        confidence_level = args['confidence_level']

        # Validate file and confidence level
        file_path = validate_file(file)
        validate_confidence_level(confidence_level)

        # Calculate VaR per trade
        var_calculator = VaR(api, file_path)
        response = var_calculator.get_trades_var(confidence_level)

        return response, 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)