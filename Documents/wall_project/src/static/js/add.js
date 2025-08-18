// Função para adicionar novo componente
function adicionarComponente() {
    const container = document.getElementById('componentes-container');
    const novoComponente = document.createElement('div');
    novoComponente.className = 'componente-item';
    
    novoComponente.innerHTML = `
        <div class="form-group">
            <label>Nome do Componente</label>
            <input type="text" name="componente-nome" placeholder="Ex: Resistor 10kΩ">
        </div>
        <div class="form-group">
            <label>Quantidade</label>
            <input type="number" name="componente-quantidade" min="0" value="1">
        </div>
        <button type="button" class="btn-remover" onclick="removerComponente(this)">×</button>
    `;
    
    container.appendChild(novoComponente);
}

// Função para remover componente
function removerComponente(botao) {
    const componenteItem = botao.closest('.componente-item');
    const container = document.getElementById('componentes-container');
    
    // Não permitir remover se for o último componente
    if (container.children.length > 1) {
        componenteItem.remove();
    } else {
        alert('Deve haver pelo menos um componente.');
    }
}

// Função para abrir link do Tinkercad
function abrirTinkercad() {
    const link = document.getElementById('tinkercadLink').value;
    if (link) {
        window.open(link, '_blank');
    } else {
        alert('Por favor, insira um link válido do Tinkercad.');
    }
}

// Função para coletar dados do formulário
function coletarDadosFormulario() {
    const nome = document.getElementById('nome-projeto').value.trim();
    const descricao = document.getElementById('descricao-projeto').value.trim();
    const tinkercadLink = document.getElementById('tinkercadLink').value.trim();
    
    // Coletar componentes
    const componentesInputs = document.querySelectorAll('.componente-item');
    const componentes = [];
    
    componentesInputs.forEach(item => {
        const nomeInput = item.querySelector('input[name="componente-nome"]');
        const quantidadeInput = item.querySelector('input[name="componente-quantidade"]');
        
        const nomeComponente = nomeInput.value.trim();
        const quantidade = parseInt(quantidadeInput.value) || 0;
        
        if (nomeComponente && quantidade > 0) {
            componentes.push({
                nome: nomeComponente,
                quantidade: quantidade
            });
        }
    });
    
    return {
        nome,
        descricao,
        tinkercad_link: tinkercadLink,
        componentes
    };
}

// Função para validar dados
function validarDados(dados) {
    if (!dados.nome) {
        return 'O nome do projeto é obrigatório.';
    }
    
    if (dados.nome.length < 3) {
        return 'O nome do projeto deve ter pelo menos 3 caracteres.';
    }
    
    if (dados.componentes.length === 0) {
        return 'Adicione pelo menos um componente válido.';
    }
    
    return null;
}

// Função para mostrar loading
function mostrarLoading(mostrar = true) {
    const loading = document.getElementById('loading');
    if (mostrar) {
        loading.classList.remove('hidden');
    } else {
        loading.classList.add('hidden');
    }
}

// Função para salvar projeto
async function salvarProjeto(dados) {
    try {
        const response = await fetch('/api/projetos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        const resultado = await response.json();
        
        if (!response.ok) {
            throw new Error(resultado.error || `Erro ${response.status}: ${response.statusText}`);
        }
        
        return resultado;
        
    } catch (error) {
        console.error('Erro ao salvar projeto:', error);
        throw error;
    }
}

// Event listener para o formulário
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar event listener para o botão de adicionar componente
    document.getElementById('adicionar-componente').addEventListener('click', adicionarComponente);
    
    // Adicionar event listener para o formulário
    document.getElementById('projeto-form').addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Coletar dados
        const dados = coletarDadosFormulario();
        
        // Validar dados
        const erro = validarDados(dados);
        if (erro) {
            alert(erro);
            return;
        }
        
        // Mostrar loading
        mostrarLoading(true);
        
        try {
            // Salvar projeto
            const resultado = await salvarProjeto(dados);
            
            // Sucesso
            alert('Projeto salvo com sucesso!');
            
            // Redirecionar para a página de visualização do projeto
            window.location.href = `/view/${resultado.id}`;
            
        } catch (error) {
            // Erro
            alert(`Erro ao salvar projeto: ${error.message}`);
        } finally {
            // Esconder loading
            mostrarLoading(false);
        }
    });
});

// Função para limpar formulário
function limparFormulario() {
    document.getElementById('projeto-form').reset();
    
    // Manter apenas um componente
    const container = document.getElementById('componentes-container');
    const primeiroComponente = container.querySelector('.componente-item');
    container.innerHTML = '';
    container.appendChild(primeiroComponente);
    
    // Limpar valores do primeiro componente
    primeiroComponente.querySelector('input[name="componente-nome"]').value = '';
    primeiroComponente.querySelector('input[name="componente-quantidade"]').value = '1';
}

