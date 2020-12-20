from conjecture import fast_streak, streak, N2357, N237, prime_powers2357
from itertools import product
from graphviz import Digraph
from string import Template

g = Digraph(
      comment='Multiplicative Persistence', 
      format='svg', 
      filename='test',
      engine='twopi',
      strict=True
      )

g.attr('graph', overlap='false', ratio="auto", splines='true')
g.attr('node', shape='box', style='filled', fontname="Arial",
# fixedsize="true", width="1.0", height="0.40",
fontsize='10')

colors = [ '#F5B7B1', '#D2B4DE', '#A9CCE3',
           '#7DCEA0', '#D5F5E3', '#FCF3CF',
           '#FDEBD0', '#FAE5D3', '#F6DDCC',
           '#E6B0AA'
         ]

def html_node(TWO,THREE,FIVE,SEVEN):
    num = N2357(TWO,THREE,FIVE,SEVEN)
    s = Template('''<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0">
      <TR>
        <TD COLSPAN="4">$num</TD>
      </TR>
      <TR>
        <TD>$two</TD>
        <TD>$three</TD>
        <TD>$five</TD>
        <TD>$seven</TD>
      </TR>
    </TABLE>>'''
    )
    return s.substitute(num=str(num),two=str(TWO),three=str(THREE),five=str(FIVE),seven=str(SEVEN))

def add_to_graph(TWO,THREE,SEVEN):
    _streak = streak(N237(TWO,THREE,SEVEN))
    color = colors[len(_streak)-1]
    prev = _streak[0]
    # print(type(html_node(TWO,THREE,0,SEVEN)))
    g.node(str(prev),label=html_node(TWO,THREE,0,SEVEN),fillcolor=color)
    g.node('0_9', label="SINGLE\nDIGIT", shape="point",fillcolor="gainsboro")
    for i,n in enumerate(_streak[1:]) :
        two, three, five, seven = prime_powers2357(n)
        g.node(str(n),label=html_node(two,three,five,seven),fillcolor=colors[len(_streak)-i-2])
        g.edge(str(prev),str(n))
        prev = n
    g.edge(str(prev),'0_9')

if __name__ == '__main__':
    for seven, three, two in product( range(50), range(50), range(50) ):
        n = 2**two * 3**three * 7**seven
        # if '0' not in str(n) :
        if '0' not in str(n) and len( fast_streak(n) ) > 4:
            print( '\r({}, {}, {}) = {}'.format( two, three, seven , n ) )
            add_to_graph(two,three,seven)
    
    
    # print(g.source)
    g.render()
