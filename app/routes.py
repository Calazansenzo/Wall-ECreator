from flask import render_template, flash, redirect, url_for, Blueprint, request, jsonify

# Importar db do módulo raiz
try:
    from __init__ import db
except ImportError:
    # Para quando executado dentro do contexto da aplicação
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

from app.models import Projeto, Componente
import sqlalchemy as sa   
from app.forms import ProjetoForm, ComponenteForm, ComponenteEditForm

# Criar blueprint
bp = Blueprint('main', __name__)

# API de Pesquisa
@bp.route('/api/search')
def api_search():
    query = request.args.get('q', '').strip()
    
    if len(query) < 2:
        return jsonify({'componentes': []})
    
    try:
        # Buscar componentes que contenham o termo no nome ou descrição
        componentes_query = sa.select(Componente).where(
            sa.or_(
                Componente.nome.ilike(f'%{query}%'),
                Componente.descricao.ilike(f'%{query}%')
            )
        ).order_by(Componente.nome)
        
        componentes = db.session.scalars(componentes_query).all()
        
        resultado = []
        for componente in componentes:
            # Para cada componente, buscar os projetos relacionados
            projetos_data = []
            for projeto in componente.projetos:
                projetos_data.append({
                    'id': projeto.id,
                    'nome': projeto.nome,
                    'descricao': projeto.descricao,
                    'url': projeto.url,
                    'total_componentes': len(projeto.componentes)
                })
            
            resultado.append({
                'id': componente.id,
                'nome': componente.nome,
                'descricao': componente.descricao,
                'url': componente.url,
                'quantidade': componente.quantidade,
                'projetos': projetos_data
            })
        
        return jsonify({'componentes': resultado})
        
    except Exception as e:
        return jsonify({'error': str(e), 'componentes': []}), 500

# Rotas para Projeto
@bp.route('/projetos')
def lista_projetos():
    query = sa.select(Projeto)
    projetos = db.session.scalars(query).all()
    return render_template('lista_projetos.html', title='Projetos', projetos=projetos)

@bp.route('/projeto/novo', methods=['GET', 'POST'])
def novo_projeto():
    form = ProjetoForm()
    
    # Preencher as opções dos componentes disponíveis
    componentes = Componente.query.order_by('nome').all()
    form.componentes.choices = [(c.id, c.nome) for c in componentes]
    
    if form.validate_on_submit():
        try:
            projeto = Projeto(
                nome=form.nome.data,
                descricao=form.descricao.data,
                url=form.url.data
            )
            
            # Adicionar os componentes selecionados
            if form.componentes.data:
                componentes_selecionados = Componente.query.filter(Componente.id.in_(form.componentes.data)).all()
                projeto.componentes.extend(componentes_selecionados)
            
            db.session.add(projeto)
            db.session.commit()
            flash('Projeto criado com sucesso!', 'success')
            return redirect(url_for('main.lista_projetos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar projeto: {str(e)}', 'error')
    
    return render_template('projeto_form.html', title='Novo Projeto', form=form, componentes=componentes)

@bp.route('/projeto/editar/<int:id>', methods=['GET', 'POST'])
def editar_projeto(id):
    projeto = db.session.get(Projeto, id)
    if not projeto:
        flash('Projeto não encontrado.', 'error')
        return redirect(url_for('main.lista_projetos'))

    form = ProjetoForm(obj=projeto)
    
    # Preencher as opções dos componentes disponíveis
    componentes = Componente.query.order_by('nome').all()
    form.componentes.choices = [(c.id, c.nome) for c in componentes]
    
    if form.validate_on_submit():
        try:
            projeto.nome = form.nome.data
            projeto.descricao = form.descricao.data
            projeto.url = form.url.data
            
            # Atualizar componentes
            if form.componentes.data:
                componentes_selecionados = Componente.query.filter(Componente.id.in_(form.componentes.data)).all()
                projeto.componentes = componentes_selecionados
            else:
                projeto.componentes = []
            
            db.session.commit()
            flash('Projeto atualizado com sucesso!', 'success')
            return redirect(url_for('main.lista_projetos'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar projeto: {str(e)}', 'error')

    # Pre-selecionar os componentes atuais
    form.componentes.data = [c.id for c in projeto.componentes]

    return render_template('projeto_form.html', title='Editar Projeto', form=form, projeto=projeto, componentes=componentes)

@bp.route('/projeto/excluir/<int:id>')
def excluir_projeto(id):
    projeto = db.session.get(Projeto, id)
    if projeto:
        try:
            db.session.delete(projeto)
            db.session.commit()
            flash('Projeto excluído com sucesso!', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao excluir projeto: {str(e)}', 'error')
    else:
        flash('Projeto não encontrado.', 'error')
    
    return redirect(url_for('main.lista_projetos'))

@bp.route('/projeto/detalhes/<int:id>')
def detalhes_projeto(id):
    projeto = db.session.get(Projeto, id)
    if not projeto:
        flash('Projeto não encontrado.', 'error')
        return redirect(url_for('main.lista_projetos'))
    
    return render_template('detalhes_projeto.html', title=projeto.nome, projeto=projeto)

# Rotas para Componente
@bp.route('/componentes')
def lista_componentes():
    query = sa.select(Componente)
    componentes = db.session.scalars(query).all()
    return render_template('lista_componentes.html', title='Componentes', componentes=componentes)

@bp.route('/componente/novo', methods=['GET', 'POST'])
def novo_componente():
    form = ComponenteForm()
    
    if form.validate_on_submit():
        try:
            componente = Componente(
                nome=form.nome.data,
                descricao=form.descricao.data,
                url=form.url.data,
                quantidade=form.quantidade.data
            )
            
            db.session.add(componente)
            db.session.commit()
            
            flash('Componente criado com sucesso!', 'success')
            return redirect(url_for('main.lista_componentes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar componente: {str(e)}', 'error')
    
    return render_template('componente_form.html', title='Novo Componente', form=form)

@bp.route('/componente/editar/<int:id>', methods=['GET', 'POST'])
def editar_componente(id):
    componente = db.session.get(Componente, id)
    if not componente:
        flash('Componente não encontrado.', 'error')
        return redirect(url_for('main.lista_componentes'))

    form = ComponenteEditForm(obj=componente)
    
    if form.validate_on_submit():
        try:
            componente.nome = form.nome.data
            componente.descricao = form.descricao.data
            componente.url = form.url.data
            componente.quantidade = form.quantidade.data
            
            db.session.commit()
            flash('Componente atualizado com sucesso!', 'success')
            return redirect(url_for('main.lista_componentes'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao atualizar componente: {str(e)}', 'error')
    
    return render_template('componente_form.html', title='Editar Componente', form=form, componente=componente)

@bp.route('/componente/excluir/<int:id>')
def excluir_componente(id):
    componente = db.session.get(Componente, id)
    if componente:
        db.session.delete(componente)
        db.session.commit()
        flash('Componente excluído com sucesso!', 'success')
    else:
        flash('Componente não encontrado.', 'error')
    return redirect(url_for('main.lista_componentes'))

@bp.route('/componente/detalhes/<int:id>')
def detalhes_componente(id):
    componente = db.session.get(Componente, id)
    if not componente:
        flash('Componente não encontrado.', 'error')
        return redirect(url_for('main.lista_componentes'))
    
    return render_template('detalhes_componente.html', title=componente.nome, componente=componente)

# Rota principal (home)
@bp.route('/')
@bp.route('/index')
def index():
    # Mostrar estatísticas ou últimos componentes adicionados
    total_projetos = db.session.scalar(sa.select(sa.func.count(Projeto.id)))
    total_componentes = db.session.scalar(sa.select(sa.func.count(Componente.id)))
    
    ultimos_componentes = db.session.scalars(
        sa.select(Componente).order_by(Componente.id.desc()).limit(5)
    ).all()
    
    return render_template('index.html', 
                         title='Home',
                         total_projetos=total_projetos,
                         total_componentes=total_componentes,
                         ultimos_componentes=ultimos_componentes)