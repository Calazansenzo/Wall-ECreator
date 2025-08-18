from src.models.user import db
from datetime import datetime
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so

class Projeto(db.Model):
    __tablename__ = 'projetos'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    nome: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    descricao: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    tinkercad_link: so.Mapped[Optional[str]] = so.mapped_column(sa.Text)
    data_criacao: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.utcnow)
    
    # Relacionamento com componentes
    componentes = db.relationship('Componente', backref='projeto', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Projeto {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'tinkercad_link': self.tinkercad_link,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'componentes': [comp.to_dict() for comp in self.componentes]
        }

class Componente(db.Model):
    __tablename__ = 'componentes'
    
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    projeto_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('projetos.id'), nullable=False)
    nome: so.Mapped[str] = so.mapped_column(sa.String(255), nullable=False)
    quantidade: so.Mapped[int] = so.mapped_column(sa.Integer, nullable=False, default=0)

    def __repr__(self):
        return f'<Componente {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'projeto_id': self.projeto_id,
            'nome': self.nome,
            'quantidade': self.quantidade
        }

