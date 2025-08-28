import os
import sys

# Adiciona o diretório pai ao path do Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar do módulo raiz
from __init__ import create_app, db
from app.models import Projeto, Componente

def init_db():
    # Cria o aplicativo Flask
    app = create_app()
    
    with app.app_context():
        # Remover todas as tabelas existentes primeiro
        db.drop_all()
        
        # Criar todas as tabelas com a nova estrutura
        db.create_all()
        
        db.session.commit()
        
        print("Banco de dados inicializado com sucesso!")
        print(f"Projetos criados: {Projeto.query.count()}")
        print(f"Componentes criados: {Componente.query.count()}")

if __name__ == "__main__":
    init_db()