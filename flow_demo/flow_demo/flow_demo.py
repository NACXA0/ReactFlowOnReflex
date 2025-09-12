"""Welcome to Reflex! This file showcases the custom component in a basic app."""

from rxconfig import config # 这里是正确的，虽然有红线  from rxconfig import config
import reflex as rx
from reflex_flow import flow, background, base_edge, control_button, controls, edge_label_renderer, edge_text, handle, mini_map, node_resize_control, node_resizer, node_toolbar, panel, viewport_portal
import random
from collections import defaultdict
from typing import Any, Dict, List
filename = f"{config.app_name}/{config.app_name}.py"
# 下面是默认值
initial_nodes = [
    {
        'id': '1',
        'position': {'x': 0, 'y': 0},
        'data': {'label': '150'},
        'type': 'input',
    },
    {
        'id': '2',
        'type': 'default',
        'data': {'label': '25'},
        'position': {'x': 50, 'y': 125},
    },
    {
        'id': '3',
        'type': 'default',
        'data': {'label': '5'},
        'position': {'x': 250, 'y': 0},
    },
    {
        'id': '4',
        'type': 'default',
        'data': {'label': '5'},
        'position': {'x': 350, 'y': 150},
    },
    {
        'id': '5',
        'position': {'x': 300, 'y': 300},
        'data': {'label': '节点-完全体示例'},
        'sourcePosition': 'left',   # 可选参数：'left', 'top', 'right', 'bottom'
        'targetPosition': 'left',   #  可选参数：'left', 'top', 'right', 'bottom'
        'hidden': False, # 节点是否隐藏
        'selected': False,   # 是否被选中
        'dragging': False, # 当前是否正在拖动节点。
        'draggable': True,  # 节点是否可以拖动。
        'selectable': True, # 是否可以被选中
        'connectable': True, # 是否可以被连接
        'deletable': True, # 是否可以被删除
        'dragHandle':  'handel5',   # 一个类名称，可以应用于节点内的元素，允许这些元素起作用 作为拖动手柄，允许用户通过单击并拖动这些元素来拖动节点。
        'width': 200, # 宽度
        'height': 50, # 高度
        'initialWidth': 50, # 内部宽度
        'initialHeight': 30, # 内部高度
        'parentId': 'unknow',   # 父节点 ID，用于创建子流
        'zIndex': 1,    # z轴高度
        'extent': [[-500, -500], [500, 500]], # 可以移动节点的边界       可选参数: [[number, number], [number, number]] | "parent" | null    参数解释: 1. 坐标范围表示坐标系中的两个点：一个位于顶部 左角和右下角的一个。它用于表示 流中节点的边界或视口的边界。 2. 跟随父节点 3. 【常用】无限大
        'expandParent': True,    # 当 True时，如果将父节点拖动到 父节点的边界
        'ariaLabel': '',  # 【未知】 aria标签
        'origin': [0, 0], # 节点相对于其位置的原点。  示例数据:[0, 0][0.5, 0.5][1, 1]  节点的原点决定了它相对于其自身坐标的放置方式。 将其放置在其位置的左上角、右侧中央和右下角。
        'handles': {
            'width': 200,
            'height': 100,
            'id': None, #    None 或者 str
            'x': 0,
            'y': 0,
            'position': 'left',   # 可选参数：'left', 'top', 'right', 'bottom'
            'type': 'source',  # 可选参数： 'source' | 'target'
        },
        'measured': {'width': 200, 'height': 100},
        'type': 'output',   # nodeTypes 中定义的节点类型    可选参数: 'input' | 'output' | 'default' | 'group'
        'style': {},
        'className': 'undefine',
        'resizing': False, # 正在重设大小
        'focusable': True,    # 是否可聚焦
        # 'ariaRole': 'group'  # 节点元素的 ARIA 角色属性，用于辅助功能。 【未知】
        # 'domAttributes': # 用于向节点的 DOM 元素添加自定义属性的通用逃生舱口。    【未知】



    }
]

initial_edges = [
    {
        'id': 'e1-2',
        'source': '1',
        'target': '2',
        'label': '*',
        'animated': True
    },
    {
        'id': 'e2-3',
        'source': '2',
        'target': '3',
        'label': '+',
        'animated': False,
        'data': {
          'label': '连接线标签',
        },
        'type': 'custom',
    },
    {   # 参考文档：https://reactflow.dev/api-reference/types/edge
        'id': 'e3-4',
        'type': 'default',   # 线条样式  可选内容: "default" | "straight" | "step" | "smoothstep" | "simplebezier"       可选内容解释： 1. default贝塞尔曲线(曲线样式) 2.smoothstep平滑阶梯边缘(直角样式)https://reactflow.dev/api-reference/types/edge
        'source': '3',  # 源节点的 ID。
        'target': '4',  # 目标节点的 ID。
        #'sourceHandle': '3', # string | null    注意！源句柄的 ID，仅当每个节点有多个句柄时才需要。 否则显示不出来
        #'targetHandle': '4', # string | null    注意！目标句柄的 ID，仅当每个节点有多个句柄时才需要。 否则显示不出来
        'animated': True,  # 动画连接线
        'hidden': False,    # 是否隐藏
        'deletable': True,     # 是否可删除
        'selectable': True, # 是否可被选中
        'data': {   # 类型: EdgeData       EdgeData
            'label': '连接线标签',
            'startLabel': '连接线起始标签',
            'endLabel': '连接线结束标签',
        },
        'selected': True,  # 选中了吗
        'markerStart': {    # 类型: EdgeMarkerType   将标记设置在边的开头。
            'type': 'arrow', #可选参数: "arrow" | "arrowclosed"
            'color': 'green',  # str | None    颜色
            'width': 10,  # int
            'height': 10,     # int
            'markerUnits': '',   # str 【未明确】
            'orient': '',     # str 【未明确】
            'strokeWidth': 10    # int 【未明确】
        },
        'markerEnd': {  # 类型: EdgeMarkerType   将标记设置在边的末端。
            'type': 'arrow', #可选参数: "arrow" | "arrowclosed"
            'color': 'green',  # str | None    颜色
            'width': 10,  # int
            'height': 10,     # int
            'markerUnits': '',   # str 【未明确】
            'orient': '',     # str 【未明确】
            'strokeWidth': 10    # int 【未明确】
        },
        'zIndex': 1, # z轴高度
        'ariaLabel': '',    # str   【未知作用】
        'interactionWidth': 10,   # int   ReactFlow 在每个边缘周围渲染一条不可见的路径，使它们更容易单击或点击。 此属性设置该不可见路径的宽度。
        'label': '连接线完全体', # 类型：ReactNode     要沿边缘渲染的标签或自定义元素。这通常是文本标签或一些自定义控件。
        'labelStyle': {},     # css 要应用于标签的自定义样式。
        'labelShowBg': True,     # bool
        'labelBgStyle': {},  # css
        'labelBgPadding': [10, 20],  # 【未知作用】
        'labelBgBorderRadius': 10,   # 【未知作用】
        'style': {},    #
        'className': 'undefine',    # str
        'reconnectable': True, # 类型: boolean | HandleType     确定是否可以通过将源或目标拖动到新节点来更新边。 此属性将覆盖组件上 prop 设置的默认值。edgesReconnectable<ReactFlow />
        'focusable': True, # 是否可聚焦
        # 'ariaRole': 'group',    # 【未知】  类型：AriaRole     边缘的 ARIA 角色属性，用于辅助功能。
        # 'domAttributes': # 用于向节点的 DOM 元素添加自定义属性的通用逃生舱口。    【未知】
    },

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

    # 占位符事件处理器-可接受(0~5)个参数——为事件处理器提供一个虚假的接入点
    @rx.event
    def fake_event_handel(self , a=None, b=None, c=None, d=None, e=None):
        print('触发了占位符事件处理器.******************************')
        if a:
            print(f"包含参数:类型={type(a)}, 值={a}")
        if b:
            print(f"包含两个参数:类型={type(b)}, 值={b}")
        if c:
            print(f"包含三个参数:类型={type(c)}, 值={c}")
        if d:
            print(f"包含四个参数:类型={type(d)}, 值={d}")
        if e:
            print(f"包含参五个数:类型={type(e)}, 值={e}")


# region 下面是一级组件
# 背景——完全版
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
# 连接线基础——完全版
def component_base_edge() -> rx.Component:
    return base_edge(
        path=None,  # 'M 0 0 L 100 100'
        markerStart=None,
        markerEnd=None,
        #label=None,
        labelStyle={},
        labelShowBg=None,
        labelBgStyle={},
        labelBgPadding=None,
        labelBgBorderRadius=None,
        interactionWidth=20,
        labelX=None,
        labelY=None
    )
# 控制按钮——完全版
def component_control_button() -> rx.Component:
    '只能用在controls()里作为子组件'
    return control_button()
# 控制——完全版
def component_controls() -> rx.Component:
    return controls(
        control_button(),   # 【以后再说】这里应该是要放什么组件的，用来修改控制区域的按钮样式
        panel(position='top-left'),

        showZoom=True,
        showFitView=True,
        showInteractive=True,
        # fitViewOptions=None   【以后再说】
        onZoomIn=State.fake_event_handel,   # 放大时调用
        onZoomOut=State.fake_event_handel,  # 缩小时调用
        onFitView=State.fake_event_handel,  # 修复视角时调用
        onInteractiveChange=State.fake_event_handel,    # 锁定按钮调用
        position='bottom-left',
        children=None,
        style={},  # 应用于容器的样式
        className=None,  # 应用于容器的类名
        aria_label='React Flow controls',
        orientation='vertical'
    )
# 连接线标签特别样式——完全版
def component_edge_label_renderer() -> rx.Component:
    return edge_label_renderer()
# 连接线文本——完全版
def component_edge_text() -> rx.Component:
    return edge_text(
        x=-10,
        y=-10,
        #label='abc',
        labelStyle={'fill': 'white'},
        labelShowBg=True,
        labelBgStyle={'fill': 'red'},
        labelBgPadding=[2, 4],
        labelBgBorderRadius=2
    )
# 连接点——完全版
def component_handle() -> rx.Component:
    return handle(
        id='undefine_handle',
        type='source',
        position='left',  # 可选参数：'left', 'top', 'right', 'bottom'
        isConnectable=True,
        isConnectableStart=True,
        isConnectableEnd=True,
        onConnect=State.fake_event_handel
    )
# 地图——完全版
def component_mini_map() -> rx.Component:
    return mini_map(
        panel(position='top-left'),

        position='bottom-right',  # 小地图在窗格上的位置。
        onClick=State.fake_event_handel,
        nodeColor="#e2e2e2",  # 小地图上节点的颜色。
        nodeStrokeColorL="transparent",  # 小地图上节点的笔划颜色。
        nodeClassName='undefine_mini_map_class_name',  # 应用于小地图节点的类名。      默认值是空字符串
        nodeBorderRadius=5,  # 小地图上节点的边界半径。
        nodeStrokeWidth=2,  # 小地图上节点的笔划宽度。
        # nodeComponent='abc',    这个还有很大问题https://reactflow.dev/api-reference/components/minimap#nodecomponent
        bgColor='gray',  # 小地图的背景颜色
        maskColor="rgba(240, 240, 240, 0.6)",  # 覆盖小地图中当前不可见的部分的遮罩的颜色 视窗。
        maskStrokeColor='transparent',  # 表示视口的蒙版的描边颜色
        maskStrokeWidth=1,  # 表示视口的蒙版的描边宽度。
        onNodeClick=State.fake_event_handel,  # 点击小地图上的节点时调用回调。
        pannable=False,  # 确定是否可以通过在小地图内拖动来平移视口
        zoomable=False,  # 确定是否可以通过在小地图内滚动来缩放视口。
        ariaLabel="Mini Map",  # 小地图中没有文本供屏幕阅读器用作可访问的名称，因此它是 重要提示 我们提供了一个使小地图易于访问。默认值就足够了，但你可以 想要将其替换为与您的应用或产品更相关的内容。
        inversePan=False,  # 平移小地图视口时反转方向。
        zoomStep=10,  # 在小地图上放大/缩小的步长。
        offsetScale=5,  # 在小地图上偏移视口，就像填充一样。         只是number可以是int或者float
    )
# 节点—自定义调整大小控件—完全版
def component_node_resize_control() -> rx.Component:
    return node_resize_control(
        nodeID='undefine_node_resize_control_class_name',  # 它正在调整大小的节点的 ID。
        color=None,  # 调整大小手柄的颜色。
        minWidth=10,  # 节点的最小宽度。
        minHeight=10,  # 节点的最小高度。
        maxWidth=10,
        # 节点的最大宽度。    【未知】默认值: Number.MAX_VALUE https://reactflow.dev/api-reference/components/node-resize-control#maxwidth
        maxHeigh=10,
        # 节点的最大高度。    【未知】默认值: Number.MAX_VALUE https://reactflow.dev/api-reference/components/node-resize-control#maxwidth
        keepAspectRatio=False,  # 调整大小时保持纵横比
        shouldResize=State.fake_event_handel,  # 回调，用于确定是否应调整节点大小。
        autoScale=True,  # 使用缩放级别缩放控件。
        # onResizeStart:   # 调整大小开始时调用回调。  数据类型: OnResizeStart
        # onResize:    # 调整大小时调用的回调。  数据类型: OnResize
        # onResizeEnd: # 调整大小结束时调用回调。  数据类型: OnResizeEnd
        # position:    # 控件的位置。  数据类型: ControlPosition
        variant='handle',  # 控件的变体。  数据类型: ResizeControlVariant
        # resizeDirection:    # 用户可以调整节点大小的方向。 如果未提供，用户可以向任何方向调整大小。   数据类型:  ResizeControlDirection
        className='',
        style={},
        # children:    # 数据类型: ReactNode
    )
# 节点-调节大小——完全版   # 这个还有很大问题，不知道如何使用，必须要修改，只是参数差不多了
def component_node_resizer() -> rx.Component:
    return node_resizer(
        nodeId='4',  # 它正在调整大小的节点的 ID。
        color='blue',  # 调整大小手柄的颜色。
        handleClassName='undefine_node_resizer_handle_class_name',  # 应用于句柄的类名。
        handleStyle={},  # 应用于手柄的样式。
        lineClassName='undefine_node_resizer_line_class_name',  # 应用于线的类名。
        lineStyle={},  # 应用于线的样式。
        isVisible=True,  # 控件是否可见。
        minWidth=10,  # 节点的最小宽度。
        minHeight=10,  # 节点的最小高度。
        maxWidth=10,  # 节点的最大宽度。  【未知】默认值: Number.MAX_VALUE
        maxHeight=10,  # 节点的最大高度。  【未知】默认值: Number.MAX_VALUE
        keepAspectRatio=False,  # 调整大小时保持纵横比。
        autoScale=True,  # 使用缩放级别缩放控件。
        shouldResize=State.fake_event_handel,  # 回调，用于确定是否应调整节点大小。
        onResizeStart=State.fake_event_handel,  # 调整大小开始时调用回调。
        onResize=State.fake_event_handel,  # 调整大小时调用的回调。
        onResizeEnd=State.fake_event_handel,  # 调整大小结束时调用回调。
    )
# 节点—工具栏—完全版
def component_node_toolbar() -> rx.Component:
    return node_toolbar(
        nodeId=['3', '4'],  # 通过传入节点 ID 数组，您可以为组或集合渲染单个工具提示 节点数。
        isVisible=True,  # 如果 True，即使未选择节点，节点工具栏也可见。
        position='top',  # 工具栏相对于节点的位置。
        offset=10,  # 节点和工具栏之间的空间，以像素为单位。
        align='center',  # 相对于节点对齐工具栏      数据类型: Align
    )
# 面板——完全版——将内容放置在视口上方
def component_panel() -> rx.Component:
    return panel(position='top-left')
# 视图——完全版
def component_viewport_portal() -> rx.Component:
    return viewport_portal(
        # children
    )


# react_flow主要部分——完全版
def component_flow() -> rx.Component:
    return flow(

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
        on_error=State.fake_event_handel,   # 【未测试成功, 不确定返回值】
        on_init=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_delete=State.fake_event_handel,  # 【未测试成功, 不确定返回值】
        on_before_delete=State.fake_event_handel,   # 【未测试成功, 不确定返回值】
        # endregion

        # region 事件处理程序——节点(Node)事件
        on_node_click=State.fake_event_handel,
        on_node_double_click=State.fake_event_handel,
        on_node_drag_start=lambda e0, e1, e2: State.fake_event_handel(e0, e1, e2),
        on_node_drag=lambda e0, e1, e2: State.fake_event_handel(e0, e1, e2),
        on_node_drag_stop=lambda e0, e1, e2: State.fake_event_handel(e0, e1, e2),
        on_node_mouse_enter=State.fake_event_handel,
        on_node_mouse_move=State.fake_event_handel,
        on_node_mouse_leave=State.fake_event_handel,
        on_node_context_menu=State.fake_event_handel,
        on_nodes_delete=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_nodes_change=lambda e0, e1: State.on_nodes_change(e0, e1),
        # endregion

        # region 事件处理程序——边缘(Edge)事件
        on_edge_click=State.fake_event_handel,
        on_edge_double_click=State.fake_event_handel,
        on_edge_mouse_enter=State.fake_event_handel,
        on_edge_mouse_move=State.fake_event_handel,
        on_edge_mouse_leave=State.fake_event_handel,
        on_edge_context_menu=State.fake_event_handel,
        on_reconnect=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_reconnect_start=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_reconnect_end=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_edges_delete=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_edges_change=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        # endregion

        # region 事件处理程序——连接(Connect)事件
        on_connect=lambda e0: State.on_connect(e0),
        on_connect_start=lambda e0, e1: State.fake_event_handel(e0, e1),
        on_connect_end=lambda e0, e1: State.fake_event_handel(e0, e1),
        on_click_connect_start=State.fake_event_handel,    # 【未测试成功, 不确定返回值】
        on_click_connect_end=State.fake_event_handel,      # 【未测试成功, 不确定返回值】
        is_valid_connection=lambda e0: State.fake_event_handel(e0),
        # endregion

        # region 事件处理程序——窗格(Pane)事件 OK
        on_move=lambda e0, e1: State.fake_event_handel(e0, e1),
        on_move_strat=lambda e0, e1: State.fake_event_handel(e0, e1),
        on_move_end=lambda e0, e1: State.fake_event_handel(e0, e1),
        on_pane_click=State.fake_event_handel,
        on_pane_context_menu=State.fake_event_handel,
        on_pane_scroll=State.fake_event_handel,
        on_pane_mouse_move=State.fake_event_handel,
        on_pane_mouse_enter=State.fake_event_handel,
        on_pane_mouse_leave=State.fake_event_handel,

        # 【不知道怎么触发】on_pane_context_menu=lambda *args, **kwargs: State.fake_event_handel(*args, **kwargs),
        # 【不知道怎么触发】on_pane_scroll=lambda *args, **kwargs: State.fake_event_handel(*args, **kwargs),
        # 【不知道怎么触发】on_pane_mouse_move=lambda *args, **kwargs: State.fake_event_handel(*args, **kwargs),
        # 【不知道怎么触发】on_pane_mouse_enter=lambda *args, **kwargs: State.fake_event_handel(*args, **kwargs),
        # 【不知道怎么触发】on_pane_mouse_leave=lambda *args, **kwargs: State.fake_event_handel(*args, **kwargs),
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

# react_flow主要部分——使用示例
def component_flow_demo() -> rx.Component:
    '''
    - 组件在这个主要部分里面使用
    '''
    return flow(
        # 调用组件部分
        background(),
        # 【以后再说】base_edge(),    外观非功能，看不太懂，一直没效果
        controls(),
        #edge_label_renderer(),  # 【以后再说】【未测试】【看不到变化】
        # edge_text(),    # 【以后再说】
        #handle(),
        mini_map(),
        #node_resize_control(),
        #node_resizer(), # 这个还有很大问题，不知道如何使用，必须要修改，只是参数差不多了
        #node_toolbar(),  # 这个还有很大问题，不知道如何使用，必须要修改，只是参数差不多了
        #panel组件由组件 controls 或 mini_map内部使用     panel可帮助您将内容放置在视口上方
        #viewport_portal(),    # 这个还有很大问题，不知道如何使用，必须要修改



        # 本身参数部分
        nodes_draggable=True,
        nodes_connectable=True,
        on_connect=lambda e0: State.on_connect(e0),
        on_nodes_change=lambda e0: State.on_nodes_change(e0),
        nodes=State.nodes,
        edges=State.edges,
        fit_view=True,

    )


# endregion







# 下面是页面组件
def index() -> rx.Component:
    return rx.vstack(
        component_flow_demo(),


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
