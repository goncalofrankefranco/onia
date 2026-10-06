# Códigos Python de Machine Learning que usei para estudar para a ONIA
### Estão reunidos aqui diversas demonstrações de modelos de ML Clássico, útil para quem gostaria de entender exemplos simples dos mesmos.

## Demonstração
![Demonstração](./assets/demo.png)


## Instalação
É necessário ter python, scikit-learn, pandas, matplotlib, numpy, pytorch, tqdm e seaborn instalados no sistema. As versões específicas estão disponíveis em https://github.com/goncalofrankefranco/onia/blob/main/requirements.txt

Além disso, git é preferido para que se possa clonar o projeto. 

Para instalar o repositório, digite git clone https://github.com/goncalofrankefranco/onia.git em qualquer pasta para salvar os arquivos. Em seguida, entre na pasta do projeto e escreva pip install -r requirements.txt para garantir que todas as bibliotecas necessárias estão instaladas. Para executar FlorestaAleatoria.py, por exemplo, basta usar a IDE de sua preferência com Python configurado e rodar o código. Esse código procura Data/diabetes.csv a partir da pasta de execução, então é importante não embaralhar a hierarquia das pastas do projeto.

Para executar a demonstração de trânsito, basta realizar o mesmo procedimento descrito acima mas com o arquivo Q-Learning.py.

## Exemplo

Ao executar FlorestaAleatoria.py, com random_state=42, o código deverá imprimir as seguintes informações:
TRAINING:
Accuracy: 84.52768729641694%
Precision: 72.01492537313433%
Recall: 90.61032863849765%
F1: 80.24948024948026%
Confusion Matrix: [[326  75]
 [ 20 193]]

TEST:
Accuracy: 74.67532467532467%
Precision: 60.526315789473685%
Recall: 83.63636363636363%
F1: 70.22900763358778%
Confusion Matrix: [[69 30]
 [ 9 46]]

 ## Estrutura do Projeto
 /Data -> possui todos os dados necessários para rodar os códigos Python que não estão dentro da pasta PyTorch.
 /PyTorch -> apresenta 5 códigos cujos datasets não estão disponíveis. É útil principalmente para analisar a estrutura do código em vez de testar.
 Além disso -> todos os códigos de ML clássico, com seus datasets em /Data.

 ## Licença
 A licença utilizada é a do MIT, disponível em ![Licença](./LICENCE)
 
 Texto da licença:
 MIT License

Copyright (c) 2026 Gonçalo Franco

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

 
