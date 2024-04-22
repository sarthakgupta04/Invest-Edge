from flask import Blueprint, request, jsonify
from .database import db
from .models import Portfolio  # Changed import to relative

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolios', methods=['POST'])
def create_portfolio():
    user_id = request.json.get('user_id')
    name = request.json.get('name')
    if not user_id or not name:
        return jsonify({"error": "User ID and name are required"}), 400

    new_portfolio = Portfolio(user_id=user_id, name=name)
    db.session.add(new_portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio created", "portfolio": {"id": new_portfolio.id, "name": new_portfolio.name}}), 201

@portfolio_bp.route('/portfolios', methods=['GET'])
def get_portfolios():
    user_id = request.args.get('user_id')
    portfolios = Portfolio.query.filter_by(user_id=user_id).all()
    return jsonify([{"id": p.id, "name": p.name} for p in portfolios])

@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['PUT'])
def update_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    portfolio.name = request.json.get('name', portfolio.name)
    db.session.commit()
    return jsonify({"message": "Portfolio updated", "portfolio": {"id": portfolio.id, "name": portfolio.name}})

@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['DELETE'])
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    db.session.delete(portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio deleted"})