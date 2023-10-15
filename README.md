# Trabalho sobre RPC

O objetivo deste trabalho é implementar uma ferramenta para CSCW (Computer Supported Cooperative Work) que permita a edição de documentos de forma concorrente por diversos usuários. A ferramenta utiliza uma arquitetura cliente/servidor e deve ser implementada usando RPC.
Os usuários devem estar previamente cadastrados em um arquivo "users.txt", o qual o servidor utiliza para fazer a autenticação de cada usuário.

Cada usuário pode criar documentos. Um documento pode ser compartilhado por diversos usuários. Para que isso aconteça, um dos usuários do documento deve habilitar o acesso ao documento para outro usuário existente na base de usuários.

Os documentos não podem ser apagados. Não é necessário manter a persistência dos documentos, isto é, as informações podem ser mantidas em memória.
Um documento possui um título e data/hora de última atualização. Cada documento é formado por um conjunto de "notas". Para adicionar conteúdo ao documento, qualquer usuário que possua acesso ao documento deve requisitar a inclusão de uma nova nota e indicar o conteúdo da mesma. Cada nota deve possuir um título e conteúdo. Além disso, qualquer usuário com acesso ao documento
também pode editar qualquer nota do documento. Uma nota só pode ser editada por um usuário por vez. Caso seja realizada a tentativa de editar uma nota em processo de edição por outro usuário, então a requisição deve retornar um erro.

O programa cliente deve permitir as seguintes funções ao usuário:
1) Listar usuários existentes no servidor
2) Criar um documento
3) Associar um outro usuário ao documento
4) Listar documentos que tem acesso apresentando o título de cada documento
5) Listar documentos que tem acesso e foram alterados a partir de uma data/hora específica
6) Apresentar detalhes sobre um documento, como: título do documento, última alteração, usuários que têm acesso, títulos das notas e indicação se existe algum usuário editando alguma nota no momento
7) Criar uma nota em um documento
8) Editar uma nota em um documento
9) Listar o conteúdo de uma nota
10) Listar o conteúdo de um documento (todas as notas)

A entrega do trabalho será feita por todos os grupos até o dia 09/10. Além disso, cada grupo deverá fazer uma apresentação em sala de
aula laboratório (no dia da entrega). Nesse dia, todos os participantes do grupo deverão estar presentes participantes ausentes ficarão sema nota do trabalho 2. O grupo deverá entregar a documentação e enviar para o e-mail do professor o código fonte do programa após a apresentação. A documentação deve obrigatoriamente incluir a descrição de como deve ser executado o programa do grupo e uma explicação sobre a implementação. Somente serão avaliados trabalhos que executem. Todos os trabalhos serão analisados e
comparados. Caso seja identificada cópia de trabalhos, todos os trabalhos envolvidos receberão nota ZERO. Trabalhos com atraso serão aceitos mediante um desconto de 2.0 pontos na nota final por dia de aula de
atraso. Este trabalho deverá ser feito em grupo de no máximo 4 componentes.

## Instruções

1) Clone o repo.
2) Instale as depêndencias
3) Rode o codigo do server e do client