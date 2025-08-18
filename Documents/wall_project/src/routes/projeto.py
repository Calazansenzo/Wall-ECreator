from flask import Blueprint, request, jsonify, render_template
from src.models.user import db
from src.models.projeto import Projeto, Componente

projeto_bp = Blueprint('projeto', __name__)

@projeto_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'ok',
        'message': 'API de Projetos está funcionando',
        'version': '1.0.0'
    })

@projeto_bp.route('/projetos', methods=['GET'])
def listar_projetos():
    try:
        projetos = Projeto.query.order_by(Projeto.data_criacao.desc()).all()
        return jsonify([projeto.to_dict() for projeto in projetos])
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar projetos: {str(e)}'}), 500

@projeto_bp.route('/projetos', methods=['POST'])
def criar_projeto():
    try:
        data = request.get_json()
        if not data or 'nome' not in data:
            return jsonify({'error': 'O nome do projeto é obrigatório'}), 400
        
        # Criar novo projeto
        projeto = Projeto(
            nome=data['nome'],
            descricao=data.get('descricao', ''),
            tinkercad_link=data.get('tinkercad_link', '')
        )
        
        db.session.add(projeto)
        db.session.flush()  # Para obter o ID do projeto
        
        # Adicionar componentes se fornecidos
        if 'componentes' in data and isinstance(data['componentes'], list):
            for comp_data in data['componentes']:
                if comp_data.get('nome') and comp_data.get('quantidade') is not None:
                    componente = Componente(
                        projeto_id=projeto.id,
                        nome=comp_data['nome'],
                        quantidade=int(comp_data['quantidade'])
                    )
                    db.session.add(componente)
        
        db.session.commit()
        
        return jsonify({
            'id': projeto.id,
            'nome': projeto.nome,
            'descricao': projeto.descricao,
            'tinkercad_link': projeto.tinkercad_link,
            'message': 'Projeto criado com sucesso!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar projeto: {str(e)}'}), 500

@projeto_bp.route('/projetos/<int:projeto_id>', methods=['GET'])
def obter_projeto(projeto_id):
    try:
        projeto = Projeto.query.get_or_404(projeto_id)
        return jsonify(projeto.to_dict())
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar projeto: {str(e)}'}), 500

@projeto_bp.route('/projetos/<int:projeto_id>', methods=['PUT'])
def atualizar_projeto(projeto_id):
    try:
        projeto = Projeto.query.get_or_404(projeto_id)
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos para atualização'}), 400
        
        # Atualizar campos do projeto
        if 'nome' in data:
            projeto.nome = data['nome']
        if 'descricao' in data:
            projeto.descricao = data['descricao']
        if 'tinkercad_link' in data:
            projeto.tinkercad_link = data['tinkercad_link']
        
        # Atualizar componentes se fornecidos
        if 'componentes' in data and isinstance(data['componentes'], list):
            # Remover componentes existentes
            Componente.query.filter_by(projeto_id=projeto_id).delete()
            
            # Adicionar novos componentes
            for comp_data in data['componentes']:
                if comp_data.get('nome') and comp_data.get('quantidade') is not None:
                    componente = Componente(
                        projeto_id=projeto.id,
                        nome=comp_data['nome'],
                        quantidade=int(comp_data['quantidade'])
                    )
                    db.session.add(componente)
        
        db.session.commit()
        return jsonify({'message': 'Projeto atualizado com sucesso!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar projeto: {str(e)}'}), 500

@projeto_bp.route('/projetos/<int:projeto_id>', methods=['DELETE'])
def deletar_projeto(projeto_id):
    try:
        projeto = Projeto.query.get_or_404(projeto_id)
        db.session.delete(projeto)
        db.session.commit()
        return jsonify({'message': 'Projeto deletado com sucesso!'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar projeto: {str(e)}'}), 500

