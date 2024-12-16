# README

## Membros do Grupo
- **Gabriel Franco Jallais**
- **Henrique Daniel de Sousa**
- **Igor Joaquim da Silva Costa**

## Explicação do Sistema
O sistema desenvolvido tem como objetivo extrair dados presentes em documentos e validá-los conforme regras de negócio pré-definidas. Algumas informações, como o **TIPO DE DOCUMENTO** e **ASSUNTO**, são extraídas do contexto geral do texto, enquanto outras, como **CIDADE** ou **EMPRESA**, são verificadas com base em uma base de dados conhecida.

A IA utilizada no sistema, apresenta as seguintes características principais:
- Dispensa um volume significativo de documentos para treinamento inicial.
- Não exige que os documentos sigam formatações específicas ou utilizem templates padronizados.

## Tecnologias Utilizadas

### Backend
- **Python**: Linguagem principal utilizada no sistema.
- **Google Generative AI**: Utilizada para gerar conteúdos por meio do modelo **Gemini 1.5 Flash**.

### Frontend
- **HTML, CSS e JavaScript**: Linguagens padrão para estrutura, estilo e interatividade.
- **Bootstrap**: Framework CSS utilizado para um design responsivo e estilizado.

### Funcionalidades
A comunicação entre o backend e o modelo **Gemini 1.5 Flash** é feita utilizando as bibliotecas disponibilizadas pelo Google Generative AI. O modelo é configurado para gerar respostas otimizadas com até 5000 tokens, utilizando um **temperature** de 0.2 e **top-p** de 0.9, garantindo precisão e contextualização.
