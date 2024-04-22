from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .utils import validate_json  
from .database import db
from .models import Portfolio

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolios', methods=['POST'])
@login_required
@validate_json('name')  
def create_portfolio():
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"error": "Portfolio name is required"}), 400
    name=request.json ['name']
    new_portfolio = Portfolio(user_id=current_user.id, name=name)
    db.session.add(new_portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio created", "portfolio": {"id": new_portfolio.id, "name": new_portfolio.name}}), 201

@portfolio_bp.route('/portfolios', methods=['GET'])
@login_required
def get_portfolios():
    portfolios = Portfolio.query.filter_by(user_id=current_user.id).all()
    return jsonify([{"id": p.id, "name": p.name} for p in portfolios])

@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['PUT'])
@login_required
def update_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    portfolio.name = request.json.get('name', portfolio.name)
    db.session.commit()
    return jsonify({"message": "Portfolio updated", "portfolio": {"id": portfolio.id, "name": portfolio.name}})

@portfolio_bp.route('/portfolios/<int:portfolio_id>', methods=['DELETE'])
@login_required
def delete_portfolio(portfolio_id):
    portfolio = Portfolio.query.get_or_404(portfolio_id)
    if portfolio.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403

    db.session.delete(portfolio)
    db.session.commit()
    return jsonify({"message": "Portfolio deleted"})
