import re

# 官方的命名转换，可能用于包裹react时，将react组件参数的camel(驼峰命名法)转为snake(蛇形命名法)
class offical_switch_case:
    # .venv/Lib/site-packages/reflex/utils/format.py:156
    def to_snake_case(text: str) -> str:
        """Convert a string to snake case.

        The words in the text are converted to lowercase and
        separated by underscores.

        Args:
            text: The string to convert.

        Returns:
            The snake case string.
        """
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", text)
        return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower().replace("-", "_")

    def to_camel_case(text: str, treat_hyphens_as_underscores: bool = True) -> str:
        """Convert a string to camel case.

        The first word in the text is converted to lowercase and
        the rest of the words are converted to title case, removing underscores.

        Args:
            text: The string to convert.
            treat_hyphens_as_underscores: Whether to allow hyphens in the string.

        Returns:
            The camel case string.
        """
        if treat_hyphens_as_underscores:
            text = text.replace("-", "_")
        words = text.split("_")
        # Capitalize the first letter of each word except the first one
        if len(words) == 1:
            return words[0]
        return words[0] + "".join([w.capitalize() for w in words[1:]])


print(offical_switch_case.to_snake_case('onPaneContextMenu'))

{
    'isValid': False, 'from': {'x': 124.99982508047702, 'y': 163.9999125402385},
    'fromHandle': {'id': None, 'type': 'source'': '2', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}, 'fromPosition': 'bottom', 'fromNode': {'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 50, 'y': 125}, 'measured': {'width': 150, 'height': 40}, 'internals': {'positionAbsolute':
                       {'x': 50, 'y': 125}, 'handleBounds': {'source': [
            {'id': None, 'type': 'source', 'nodeId': '2', 'position': 'bottom', 'x': 71.99982508047702,
             'y': 35.99991254023851, 'width': 6, 'height': 6}], 'target': [
    {'id': None, 'type': 'target', 'nodeId': '2', 'position': 'top', 'x': 71.99982508047702, 'y': -1.999994525565665,
     'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '2', 'type': 'default', 'data': {'label': '25'},
                                                      'position': {'x': 50, 'y': 125}}}}, 'to': {'x': 416,
                                                                                                 'y': 220}, 'toHandle': {
    'id': None, 'type': 'source', 'nodeId': '4', 'position': 'bottom', 'x': 424.999825080477, 'y': 188.9999125402385,
    'width': 6, 'height'
    : 6}, 'toPosition': 'top', 'toNode': {'id': '4', 'type': 'default', 'data': {'label': '5'},
                                          'position': {'x': 350, 'y': 150}, 'measured': {'width': 150, 'heig
        ht': 40}, 'internals': {'positionAbsolute': {'x': 350, 'y': 150}, 'handleBounds': {'source': [{'id': None, 'type
                                                                                         ': 'source', 'nodeId': '4
                                                                                         ', 'position': 'botto
                                                                                         m', 'x': 71.99982508047702, '
                                                                                         y': 35.99991254023851, '
                                                                                         width': 6, 'height': 6}], '
                                                                                         target': [{'id': None, '
                                                                                         type': 'target', 'nodeId': '
                                                                                         4', 'position': 'top', 'x'
: 71.99982508047702, 'y': -1.999994525565665, 'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '4',
                                                                                               'type': 'default',
                                                                                               'data': {'label': '5'},
                                                                                               'position': {'x': 350,
                                                                                                            'y': 150}}}}}
