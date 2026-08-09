# Roadmap — PERSPICIO

O desenvolvimento do PERSPICIO prioriza utilidade operacional,
simplicidade, processamento local sempre que possível e transparência
sobre a origem das informações.

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

## Sprint 3 — Avaliação de coletores públicos

- [x] Desenvolvimento inicial de coletores por username
- [x] Avaliação prática das fontes disponíveis
- [x] Testes com GitHub, GitLab e Mastodon
- [x] Remoção da busca por username após avaliação de utilidade

A busca por username foi retirada porque as principais redes sociais
não oferecem acesso público adequado ao modelo de funcionamento
pretendido pelo PERSPICIO.

A decisão estabelece um princípio do projeto: uma funcionalidade não
será mantida apenas porque é tecnicamente possível implementá-la.

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
- [x] Adoção da identidade PERSPICIO
- [x] Renomeação do pacote Python para `perspicio`
- [x] Renomeação do comando principal para `perspicio`

---

## Sprint 5 — Análise de Propaganda Adversa — OCAVE

- [ ] Criar estrutura do módulo de análise de propaganda
- [ ] Criar modelo de análise OCAVE
- [ ] Origem — Quem?
- [ ] Conteúdo — O quê?
- [ ] Audiência-alvo — Para quem?
- [ ] Veículo de Difusão — Como?
- [ ] Efeito — Para quê?
- [ ] Permitir quesitos ainda não determinados
- [ ] Registrar observações do analista
- [ ] Criar apresentação padronizada da análise
- [ ] Integrar o comando à CLI
- [ ] Testar uma análise OCAVE completa

A análise OCAVE deverá apoiar o raciocínio do operador sem forçar
conclusões quando os dados disponíveis forem insuficientes.

O PERSPICIO organiza e apresenta os elementos da análise.
A interpretação e as conclusões permanecem sob responsabilidade
do operador.

---

# Próximas etapas

As próximas capacidades serão desenvolvidas conforme necessidade
operacional e maturidade da arquitetura.

## Interface gráfica

- [ ] Interface gráfica para operação do sistema
- [ ] Integração dos recursos existentes da CLI
- [ ] Integração das ferramentas de análise
- [ ] Visualização estruturada dos resultados
- [ ] Exportação de resultados quando houver necessidade operacional
- [ ] Avaliar distribuição como AppImage

## Persistência e investigações

- [ ] Banco de dados local
- [ ] Casos de investigação
- [ ] Registro de evidências
- [ ] Timeline
- [ ] Histórico de consultas
- [ ] Histórico de análises

## Métodos de análise

- [ ] Avaliar outros métodos estruturados de análise
- [ ] Desenvolver novos módulos somente quando houver utilidade
      operacional demonstrada
- [ ] Permitir integração entre informações coletadas e métodos
      analíticos

## Expansões

- [ ] Sistema de plugins
- [ ] Integração opcional com IA local
- [ ] Novos coletores públicos quando houver fontes adequadas
- [ ] Correlação de dados quando houver base confiável
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

O PERSPICIO deverá priorizar:

1. operador no centro do processo;
2. funcionamento local sempre que possível;
3. privacidade;
4. simplicidade;
5. fontes públicas e legalmente acessíveis;
6. transparência sobre a origem das informações;
7. separação entre fato observado e interpretação;
8. explicabilidade;
9. modularidade;
10. ausência de dependências desnecessárias;
11. utilidade operacional acima da quantidade de funcionalidades.
