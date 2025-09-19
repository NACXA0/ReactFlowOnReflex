"""反射自定义组件ReactFlow."""
'''
- 为参数添加默认值的方法：
    LiteralVar.create(False)
    示例：
        closeButton boolean false
    转换为：
        close_button: Var[bool] = LiteralVar.create(False)
- 【未测试】没有参数的事件处理器要加的规范：
    on_autosize: EventHandler[no_args_event_spec]
    或者 on_autosize: rx.EventHandler[no_args_event_spec]
- 【未测试】有参数的事件处理器统一管理方法
    def _event_points_data_signature(e0: Var) -> tuple[Var[list[Point]]]:
        """For plotly events with event data containing a point array.
    
        Args:
            e0: The event data.
    
        Returns:
            The event data and the extracted points.
        """
        return (Var(_js_expr=f"extractPoints({e0}?.points)"),)
    
    on_selected: EventHandler[_event_points_data_signature]
    
- 

- JS参数后面有 问号 ？ 的
    不用写 Option[]
    示例：
        closeButton?: boolean;
    转换为：
        close_button: Var[bool] = LiteralVar.create(False)
- 组件道具 props的类型是 rx.Var[rx.Component]
    https://reflex.dev/docs/wrapping-react/props/
    有些组件偶尔会接受其他组件作为 props，通常被注释为 ReactNode。在 Reflex 中，这些被定义为 rx。组件 。
    
    class ComponentPropsComponent(MyBaseComponent):
        """MyComponent."""
    
        # A prop that takes a component as an argument.
        component_props: rx.Var[rx.Component]
'''
# 用于包装react指南, 查看 https://reflex.dev/docs/wrapping-react/overview/

import reflex as rx
from typing import Any, Dict, List, Union, Literal, TypedDict, Tuple, Callable, Iterable, TypeVar, Generic, Optional
from reflex.components.component import NoSSRComponent
from reflex.components import Component
from reflex.vars import Var, LiteralVar, VarData
from reflex.constants import Hooks
from reflex.components.el.elements import Div
from reflex.utils.imports import ImportVar
from reflex.event import EventHandler, no_args_event_spec
from .types import (
    BackgroundVariant,
    ConnectionLineType, ConnectionLineComponentProps, ConnectionMode, CSSType,
    DefaultEdgeOptions,
    Edges, EdgeMouseHandler,
    IsValidConnection,
    KeyCode,
    Nodes, NodeMouseHandler,
    OnBeforeDelete, OnConnect, OnConnectStart, OnConnectEnd, OnDelete, OnEdgesChange, OnEdgesDelete,OnError, OnInit, OnMove, OnNodeDrag, OnNodesChange, OnNodesDelete, OnReconnect, OnSelectionChangeFunc, OnResizeHandler,
    PanelPosition, PanOnScrollMode, ProOptions,
    ReactNode,
    SelectionDragHandler, SelectionMode,
    Viewport
)

# 要包装的某些库可能需要动态导入。
# 这是因为它们可能与服务器端渲染（SSR）不兼容。
# 要在Reflex中处理这一点，您需要做的只是子类`NoSSRComponent`。
# 例如：
# from reflex.components.component import NoSSRComponent
# class Flow(NoSSRComponent):
#     pass

# 基本库

Position = Literal['top', 'right', 'bottom', 'left']



class FlowLib(NoSSRComponent):
    """Flow component."""

    # The React library to wrap.
    library = "@xyflow/react"

    def _get_custom_code(self) -> str:
        return """import '@xyflow/react/dist/style.css';
        """

    # ticket如果标签是模块的默认导出, 你必须设置 is_default = True.
    # 当导入时组件周围没有花括号时，通常使用此选项。
    # is_default = True

    # 如果要包装与项目中的构件具有相同标记的其他构件
    # 可以使用别名来区分它们，并避免命名冲突。
    #alias = "react-flow"   # 这个不能启用，一启用就报错

    # React组件的道具。
    # 注意：当Reflex将组件编译为Javascript时，
    # `snake_case`属性名称自动格式化为`camelCase`。
    # 道具名称也可以在“camelCase”中定义。
    # some_prop: rx.Var[str] = "some default value"
    # some_other_prop: rx.Var[int] = 1

    # 默认情况下，Reflex将安装在库属性中指定的库。
    # 然而，有时您可能需要安装其他库才能使用组件。
    # 在这种情况下，可以使用lib_dependencies属性指定要安装的其他库。
    # lib_dependencies: list[str] = []

    # 事件触发声明（如果有）。
    # 下面相当于合并 `{ "on_change": lambda e: [e] }`
    # 父/基组件的默认事件触发器。
    # 为javascript的`on_change`触发器映射事件定义的函数
    # 触发将传递给后端事件处理程序函数的内容。
    # on_change: rx.EventHandler[lambda e: [e]]

    # 将自定义代码添加到组件
    # def _get_custom_code(self) -> str:
    #     return "const customCode = 'customCode';"


# 基本(common)组件
class Flow(FlowLib):
    '''
    - 虽然有不同的类型，不同的功能，但是要放到一起，为了效率，为了结构扁平化，都是可调用的方法。也有一些迁移出去成为了组件。
    - 目录: 按照类型分类:   顺序: 依照官方文档顺序
        道具(Props) = React组件的输入参数
        事件(Events) = 用户交互的响应入口
        活动(Actions) = 组件实例的可调用方法
    '''

    # region 下面是TypedDict 定义，规定数据形式.

    class ProOptions(TypedDict):
        account: str
        hideAttribution: bool


    # 【以后再做】
    class ConnectionLineComponentProps(TypedDict):  # https://github.com/xyflow/xyflow/blob/main/packages/react/src/types/edges.ts#L2651

        connection_line_style: dict = {}  # 对应CSSProperties
        connection_line_type: str  # ConnectionLineType
        from_node: Any   # InternalNode<NodeType>
        from_handle: dict  # Handle类型
        from_x: float
        from_y: float
        to_x: float
        to_y: float
        from_position: str # Position枚举
        to_position: str
        connection_status: Literal['valid', 'invalid'] | None = None  # 'valid' | 'invalid' | None
        to_node: Any | None = None  # 注意Optional处理
        to_handle: Optional[dict] | None = None


    # endregion


    # 组件标签.
    tag = "ReactFlow"

    # region 常见道具
    width: rx.Var[float]  # 为Flow设置固定宽度。
    height: rx.Var[float] # 设置Flow的固定高度。
    nodes: rx.Var[Nodes | List[Dict[str, Any]]] = LiteralVar.create([]) # 原版是这样，但我觉得包括起来更好 【未测试】Nodes | rx.Var[List[Dict[str, Any]]] | None = None
    edges: rx.Var[Edges | List[Dict[str, Any]]] = LiteralVar.create([])
    default_nodes: rx.Var[Nodes | List[Dict[str, Any]]]    # 要在不受控制的流中渲染的初始节点。
    default_edges: rx.Var[Edges | List[Dict[str, Any]]]    # 要在不受控制的流中渲染的初始边。
    pane_click_distance: rx.Var[int] = LiteralVar.create(0)  # 鼠标可以在鼠标向下/向上之间移动的距离，这将触发单击
    node_click_distance: rx.Var[int] = LiteralVar.create(0)  # 鼠标可以在鼠标向下/向上之间移动的距离，这将触发单击。
    node_types: rx.Var[str] # 【以后再说】没定义好 要能传入组件node_resize_control #rx.Var[Literal['input', 'default', 'output', 'group']] = LiteralVar.create('default')   # 要在流中提供的自定义节点类型。 React Flow 将节点的类型与对象中的组件进行匹配
    edge_types: rx.Var[Literal['default', 'straight', 'step', 'smoothstep', 'simplebezier']] = LiteralVar.create('default') # 流中可用的自定义边缘类型。 React Flow 将边缘的类型与对象中的组件进行匹配。edgeTypes
    auto_pan_on_node_focus: rx.Var[bool] = LiteralVar.create(True)    # 当节点聚焦时，视口将平移
    node_origin: rx.Var[List[int]] = LiteralVar.create([0, 0])  # 在将节点放置在流中或查找其位置时要使用的节点的原点。原点表示节点的左上角将放置在 和 位置。xy[0, 0]xy
    pro_options: rx.Var[ProOptions]  # 默认情况下，我们会在流的角落呈现一个小归因，该归因链接回项目。   任何人都可以自由删除此归属，无论他们是否是 Pro 订阅者 但我们要求您快速浏览我们的 https://reactflow.dev/learn/troubleshooting/remove-attribution  移除归因指南 在这样做之前。
    node_drag_threshold: rx.Var[int] = LiteralVar.create(1)  # 如果阈值大于零，则可以延迟节点拖动事件。 如果阈值等于 1，则需要在触发拖动事件之前将节点拖动 1 像素。 1 是默认值，因此点击不会触发拖动事件。
    connection_drag_threshold: rx.Var[int] = LiteralVar.create(1)    # 在连接线开始拖动之前，鼠标必须移动的阈值（以像素为单位）。 这对于防止单击手柄时意外连接非常有用。
    color_mode: rx.Var[Literal['light', 'dark', 'system']] = LiteralVar.create('light')   # 控制用于设置流样式的配色方案。
    debug: rx.Var[bool] = LiteralVar.create(False) # 一些调试信息将记录到控制台，例如触发了哪些事件。
    aria_label_config: rx.Var[Any] # Optional[rx.Var[Any]]    # 【以后再做】 # 可自定义标签、描述和 UI 文本的配置。提供的键将覆盖相应的默认值。 允许本地化、自定义 ARIA 描述、控件标签、小地图标签和其他 UI 字符串。
    # 这里有很大问题，说是不用显式声明，对应的是common_props: rx.Var[Dict[str, Union[str, int, float, bool, Var, None]]]   # rx.Var[HTMLDivPropsOmitOnError]  # 支持所有 HTML 属性（除 onError）    https://reactflow.dev/api-reference/react-flow#props
    # endregion

    # region 视觉(viewport)道具
    default_viewport: rx.Var[Viewport] = LiteralVar.create({ 'x': 0, 'y': 0, 'zoom': 1 }) # 设置视口的初始位置和缩放。如果提供了默认视口但已启用，则默认视口将被忽略
    viewport: rx.Var[Viewport]  # 当你传递一个 prop 时，它是受控的，你也需要传递来处理内部更改。viewporton ViewportChange
    on_viewport_change: rx.Var[Any]   # 【以后再做】    # 使用受控视口更新用户视口状态时使用。
    fit_view: rx.Var[bool] = LiteralVar.create(True)  # 修正初始视角    流将被缩放和平移以适合最初提供的所有节点
    fitView_options: rx.Var[Any]   # 【以后再做】  # 当您通常调用 时，可以提供 选项来自定义其行为。这个 prop 允许你对初始调用执行相同的作。fitView ReactFlowInstance fitView
    min_zoom: rx.Var[float] = LiteralVar.create(0.5)  # 最小缩放级别。
    max_zoom: rx.Var[float] = LiteralVar.create(2.0)    # 最大变焦级别。
    snap_to_grid: rx.Var[bool]    # 启用后，节点将在拖动时捕捉到网格。
    snap_grid: rx.Var[List[float]]   # 如果启用，则此属性将配置节点将捕捉到的网格。snapToGrid
    only_render_visible_elements: rx.Var[bool] = LiteralVar.create(False)   # 你可以启用此优化来指示 React Flow 仅渲染视口中可见的节点和边缘。  当您拥有大量节点和 Edge 时，这可能会提高性能，但也会增加开销。
    translate_extent: rx.Var[List[List[float]]]    # 默认情况下，视口无限延伸。您可以使用此 prop 来设置边界。 第一对坐标是左上角的边界，第二对坐标是右下角的边界。
    node_extent: rx.Var[List[List[float]]]  # 默认情况下，节点可以放置在无限流上。您可以使用此 prop 来设置边界。 第一对坐标是左上角的边界，第二对坐标是右下角的边界。
    prevent_scrolling:rx.Var[bool] = LiteralVar.create(True)   # 禁用此属性将允许用户滚动页面，即使他们的指针位于流上。
    attribution_position: rx.Var[Literal['top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right']] = LiteralVar.create('bottom-right')     # 默认情况下，React Flow 会在流程的右下角渲染一个小的归因。    您可以使用此道具来更改其位置，以防您想在那里放置其他东西。
    # ..props
    # endregion

    # region 边缘(edge)道具
    elevate_edges_on_select: rx.Var[bool] = LiteralVar.create(False)   # 启用此选项将在选择边时提高边的 z 索引。
    default_marker_color: rx.Var[str | None] = LiteralVar.create('#b1b1b7')   # 边缘标记的颜色。 您可以传递以使用 CSS 变量作为标记颜色。null--xy-edge-stroke   如：'#b1b1b7'
    default_edge_options: Optional[DefaultEdgeOptions]  #!不能加rx.Var[] # 新边上的属性将覆盖这些默认值（如果存在）。
    reconnect_radius: rx.Var[float] = LiteralVar.create(10)    # 可以触发边重新连接的边连接周围的半径。
    edges_reconnectable: rx.Var[bool] = LiteralVar.create(True) # 创建边后是否可以更新。当此 prop 同时提供处理程序时，用户可以将现有边缘拖到新源或 目标。单个边可以使用其可重新连接属性覆盖此值。true  onReconnect
    # endregion


    # region 事件处理程序——一般(general)事件
    on_error: Optional[OnError]   #rx.EventHandler
    on_init: rx.EventHandler[no_args_event_spec]  # 【以后再做】【未测试成功, 不确定返回值】
    on_delete: OnDelete   # rx.EventHandler  # 删除节点或边缘时调用此事件处理程序。
    on_before_delete: OnBeforeDelete  # 【以后再做】【未测试成功, 不确定返回值】
    # endregion

    # region 事件处理程序——节点(Node)事件 OK
    on_node_click: NodeMouseHandler    # rx.EventHandler # 当用户单击节点时，将调用此事件处理程序。
    on_node_double_click: NodeMouseHandler   # 当用户双击节点时，将调用此事件处理程序。
    on_node_drag_start: OnNodeDrag  #rx.EventHandler[lambda e0, e1, e2: [e0, e1, e2]] # 当用户开始拖动节点时，将调用此事件处理程序。   包含三个返回值(dict, dict,list):  值=[{'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 52.5, 'y': 138.5}, 'dragging': True}]   值={'isTrusted': True}   值={'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}, 'dragging': True}  值=[{'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}, 'dragging': True}]
    on_node_drag: OnNodeDrag    #rx.EventHandler[lambda e0, e1, e2: [e0, e1, e2]]      # 当用户拖动节点时，将调用此事件处理程序。      包含三个返回值(dict, dict,list):  值={'isTrusted': True}   值={'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 59.5, 'y': 147}, 'dragging': True}    值=[{'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 59.5, 'y': 147}, 'dragging': True}]
    on_node_drag_stop: OnNodeDrag   #rx.EventHandler[lambda e0, e1, e2: [e0, e1, e2]]      # 当用户停止拖动节点时，将调用此事件处理程序。   包含三个返回值(dict, dict,list):  值={'isTrusted': True}   值={'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 59.5, 'y': 147}, 'dragging': True}    值=[{'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 59.5, 'y': 147}, 'dragging': True}]
    on_node_mouse_enter: NodeMouseHandler    # 当用户的鼠标进入节点时，将调用此事件处理程序。  无返回值
    on_node_mouse_move: NodeMouseHandler    # 当用户的鼠标移动到节点上时，将调用此事件处理程序。    无返回值  注意：当鼠标在节点上时，移动鼠标会产生一连串的触发效果
    on_node_mouse_leave: NodeMouseHandler    # 当用户的鼠标离开节点时，将调用此事件处理程序。  无返回值
    on_node_context_menu: NodeMouseHandler   # 当用户右键单击节点时，将调用此事件处理程序。  无返回值
    # on_nodes_delete: rx.EventHandler    # OnNodesDelete     # 【未测试成功, 不确定返回值】删除节点时调用此事件处理程序。
    on_nodes_change: OnNodesChange # 使用此事件处理程序向受控流添加交互性。它在节点拖动、选择和移动时调用。  包含返回值list: [{'id': '1', 'type': 'dimensions','dimensions': {'width': 150,'height': 40}},{'id': '2', 'type': 'dimensions','dimensions': {'width':150, 'height': 40}}, {'id': '3', 'type': 'dimensions','dimensions': {'width': 150,'height': 40}}, {'id': '4', 'type': 'dimensions','dimensions': {'width': 150,'height': 40}}]
    # endregion

    # region 事件处理程序——边缘(Edge)事件 OK
    on_edge_click: EdgeMouseHandler # 当用户单击边缘时，将调用此事件处理程序。  无返回值
    on_edge_double_click: EdgeMouseHandler   # 当用户双击边缘时，将调用此事件处理程序。  无返回值
    on_edge_mouse_enter: EdgeMouseHandler    # 当用户的鼠标进入边缘时，将调用此事件处理程序。  无返回值
    on_edge_mouse_move: EdgeMouseHandler # 当用户的鼠标移动到边缘上时，将调用此事件处理程序。  无返回值
    on_edge_mouse_leave: EdgeMouseHandler    # 当用户的鼠标离开边缘时，将调用此事件处理程序  无返回值
    on_edge_context_menu: EdgeMouseHandler   # 当用户右键单击边缘时，将调用此事件处理程序。  无返回值
    on_reconnect: OnReconnect   # 接收两个参数 # 触发：鼠标多动已连接的边断开，然后重新连回去 # 当可重新连接边的源或目标从当前节点拖动时，将调用此处理程序。即使边的源或目标最终没有更改，它也会触发。您可以使用该实用程序将连接转换为新边。reconnectEdge # 包含参数:类型=<class 'dict'>, 值={'id': 'e4-6', 'source': '4', 'target': '6', 'label': '-', 'animated': True}    包含两个参数:类型=<class 'dict'>, 值={'source': '4', 'sourceHandle': None, 'target': '7', 'targetHandle': None}
    on_reconnect_start: rx.EventHandler[no_args_event_spec]    # 【未测试成功, 不确定返回值】当用户开始拖动可编辑边的源或目标时，将触发此事件。
    on_reconnect_end: rx.EventHandler[no_args_event_spec]  # 【未测试成功, 不确定返回值】当用户释放可编辑边缘的源或目标时，将触发此事件。它被称为即使未发生边缘更新。
    # on_edges_delete: rx.EventHandler # OnEdgesDelete  # 【未测试成功, 不确定返回值】删除边缘时调用此事件处理程序。
    on_edges_change: OnEdgesChange   # 接收一个参数    # 使用此事件处理程序可向受控流添加交互性。它在边缘选择时称为?并删除。    # 值=[{'id': 'e3-4', 'type': 'select', 'selected': False}]
    # endregion

    # region 事件处理程序——连接(Connect)事件 OK
    on_connect: OnConnect   # 接收一个参数rx.EventHandler[lambda e0: [e0]]   # rx.EventHandler[lambda e0: [e0]]
    on_connect_start: OnConnectStart    # 接收两个参数  # 当用户开始拖动连接线时，将调用此事件处理程序。  注意: 在点击手柄拖动引出线的时候触发   包含两个参数(dict, dict): 值={'isTrusted': True}   值={'nodeId': '4', 'handleId': None, 'handleType': 'source'}
    on_connect_end: OnConnectEnd    # 接收两个参数    # 无论是否可以建立有效连接，此回调都会触发。您可以 使用第二个参数在连接时具有不同的行为 不成功。connectionState  注意: 引出连接线后，不论有没有连接上，只要松开线消失都会触发。  包含两个参数(dict, dict): 值={'isTrusted': True}  (很长)值={'isValid': False, 'from': {'x': 124.99982508047702, 'y': 163.9999125402385}, 'fromHandle': {'id': None, 'type': 'source'': '2', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}, 'fromPosition': 'bottom', 'fromNode': {'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 50, 'y': 125}, 'measured': {'width': 150, 'height': 40}, 'internals': {'positionAbsolute':          {'x': 50, 'y': 125}, 'handleBounds': {'source': [{'id': None, 'type': 'source', 'nodeId': '2', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}], 'target': [{'id': None, 'type': 'target', 'nodeId': '2', 'position': 'top', 'x': 71.99982508047702, 'y': -1.999994525565665, 'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 50, 'y': 125}}}}, 'to': {'x': 416, 'y': 220}, 'toHandle': {'id': None, 'type': 'source', 'nodeId': '4', 'position': 'bottom', 'x': 424.999825080477, 'y': 188.9999125402385, 'width': 6, 'height': 6}, 'toPosition': 'top', 'toNode': {'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}, 'measured': {'width': 150, 'height': 40}, 'internals': {'positionAbsolute': {'x': 350, 'y': 150}, 'handleBounds': {'source': [{'id': None, 'type': 'source', 'nodeId': '4', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}], 'target': [{'id': None, 'type': 'target', 'nodeId': '4', 'position': 'top', 'x': 71.99982508047702, 'y': -1.999994525565665, 'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}}}}}
    on_click_connect_start: OnConnectStart   # 接收两个参数   # 当用户点击拖动连接线时，将调用此事件处理程序。
    on_click_connect_end: OnConnectEnd    # 接收两个参数  # 当用户松开拖动连接线时，将调用此事件处理程序。
    is_valid_connection: IsValidConnection  # 此回调可用于验证新连接   注意: 1.加了这个参数会导致链接不上不知道为什么 2. 拖动连接线靠近另一个连接点时会触发很多次   包含返回值dict: {'source': '4', 'sourceHandle': None, 'target': '5', 'targetHandle': None}    如果返回，则不会将边缘添加到流中。 如果您有自定义连接逻辑，出于性能原因，最好使用此回调而不是句柄组件上的 prop。falseisValidConnection
    # endregion

    # region 事件处理程序——窗格(Pane)事件 OK
    on_move: OnMove # 接收两个参数的事件处理器  # 当用户平移或缩放视口时，将调用此事件处理程序。  包含两个返回值(dict, dict): 值={'isTrusted': True}  值={'x': 106.35714285714286, 'y': 13.999999999999943, 'zoom': 0.9085714285714286}
    on_move_start: OnMove # 接收两个参数的事件处理器 # 当用户开始平移或缩放视口时，将调用此事件处理程序。     包含两个返回值(dict, dict): 值={'isTrusted': True}  值=值={'x': 124.35714285714286, 'y': 16.99999999999997, 'zoom': 0.9085714285714286}
    on_move_end: OnMove # 接收两个参数的事件处理器   # 当平移或缩放视口移动停止时调用此事件处理程序。 如果移动不是用户发起的，则事件参数将为 。null     包含两个返回值(dict, dict): 值={'isTrusted': True}  值=值={'x': 124.35714285714286, 'y': 16.99999999999997, 'zoom': 0.9085714285714286}
    on_pane_click: rx.EventHandler[no_args_event_spec] # 当用户在窗格内单击时，将调用此事件处理程序。     无返回值
    on_pane_context_menu: rx.EventHandler[no_args_event_spec] # 当用户在窗格内右键单击时，将调用此事件处理程序。  无返回值
    on_pane_scroll: rx.EventHandler[no_args_event_spec]      # 当鼠标在窗格内滚动时，将调用此事件处理程序。  无返回值   调试注意: 只有在滚轮放大到最大后再滚轮放大，或者滚轮缩小到最小后再缩小才会触发，每滚轮一格触发一次    调试注意: 需要先聚焦窗口，准备好才会触发
    on_pane_mouse_move: rx.EventHandler[no_args_event_spec]  # 当鼠标移动到窗格时，将调用此事件处理程序。  无返回值    调试注意: 需要先聚焦窗口，准备好才会触发
    on_pane_mouse_enter: rx.EventHandler[no_args_event_spec] # 当鼠标进入到窗格时，将调用此事件处理程序。  无返回值    调试注意: 需要先聚焦窗口，准备好才会触发
    on_pane_mouse_leave: rx.EventHandler[no_args_event_spec] # 当鼠标离开到窗格时，将调用此事件处理程序。  无返回值    调试注意: 需要先聚焦窗口，准备好才会触发
    # endregion

    # region 事件处理程序——选择(select)事件
    on_selection_change: OnSelectionChangeFunc  # 接收一个参数的事件处理器   # 当用户更改流中的选定元素组时，将调用此事件处理程序。   # 示例返回值：类型=<class 'dict'>, 值={'nodes': [], 'edges': [{'id': 'e3-4', 'type': 'default', 'source': '3', 'target': '4', 'animated': True, 'hidden': False, 'deletable': True, 'selectable': True, 'data': {'label': '连接线标签', 'startLabel': '连接线起始标签', 'endLabel': '连接线结束标签'}, 'selected': True, 'markerStart': {'type': 'arrow', 'color': 'green', 'width': 10, 'height': 10, 'markerUnits': '', 'orient': '', 'strokeWidth': 10}, 'markerEnd': {'type': 'arrow', 'color': 'green', 'width': 10, 'height': 10, 'markerUnits': '', 'orient': '', 'strokeWidth': 10}, 'zIndex': 1, 'ariaLabel': '', 'interactionWidth': 10, 'label': '连接线完全体', 'labelStyle': {}, 'labelShowBg': True, 'labelBgStyle': {}, 'labelBgPadding': [10, 20], 'labelBgBorderRadius': 10, 'style': {}, 'className': 'undefine', 'reconnectable': True, 'focusable': True, 'ariaRole': 'group', 'domAttributes': {}}]}
    on_selection_drag_start: SelectionDragHandler   # 【以后再说】【未测试成功, 不确定返回值】    # 【未测试成功, 不确定返回值】当用户开始拖动选择框时，将调用此事件处理程序。
    on_selection_drag: SelectionDragHandler   # 【以后再说】【未测试成功, 不确定返回值】 # 【未测试成功, 不确定返回值】当用户拖动选择框时，将调用此事件处理程序。
    on_selection_drag_stop: SelectionDragHandler    # 【以后再说】【未测试成功, 不确定返回值】当用户停止拖动选择框时，将调用此事件处理程序。
    on_selection_start: rx.EventHandler[lambda e0: [e0]]    # 【以后再说】【未测试成功, 不确定返回值】当用户选择开始时，将调用此事件处理程序。
    on_selection_end: rx.EventHandler[lambda e0: [e0]]  # 【以后再说】【未测试成功, 不确定返回值】当用户选择结束时，将调用此事件处理程序。
    on_selection_context_menu: rx.EventHandler[lambda event, nodes: [event, nodes]]  # 【以后再说】【未测试成功, 不确定返回值】当用户右键单击节点选择时，将调用此事件处理程序。
    # endregion

    # region 下面是交互(interaction)道具
    nodes_draggable: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制所有节点是否应可拖动
    nodes_connectable: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制所有节点是否应可连接
    nodes_focusable: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制节点之间的焦点可以使用该键循环并使用该键进行选择
    edges_focusable: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 可以使用该键循环对边缘之间的焦点并使用该键进行选择。此选项可以通过设置其 prop 来覆盖单个边
    elements_selectable: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 可以通过单击元素（节点和边）来选择它们。此选项可以是 通过设置其 prop 被单个元素覆盖
    auto_pan_on_connect: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 当光标移动到 创建连接时的视口
    auto_pan_on_node_dragt: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 当光标移动到 视口，同时拖动节点。
    auto_pan_speed: Optional[rx.Var[float]] = LiteralVar.create(15)  # 拖动节点或选择框时视口平移的速度。
    pan_on_drag: Optional[rx.Var[bool] | rx.Var[List[float]]] = LiteralVar.create(True)  # 启用此属性允许用户通过单击和拖动来平移视口。 您还可以将此 prop 设置为数字数组，以限制哪些鼠标按钮可以激活平移。
    selection_on_drag: Optional[rx.Var[bool]] = LiteralVar.create(False)  # 使用选择框选择多个元素，无需按 。selectionKey
    selection_mode: rx.Var[Literal['free', 'vertical', 'horizontal']] = LiteralVar.create('free')  # rx.Var[SelectionMode] = 'full'  # 当设置为"partial"时，当用户通过单击并拖动节点创建选择框时，该节点 在框中仅部分仍处于选中状态  # 1. Full：仅当选择矩形完全包含节点时，才会选择节点 2. Partial：当选择矩形与节点部分重叠时，将选择节点
    pan_on_scroll: Optional[rx.Var[bool]] = LiteralVar.create(False)  # 控制视口是否应通过在容器内滚动来平移。 可以使用panOnScrollMode限制为特定方向。
    pan_on_scroll_speed: Optional[rx.Var[float]] = LiteralVar.create(0.5)  # 控制滚动时平移视口的速度。 panOnScroll与道具一起使用。x
    pan_on_scroll_mode: rx.Var[Literal['free', 'vertical', 'horizontal']] = LiteralVar.create('free') # Optional[rx.Var[PanOnScrollMode]] = 'free'    # 启用时，此属性用于限制平移方向。 该选项允许向任何方向平移。    https://reactflow.dev/api-reference/types/pan-on-scroll-mode
    zoom_on_scroll: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制视口是否应通过在容器内滚动来缩放。
    zoom_on_pinch: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制视口是否应通过捏合触摸屏来缩放。
    zoom_on_double_click: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 控制视口是否应通过双击流上的某个位置来缩放。
    select_nodes_on_drag: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 在拖动时选择节点
    elevate_nodes_on_select: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 在选择节点时提高节点的 z 索引
    connect_on_click: Optional[rx.Var[bool]] = LiteralVar.create(True)  # 该选项允许您单击或点击源句柄以启动连接 然后单击目标句柄以完成连接。connectOnClick    如果将此选项设置为 ，用户将需要将连接线拖动到目标 句柄以创建连接。false
    connection_mode: rx.Var[Literal['default', 'straight', 'step', 'smoothstep', 'simplebezier']] = LiteralVar.create('strict')   # Optional[rx.Var[ConnectionMode]] = 'strict'  #     # rx.Var[Literal['strict', 'loose']]  # 松散连接模式将允许您连接不同类型的手柄，包括 源到源连接。但是，它不支持目标到目标的连接。严格 模式仅允许源句柄和目标句柄之间的连接。 Strict: 只能从源句柄开始并在目标句柄结束时建立连接 # Loose: 可以在任何手柄之间进行连接，无论类型如何
    # endregion

    # region 下面是连接线(connection)道具
    connection_line_style: Optional[rx.Var[CSSType]] # 要应用于连接线的样式。
    connection_line_type: rx.Var[Literal['default', 'straight', 'step', 'smoothstep', 'simplebezier']] = LiteralVar.create('default')  # Optional[rx.Var[ConnectionLineType]] = 'default'  # 用于连接线的边路径类型。 虽然创建的边可以是任何类型，但在创建边之前，React Flow 需要知道要为连接线渲染什么类型的路径！
    connection_radius: Optional[rx.Var[float]] = LiteralVar.create(20)  # 手柄周围的半径，在其中放置连接线以创建新边。
    # 【以后再做】connection_line_component: Optional[rx.Var[ConnectionLineComponent]] # React 组件用作连接线。
    connection_line_container_style: Optional[rx.Var[CSSType]]    # 要应用于连接线容器的样式。
    # endregion

    # region 下面是键盘(KBd)道具
    # reflex里键盘案件的数据类型是str
    delete_key_code: rx.Var[KeyCode] = LiteralVar.create('Backspace')  # 按下键或弦将删除任何选定的节点和边。传递数组 表示可以按下的多个键。 例如，将删除按下任一键时的选定元素。["Delete", "Backspace"]
    selection_key_code: rx.Var[KeyCode] = LiteralVar.create('Shift')  # 按住此键将允许您单击并拖动以在多个周围绘制一个选择框 节点和边。传递数组表示可以按下的多个键。   例如，当任一键为 压。["Shift", "Meta"]
    multi_selection_key_kode: rx.Var[KeyCode] = LiteralVar.create("'Meta' for macOS, 'Control' for other systems")  # 按下此键，您可以通过单击选择多个元素。
    zoom_activation_key_code: rx.Var[KeyCode] = LiteralVar.create("'Meta' for macOS, 'Control' for other systems")  # 如果设置了关键帧，则即使设置为 ，您也可以在按住该关键帧时缩放视口。panOnScrollfalse    通过将此属性设置为，您可以禁用此功能。null
    pan_activation_key_code: rx.Var[KeyCode] = LiteralVar.create('Space')  # 如果设置了关键帧，则即使设置为 ，也可以在按住该关键帧时平移视口。panOnScrollfalse 通过将此属性设置为，您可以禁用此功能。null
    disable_keyboard_a11y: rx.Var[bool] = LiteralVar.create(False)  # 您可以使用此 prop 禁用键盘辅助功能，例如选择节点或 使用箭头键移动选定节点。
    # endregion

    # region 下面是风格(Style)道具
    no_pan_class_name: rx.Var[str] = LiteralVar.create('nopan')  # 如果画布中的某个元素没有阻止鼠标事件传播，则单击和拖动 该元素将平移视口。添加类可以防止此行为和此 prop 允许您更改该类的名称
    no_drag_class_name: rx.Var[str] = LiteralVar.create('nodrag')  # 如果节点是可拖动的，则单击并拖动该节点将在画布上移动它。添加 该类阻止了这种行为，并且这个 prop 允许你更改它的名称 类
    no_wheel_class_name: rx.Var[str] = LiteralVar.create('nowheel')  # 通常，当鼠标悬停在画布上时滚动鼠标滚轮将缩放视口。 将类添加到画布上的元素 n 将阻止此行为和此 prop 允许您更改该类的名称。"nowheel"
    # endregion

    # region 下面是Hooks
    # 导入包，为了hooks使用，上面组件需要的包reflex会自动导入。
    def add_imports(self) -> dict[str, list[ImportVar]]:  # 这里是为了给hooks的使用而导入包，好像也能在hook的imports=里导入，区别还不清楚
        return {
            "@xyflow/react": [
                ImportVar(tag="ReactFlowProvider"),  # 导入 Provider
                # 已有的 hooks
                ImportVar(tag="useNodesState"),
                ImportVar(tag="useEdgesState"),
                # 新增需要的 hook
                ImportVar(tag="useConnection"),  # 显式导入 useConnection
                ImportVar(tag="useEdges"),  # 显式导入
                ImportVar(tag="useHandleConnections"),  # 显式导入
                #ImportVar(tag="useInternalNode"),  # 显式导入
                ImportVar(tag="useKeyPress"),  # 显式导入
                ImportVar(tag="useNodeConnections"),  # 显式导入
                ImportVar(tag="useNodeId"),  # 显式导入
                ImportVar(tag="useNodes"),  # 显式导入
                ImportVar(tag="useNodesData"),  # 显式导入
                ImportVar(tag="useReactFlow"),  # 显式导入
                ImportVar(tag="useNodesInitialized"),  # 显式导入
                ImportVar(tag="useOnSelectionChange"),  # 显式导入
                ImportVar(tag="useOnViewportChange"),  # 显式导入
                ImportVar(tag="useStore"),  # 显式导入
                ImportVar(tag="useStoreApi"),  # 显式导入
                ImportVar(tag="useUpdateNodeInternals"),  # 显式导入
                ImportVar(tag="useViewport"),  # 显式导入
            ]
        }




    # 【暂停】下面是Hooks***************
    def add_hooks(self) -> list[str | Var]:
        '''
        在这里添加基类的hooks
        hooks不能无目的的调用，必须有需要执行的某些操作
        hooks是仅限前端的行为动作，不存在于react hook本身，而是可以自己定义它的额外行为，这需要直接写js
        '''
        hooks = []

        # 使用连接  https://reactflow.dev/api-reference/hooks/use-connection


        # 保留参考，错误但可能有用
        #hook_use_connection = Var('const connection = useConnection;', # ！最后不要加括号！
        #    _var_data=VarData(
        #        imports={"@xyflow/react": ["useConnection"]},
        #        position = Hooks.HookPosition.PRE_TRIGGER
        #    )
        #)

        #print(f'触发Hook：hook_use_connection:{hook_use_connection}')
        #hooks.append(hook_use_connection)
        #hook_use_effect = Var('useEffect() => {};',
        #        _var_data = VarData(
        #            imports={"react": ["useEffect"]},
        #            position = Hooks.HookPosition.POST_TRIGGER
        #        )
        #    )

        #print(f'触发Hook：hook_use_connection2:{hook_use_effect}')
        #hooks.append(hook_use_effect)



        # 使用边缘  https://reactflow.dev/api-reference/hooks/use-edges
        hook_use_edge = 'const edges = useEdges();'
        #hooks.append(hook_use_edge)

        # 使用边缘state https://reactflow.dev/api-reference/hooks/use-edges-state
        hook_use_edges_state = "const initialNodes = [];" + \
            "const initialEdges = [];" + \
            "const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);" + \
            "const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);"
         # 是的，变量放里面
        #hooks.append(hook_use_edges_state)

        # 【弃用】使用手柄连接    useHandleConnections被弃用，取而代之的是功能更强大的 useNodeConnections。  https://reactflow.dev/api-reference/hooks/use-handle-connections

        # 使用内部节点    https://reactflow.dev/api-reference/hooks/use-internal-node
        #hook_use_internal_node = "const internalNode = useInternalNode('node-1');" +\
        #    "const absolutePosition = internalNode.internals.positionAbsolute;"
            
        #hooks.append(hook_use_internal_node)

        # 使用按键 https://reactflow.dev/api-reference/hooks/use-key-press
        '这里还需要修改，要把所有的按键都添加进来吗？还是有什么方法可以全部都检测？'
        hook_use_key_press = "const spacePressed = useKeyPress('Space');" +\
            "const cmdAndSPressed = useKeyPress(['Meta+s', 'Strg+s']);"
            
        #hooks.append(hook_use_key_press)

        # useNodeConnections    https://reactflow.dev/api-reference/hooks/use-node-connections
        hook_use_node_connections = "const connections = useNodeConnections({handleType: 'target', handleId: 'my-handle'});"
        #hooks.append(hook_use_node_connections)

        # useNodeId https://reactflow.dev/api-reference/hooks/use-node-id
        pass

        # 使用节点  https://reactflow.dev/api-reference/hooks/use-nodes
        hook_use_nodes = 'const nodes = useNodes();'
        #hooks.append(hook_use_nodes)

        # 使用节点数据    https://reactflow.dev/api-reference/hooks/use-nodes-data
        hook_use_nodes_data = "const nodeData = useNodesData('nodeId-1');" +\
            "const nodesData = useNodesData(['nodeId-1', 'nodeId-2']);"
            
        #hooks.append(hook_use_nodes_data)

        # useNodesInitialized（） https://reactflow.dev/api-reference/hooks/use-nodes-initialized
        pass

        # 使用节点state https://reactflow.dev/api-reference/hooks/use-nodes-state
        hook_use_nodes_state = "const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);" +\
            "const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);"
            
        #hooks.append(hook_use_nodes_state)

        # useOnSelectionChange（）    https://reactflow.dev/api-reference/hooks/use-on-selection-change
        pass

        # useOnViewportChange（） https://reactflow.dev/api-reference/hooks/use-on-viewport-change
        pass

        # 使用ReactFlow（） https://reactflow.dev/api-reference/hooks/use-react-flow
        hook_use_react_flow = "const reactFlow = useReactFlow();" +\
            "const [count, setCount] = useState(0);" +\
            "const countNodes = useCallback(() => {setCount(reactFlow.getNodes().length);}, [reactFlow]);"
            # you need to pass it as a dependency if you are using it with useEffect or useCallback
            # because at the first render, it's not initialized yet and some functions might not work.
            
            
        #hooks.append(hook_use_react_flow)

        # 使用存储（）    https://reactflow.dev/api-reference/hooks/use-store
        pass

        # 使用存储 Api（）    https://reactflow.dev/api-reference/hooks/use-store-api
        pass

        # useUpdateNodeInternals   https://reactflow.dev/api-reference/hooks/use-update-node-internals
        hook_use_update_node_internals = "const updateNodeInternals = useUpdateNodeInternals();" +\
            "const [handleCount, setHandleCount] = useState(0);" +\
            "const randomizeHandleCount = useCallback(() => {" +\
                "setHandleCount(Math.floor(Math.random() * 10));" +\
                "updateNodeInternals(id);" +\
            "}, [id, updateNodeInternals]);"
            
        #hooks.append(hook_use_update_node_internals)

        # 使用视口  https://reactflow.dev/api-reference/hooks/use-viewport
        hook_use_viewport = 'const { x, y, zoom } = useViewport();'
        #hooks.append(hook_use_viewport)


        return hooks


    # endregion



# region 下面是组件
# OK
class Background(FlowLib):
    '''
    背景组件可以方便地渲染基于节点的 UI 中常见的不同类型的背景。它有三种变体：线条、点和十字。
    Args:
        id: 当页面上存在多个背景时，每个背景都应具有唯一的 ID。
        color
        bgColor
        className
        patternClassName
        gap
        size
        offset
        lineWidth
        variant
        style
    '''
    tag = "Background"

    id: rx.Var[str] # 当页面上存在多个背景时，每个背景都应具有唯一的 ID。
    color: rx.Var[str]  # 图案的颜色。
    bg_color: rx.Var[str]    # 背景颜色
    class_name: rx.Var[str]  # 应用于容器的类
    pattern_class_name: rx.Var[str]   # 应用于模式的类。
    gap: rx.Var[Union[float, list[float], Tuple[float, float]]] = LiteralVar.create(20)    # 模式之间的间隙。传入元组可以控制 x 和 y 间隙 独立地。
    size: rx.Var[Literal[1, 2, 3, 4, 5, 6]]   # https://reactflow.dev/api-reference/components/background#size
    offset: rx.Var[Union[float, list[float], Tuple[float, float]]] = LiteralVar.create(0)    # 图案的偏移量
    line_width: rx.Var[float] = LiteralVar.create(1) # 绘制图案时使用的描边粗细。
    variant: rx.Var[BackgroundVariant] = LiteralVar.create('dots')    # 图案的变体。 默认值：'dots'
    style: rx.Var[CSSType] = {} # 应用于容器的样式。
# 【以后再说】base_edge(),    外观非功能，看不太懂，一直没效果
class BaseEdge(FlowLib):   # https://reactflow.dev/api-reference/components/base-edge
    '''该组件在内部用于所有边。它可以是 在自定义边缘内使用，并处理不可见的辅助边和边缘标签 给你的。'''
    tag = 'BaseEdge'

    path: rx.Var[str]    # 定义边缘的 SVG 路径字符串。这应该类似于一条简单的线。实用函数，如 can 用于为您生成此字符串。'M 0 0 L 100 100' getSimpleBezierEdge
    marker_start: rx.Var[str]    # 要在边缘开头使用的 SVG 标记的 id。这应该在单独的 SVG 文档或元素的元素中定义。使用格式“url（#markerId）”，其中 markerId 是标记定义的 ID。<defs>
    marker_end: rx.Var[str]  # 要在边缘末尾使用的 SVG 标记的 ID。这应该在单独的 SVG 文档或元素的元素中定义。使用格式“url（#markerId）”，其中 markerId 是标记定义的 ID。<defs>
    # label: rx.Var[ReactNode]     # 做到这里了，这个数据类型ReactNode还不确定 # 要沿边缘渲染的标签或自定义元素。这通常是文本标签或一些 自定义控件。
    label_style: rx.Var[CSSType]   # 要应用于标签的自定义样式。
    label_show_bg: rx.Var[bool]
    label_bg_style: rx.Var[CSSType]
    label_bg_padding: rx.Var[Union[list[float], Tuple[float, float]]]
    label_bg_border_radius: rx.Var[float]
    interaction_width: rx.Var[float] = LiteralVar.create(20)   # 用户可以与之交互的边缘周围不可见区域的宽度。这是 对于使边缘更易于单击或将鼠标悬停在上面很有用。
    label_x: rx.Var[float]   # 边缘标签的 x 位置
    label_y: rx.Var[float]   # 边标的y位置
    # ..props   # Omit<SVGAttributes<SVGPathElement>, "d" | "path" | "markerStart" | "markerEnd">

class ControlButton(FlowLib):
    tag = 'ControlButton'
    # ..props   # Omit<SVGAttributes<SVGPathElement>, "d" | "path" | "markerStart" | "markerEnd">

# OK
class Controls(FlowLib):
    '''控制区域'''
    tag = "Controls"

    show_zoom: rx.Var[bool] = LiteralVar.create(True)    # 是否显示放大和缩小按钮。这些按钮将调整视口 每次按下以固定量缩放。
    show_fit_view: rx.Var[bool] = LiteralVar.create(True)    # 是否显示适合视图按钮。默认情况下，此按钮将调整视口，以便 所有节点都同时可见。
    show_interactive: rx.Var[bool] = LiteralVar.create(True)    # 用于切换交互性的显示按钮
    # 【以后再做】fitViewOptions: rx.Var[FitViewOptionsBase[Any]] = rx.Var.create(FitViewOptionsBase())  # https://reactflow.dev/api-reference/components/controls#fitviewoptions # 自定义适合视图按钮的选项。这些选项与您将传递给 fitView 函数。
    on_zoom_in: rx.EventHandler[no_args_event_spec]   # 调用单击放大按钮时的默认缩放行为。
    on_zoom_out: rx.EventHandler[no_args_event_spec]   # 调用单击缩小按钮时的默认缩放行为。
    on_fit_view: rx.EventHandler[no_args_event_spec]   # 单击“拟合视图”按钮时调用。如果未提供此选项，则视口将为 调整为所有节点都可见。
    on_interactive_change: rx.EventHandler[lambda interactiveStatus: [interactiveStatus]] # 单击交互式（锁定）按钮时调用。  # 示例返回值：类型=<class 'bool'>, 值=True
    position: rx.Var[PanelPosition] = LiteralVar.create('bottom-left')    # 控件在窗格上的位置
    # children: rx.Var[rx.Component] = None # ReactNode = None   # 【以后再说】 很大问题，加了不能运行,按照官方的做成rx.Var[rx.Component]也不行（官方也没有示例）  # 对于react-flow.Controls.children    类型的说明:https://github.com/DefinitelyTyped/DefinitelyTyped/blob/d7e13a7c7789d54cf8d601352517189e82baf502/types/react/index.d.ts#L264
    style: rx.Var[CSSType] = {}   # 不知道为什么必须要默认值，斗则不能运行 # 应用于容器的样式    示例数据：{'color':'blue'}
    className: rx.Var[str] = None   # 应用于容器的类名
    aria_label: rx.Var[str] = LiteralVar.create('React Flow controls')
    orientation: rx.Var[Literal['horizontal', 'vertical']] = LiteralVar.create('vertical')

class EdgeLabelRenderer(FlowLib):
    '''边缘基于 SVG。如果您想渲染更复杂的标签，您可以使用该组件访问基于 div 的渲染器。
    此组件 <EdgeLabelRenderer />是一个入口，用于渲染位于 <div />边缘。
    您可以在边缘标签渲染器(https://reactflow.dev/examples/edges/edge-label-renderer)示例中查看组件的示例用法'''
    tag = 'EdgeLabelRenderer'
    # children: rx.Var[ReactFlow.Nodes | List[Dict[str, Any]]] | None = None

class EdgeText(FlowLib):
    '''您可以将该组件用作辅助组件来显示文本 <EdgeText />在自定义边缘中。'''
    tag = 'EdgeText'

    x: rx.Var[float]  # 应呈现标签的 x 位置。

    y: rx.Var[float]  # 应呈现标签的 y 位置。

    label: ReactNode  # 数据类型: ReactNode   要沿边缘渲染的标签或自定义元素。这通常是文本标签或一些 自定义控件。

    label_style: rx.Var[CSSType] = {} # 要应用于标签的自定义样式。

    label_show_bg: rx.Var[bool]

    label_bg_style: rx.Var[CSSType] = {}

    label_bg_padding: rx.Var[Union[list[float], Tuple[float, float]]]   # [number, number]

    label_bg_border_radius: rx.Var[float]

    # ...props	Omit<SVGAttributes<SVGElement>, "x" | "y">

class Handle(FlowLib):
    '''该组件在自定义节点(https://reactflow.dev/learn/customization/custom-nodes)中用于定义连接点。<Handle />'''
    tag = 'Handle'

    id: rx.Var[str]
    type: rx.Var[Literal['source', 'target']] = LiteralVar.create('source')    # 手柄的类型。
    position: rx.Var[Literal['left', 'top', 'right', 'bottom']] = LiteralVar.create('top')    # 手柄相对于节点的位置。在水平流中，源手柄是 Position.Right通常，在垂直流动中，它们通常是 。Position.Top
    is_connectable: rx.Var[bool] = LiteralVar.create(True)   # 您是否能够连接到/从此句柄连接。
    is_connectable_start: rx.Var[bool] = LiteralVar.create(True)   # 指示连接是否可以从此句柄开始。
    is_connectable_end: rx.Var[bool] = LiteralVar.create(True)   # 指示连接是否可以在此句柄上结束。
    #isValidConnection       # 【不建议使用,使用主 ReactFlow 组件上的 isValidConnection 属性】【未知】将连接拖动到此句柄时调用。您可以使用此回调来执行一些 例如，基于连接目标和源的自定义验证逻辑。在可能的情况下， 我们建议您将此逻辑移动到主 ReactFlow 上的 prop 组件出于性能原因。isValidConnection
    on_connect: OnConnect    # 建立连接时调用回调事件处理器
    # props https://reactflow.dev/api-reference/components/handle#props

    # 导入包，为了hooks使用，上面组件需要的包reflex会自动导入。
    #def add_imports(self) -> dict[str, list[ImportVar]]:  # 这里是为了给hooks的使用而导入包，好像也能在hook的imports=里导入，区别还不清楚
    #    return {
    #        "@xyflow/react": [
    #            ImportVar(tag="useUpdateNodeInternals"),  # 显式导入
    #        ]
    #    }

    # hook
    #def add_hooks(self) -> list[str | Var]:
        # 参考：https://reactflow.dev/api-reference/hooks/use-update-node-internals
    #    return []

class MiniMap(FlowLib):

    tag = 'MiniMap'

    position: rx.Var[Literal['top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right']] = LiteralVar.create('bottom-right')   # 小地图在窗格上的位置。
    on_click: rx.EventHandler[lambda e0: [e0]]
    node_color: rx.Var[str] = LiteralVar.create("#e2e2e2")   # 小地图上节点的颜色。
    node_stroke_color: rx.Var[str] = LiteralVar.create("transparent")   # 小地图上节点的笔划颜色。
    node_class_name: rx.Var[str] = LiteralVar.create('') # 应用于小地图节点的类名。      默认值是空字符串
    node_border_radius: rx.Var[int] = LiteralVar.create(5)   # 小地图上节点的边界半径。
    node_stroke_width: rx.Var[int] = LiteralVar.create(2)    # 小地图上节点的笔划宽度。
    # node_component: rx.Var[Component]    #这个还有很大问题https://reactflow.dev/api-reference/components/minimap#nodecomponent
    bg_color: rx.Var[str]    # 小地图的背景颜色
    mask_color: rx.Var[str] = LiteralVar.create("rgba(240, 240, 240, 0.6)")  # 覆盖小地图中当前不可见的部分的遮罩的颜色 视窗。
    mask_stroke_color: rx.Var[str] = LiteralVar.create('transparent')    # 表示视口的蒙版的描边颜色
    mask_stroke_width: rx.Var[int] = LiteralVar.create(1)    # 表示视口的蒙版的描边宽度。
    on_node_click: rx.EventHandler[lambda e0: [e0]]    # 点击小地图上的节点时调用回调。
    pannable: rx.Var[bool] = LiteralVar.create(False)  # 确定是否可以通过在小地图内拖动来平移视口
    zoomable: rx.Var[bool] = LiteralVar.create(False)  # 确定是否可以通过在小地图内滚动来缩放视口。
    ariaLabel: rx.Var[str | None] = LiteralVar.create("Mini Map")  # 小地图中没有文本供屏幕阅读器用作可访问的名称，因此它是 重要提示 我们提供了一个使小地图易于访问。默认值就足够了，但你可以 想要将其替换为与您的应用或产品更相关的内容。
    inverse_pan: rx.Var[bool] = LiteralVar.create(False)    # 平移小地图视口时反转方向。
    zoom_step: rx.Var[int] = LiteralVar.create(10)  # 在小地图上放大/缩小的步长。
    offset_scale: rx.Var[int] = LiteralVar.create(5)  # 在小地图上偏移视口，就像填充一样。         只是number可以是int或者float
    # props https://reactflow.dev/api-reference/components/minimap#props

class NodeResizeControl(FlowLib):
    '''要创建自己的调整大小 UI，您可以使用可以传递子组件（例如图标）NodeResizeControl的组件。'''
    tag = 'NodeResizeControl'

    node_id: rx.Var[str | None] = None   # 它正在调整大小的节点的 ID。
    color: rx.Var[str | None] = None    # 调整大小手柄的颜色。
    min_width: rx.Var[float] = LiteralVar.create(10)  # 节点的最小宽度。
    min_height: rx.Var[float] = LiteralVar.create(10) # 节点的最小高度。
    max_width: rx.Var[float]   # 节点的最大宽度。    【未知】默认值: Number.MAX_VALUE https://reactflow.dev/api-reference/components/node-resize-control#maxwidth
    max_heigh: rx.Var[float]   # 节点的最大高度。    【未知】默认值: Number.MAX_VALUE https://reactflow.dev/api-reference/components/node-resize-control#maxwidth
    keep_aspect_ratio: rx.Var[bool] = LiteralVar.create(False)   # 调整大小时保持纵横比
    should_resize: rx.EventHandler[lambda e0: [e0]]  # 回调，用于确定是否应调整节点大小。
    auto_scale: rx.Var[bool] = LiteralVar.create(True)  # 使用缩放级别缩放控件。
    on_resize_start: OnResizeHandler   # 调整大小开始时调用回调。  数据类型: OnResizeStart
    on_resize: OnResizeHandler    # 调整大小时调用的回调。  数据类型: OnResize
    on_resize_end: OnResizeHandler # 调整大小结束时调用回调。  数据类型: OnResizeEnd
    position: rx.Var[Literal['top', 'bottom', 'left', 'right', 'top-left', 'top-right', 'bottom-left', 'bottom-right']]   # 控件的位置。  数据类型: ControlPosition
    variant: rx.Var[Literal['handle']] = LiteralVar.create('handle')   # 控件的变体。  数据类型: ResizeControlVariant
    resize_direction: rx.Var[Literal['horizontal', 'vertical']]   # 用户可以调整节点大小的方向。 如果未提供，用户可以向任何方向调整大小。   数据类型:  ResizeControlDirection
    class_name: rx.Var[str]
    style: rx.Var[CSSType] = {}
    #children:    # 数据类型: ReactNode

class NodeResizer(FlowLib):
    '''该组件可用于将调整大小功能添加到 <NodeResizer />节点。它渲染节点周围的可拖动控件，以在各个方向上调整大小。'''
    tag='NodeResizer'

    node_id: rx.Var[str]   # 它正在调整大小的节点的 ID。
    color: rx.Var[str]    # 调整大小手柄的颜色。
    handle_class_name: rx.Var[str]  # 应用于句柄的类名。
    handle_style: CSSType    # 应用于手柄的样式。 不能加 rx.Var[] 否则不可运行
    line_class_name: rx.Var[str]    # 应用于线的类名。
    line_style: CSSType  # 应用于线的样式。 不能加 rx.Var[] 否则不可运行
    is_visible: rx.Var[bool] = LiteralVar.create(True)  # 控件是否可见。
    min_width: rx.Var[float] = LiteralVar.create(10)  # 节点的最小宽度。
    min_height: rx.Var[float] = LiteralVar.create(10) # 节点的最小高度。
    max_width: rx.Var[float]# = LiteralVar.create(float('inf'))    # 节点的最大宽度。  【未知】默认值: Number.MAX_VALUE
    max_height: rx.Var[float]#  = LiteralVar.create(float('inf'))  # 节点的最大高度。  【未知】默认值: Number.MAX_VALUE
    keep_aspect_ratio: rx.Var[bool] = LiteralVar.create(False)   # 调整大小时保持纵横比。
    auto_scale: rx.Var[bool] = LiteralVar.create(True)  # 使用缩放级别缩放控件。
    should_resize: rx.EventHandler[lambda event, params: [event, params]]   # 回调，用于确定是否应调整节点大小。
    on_resize_start: OnResizeHandler # 调整大小开始时调用回调。
    on_resize: OnResizeHandler # 调整大小时调用的回调。
    on_resize_end: OnResizeHandler  # 调整大小结束时调用回调。

class NodeToolbar(FlowLib):
    '''此组件可以将工具栏或工具提示渲染到自定义节点的一侧。这 工具栏不会随视口缩放，因此内容始终可见。'''

    tag='NodeToolbar'
    node_id: rx.Var[str | List[str]]   # 通过传入节点 ID 数组，您可以为组或集合渲染单个工具提示 节点数。
    is_visible: rx.Var[bool]   # 如果 True，即使未选择节点，节点工具栏也可见。
    position: rx.Var[Literal['left', 'top', 'right', 'bottom']] = LiteralVar.create('top')  # 工具栏相对于节点的位置。
    offset: rx.Var[int] = LiteralVar.create(10)    # 节点和工具栏之间的空间，以像素为单位。
    align: rx.Var[str] = LiteralVar.create('center')    # 相对于节点对齐工具栏      数据类型: Align
    # ..props   # Omit<SVGAttributes<SVGPathElement>, "d" | "path" | "markerStart" | "markerEnd">

class Panel(FlowLib):
    '''该组件可帮助您将内容放置在视口上方。是的 <Panel />由 <MiniMap /> 和 <Controls /> 组件内部使用。'''
    tag='Panel'
    position: Literal['top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right'] = 'top-left'
    # ..props   # Omit<SVGAttributes<SVGPathElement>, "d" | "path" | "markerStart" | "markerEnd">

class ViewportPortal(FlowLib):
    '''<ViewportPortal />组件可用于将组件添加到渲染节点和边的流的同一视口。当您想要渲染自己的组件时，这非常有用，这些组件与节点和边遵循相同的坐标系，并且还受缩放和平移的影响'''
    tag='ViewportPortal'

    # children=
# endregion

# 从types哪里引入了变量，然后报错了，现在明明已经去除了，但js报错，可能是因为没有恢复干净


# region 下面是实例化组件
flow = Flow.create
background = Background.create
base_edge = BaseEdge.create
control_button = ControlButton.create
controls = Controls.create
edge_label_renderer = EdgeLabelRenderer.create
edge_text = EdgeText.create
handle = Handle.create
mini_map = MiniMap.create
node_resize_control = NodeResizeControl.create
node_resizer = NodeResizer.create
node_toolbar = NodeToolbar.create
panel = Panel.create
viewport_portal = ViewportPortal.create
# endregion






