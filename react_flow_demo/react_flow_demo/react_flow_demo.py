"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config # 这里是正确的，虽然有红线  from rxconfig import config
import reflex as rx
from reflex_react_flow import react_flow, background, controls
import random
from collections import defaultdict
from typing import Any, Dict, List
filename = f"{config.app_name}/{config.app_name}.py"

# 下面是默认值
initial_nodes = [
    {
        'id': '1',
        'type': 'input',
        'data': {'label': '150'},
        'position': {'x': 0, 'y': 0},
    },
    {
        'id': '2',
        'data': {'label': '25'},
        'position': {'x': 100, 'y': 125},
    },
    {
        'id': '3',
        'type': 'output',
        'data': {'label': '5'},
        'position': {'x': 250, 'y': 250},
    },
]

initial_edges = [
    {'id': 'e1-2', 'source': '1', 'target': '2', 'label': '*', 'animated': True},
    {'id': 'e2-3', 'source': '2', 'target': '3', 'label': '+', 'animated': True},
]


class State(rx.State):
    """The app state."""
    nodes: List[Dict[str, Any]] = initial_nodes
    edges: List[Dict[str, Any]] = initial_edges
    new_node_example: Dict[str, Any] = {}   # 示例节点: 编辑希望添加的节点的样式
    new_node_type: str = ''

    @rx.event
    def add_random_node(self):
        new_node_id = f'{len(self.nodes) + 1}'
        node_type = random.choice(['default'])
        # Label is random number
        label = new_node_id
        x = random.randint(0, 500)
        y = random.randint(0, 500)

        new_node = {
            'id': new_node_id,
            'type': node_type,
            'data': {'label': label},
            'position': {'x': x, 'y': y},
            'draggable': True,
        }
        self.nodes.append(new_node)

    @rx.event
    def clear_graph(self):
        self.nodes = []  # Clear the nodes list
        self.edges = []  # Clear the edges list

    @rx.event
    def on_connect(self, new_edge):
        # Iterate over the existing edges
        for i, edge in enumerate(self.edges):
            # If we find an edge with the same ID as the new edge
            if edge["id"] == f"e{new_edge['source']}-{new_edge['target']}":
                # Delete the existing edge
                del self.edges[i]
                break

        # Add the new edge
        self.edges.append({
            "id": f"e{new_edge['source']}-{new_edge['target']}",
            "source": new_edge["source"],
            "target": new_edge["target"],
            "label": random.choice(["+", "-", "*", "/"]),
            "animated": True,
        })

    @rx.event
    def on_nodes_change(self, node_changes: List[Dict[str, Any]]):
        # 在发生拖动等事件时接收节点列表
        map_id_to_new_position = defaultdict(dict)

        # 循环更改并存储新位置
        for change in node_changes:
            if change["type"] == "position" and change.get("dragging") == True:
                map_id_to_new_position[change["id"]] = change["position"]

        # 在节点上循环并更新位置
        for i, node in enumerate(self.nodes):
            if node["id"] in map_id_to_new_position:
                new_position = map_id_to_new_position[node["id"]]
                self.nodes[i]["position"] = new_position

    @rx.event
    def reset_var(self):
        self.reset()

def index() -> rx.Component:
    return rx.vstack(
        react_flow(
            background(
                id=None,
                color='black',   # 图案的颜色。
                bgColor='white',  # 背景颜色
                className=None,  # 应用于容器的类
                patternClassName=None,  # 应用于模式的类。
                gap=20,  # 模式之间的间隙。传入元组可以控制 x 和 y 间隙 独立地。
                size=None,
                offset=0,  # 图案的偏移量
                lineWidth=1,  # 绘制图案时使用的描边粗细。
                variant=None,  # 图案的变体。
                style={}  # 应用于容器的样式。
            ),
            controls(),
            nodes_draggable=True,
            nodes_connectable=True,
            on_connect=lambda e0: State.on_connect(e0),
            on_nodes_change=lambda e0: State.on_nodes_change(e0),
            nodes=State.nodes,
            edges=State.edges,
            fit_view=True,
        ),


        rx.button(
            "清除图像",
            on_click=State.clear_graph,
            width="100%",
        ),
        rx.button(
            "添加节点",
            on_click=State.add_random_node,
            width="100%",
        ),
        rx.button(
            '重置',
            on_click=State.reset_var,
            width="100%",
        ),
        rx.card(
            #react_flow(
            #    nodes_draggable=True,
            #    nodes_connectable=True,
            #    nodes=State.example_node,
            #    fit_view=True,
            #),

        ),
        height="30em",
        width="100%",
    )










# Add state and page to the app.
app = rx.App()
app.add_page(index)
