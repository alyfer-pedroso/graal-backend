from flask import Flask
from flask_cors import CORS

from .routes.cargos_route import cargo_bp
from .routes.categorias_route import categoria_bp
from .routes.fornecedores_route import fornecedor_bp
from .routes.funcionarios_route import funcionario_bp
from .routes.itens_route import item_bp
from .routes.produto_roule import produto_bp
from .routes.venda_route import venda_bp

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = True

    CORS(app)

    app.register_blueprint(cargo_bp)
    app.register_blueprint(categoria_bp)
    app.register_blueprint(fornecedor_bp)
    app.register_blueprint(funcionario_bp)
    app.register_blueprint(item_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(venda_bp)

    return app

