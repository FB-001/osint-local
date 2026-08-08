# Roadmap — OSINT Local

O desenvolvimento do OSINT Local prioriza utilidade operacional,
simplicidade, funcionamento local e uso de fontes públicas confiáveis.

Funcionalidades sem utilidade prática suficiente ou dependentes de
fontes instáveis não serão mantidas apenas para ampliar o número de
recursos do sistema.

---

## Sprint 1 — Base do projeto

- [x] Estrutura inicial do projeto
- [x] CLI
- [x] Análise de metadados de imagens
- [x] Extração de EXIF
- [x] Cálculo de SHA-256
- [x] Comparação de arquivos por SHA-256

---

## Sprint 2 — Interface e confiabilidade

- [x] Interface em português
- [x] Padronização da saída no terminal
- [x] Padronização dos relatórios
- [x] Tratamento de erros
- [x] Mensagens amigáveis ao operador
- [x] Organização da interface da CLI

---

## Sprint 3 — Coletores públicos

- [x] Desenvolvimento inicial de coletores por username
- [x] Avaliação prática das fontes disponíveis
- [x] Testes com GitHub, GitLab e Mastodon
- [x] Remoção da busca por username após avaliação de utilidade

A busca por username foi retirada porque as principais redes sociais
não oferecem acesso público adequado para o modelo de funcionamento
pretendido pelo OSINT Local.

---

## Sprint 4 — Consulta empresarial e refatoração

- [x] Consulta pública por CNPJ
- [x] Integração com BrasilAPI
- [x] Razão social e nome fantasia
- [x] Situação cadastral
- [x] Porte da empresa
- [x] Data de início da atividade
- [x] Capital social
- [x] Natureza jurídica
- [x] Atividade principal
- [x] Atividades secundárias
- [x] Endereço
- [x] Telefone e e-mail quando disponíveis
- [x] Quadro societário
- [x] Identificação da fonte consultada
- [x] Observação sobre tratamento de dados e LGPD

### Refatoração

- [x] Organização dos coletores por domínio
- [x] Estrutura `collectors/company/`
- [x] Estrutura `collectors/image/`
- [x] Remoção dos coletores de username
- [x] Remoção de modelos experimentais não utilizados
- [x] Remoção de código legado
- [x] Simplificação da estrutura do projeto

---

## Sprint 5 — Relatórios HTML offline

- [ ] Definir estrutura padrão do relatório HTML
- [ ] Criar gerador HTML reutilizável
- [ ] Exportar consulta de CNPJ para HTML
- [ ] Exportar análise de imagem para HTML
- [ ] Exportar comparação SHA-256 para HTML
- [ ] Registrar data e hora da geração
- [ ] Registrar versão do OSINT Local
- [ ] Registrar fonte dos dados quando aplicável
- [ ] Garantir funcionamento totalmente offline
- [ ] Garantir que o relatório seja autossuficiente

O relatório HTML deverá funcionar sem conexão com a internet e não
depender de CSS, fontes, scripts ou outros recursos externos.

A geração nativa de PDF não faz parte da versão 1.0. Quando necessário,
o relatório HTML poderá ser convertido para PDF pelo navegador.

---

# Objetivo da versão 1.0 CLI

A versão 1.0 deverá fornecer uma ferramenta local, simples e confiável
para:

- análise de metadados de imagens;
- verificação e comparação de integridade por SHA-256;
- consulta pública de informações empresariais por CNPJ;
- apresentação padronizada dos resultados;
- exportação de relatórios HTML offline.

---

# Após a versão 1.0

Funcionalidades futuras serão avaliadas conforme necessidade prática.

## Interface gráfica

- [ ] Interface gráfica para operação do sistema
- [ ] Integração dos recursos existentes da CLI
- [ ] Exportação de relatórios pela interface
- [ ] Distribuição como AppImage

## Persistência e investigações

- [ ] Banco de dados local
- [ ] Casos de investigação
- [ ] Registro de evidências
- [ ] Timeline
- [ ] Histórico de consultas

## Expansões

- [ ] Sistema de plugins
- [ ] Integração opcional com IA local
- [ ] Novos coletores públicos quando houver fontes adequadas
- [ ] Correlação de dados
- [ ] API local

## Auditoria e operação em equipe

- [ ] Perfis de operador
- [ ] Identificação do responsável por cada ação
- [ ] Histórico de alterações
- [ ] Registro de coleta de evidências
- [ ] Trilha de auditoria
- [ ] Controle de acesso por perfil

---

# Princípios do projeto

O OSINT Local deverá priorizar:

1. funcionamento local sempre que possível;
2. privacidade;
3. simplicidade para o operador;
4. fontes públicas e legalmente acessíveis;
5. transparência sobre a origem das informações;
6. modularidade;
7. ausência de dependências desnecessárias;
8. utilidade operacional acima da quantidade de funcionalidades.
