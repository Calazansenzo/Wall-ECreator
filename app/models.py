from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional, List
import sqlalchemy as sa
import sqlalchemy.orm as so

# Importar db do módulo raiz
try:
    from __init__ import db
except ImportError:
    # Para quando executado dentro do contexto da aplicação
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy()

# Tabela de associação para muitos-para-muitos entre Projeto e Componente
class ProjetoComponente(db.Model):
    __tablename__ = 'projeto_componente'
    projeto_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('projeto.id', ondelete='CASCADE'),
        primary_key=True
    )
    componente_id: so.Mapped[int] = so.mapped_column(
        sa.ForeignKey('componente.id', ondelete='CASCADE'), 
        primary_key=True
    )

class Projeto(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text)
    url: so.Mapped[str] = so.mapped_column(sa.String(200))
    
    # Relacionamento muitos-para-muitos com componentes
    componentes: so.Mapped[List['Componente']] = so.relationship(
        'Componente',
        secondary='projeto_componente',
        back_populates='projetos'
    )

    def __repr__(self):
        return f'<Projeto {self.nome}>'

class Componente(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    descricao: so.Mapped[str] = so.mapped_column(sa.Text)
    url: so.Mapped[str] = so.mapped_column(sa.String(200))
    quantidade: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    
    # Relacionamento muitos-para-muitos com projetos
    projetos: so.Mapped[List[Projeto]] = so.relationship(
        'Projeto',
        secondary='projeto_componente',
        back_populates='componentes'
    )

    def __repr__(self):
        return f'<Componente {self.nome}>'