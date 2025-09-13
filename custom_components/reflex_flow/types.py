# 类型 https://reactflow.dev/api-reference/types
'''
添加指南：
    变量示例：
    handles?: NodeHandle[];
        handles - 属性名称
        ? - 表示这个属性是可选的（optional）
        NodeHandle - 数组中元素的类型
        [] - 表示这是一个数组类型 用列表包裹   List[handles]
'''
import reflex as rx
from typing import Any, Dict, List, Union, Literal, TypedDict, Tuple, Callable, Iterable, TypeVar, Generic, Optional
from enum import Enum

from jinja2.nodes import Literal


# 有些class在react文档中的数据类型声明靠后的，但是前面有需要要调用靠后面的: 还是调整顺序，优先于python调用吧，不遵从文档了
# reflex包裹react的数据类型不是都要定义为类
# 需要定义为响应式状态变量需要用 rx.Var[] 包裹

# region 主要类型使用的类型，但不在文档里的（包含: 嵌套对象和类型别名化）

class AriaLiveMessageParams(TypedDict):
    """
    对应 `node.a11yDescription.ariaLiveMessage` 函数的入参类型
    - TypedDict 用于精准描述键值对参数结构（Reflex 会自动映射为 JS 对象）
    定义函数参数类型（对应 JS 的 { direction: string; x: number; y: number }）
    """
    direction: str  # JS 的 string → Python 的 str
    x: float  # JS 的 number → Python 的 float（兼容 int 和 float）
    y: float  # JS 的 number → Python 的 float

class NodeA11yDescription(rx.Base):
    """
    对应 React Flow 中 `node.a11yDescription` 的嵌套对象类型
    - 继承 rx.Base 实现 Reflex 与 JS 对象的自动映射
    - 字段默认值可参考官方 defaultAriaLabelConfig 填充
    定义嵌套对象：NodeA11yDescription（对应 node.a11yDescription）
    """
    # 基础字符串字段：默认节点无障碍描述
    default: str = "Press enter or space to select a node. Press delete to remove it and escape to cancel."
    # 基础字符串字段：键盘可用时的节点无障碍描述
    keyboard_disabled: str = "Press enter or space to select a node. You can then use the arrow keys to move the node around. Press delete to remove it and escape to cancel."
    # 函数字段：ariaLive 消息生成函数（接收 AriaLiveMessageParams，返回字符串）
    aria_live_message: Callable[[AriaLiveMessageParams], str] = (
        lambda
            params: f"Moved selected node {params['direction']}. New position, x: {params['x']}, y: {params['y']}"
    )

class EdgeA11yDescription(rx.Base):
    """
    对应 React Flow 中 `edge.a11yDescription` 的嵌套对象类型
    定义嵌套对象：EdgeA11yDescription（对应 edge.a11yDescription）
    """
    # 基础字符串字段：默认边无障碍描述
    default: str = "Press enter or space to select an edge. You can then press delete to remove it or escape to cancel."

class ControlsAriaLabel(rx.Base):
    """
    对应 React Flow 中 `controls` 下的所有 ariaLabel 字段
    定义嵌套对象：ControlsAriaLabel（对应 controls 下的 ariaLabel 字段）
    """
    # 基础字符串字段：控制面板整体无障碍标签
    aria_label: str = "Control Panel"
    # 基础字符串字段：放大按钮无障碍标签
    zoom_in: dict[str, str] = {"ariaLabel": "Zoom In"}  # 对应 controls.zoomIn.ariaLabel
    # 基础字符串字段：缩小按钮无障碍标签
    zoom_out: dict[str, str] = {"ariaLabel": "Zoom Out"}  # 对应 controls.zoomOut.ariaLabel
    # 基础字符串字段：适配视图按钮无障碍标签
    fit_view: dict[str, str] = {"ariaLabel": "Fit View"}  # 对应 controls.fitView.ariaLabel
    # 基础字符串字段：交互开关无障碍标签
    interactive: dict[str, str] = {"ariaLabel": "Toggle Interactivity"}  # 对应 controls.interactive.ariaLabel

NodeId: str
EdgeId: str

EdgeChangeType = Literal['add', 'update', 'remove']

# region padding部分
'''
来源：https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/general.ts#L150
使用示例1：
    PaddingConfig(
        x=20,        # 左右各 20px
        top="10px",  # 上 10px
        bottom=10    # 下 10px（默认 px）
    )
使用示例2：
    padding=20
使用示例3：
    padding="15%"
'''
# PaddingUnit = Literal['px', '%']  在python里没有程序意义，但js有，所以统一规范应写在这里。 用来声明下面的PaddingWithUnit是字符串时，组合必须是（数字+px或%）的形式
PaddingWithUnit = Union[int, float, str]    # 字符串时，组合必须是（数字+px或%）的形式    示例：15px、10%
class PaddingConfig(rx.BaseModel):
    """
    padding 精细配置对象：支持按方向（上下左右）或轴（水平x/垂直y）设置
    优先级：具体方向（top/right等）> 轴（x/y）
    """
    # 方向配置（可选）
    top: Optional[PaddingWithUnit] = None    # 上 padding
    right: Optional[PaddingWithUnit] = None  # 右 padding
    bottom: Optional[PaddingWithUnit] = None # 下 padding
    left: Optional[PaddingWithUnit] = None   # 左 padding
    # 轴配置（可选，x=左右，y=上下）
    x: Optional[PaddingWithUnit] = None      # 水平轴统一 padding
    y: Optional[PaddingWithUnit] = None      # 垂直轴统一 padding
Padding = Union[PaddingWithUnit, PaddingConfig]
# endregion

HandleType = Literal['source', 'target']   # https://github.com/xyflow/xyflow/blob/main/packages/system/src/types/handles.ts/#L6C13-L6C46

BuiltInNode: Union[Literal["input", "output", "default", "group"], None] = "default" # 没用到


class Data(TypedDict):
    label: str

''' 关于NodeType的架构   NodeType 很特别，
注意！！NodeType≠NodeTypes， 这里的NodeType是NodeTypes的键， NodeTypes是真正的组件Component，  由NodeType制定调用NodeTypes的那一部分
    多个Component但只用一个：不同的节点从一个NodeTypes选择各自需要用的Component
相关代码只有NodeType extends string | undefined = string | undefined（https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L13C3-L13C59）
    和 下面的 undefined extends NodeType （https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L80C6-L80C32）

意义不太大的起源：https://reactflow.dev/api-reference/types/node#type
自定义节点浅度说明：(https://reactflow.dev/learn/customization/custom-nodes)

清晰的说明示例：
    // 1. 定义自定义节点组件
    const CustomNode = (props) => {
      // props包含：id, position, data, type等
      return (
        <div style={{ background: props.data.color }}>
          {props.data.label}
        </div>
      );
    };
    
    // 2. 创建NodeTypes对象
    const nodeTypes: NodeTypes = {
      // 键是字符串，值是组件
      'custom': CustomNode,
      'input': InputNode,
      'output': OutputNode
    };
    
    // 3. 定义节点数据（type是字符串，不是组件）
    const nodes: Node[] = [
      {
        id: '1',
        type: 'custom',  // 这里是字符串，对应nodeTypes中的键
        position: { x: 0, y: 0 },
        data: { 
          label: 'Custom Node',
          color: 'lightblue'
        }
      }
    ];
    
    // 4. 在React Flow中使用
    <ReactFlow 
      nodes={nodes} 
      nodeTypes={nodeTypes}  // 提供映射关系
    />

'''
NodeType: str | None = None


class Measured(TypedDict):
    width: Optional[float]
    height: Optional[float]




# endregion


# 下面是主要的类型
class AriaLabelConfig:
    """
    React Flow 顶层 AriaLabelConfig 类型
    - 聚合所有嵌套对象，完整映射官方类型结构
    - Reflex 会自动将其转换为 JS 对象，与 React Flow 组件预期类型兼容
    """
    # 嵌套对象：节点无障碍描述（对应 node.a11yDescription）
    node: dict[str, NodeA11yDescription] = {"a11yDescription": NodeA11yDescription()}
    # 嵌套对象：边无障碍描述（对应 edge.a11yDescription）
    edge: dict[str, EdgeA11yDescription] = {"a11yDescription": EdgeA11yDescription()}
    # 嵌套对象：控制面板无障碍标签（对应 controls 下所有字段）
    controls: ControlsAriaLabel = ControlsAriaLabel()
    # 基础字符串字段：小地图无障碍标签（对应 minimap.ariaLabel）
    minimap: dict[str, str] = {"ariaLabel": "Mini Map"}
    # 基础字符串字段：节点手柄无障碍标签（对应 handle.ariaLabel）
    handle: dict[str, str] = {"ariaLabel": "Handle"}

BackgroundVariant = Literal['lines', 'dots', 'cross']

ColorMode = Literal['light', 'dark', 'system']

Position = Literal['top', 'right', 'bottom', 'left']

class XYPosition(rx.Base):
    x: float = 0
    y: float = 0

class Connection(rx.Base):
    """
    React Flow 的 Connection 类型：表示节点间的连接关系
    字段可选性、类型完全对齐官方定义，支持 null 取值（如 sourceHandle: None）
    """
    # 必选：起始节点 ID（string 类型，无默认值，必须显式传入）
    source: NodeId
    # 可选：起始节点手柄位置（Position 枚举值 / null / None，默认 None）
    source_handle: Optional[Union[Position, None]] = None
    # 必选：目标节点 ID（string 类型，无默认值）
    target: NodeId
    # 可选：目标节点手柄位置（Position 枚举值 / null / None，默认 None）
    target_handle: Optional[Union[Position, None]] = None
    # 可选：连接的唯一 ID（自动生成时可省略，默认 None）
    id: Optional[EdgeId] = None
    # 可选：起始点坐标（嵌套 XYPosition 对象，默认 None）
    source_position: Optional[XYPosition] = None
    # 可选：目标点坐标（嵌套 XYPosition 对象，默认 None）
    target_position: Optional[XYPosition] = None
    # 可选：是否为潜在连接（拖拽中，默认 None）
    is_potential: Optional[bool] = None
    # 可选：潜在连接是否有效（默认 None）
    is_valid: Optional[bool] = None

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

class ConnectionLineComponent:
    def __call__(self, props: ConnectionLineComponentProps) -> rx.Component:
        """
        React Flow 连接线条组件的类型协议
        :param props: 组件的入参属性，必须符合 ConnectionLineComponentProps 结构
        :return: Reflex 组件实例（对应 React 组件）
        """
        rx.text('【未完成】数据类型ConnectionLineComponent，应该返回ConnectionLineComponentProps')

ConnectionLineType = Literal['default', 'straight', 'step']

ConnectionMode = Literal['strict', 'loose']

class ConnectionState:
    pass

class CoordinateExtent:
    pass

class DefaultEdgeOptions(TypedDict):  # https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type
    class Data(TypedDict):
        class Value(TypedDict):
            age: int
            breed: str

        miffy: Value
        boris: Value
        mordred: Value

    class EdgeMarker(TypedDict):
        type: Union[Literal["arrow", "arrowclosed"], str]  # 【以后在做】https://reactflow.dev/api-reference/types/marker-type
        color: str | None = None
        width: int
        height: int
        markerUnits: str
        orient: str
        strokeWidth: int

    type: str | None = None
    animated: bool
    hidden: bool
    deletable: bool
    selectable: bool
    data: Data | None = None  # 传递到边缘的任意数据。
    markerStart: EdgeMarker  # 将标记设置在边的开头。
    markerEnd: EdgeMarker  # 将标记设置在边的末端。
    zIndex: int
    ariaLabel: str
    interactionWidth: int  # ReactFlow 在每个边缘周围渲染一条不可见的路径，使它们更容易单击或点击。 此属性设置该不可见路径的宽度。
    label: Any  # 【以后再做】   # 要沿边缘渲染的标签或自定义元素。这通常是文本标签或一些 自定义控件。
    labelStyle: Any  # 【以后再做】   # 要应用于标签的自定义样式。
    labelShowBg: bool
    labelBgStyle: Any  # 【以后再做】
    labelBgPadding: List[int]
    labelBgBorderRadius: int
    style: Any  # 【以后再做】
    className: str
    reconnectable: bool | Any  # 【以后再做】     # 确定是否可以通过将源或目标拖动到新节点来更新边。 此属性将覆盖组件上 prop 设置的默认值。edgesReconnectable<ReactFlow />
    focusable: bool
    ariaRole: Any  # 【以后再做】    # 边缘的 ARIA 角色属性，用于辅助功能。
    domAttributes: Any  # 【以后再做】

class DeleteElements:
    pass

class EdgeMarker(TypedDict):
    type: Union[Literal["arrow", "arrowclosed"], str]  # 【以后在做】https://reactflow.dev/api-reference/types/marker-type
    color: str | None = None
    width: int
    height: int
    markerUnits: str
    orient: str
    strokeWidth: int

class Edges(TypedDict):
    # region 下面是TypedDict 定义，规定数据形式.

    class Data(TypedDict):
        label: str

    # endregion

    id: str
    type: str | None = None # 【以后在做】
    source: str
    target: str
    sourceHandle: str
    targetHandle: str
    animated: bool
    hidden: bool
    deletable: bool
    selectable: bool
    data: Any   # 【以后在做】
    selected: bool
    markerStart: EdgeMarker # 将标记设置在边的开头。
    markerEnd: EdgeMarker   # 将标记设置在边的末端。
    zIndex: int
    ariaLabel: str
    interactionWidth: int   # ReactFlow 在每条边周围渲染一条不可见的路径，以便于单击或点击它们。此属性设置该不可见路径的宽度。
    label: Any  # 【以后在做】
    labelStyle: Any # 【以后在做】
    labelShowBg: bool
    labelBgStyle: Any # 【以后在做】
    labelBgPadding: List[int]
    labelBgBorderRadius: int
    style: Any # 【以后在做】
    className: str
    reconnectable: bool | Any # 【以后在做】  # 确定是否可以通过将源或目标拖动到新节点来更新边。 此属性将覆盖组件上 prop 设置的默认值。edgesReconnectable<ReactFlow />
    focusable: bool
    ariaRole: Any # 【以后在做】  边缘的 ARIA 角色属性，用于辅助功能。
    domAttributes: Any # 【以后在做】

class EdgeChange:
    """React Flow 边缘变更对象，包含操作类型、当前边缘数据、历史数据（可选）"""
    # 必选：操作类型（添加/更新/删除）
    type: EdgeChangeType
    # 必选：当前边缘数据（添加时为新数据，更新/删除时为当前数据）
    edge: Edges
    # 可选：变更前的边缘数据（仅 update/remove 操作存在，add 操作无此字段）
    previous_edge: Optional[Edges] = None

class EdgeMouseHandler:
    pass

class EdgeProps:
    pass


class Handle:
    id: str | None = None
    nodeId: str
    x: float
    y: float
    position: Position
    type: HandleType
    width: float
    height: float

# 非react-flow文档中的主要类型，但因上下文需要在这里
class NodeBounds:
    '''
    export type NodeBounds = XYPosition & {
      width: number | null;
      height: number | null;
    };
    https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L137
    '''
    # 宽高字段，支持数值或 None（对应前端 null）
    width: Optional[float] = None  # 对应 number | null
    height: Optional[float] = None  # 对应 number | null
# 非react-flow文档中的主要类型，但因上下文需要在这里
class NodeHandleBounds:
    '''
    export type NodeHandleBounds = {
      source: Handle[] | null;
      target: Handle[] | null;
    };
    https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L126
    '''
    # 源连接点数组，支持 None（对应前端 null）
    source: Optional[List[Handle]] = None  # 对应 Handle[] | null

    # 目标连接点数组，支持 None（对应前端 null）
    target: Optional[List[Handle]] = None  # 对应 Handle[] | null
# 非react-flow文档中的主要类型，但因上下文需要在这里
class InternalNodeInternals:
    """
    InternalNode 中的 internals 字段类型，对应前端定义：
    {
      positionAbsolute: XYPosition;
      z: number;
      userNode: NodeType;
      handleBounds?: NodeHandleBounds;
      bounds?: NodeBounds;
    }
    https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L95
    """
    # 绝对位置（包含父节点偏移）
    position_absolute: XYPosition  # 对应前端 positionAbsolute

    # 层级 z-index（数值类型）
    z: int  # 对应前端 z

    # 原始用户节点对象（泛型，保留用户定义的节点数据）
    user_node: NodeType  # 对应前端 userNode

    # 连接点边界信息（可选）
    handle_bounds: Optional[NodeHandleBounds] = None  # 对应前端 handleBounds

    # 节点整体边界信息（可选）
    bounds: Optional[NodeBounds] = None  # 对应前端 bounds


class NodeHandle:
    width: float
    height: float
    id: str | None = None
    x: float
    y: float
    position: Position
    type: Handle

class Nodes(TypedDict):
    '''
    # JS源码参数带问号?的是可选参数的意思，用Optional[]包裹，等同于 X | None = None
    # region 下面是TypedDict 定义，规定数据形式.
    type: Optional[NodeType] # 节点类型，  如果定义了nodeTypes就必填, 否则报错
    '''

    id: str # 节点的唯一 ID。
    position: XYPosition  # 节点在窗格上的位置。 如：{'x': 0, 'y': 0}
    data: Optional[Data]    # 传递给节点的任意数据。  如：{'label': '150'}
    sourcePosition: Optional[Position]    # 仅与默认、源、目标 nodeType 相关。控制源位置。
    targetPosition: Optional[Position]    # 仅与默认、源、目标 nodeType 相关。控制目标位置。
    hidden: Optional[bool]    # 节点是否应在画布上可见。
    selected: Optional[bool]
    dragging: Optional[bool]  # 当前是否正在拖动节点。
    draggable: Optional[bool] # 节点是否可以拖动。
    selectable: Optional[bool]
    connectable: Optional[bool]
    deletable: Optional[bool]
    dragHandle: Optional[str] # 一个类名称，可以应用于节点内的元素，允许这些元素起作用 作为拖动手柄，允许用户通过单击并拖动这些元素来拖动节点。
    width: Optional[float]
    height: Optional[float]
    initialWidth: Optional[float]
    initialHeight: Optional[float]
    parentId: Optional[str]   # 父节点 ID，用于创建子流。
    zIndex: Optional[int]
    extent: Optional[Literal['parent'] | List[List[float]]]   # 可以移动节点的边界。    示例： 'parent'、 [[0, 0], [100, 100]]
    expandParent: Optional[bool]  # 如果将父节点拖动到 父节点的边界
    ariaLabel: Optional[str]
    origin: Optional[List[float]]  # 节点相对于其位置的原点。 示例： [0.5, 0.5] // centers the node、[0, 0] // top left、[1, 1] // bottom right
    handles: Optional[Optional[List[HandleType]]]
    measured: Optional[Measured]
    type: Optional[NodeType] # 节点类型，  如果定义了nodeTypes就必填, 否则报错        也可以自定义节点(https://reactflow.dev/learn/customization/custom-nodes)
    style: Optional[Union[str, int]]
    className: Optional[str]
    resizing: Optional[bool]
    focusable: Optional[bool]
    ariaRole: Optional[Literal['group']]
    # domAttributes: None = None

class FitViewOptions:
    padding: Padding
    includeHiddenNodes: bool
    minZoom: float
    maxZoom: float
    duration: float
    ease: str = '(t: number) => ((t *= 2) <= 1 ? t * t * t : (t -= 2) * t * t + 2) / 2;'    # 接收一个输出0~1float的def，用于显示动画. AI说可以转换成JS的函数，但感觉有点悬，所以先用react提供的JS字符串吧,这里是先加速后减速的缓动函数
    interpolate: Literal["smooth", "linear"]
    nodes: Nodes    # 当使用这个参数时，Nodes中的id必填。 https://reactflow.dev/api-reference/types/fit-view-options#nodes



class HandleConnection:
    # https://reactflow.dev/api-reference/types/handle-connection
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None
    edgeId: str

class InternalNode: # 【！！潜在问题】
    '''
    文档里的类型说明很奇怪，比如 width	NodeType["width"]
    在处理的时候就是说这里的类型定于与Nodes里那个的参数的类型定义相同就可以了。
    ！！潜在问题：官方文档这样说，可能是因为 使用的时候传入参数的数据类型也要相同， 如果擦混入不同类型的数据可能报错
    '''
    width: Optional[float]
    height: Optional[float]
    id: str
    position: XYPosition
    type: Optional[NodeType] # 节点类型，  如果定义了nodeTypes就必填, 否则报错
    data: Optional[Data]    # 传递给节点的任意数据。  如：{'label': '150'}
    sourcePosition: Optional[Position]
    targetPosition: Optional[Position]
    hidden: Optional[bool]    # 节点是否应在画布上可见。
    selected: Optional[bool]
    dragging: Optional[bool]  # 当前是否正在拖动节点。
    draggable: Optional[bool] # 节点是否可以拖动。
    selectable: Optional[bool]
    connectable: Optional[bool]
    deletable: Optional[bool]
    dragHandle: Optional[str] # 一个类名称，可以应用于节点内的元素，允许这些元素起作用 作为拖动手柄，允许用户通过单击并拖动这些元素来拖动节点。
    initialWidth: Optional[float]
    initialHeight: Optional[float]
    parentId: Optional[str]  # 父节点 ID，用于创建子流。
    zIndex: Optional[int]
    extent: Optional[Literal['parent'] | List[List[float]]]  # 可以移动节点的边界。    示例： 'parent'、 [[0, 0], [100, 100]]
    expandParent: Optional[bool]  # 如果将父节点拖动到 父节点的边界
    ariaLabel: Optional[str]
    origin: Optional[List[float]]  # 节点相对于其位置的原点。 示例： [0.5, 0.5] // centers the node、[0, 0] // top left、[1, 1] // bottom right
    handles: Optional[Optional[List[HandleType]]]
    measured: Optional[Measured]
    internals: InternalNodeInternals


class IsValidConnection:
    pass

class KeyCode:
    pass

MarkerType = Literal['arrow', 'arrowclosed']

class MiniMapNodeProps:
    id: str
    x: float
    y: float
    width: float
    height: float
    borderRadius: float
    className: str
    color: str
    shapeRendering: str
    strokeColor: str
    strokeWidth: float
    style: dict#[str, Any]
    selected: bool
    onClick: rx.EventHandler[lambda id: [id]]




class NodeChange:
    pass

class NodeConnection:
    source: str
    target: str
    sourceHandle: str | None = None
    targetHandle: str | None = None
    edgeId: str



class NodeMouseHandler:
    pass

NodeOrigin: List[float, float]


class NodeProps:    # 可能要加  (rx.Base)
    """
    Reflex 中 React Flow 节点组件的属性类型，完全对齐官方 NodeProps：
    https://reactflow.dev/api-reference/types/node-props
    """
    id: str  # 节点唯一 ID（官方：string，必传）
    data: Data  # 节点自定义数据（官方：NodeData，灵活结构）
    width: float  # 节点宽度（官方：number | undefined，自动计算或手动设置）
    height: float  # 节点高度（官方：number | undefined，自动计算或手动设置）
    source_position: Optional[Position] = None  # 源连接点位置（官方：Position | undefined，如 "right"）
    target_position: Optional[Position] = None  # 目标连接点位置（官方：Position | undefined，如 "left"）
    drag_handle: Optional[str] = None  # 拖拽手柄类名（官方：string | undefined，指定 CSS 类名的元素可拖拽）
    parentId: str   # 父节点 ID，用于创建子流。
    type: Optional[NodeType]  # 节点类型（对应 NodeTypes 中的键，官方：NodeType）    如果定义了nodeTypes就必填, 否则报错
    dragging: bool  # 是否正在拖拽（官方：boolean，框架自动更新）
    z_index: int  # 层级（官方：number，z-index，控制节点显示顺序）
    selectable: bool  # 是否可选中（官方：boolean，默认 true）
    deletable: bool  # 是否可删除（官方：boolean，默认 true）
    selected: bool  # 是否被选中（官方：boolean，框架自动更新）
    draggable: bool  # 是否可拖拽（官方：boolean，默认 true）
    is_connectable: bool  # 是否可连接（官方：boolean，受 connectable 配置影响）
    position_absolute_x: float  # 绝对位置X
    position_absolute_y: float  # 绝对位置Y

# 这里很重耶，且很可能有问题，Callable可能是别的
NodeTypes: Dict[str, Callable[[NodeProps], rx.Component]] # 详见上方NodeType注释 注！NodeTypes≠NodeType， 这里是存放供NodeType调用的Component

class NodeComponentType:
    pass


class OnBeforeDelete:
    pass

class OnConnect:
    pass

class OnConnectEnd:
    pass

class OnConnectStart:
    pass

class OnDelete:
    pass

class OnEdgesChange:
    pass

class OnEdgesDelete:
    pass

class OnError:
    pass

class OnInit:
    pass

class OnMove:
    pass

class OnNodeDrag:
    pass

class OnNodesChange:
    pass

class OnNodesDelete:
    pass

class OnReconnect:
    pass

class OnSelectionChangeFunc:
    pass

PanOnScrollMode = Literal['free', 'vertical', 'horizontal']


PanelPosition = Literal[
    'top-left',
    'top-center',
    'top-right',
    'bottom-left',
    'bottom-center',
    'bottom-right',
    'center-left',
    'center-right'
]



class ProOptions(TypedDict):
    account: str
    hideAttribution: bool

class ReactFlowInstance:
    pass

class Viewport(rx.BaseModel):
    """
    React Flow 视图窗口配置类，包含以下核心字段：
    - x: 水平偏移量（px）
    - y: 垂直偏移量（px）
    - zoom: 缩放比例（默认 1.0，建议范围 0.1~3.0）
    """
    # 必选：水平偏移量（正数向右，负数向左）
    x: float
    # 必选：垂直偏移量（正数向下，负数向上）
    y: float
    # 必选：缩放比例（默认值设为 1.0，符合 React Flow 初始缩放）
    zoom: float = 1.0

class ReactFlowJsonObject:
    nodes: Nodes
    edges: Edges
    viewport: Viewport

class Rect:
    width: float
    height: float
    x: float
    y: float

class ResizeParams:
    x: float
    y: float
    width: float
    height: float

class SelectionDragHandler:
    pass

SelectionMode = Literal['partial', 'full']

class SnapGrid:
    """
    SnapGrid 的分步长对象类型：横向（x）和纵向（y）步长可单独设置
    - x: 横向吸附步长（单位：px）
    - y: 纵向吸附步长（单位：px）
    """
    x: float  # 横向步长（必选，无默认值，需显式传入）
    y: float  # 纵向步长（必选，无默认值，需显式传入）












