"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config # 这里是正确的，虽然有红线  from rxconfig import config
import reflex as rx
from reflex_react_flow import react_flow, background, controls#base_edge, control_button, controls#, edge_label_renderer, edge_text, handle, mini_map, node_resize_control, node_resizer, node_toolbar, panel, viewport_portal
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

    # 占位符事件处理器——为事件处理器提供一个虚假的接入点
    @rx.event
    def fake_event_handel(self, *args, **kwargs):
        print('触发了占位符事件处理器.******************************')
        print("位置参数:") if args else None
        for arg in args:
            print(f'触发事件数据类型:{type(arg)}, 触发事件数据:{arg}')

        print("\n关键字参数:") if kwargs else None
        for key, value in kwargs.items():
            print(f"{key}: {value}")


# region 下面是一级组件
# 背景
def component_background() -> rx.Component:
    '''这个做的比较完善，可以参考'''
    return background(
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
    )
#
def component_base_edge() -> rx.Component:
    return #base_edge()
# 控制按钮
def component_control_button() -> rx.Component:
    return #control_button()
# 控制
def component_controls() -> rx.Component:
    return controls(
        #showZoom=True,
        #showFitView=True,
        #showInteractive=True,
        # fitViewOptions=None   【以后再说】
        #onZoomIn=None,
        #onZoomOut=None,
        #onFitView=None,
        #onInteractiveChange=None,
        #position='bottom-left',
        #children=None,
        #style={},  # 应用于容器的样式
        #className=None,  # 应用于容器的类名
        #aria_label='React Flow controls',
        #orientation='vertical'

    )
#
def component_edge_label_renderer() -> rx.Component:
    return #edge_label_renderer()
#
def component_edge_text() -> rx.Component:
    return #edge_text()
# 连接点
def component_handle() -> rx.Component:
    return #handle()
# 地图
def component_mini_map() -> rx.Component:
    return #mini_map()
#
def component_node_resize_control() -> rx.Component:
    return #node_resize_control()
#
def component_node_resizer() -> rx.Component:
    return #node_resizer()
#
def component_node_toolbar() -> rx.Component:
    return #node_toolbar()
#
def component_panel() -> rx.Component:
    return #panel()
#
def component_viewport_portal() -> rx.Component:
    return #viewport_portal()


# react_flow主要部分——完全版
def component_react_flow() -> rx.Component:
    return react_flow(
        # region 常见道具
        width = None,
        height = None,
        nodes = State.nodes,
        edges = State.nodes,
        defaultEdges = None,
        paneClickDistance = 0,
        nodeClickDistance = 0,
        nodeTypes = 'default',
        edgeTypes = 'default',
        autoPanOnNodeFocus = True,
        nodeOrigin = [0, 0],
        proOptions = None,
        nodeDragThreshold = 1,
        connectionDragThreshold = 1,
        colorMode = 'light',
        debug = False,
        ariaLabelConfig = None,
        # endregion

        # region 视觉(viewport)道具
        defaultViewport = { 'x': 0, 'y': 0, 'zoom': 1 },
        viewport = None,
        onViewportChange = None,
        fit_view = None,
        fitViewOptions = None,
        minZoom = 0.5,
        maxZoom = 2.0,
        snapToGrid = None,
        snapGrid = None,
        onlyRenderVisibleElements = False,
        translateExtent = None,
        nodeExtent = None,
        preventScrolling = True,
        attributionPosition = 'bottom-right',
        # endregion

        # region 边缘(edge)道具
        elevateEdgesOnSelect = None,
        defaultMarkerColor = None,
        defaultEdgeOptions = None,
        reconnectRadius = 10,
        edgesReconnectable = None,
        # endregion

        # region 事件处理程序——一般(general)事件
        onError=State.fake_event_handel('onError'),
        onInit=State.fake_event_handel('onInit'),
        onDelete=State.fake_event_handel('onDelete'),
        onBeforeDelete=State.fake_event_handel('onBeforeDelete'),
        # endregion

        # region 事件处理程序——节点(Node)事件
        # endregion

        # region 事件处理程序——节点(Node)事件
        on_nodes_change=lambda e0: State.on_nodes_change(e0),
        # endregion

        # region 事件处理程序——边缘(Edge)事件
        # endregion

        # region 事件处理程序——连接(Connect)事件
        on_connect=lambda e0: State.on_connect(e0),
        # endregion

        # region 事件处理程序——窗格(Pane)事件
        # endregion

        # region 事件处理程序——选择(select)事件
        # endregion

        # region 下面是交互(interaction)道具
        nodes_draggable = True,
        nodes_connectable = True,
        nodes_focusable = True,
        edgesFocusable = True,
        elementsSelectable = True,
        autoPanOnConnect = True,
        autoPanOnNodeDragt = True,
        autoPanSpeed = 15,
        panOnDrag = True,
        selectionOnDrag = False,
        selectionMode = 'full',
        panOnScroll = False,
        panOnScrollSpeed = 0.5,
        panOnScrollMode = 'free',
        zoomOnScroll = True,
        zoomOnPinch = True,
        zoomOnDoubleClick = True,
        selectNodesOnDrag = True,
        elevateNodesOnSelect = True,
        connectOnClick = True,
        connectionMode = 'strict',
        # endregion

        # region 下面是连接线(connection)道具
        connectionLineStyle = {},
        connectionLineType = 'default',
        connectionRadius = 20,
        # connectionLineComponent
        connectionLineContainerStyle = {},
        # endregion

        # region 下面是键盘(KBd)道具
        deleteKeyCode = 'Backspace',
        selectionKeyCode = 'Shift',
        multiSelectionKeyCode = "'Meta' for macOS, 'Control' for other systems",
        zoomActivationKeyCode = "'Meta' for macOS, 'Control' for other systems",
        panActivationKeyCode = 'Space',
        disableKeyboardA11y = False,
        # endregion

        # region 下面是风格(Style)道具
        noPanClassName = 'nopan',
        noDragClassName = 'nodrag',
        noWheelClassName = 'nowheel'
        # endregion

    )

# react_flow主要部分——使用版本  从完全版选取部分
def component_react_flow_demo() -> rx.Component:
    return react_flow(
        # 调用组件部分
        background(),
        controls(),
        做到这里了，1. 组件需要调用的 2.尽量在运行的时候调试，不然真的追踪不到报错 3. hooks暂时放一放
        # 本身参数部分
        nodes_draggable=True,
        nodes_connectable=True,
        on_connect=lambda e0: State.on_connect(e0),
        on_nodes_change=lambda e0: State.on_nodes_change(e0),
        nodes=State.nodes,
        edges=State.edges,
        fit_view=True
    )


# endregion

# 下面是页面组件
def index() -> rx.Component:
    return rx.vstack(
        component_react_flow_demo(),

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
        height="30em",
        width="100%",
    )









# Add state and page to the app.
app = rx.App()
app.add_page(index)
