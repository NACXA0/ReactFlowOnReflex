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


#print(offical_switch_case.to_snake_case('onPaneContextMenu'))





import requests
import json

import os

virtual_env = os.environ.get('VIRTUAL_ENV')
if virtual_env:
    print("当前在虚拟环境中，虚拟环境路径:", virtual_env)
else:
    print("不在虚拟环境中")


