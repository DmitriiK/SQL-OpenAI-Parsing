import unittest

from modules.mermaid_diagram import MermaidDiagram


class TestMMGen(unittest.TestCase):
    def test_mm_gen(self):
        diagram = MermaidDiagram()
        diagram.add_node("A")
        diagram.add_node("B")
        diagram.add_node("C")
        diagram.add_node("D")

        diagram.add_edge("A", "B", 'a2b')
        diagram.add_edge("A", "C", 'a2c')
        diagram.add_edge("B", "D")
        diagram.add_edge("C", "D")

        mermaid_code = diagram.generate_mermaid_code()
        print(mermaid_code)


"""
This will output:
```
flowchart TD;
    A[A];
    B[B];
    C[C];
    D[D];
    A-->B;
    A-->C;
    B-->D;
    C-->D;
    
    """

if __name__ == '__main__':
    print('main')
    unittest.main()
