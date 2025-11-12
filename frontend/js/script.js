// Configuração da API
const API_URL = 'http://localhost:3000/api';

// Verificar se usuário está logado
let usuarioLogado = null;

function verificarLogin() {
    const usuario = localStorage.getItem('usuario');
    if (!usuario) {
        window.location.href = 'login.html';
        return;
    }
    usuarioLogado = JSON.parse(usuario);
    
    // Atualizar interface com dados do usuário
    document.getElementById('user-info').textContent = `${usuarioLogado.nome_completo} (${usuarioLogado.tipo_usuario})`;
    document.getElementById('welcome-message').textContent = 
        `Olá, ${usuarioLogado.nome_completo}! Você está logado como ${usuarioLogado.tipo_usuario} no curso de ${usuarioLogado.curso}.`;
}

function logout() {
    if (confirm('Deseja realmente sair?')) {
        localStorage.removeItem('usuario');
        window.location.href = 'login.html';
    }
}

// Utilitários
function mostrarMensagem(texto, tipo = 'sucesso') {
    const mensagem = document.getElementById('mensagem');
    mensagem.textContent = texto;
    mensagem.className = `mensagem show ${tipo}`;
    
    setTimeout(() => {
        mensagem.classList.remove('show');
    }, 5000);
}

function formatarData(data) {
    return new Date(data).toLocaleString('pt-BR');
}

// ========== CARREGAR CURSOS DA UNIFEI ==========
async function carregarCursos() {
    try {
        const response = await fetch(`${API_URL}/usuarios/aux/cursos/1`);
        const resultado = await response.json();
        
        if (resultado.success) {
            const selects = ['curso_id', 'disc_curso'];
            selects.forEach(selectId => {
                const select = document.getElementById(selectId);
                if (select) {
                    select.innerHTML = '<option value="">Selecione...</option>';
                    resultado.data.forEach(curso => {
                        select.innerHTML += `<option value="${curso.id}">${curso.nome}</option>`;
                    });
                }
            });
        }
    } catch (error) {
        console.error('Erro ao carregar cursos:', error);
    }
}

// ========== USUÁRIOS ==========

// Cadastrar usuário
document.getElementById('form-usuario')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        nome_completo: document.getElementById('nome_completo').value,
        email: document.getElementById('email').value,
        senha: document.getElementById('senha').value,
        confirmar_senha: document.getElementById('confirmar_senha').value,
        universidade_id: 1, // UNIFEI
        curso_id: parseInt(document.getElementById('curso_id').value),
        periodo: parseInt(document.getElementById('periodo').value),
        tipo_usuario: document.getElementById('tipo_usuario').value
    };
    
    try {
        const response = await fetch(`${API_URL}/usuarios`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Usuário cadastrado com sucesso! ID: ${resultado.usuario_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message || 'Erro ao cadastrar usuário', 'erro');
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarMensagem('Erro ao conectar com o servidor', 'erro');
    }
});

// Buscar usuários
document.getElementById('form-buscar-usuario')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const nome = document.getElementById('buscar_nome').value;
    const tipo = document.getElementById('buscar_tipo').value;
    
    let url = `${API_URL}/usuarios?`;
    if (nome) url += `nome=${encodeURIComponent(nome)}&`;
    if (tipo) url += `tipo_usuario=${encodeURIComponent(tipo)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-usuarios');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total encontrado:</strong> ${resultado.total}</p>`;
            
            resultado.data.forEach(usuario => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${usuario.id} | <strong>Nome:</strong> ${usuario.nome_completo}</p>
                        <p><strong>E-mail:</strong> ${usuario.email}</p>
                        <p><strong>Tipo:</strong> ${usuario.tipo_usuario} | <strong>Período:</strong> ${usuario.periodo}º</p>
                        <p><strong>Curso:</strong> ${usuario.curso}</p>
                        <div class="resultado-acoes">
                            <button class="btn btn-danger" onclick="excluirUsuario(${usuario.id})">Excluir</button>
                        </div>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p class="loading">Nenhum usuário encontrado.</p>';
        }
    } catch (error) {
        console.error('Erro:', error);
        mostrarMensagem('Erro ao buscar usuários', 'erro');
    }
});

async function excluirUsuario(id) {
    if (!confirm('Tem certeza que deseja excluir este usuário?')) return;
    
    try {
        const response = await fetch(`${API_URL}/usuarios/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(resultado.message, 'sucesso');
            document.getElementById('form-buscar-usuario').dispatchEvent(new Event('submit'));
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir usuário', 'erro');
    }
}

// ========== DISCIPLINAS ==========

document.getElementById('form-disciplina')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        nome: document.getElementById('disc_nome').value,
        codigo: document.getElementById('disc_codigo').value,
        universidade_id: 1, // UNIFEI
        curso_id: parseInt(document.getElementById('disc_curso').value),
        professor_id: usuarioLogado.id,
        periodo_letivo: document.getElementById('disc_periodo').value,
        descricao: document.getElementById('disc_descricao').value
    };
    
    try {
        const response = await fetch(`${API_URL}/disciplinas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Disciplina cadastrada! ID: ${resultado.disciplina_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message || 'Erro ao cadastrar disciplina', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com o servidor', 'erro');
    }
});

document.getElementById('form-buscar-disciplina')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const nome = document.getElementById('buscar_disc_nome').value;
    const periodo = document.getElementById('buscar_disc_periodo').value;
    
    let url = `${API_URL}/disciplinas?`;
    if (nome) url += `nome=${encodeURIComponent(nome)}&`;
    if (periodo) url += `periodo_letivo=${encodeURIComponent(periodo)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-disciplinas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            
            resultado.data.forEach(disc => {
                lista.innerHTML += `
                    <div class="resultado-item">
                        <p><strong>ID:</strong> ${disc.id} | <strong>Nome:</strong> ${disc.nome}</p>
                        <p><strong>Código:</strong> ${disc.codigo} | <strong>Período:</strong> ${disc.periodo_letivo}</p>
                        <p><strong>Professor:</strong> ${disc.professor}</p>
                        <p><strong>Curso:</strong> ${disc.curso}</p>
                        ${disc.descricao ? `<p><strong>Descrição:</strong> ${disc.descricao}</p>` : ''}
                        <div class="resultado-acoes">
                            <button class="btn btn-danger" onclick="excluirDisciplina(${disc.id})">Excluir</button>
                        </div>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p class="loading">Nenhuma disciplina encontrada.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar disciplinas', 'erro');
    }
});

async function excluirDisciplina(id) {
    if (!confirm('Tem certeza? Todos os tópicos relacionados serão excluídos.')) return;
    
    try {
        const response = await fetch(`${API_URL}/disciplinas/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(resultado.message, 'sucesso');
            document.getElementById('form-buscar-disciplina').dispatchEvent(new Event('submit'));
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir disciplina', 'erro');
    }
}

// ========== TÓPICOS ==========

document.getElementById('form-topico')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        titulo: document.getElementById('top_titulo').value,
        conteudo: document.getElementById('top_conteudo').value,
        disciplina_id: parseInt(document.getElementById('top_disciplina').value),
        usuario_id: usuarioLogado.id,
        categoria: document.getElementById('top_categoria').value,
        tags: document.getElementById('top_tags').value
    };
    
    try {
        const response = await fetch(`${API_URL}/topicos`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Tópico criado! ID: ${resultado.topico_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message || 'Erro ao criar tópico', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com o servidor', 'erro');
    }
});

document.getElementById('form-buscar-topico')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const titulo = document.getElementById('buscar_top_titulo').value;
    const categoria = document.getElementById('buscar_top_categoria').value;
    
    let url = `${API_URL}/topicos?`;
    if (titulo) url += `titulo=${encodeURIComponent(titulo)}&`;
    if (categoria) url += `categoria=${encodeURIComponent(categoria)}`;
    
    try {
        const response = await fetch(url);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-topicos');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            
            resultado.data.forEach(topico => {
                const classeFixo = topico.fixo ? 'topico-fixo' : '';
                lista.innerHTML += `
                    <div class="resultado-item ${classeFixo}">
                        <p><strong>ID:</strong> ${topico.id} | <strong>Título:</strong> ${topico.titulo}</p>
                        <p><strong>Autor:</strong> ${topico.autor} | <strong>Disciplina:</strong> ${topico.disciplina}</p>
                        <p><strong>Categoria:</strong> ${topico.categoria} | 
                           <strong>Status:</strong> <span class="status status-${topico.status.toLowerCase()}">${topico.status}</span></p>
                        <p><strong>Criado:</strong> ${formatarData(topico.criado_em)}</p>
                        <div class="resultado-acoes">
                            <button class="btn btn-danger" onclick="excluirTopico(${topico.id})">Excluir</button>
                        </div>
                    </div>
                `;
            });
        } else {
            lista.innerHTML = '<p class="loading">Nenhum tópico encontrado.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar tópicos', 'erro');
    }
});

async function excluirTopico(id) {
    if (!confirm('Tem certeza? Todas as respostas serão excluídas.')) return;
    
    try {
        const response = await fetch(`${API_URL}/topicos/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(resultado.message, 'sucesso');
            document.getElementById('form-buscar-topico').dispatchEvent(new Event('submit'));
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir tópico', 'erro');
    }
}

// ========== RESPOSTAS ==========

document.getElementById('form-resposta')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = {
        conteudo: document.getElementById('resp_conteudo').value,
        topico_id: parseInt(document.getElementById('resp_topico').value),
        usuario_id: usuarioLogado.id,
    };
    
    const respostaPaiId = document.getElementById('resp_pai').value;
    if (respostaPaiId) {
        formData.resposta_pai_id = parseInt(respostaPaiId);
    }
    
    try {
        const response = await fetch(`${API_URL}/respostas`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(`Resposta criada! ID: ${resultado.resposta_id}`, 'sucesso');
            this.reset();
        } else {
            mostrarMensagem(resultado.message || 'Erro ao criar resposta', 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao conectar com o servidor', 'erro');
    }
});

document.getElementById('form-buscar-resposta')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const topicoId = document.getElementById('buscar_resp_topico').value;
    
    try {
        const response = await fetch(`${API_URL}/respostas/topico/${topicoId}`);
        const resultado = await response.json();
        
        const lista = document.getElementById('lista-respostas');
        
        if (resultado.success && resultado.data.length > 0) {
            lista.innerHTML = `<p><strong>Total:</strong> ${resultado.total}</p>`;
            
            function renderizarResposta(resposta, nivel = 0) {
                const classes = ['resultado-item'];
                if (resposta.melhor_resposta) classes.push('resposta-destaque');
                if (nivel > 0) classes.push('resposta-aninhada');
                
                let html = `
                    <div class="${classes.join(' ')}">
                        <p><strong>ID:</strong> ${resposta.id} | <strong>Autor:</strong> ${resposta.autor} (${resposta.tipo_usuario})
                        ${resposta.melhor_resposta ? '<span class="badge badge-success">Melhor Resposta</span>' : ''}
                        </p>
                        <p>${resposta.conteudo}</p>
                        <p><strong>Votos:</strong> ${resposta.votos} | <strong>Data:</strong> ${formatarData(resposta.criado_em)}</p>
                        <div class="resultado-acoes">
                            <button class="btn btn-success" onclick="votar(${resposta.id}, ${usuarioLogado.id})">Votar</button>
                            <button class="btn btn-danger" onclick="excluirResposta(${resposta.id})">Excluir</button>
                        </div>
                `;
                
                if (resposta.respostas_filhas && resposta.respostas_filhas.length > 0) {
                    resposta.respostas_filhas.forEach(filha => {
                        html += renderizarResposta(filha, nivel + 1);
                    });
                }
                
                html += '</div>';
                return html;
            }
            
            resultado.data.forEach(resposta => {
                lista.innerHTML += renderizarResposta(resposta);
            });
        } else {
            lista.innerHTML = '<p class="loading">Nenhuma resposta encontrada.</p>';
        }
    } catch (error) {
        mostrarMensagem('Erro ao buscar respostas', 'erro');
    }
});

async function votar(respostaId, usuarioId) {
    try {
        const response = await fetch(`${API_URL}/respostas/${respostaId}/votar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ usuario_id: usuarioId })
        });
        
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(resultado.message, 'sucesso');
            document.getElementById('form-buscar-resposta').dispatchEvent(new Event('submit'));
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao votar', 'erro');
    }
}

async function excluirResposta(id) {
    if (!confirm('Tem certeza que deseja excluir esta resposta?')) return;
    
    try {
        const response = await fetch(`${API_URL}/respostas/${id}`, { method: 'DELETE' });
        const resultado = await response.json();
        
        if (resultado.success) {
            mostrarMensagem(resultado.message, 'sucesso');
            document.getElementById('form-buscar-resposta').dispatchEvent(new Event('submit'));
        } else {
            mostrarMensagem(resultado.message, 'erro');
        }
    } catch (error) {
        mostrarMensagem('Erro ao excluir resposta', 'erro');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    verificarLogin();
    carregarCursos();
    mostrarMensagem('Sistema carregado com sucesso!', 'info');
});
