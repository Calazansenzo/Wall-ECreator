from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length, NumberRange, ValidationError, URL
from wtforms.widgets import ListWidget, CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class ProjetoForm(FlaskForm):
    nome = StringField('Nome do Projeto', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(max=200)])
    componentes = MultiCheckboxField('Componentes', coerce=int, validators=[Optional()])
    submit = SubmitField('Salvar')

class ComponenteForm(FlaskForm):
    nome = StringField('Nome do Componente', validators=[DataRequired(), Length(max=100)])
    descricao = TextAreaField('Descrição', validators=[DataRequired()])
    url = StringField('URL', validators=[DataRequired(), URL(), Length(max=200)])
    quantidade = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Salvar')

# Formulário para edição de componente
class ComponenteEditForm(ComponenteForm):
    pass