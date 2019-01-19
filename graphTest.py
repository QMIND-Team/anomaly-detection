from graphviz import Digraph

dot = Digraph(comment="The Round Table")

dot #doctest: +ELLIPSIS

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')
dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)

dot.render('round-table.gv', view=True)