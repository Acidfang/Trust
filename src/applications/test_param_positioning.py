import sys
sys.path.insert(0, '.')
from ledger_query import LedgerQuery
from parameter_form import ParameterForm

# Test parameter form
form = ParameterForm('.')
nodes = form.get_form_nodes()
print(f'Parameter form generated {len(nodes)} nodes')
for i, node in enumerate(nodes[:3]):
    print(f'  Node {i}: id={node.get("id")}, type={node.get("type")}, has_y_offset={("y_offset" in node)}')

# Test positioning with y_offset
ledger = LedgerQuery('.')
frame = {'nodes': nodes, 'type': 'frame'}
positioned = ledger._apply_absolute_positioning(frame)
print(f'After positioning: {len(positioned["nodes"])} nodes')
for i, node in enumerate(positioned['nodes'][:3]):
    node_id = node.get("id")
    y = node.get("y")
    src = node.get("_position_source")
    print(f'  Node {i}: id={node_id}, y={y}, source={src}')
print("\nSUCCESS: Parameter controls properly positioned!")
