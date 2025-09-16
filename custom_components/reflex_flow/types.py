# 类型 https://reactflow.dev/api-reference/types
'''
添加指南：
    变量示例：
    handles?: NodeHandle[];
        handles - 属性名称
        ? - 表示这个属性是可选的（optional）
        NodeHandle - 数组中元素的类型
        [] - 表示这是一个数组类型 用列表包裹   List[handles]

    - unknown在JS里是未知类型，不是None。      js里的None是 null 和 【不完全对应】undefined
    JS示例：
        EdgeData extends Record<string, unknown> = Record<string, unknown>,
    转换为：
        EdgeData = dict[str, Any]

    - domAttributes:
    JS文档：   本质是str， 后面的是不可以的值。
        Omit<SVGAttributes<SVGGElement>, "id" | "style" | "className" | "role" | "aria-label" | "dangerouslySetInnerHTML">
        用于向边缘的 DOM 元素添加自定义属性的常规逃生舱口。
    转换为:
        Optional[Dict[str, Any]] # SVG Dict[str, Any]  不可选内容： 'id' | 'style' | 'className' | 'role' | 'aria-label' | 'dangerouslySetInnerHTML'

    - JS示例：
        ?: [number, number]
    转换为：
        Optional[List[float]]

    - 对于 on_  这类事件处理器的数据类型，     所有返回是Returns:   Type: void 这样的也都是事件处理器类型
        都是 rx.EventHandler[lambda e0: [e0]] 的形式
        根据文档可以判读出这个数据类型接收几个参数，不用向以前那样猜

    -

未解决的问题：
    1. 对于文档中的   XXX？   	string | null   这一类     对应的JS是   XXX?: string | null;
        不知道如何其完美嵌入，
        该写成 Optional[XXX] 呢？ 还是 Optional[XXX] = None 呢
        毕竟 XXX后面的？代表可选，也就是 Optional[] ，也就是等于 XXX | None
    2. ReactNode
        https://github.com/DefinitelyTyped/DefinitelyTyped/blob/946e2f414c7016bbe426ecba89d823c9a86be017/types/react/index.d.ts#L427
    3.
'''
import reflex as rx
from typing import Any, Dict, List, Union, Literal, TypedDict, Tuple, Callable, Iterable, TypeVar, Generic, Optional, Type
from enum import Enum
import math
#【很可能错误】from jinja2.nodes import Literal
from reflex.components.el.elements.base import AriaRole, AutoCapitalize, ContentEditable, EnterKeyHint, InputMode
from reflex.components.component import Component


# 有些class在react文档中的数据类型声明靠后的，但是前面有需要要调用靠后面的: 还是调整顺序，优先于python调用吧，不遵从文档了
# reflex包裹react的数据类型不是都要定义为类
# 需要定义为响应式状态变量需要用 rx.Var[] 包裹

# region 主要类型使用的类型，但不在文档里的（包含: 嵌套对象和类型别名化）

### 对CSSType的说明:
# 这个是我自己定义的，代表所有的CSS的类型，JS里是 CSSProperties。
# reflex里好像有CSS专用的，很可能就是这个 rx.style.Style，
# 总之先隔离出来，统一管理使用
###
CSSType = rx.style.Style

### 对AriaRole的说明:
# 这个是我自己定义的，同CSSProperties都是来自react的类型
# reflex里好像有AriaRole专用的, 很可能就是这个 from reflex.components.el.elements.base import AriaRole
###
AriaRole = AriaRole

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

NodeId = str
EdgeId = str

EdgeChangeType = Literal['add', 'update', 'remove']

# region padding部分
###
#来源：https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/general.ts#L150
#使用示例1：
#    PaddingConfig(
#        x=20,        # 左右各 20px
#        top="10px",  # 上 10px
#        bottom=10    # 下 10px（默认 px）
#    )
#使用示例2：
#    padding=20
#使用示例3：
#    padding="15%"
###
# PaddingUnit = Literal['px', '%']  在python里没有程序意义，但js有，所以统一规范应写在这里。 用来声明下面的PaddingWithUnit是字符串时，组合必须是（数字+px或%）的形式
PaddingWithUnit = Union[int, float, str]    # 字符串时，组合必须是（数字+px或%）的形式    示例：15px、10%
class PaddingConfig:
    """
    padding 精细配置对象：支持按方向（上下左右）或轴（水平x/垂直y）设置
    优先级：具体方向（top/right等）> 轴（x/y）
    """
    # 方向配置（可选）
    top: Optional[PaddingWithUnit]    # 上 padding
    right: Optional[PaddingWithUnit]  # 右 padding
    bottom: Optional[PaddingWithUnit] # 下 padding
    left: Optional[PaddingWithUnit]   # 左 padding
    # 轴配置（可选，x=左右，y=上下）
    x: Optional[PaddingWithUnit]      # 水平轴统一 padding
    y: Optional[PaddingWithUnit]      # 垂直轴统一 padding
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
NodeType = Union[str, None, Literal["default", "input", "output", "group"]] # 可选内容出处: https://reactflow.dev/api-reference/types/node#default-node-types
# EdgeType与上面的NodeType同理： EdgeType extends string | undefined = string | undefined  出处：https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/react/src/types/edges.ts#L55
EdgeType = Union[str, None, Literal["default", "straight", "step", "smoothstep", "simplebezier"]] # 可选内容出处：https://reactflow.dev/api-reference/types/node#default-node-types

NodeData = dict[str, Any] #（对应 TS 的 Record<string, unknown>） 出处： NodeData extends Record<string, unknown> = Record<string, unknown>, https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/nodes.ts#L12C3-L12C70
EdgeData = dict[str, Any] #（对应 TS 的 Record<string, unknown>） 出处： EdgeData extends Record<string, unknown> = Record<string, unknown>, https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/edges.ts#L4

class Measured(TypedDict):
    width: Optional[float]
    height: Optional[float]

class Dimensions:   # https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/utils.ts#L34
  width: float
  height: float

###
# ReactNode 类型：包含基础类型 + Reflex 组件 + 可迭代的 ReactNode（如列表）
# https://github.com/DefinitelyTyped/DefinitelyTyped/blob/6b9db9cb6de7119fa63ab3ce81c8544b40af04ed/types/react/index.d.ts#L427
# 说是支持react的所有类型，这个有点迷惑，不知道对不对【以后再说】
# 不用Any：ReactNode 的本质是 “有限范围的可渲染内容集合”，而非 “任意值”
# JS代码：/**
#      * Represents all of the things React can render.
#      *
#      * Where {@link ReactElement} only represents JSX, `ReactNode` represents everything that can be rendered.
#      *
#      * @see {@link https://react-typescript-cheatsheet.netlify.app/docs/react-types/reactnode/ React TypeScript Cheatsheet}
#      *
#      * @example
#      *
#      * ```tsx
#      * // Typing children
#      * type Props = { children: ReactNode }
#      *
#      * const Component = ({ children }: Props) => <div>{children}</div>
#      *
#      * <Component>hello</Component>
#      * ```
#      *
#      * @example
#      *
#      * ```tsx
#      * // Typing a custom element
#      * type Props = { customElement: ReactNode }
#      *
#      * const Component = ({ customElement }: Props) => <div>{customElement}</div>
#      *
#      * <Component customElement={<div>hello</div>} />
#      * ```
#      */
#     // non-thenables need to be kept in sync with AwaitedReactNode
#     type ReactNode =
#         | ReactElement
#         | string
#         | number
#         | bigint
#         | Iterable<ReactNode>
#         | ReactPortal
#         | boolean
#         | null
#         | undefined
#         | DO_NOT_USE_OR_YOU_WILL_BE_FIRED_EXPERIMENTAL_REACT_NODES[
#             keyof DO_NOT_USE_OR_YOU_WILL_BE_FIRED_EXPERIMENTAL_REACT_NODES
#         ]
#         | Promise<AwaitedReactNode>;
###
# 基础可渲染类型：字符串、数字、布尔值、None（对应 JS 的 null/undefined）
ReactNode = Union[
    str, int, float, bool, None,    # 常规类型
    Component,  # Reflex 组件（对应 JS 的 ReactElement 和 ReactPortal（对应 Reflex 中的：rx.portal 组件(来源： from reflex.components.el.elements.media import portal)））
    Iterable["ReactNode"],  # 可迭代的 ReactNode（如列表、生成器）
    rx.Var["ReactNode"]  # 支持 Reflex 的响应式变量（对应同步的Promise<AwaitedReactNode> ，异步的就是对此的应用来实现）
]

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
    connection_line_style: CSSType  # 对应CSSProperties
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

class ConnectionLineComponent:  # 【以后在做】https://reactflow.dev/api-reference/types/connection-line-component
    def __call__(self, props: ConnectionLineComponentProps) -> rx.Component:
        """
        React Flow 连接线条组件的类型协议
        :param props: 组件的入参属性，必须符合 ConnectionLineComponentProps 结构
        :return: Reflex 组件实例（对应 React 组件）
        """
        rx.text('【未完成】数据类型ConnectionLineComponent，应该返回ConnectionLineComponentProps')

ConnectionLineType = Literal['default', 'straight', 'step', 'smoothstep', 'simplebezier']

ConnectionMode = Literal['strict', 'loose']

class ConnectionState:
    pass

# region CoordinateExtent的前置类型声明
###
# 已解决问题: 不知道math的无穷能不能作为pydantic的数据类型声明 -> 不能，但是这里的写法没问题，float('inf'), float('-inf') 可以，他们是属于float之内的
#JS代码: export type CoordinateExtent = [[number, number], [number, number]];
# * 坐标范围表示坐标系中的两个点：一个在顶部
# *左角和右下角各一个。它用于表示
# *流中节点的边界或视口的边界。
# @备注期望“CoordinateExtent”的属性通常默认为`[[-∞，-∞]，[+∞，+∞]]`*表示无限范围。
#
#示例输入：[[-math.inf, -math.inf], [math.inf, math.inf]]
###
CoordinatePoint = Union[    # 单个坐标点 [x, y]
    List[float],  # 列表形式：[x, y]
    Tuple[float, float]  # 元组形式：(x, y)
]
# 坐标范围 [[min_x, min_y], [max_x, max_y]]
# endregion
CoordinateExtent = Union[
    List[CoordinatePoint],  # 列表嵌套：[[x1, y1], [x2, y2]]
    Tuple[CoordinatePoint, CoordinatePoint]  # 元组嵌套：([x1, y1], [x2, y2])
]




MarkerType = Literal["arrow", "arrowclosed"] # EdgeMarker的前置类型声明 出处：export enum MarkerType {Arrow = 'arrow', ArrowClosed = 'arrowclosed'}   https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/edges.ts#L110
class EdgeMarker(TypedDict):
    type: Literal[MarkerType, "arrow", "arrowclosed"]  # 出处：  type: MarkerType | `${MarkerType}`;    后面的`${MarkerType}`是说在JS里用字符串的方式传入MarkerType，这里都统一为字符串了。
    color: Optional[str] = None
    width: Optional[float]
    height: Optional[float]
    markerUnits: Optional[str]
    orient: Optional[str]
    strokeWidth: Optional[float]    # strokeWidth: 笔划宽度

class DefaultEdgeOptions(TypedDict):
    '''
    https://www.typescriptlang.org/docs/handbook/utility-types.html#recordkeys-type
    :param 文档：string | undefined   edgeTypes 中定义的边类型。
    :param label
    :param domAttributes # SVG Dict[str, Any]  不可选内容： "id" | "style" | "className" | "role" | "aria-label" | "dangerouslySetInnerHTML"
    '''
    type: Optional[EdgeType]
    animated: Optional[bool]
    hidden: Optional[bool]
    deletable: Optional[bool]
    selectable: Optional[bool]
    data: Optional[dict[str, str]] = None  # 传递到边缘的任意数据。
    markerStart: Optional[EdgeMarker]  # 将标记设置在边的开头。
    markerEnd: Optional[EdgeMarker]  # 将标记设置在边的末端。
    zIndex: Optional[int]
    ariaLabel: Optional[str]
    interactionWidth: Optional[int]  # ReactFlow 在每个边缘周围渲染一条不可见的路径，使它们更容易单击或点击。 此属性设置该不可见路径的宽度。
    label: Optional[ReactNode]   # 看起来现在是正确的，也可能是引用下面那个Nodes #【以后在做】ReactNode是什么？https://github.com/DefinitelyTyped/DefinitelyTyped/blob/946e2f414c7016bbe426ecba89d823c9a86be017/types/react/index.d.ts#L427 # 要沿边缘渲染的标签或自定义元素。这通常是文本标签或一些 自定义控件。
    labelStyle: Optional[CSSType]  # 要应用于标签的自定义样式。
    labelShowBg: Optional[bool]
    labelBgStyle: Optional[CSSType]
    labelBgPadding: Optional[List[int]]
    labelBgBorderRadius: Optional[int]
    style: CSSType  # 【以后再做】
    className: str
    reconnectable: Union[str, HandleType]  # 【以后再做】     # 确定是否可以通过将源或目标拖动到新节点来更新边。 此属性将覆盖组件上 prop 设置的默认值。edgesReconnectable<ReactFlow />
    focusable: bool
    ariaRole: AriaRole = "group"  # 边缘的 ARIA 角色属性，用于辅助功能。
    domAttributes: Optional[Dict[str, Any]] # SVG Dict[str, Any]  不可选内容： "id" | "style" | "className" | "role" | "aria-label" | "dangerouslySetInnerHTML"

class DeleteElements:
    pass


EdgeMarkerType = Union[str, EdgeMarker]  # Edges的前置类型声明  出处：export type EdgeMarkerType = string | EdgeMarker; https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/system/src/types/edges.ts#L102
class Edges:
    '''
    出处：https://github.com/xyflow/xyflow/blob/main/packages/system/src/types/edges.ts#L3
    :param domAttributes SVC   不可选内容： 'id' | 'style' | 'className' | 'role' | 'aria-label' | 'dangerouslySetInnerHTML'
    '''
    # region 下面是TypedDict 定义，规定数据形式.
    # endregion

    id: str # 边缘的唯一id
    type: Optional[EdgeType] # 在`edgeTypes中定义的边缘类型`
    source: str # 源节点的Id
    target: str # 目标节点的Id
    sourceHandle: Optional[str] = None # 源句柄的Id，仅当每个节点有多个句柄时才需要。
    targetHandle: Optional[str] = None # 目标句柄的Id，仅当每个节点有多个句柄时才需要。
    animated: Optional[bool]
    hidden: Optional[bool]
    deletable: Optional[bool]
    selectable: Optional[bool]
    data: Optional[EdgeData]   # 【以后在做】
    selected: Optional[bool]
    markerStart: Optional[EdgeMarkerType] # 将标记设置在边的开头。 在边的起点设置标记。  可选值：'arrow'或 'arrowclosed'
    markerEnd: Optional[EdgeMarkerType]   # 将标记设置在边的末端。 在边的终点设置标记。  可选值：'arrow'或 'arrowclosed'
    zIndex: Optional[int]
    ariaLabel: Optional[str]
    interactionWidth: Optional[int]   # ReactFlow 在每条边周围渲染一条不可见的路径，以便于单击或点击它们。此属性设置该不可见路径的宽度。
    label: Optional[ReactNode]  # 【以后在做】
    labelStyle: Optional[CSSType] # CSS
    labelShowBg: Optional[bool]
    labelBgStyle: Optional[CSSType] # CSS
    labelBgPadding: Optional[List[float]]
    labelBgBorderRadius: Optional[float]
    style: Optional[CSSType] # CSS
    className: Optional[str]
    reconnectable: Optional[Union[bool | HandleType]] # 确定是否可以通过将源或目标拖动到新节点来更新边。 此属性将覆盖组件上 prop 设置的默认值。edgesReconnectable<ReactFlow />
    focusable: Optional[bool]
    ariaRole: Optional[AriaRole] = "group" # AriaRole  边缘的 ARIA 角色属性，用于辅助功能。
    domAttributes: Optional[Dict[str, Any]] # SVG Dict[str, Any]  不可选内容： 'id' | 'style' | 'className' | 'role' | 'aria-label' | 'dangerouslySetInnerHTML'
# region Edge附加部分
class SmoothStepPathOptions:    # SmoothStepEdge的前置部分
  offset: Optional[float]
  borderRadius: Optional[float]
  stepPosition: Optional[float]
class SmoothStepEdge(Edges):
    """平滑阶梯边（type: "smoothstep"），含专属路径配置"""
    type: Literal["smoothstep"] = "smoothstep"
    pathOptions: Optional[SmoothStepPathOptions] = SmoothStepPathOptions() # 平滑阶梯配置

class BezierPathOptions:    # BezierEdge的前置部分
    curvature: Optional[float]  # curvature曲率
class BezierEdge(Edges):
    """贝塞尔边（type: "default"），含专属路径配置"""
    type: Literal["default"] = "default"  # 固定类型标识，与前端一致
    pathOptions: Optional[BezierPathOptions] = BezierPathOptions() # 贝塞尔路径配置

class StepPathOptions:  # StepEdge的前置部分
    offset: Optional[float]
class StepEdge(Edges):
    """阶梯边（type: "step"），含专属路径配置"""
    type: Literal["step"] = "step"
    pathOptions: Optional[StepPathOptions] = StepPathOptions() # 阶梯路径配置

class StraightEdge(Edges):
    """直线边（type: "straight"），无额外路径配置"""
    type: Literal["straight"] = "straight"
# endregion



# region EdgeChange前置部分
class EdgeAddChange:
    """边新增操作的变更类型"""
    item: EdgeType  # 新增的边对象
    type: Literal["add"]  # 固定类型标识, 可选值： "add"
    index: Optional[int]  # 新增边在数组中的位置（可选）
class EdgeRemoveChange:
    """边删除操作的变更类型"""
    id: str  # 被删除边的 ID
    type: Literal["remove"]  # 固定类型标识   可选值： "remove"
class EdgeReplaceChange:
    """边替换操作的变更类型"""
    id: str  # 被替换边的 ID
    item: EdgeType  # 用于替换的新边对象
    type: Literal["replace"]  # 固定类型标识  可选值: "replace"
class EdgeSelectionChange:
    """边选中状态变更的类型"""
    id: str  # 状态变更的边 ID
    type: Literal["select"] # 固定类型标识    可选值: "select"
    selected: bool  # 新的选中状态（True/False）
# endregion
EdgeChange = Union[
    EdgeAddChange,
    EdgeRemoveChange,
    EdgeReplaceChange,
    EdgeSelectionChange
]

class EdgeMouseHandler:
    pass

class EdgeProps:
    # 新增两个字段（JS 中添加的 data: any 和 type: any）
    # 增加字段的原因：  https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/react/src/types/general.ts#L79
    #   源自：export type EdgeTypes = Record<
    #   string,
    #   ComponentType<
    #     EdgeProps & {
    #       // eslint-disable-next-line @typescript-eslint/no-explicit-any
    #       data: any;
    #       // eslint-disable-next-line @typescript-eslint/no-explicit-any
    #       type: any;
    #     }
    #   >
    #   >;
    data: Any  # 对应 JS 的 data: any（任意类型的自定义数据）
    type: Any  # 对应 JS 的 type: any（任意类型的边类型标识）

###
# https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/react/src/types/general.ts#L76
# 详见上方EdgeType注释 注！EdgeTypes≠EdgeType， 这里是存放供EdgeType调用的Component
# JS代码：export type EdgeTypes = Record<
#   string,
#   ComponentType<
#     EdgeProps & {
#       // eslint-disable-next-line @typescript-eslint/no-explicit-any
#       data: any;
#       // eslint-disable-next-line @typescript-eslint/no-explicit-any
#       type: any;
#     }
#   >
# >;
# 「字符串→组件类」的映射
# 用Type包裹Component的原因: Type[Component] 表示 “组件类本身”    正好对应 JS 中 React.ComponentType 的语义 —— 它描述的是 “组件类 / 函数” 本身，而非组件实例。
# 新代码增加的两个参数增加到了EdgeProps里
# 需要导入 from reflex.components.component import Component
###
EdgeTypes = Dict[str, Type[Component]]


class Handle:
    id: Optional[str] = None
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
    handle_bounds: Optional[NodeHandleBounds]  # 对应前端 handleBounds

    # 节点整体边界信息（可选）
    bounds: Optional[NodeBounds]  # 对应前端 bounds

class NodeHandle:
    width: Optional[float]
    height: Optional[float]
    id: Optional[str] = None
    x: float
    y: float
    position: Position
    type: HandleType

NodeOrigin = Union[List[float], Tuple[float, float]] # 节点相对于其位置的原点。 取值范围: 0~1 示例： [0, 0]、 [0.5, 0.5]、 [1, 1]      [0, 0]左上↖、[0.5, 0.5]中央·、[1, 1]右下↘       也可以传入元组

class Nodes(TypedDict):
    '''
    # JS源码参数带问号?的是可选参数的意思，用Optional[]包裹，等同于 X | None = None
    # region 下面是TypedDict 定义，规定数据形式.
    :param type: Optional[NodeType] # 节点类型，  如果定义了nodeTypes就必填, 否则报错
    :param domAttributes: Optional[Dict[str, Any]] # SVG Dict[str, Any]  不可选内容："id" | "draggable" | "style" | "className" | "role" | "aria-label" | "defaultValue" | keyof DOMAttributes<HTMLDivElement>>
    '''

    id: str # 节点的唯一 ID。
    position: XYPosition  # 节点在窗格上的位置。 如：{'x': 0, 'y': 0}
    data: NodeData    # 传递给节点的任意数据。  如：{'label': '150'}
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
    extent: Optional[Union[Literal['parent'], CoordinateExtent]] = None   # 可以移动节点的边界。    示例： 'parent'、 [[0, 0], [100, 100]]
    expandParent: Optional[bool]  # 如果将父节点拖动到 父节点的边界
    ariaLabel: Optional[str]
    origin: Optional[NodeOrigin]  # 节点相对于其位置的原点。 示例： [0.5, 0.5] // centers the node、[0, 0] // top left、[1, 1] // bottom right
    handles: Optional[List[NodeHandle]]
    measured: Optional[Measured]
    type: Optional[NodeType] # 节点类型，  如果定义了nodeTypes就必填, 否则报错        也可以自定义节点(https://reactflow.dev/learn/customization/custom-nodes)
    style: Optional[CSSType]
    className: Optional[str]
    resizing: Optional[bool]
    focusable: Optional[bool]
    ariaRole: Optional[AriaRole] # AriaRole  边缘的 ARIA 角色属性，用于辅助功能。
    domAttributes: Optional[Dict[str, Any]] # SVG Dict[str, Any]  不可选内容："id" | "draggable" | "style" | "className" | "role" | "aria-label" | "defaultValue" | keyof DOMAttributes<HTMLDivElement>>

class FitViewOptions:
    '''
    :param nodes    如果填写，则传入的Nodes必须包含id字段。 示例： Nodes(id="node1")
    nodes:  nodes	(NodeType | { id: string; })[]
    '''

    class MinimalNode(TypedDict):   # 代表Nodes在字段nodes里的最小表示
        id: str  # 明确声明 id 为必填字段
    padding: Optional[Padding]
    includeHiddenNodes: Optional[bool]
    minZoom: Optional[float]
    maxZoom: Optional[float]
    duration: Optional[float]
    ease: Optional[str] = '(t: number) => ((t *= 2) <= 1 ? t * t * t : (t -= 2) * t * t + 2) / 2;'    # 【以后再做】【可能有问题】接收一个输出0~1float的def，用于显示动画. AI说可以转换成JS的函数，但感觉有点悬，所以先用react提供的JS字符串吧,这里是先加速后减速的缓动函数
    interpolate: Optional[Literal["smooth", "linear"]]
    nodes: Optional[List[Union[Nodes, MinimalNode]]]    # 当使用这个参数时，Nodes中的id必填。 https://reactflow.dev/api-reference/types/fit-view-options#nodes

class HandleConnection:
    # https://reactflow.dev/api-reference/types/handle-connection
    source: str # 此连接起点的节点的id。
    target: str # 此连接终点的节点的id。
    sourceHandle: str | None = None # 当不为null时，表示此连接源自的源节点上的句柄的id。
    targetHandle: str | None = None # 当不为null时，此连接终止于的目标节点上的句柄的id。
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


IsValidConnection = Union[Connection, Edges] # rx.EventHandler[lambda edge: [edge]]    # 【以后再说】 这个有点不太一样，好像不是事件处理器, 腺癌时合理的但还没有测试

KeyCode = Union[str, List[str]]

MarkerType = Literal['arrow', 'arrowclosed']

class MiniMapNodeProps:
    id: str
    x: float
    y: float
    width: float
    height: float
    borderRadius: float
    className: str
    color: Optional[str]
    shapeRendering: str
    strokeColor: Optional[str]
    strokeWidth: Optional[float]
    style: Optional[CSSType]
    selected: bool
    onClick: Optional[rx.EventHandler] # 【以后再做】可能有两个返回值，还没测试过，但为了不报错先取消返回值 onClick?: (event: MouseEvent, id: string) => void;  https://github.com/xyflow/xyflow/blob/487b13c9ad8903789f56c6fcfd8222f9cb74b812/packages/react/src/additional-components/MiniMap/types.ts#L74



# region NodeChange前置部分
class NodeDimensionChange:
    id: str
    type: Literal['dimensions']
    dimensions: Optional[Dimensions]
    resizing: Optional[bool]    # 如果这是True，则节点当前正在通过NodeResizer调整大小
    setAttributes: Optional[Union[bool, "width", "height"]]   # 如果这是True，我们将设置节点的宽度和高度，而不仅仅是测量的尺寸
class NodePositionChange:
    id: str
    type: Literal['position']
    position: Optional[XYPosition]
    positionAbsolute: Optional[XYPosition]
    dragging: Optional[bool]
class NodeSelectionChange:
    id: str
    type: Literal['select']
    selected: bool
class NodeRemoveChange:
    id: str
    type: Literal['remove']
class NodeAddChange:
    item: NodeType
    type: Literal['add']
    index: Optional[int]
class NodeReplaceChange:
    id: str
    item: NodeType
    type: Literal['replace']
# endregion
NodeChange: Union[
        NodeDimensionChange,
        NodePositionChange,
        NodeSelectionChange,
        NodeRemoveChange,
        NodeAddChange,
        NodeReplaceChange
    ]

class NodeConnection:
    source: str
    target: str
    sourceHandle: Literal[str, None] = None
    targetHandle: Literal[str, None] = None
    edgeId: str

class NodeMouseHandler:
    pass

class NodeProps:    # 可能要加  (rx.Base)       【以后再做】【很可能没做完】现有的参数都没问题，但看说明是要与自定组件联合使用，这部分没做
    """
    Reflex 中 React Flow 节点组件的属性类型，完全对齐官方 NodeProps：
    https://reactflow.dev/api-reference/types/node-props
    """
    id: str  # 节点唯一 ID（官方：string，必传）
    data: Data  # 节点自定义数据（官方：NodeData，灵活结构）
    width: Optional[float]  # 节点宽度（官方：number | undefined，自动计算或手动设置）
    height: Optional[float]  # 节点高度（官方：number | undefined，自动计算或手动设置）
    source_position: Optional[Position] = None  # 源连接点位置（官方：Position | undefined，如 "right"）
    target_position: Optional[Position] = None  # 目标连接点位置（官方：Position | undefined，如 "left"）
    drag_handle: Optional[str] = None  # 拖拽手柄类名（官方：string | undefined，指定 CSS 类名的元素可拖拽）
    parentId: Optional[str]   # 父节点 ID，用于创建子流。
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

###
# https://github.com/xyflow/xyflow/blob/88cf48289333903ac0f41c6afc12b51ca261e208/packages/react/src/types/general.ts#L76
# 详见上方NodeType注释 注！NodTypes≠NodType， 这里是存放供NodType调用的Component
# JS代码：export type EdgeTypes = Record<
#   string,
#   ComponentType<
#     EdgeProps & {
#       // eslint-disable-next-line @typescript-eslint/no-explicit-any
#       data: any;
#       // eslint-disable-next-line @typescript-eslint/no-explicit-any
#       type: any;
#     }
#   >
# >;
# 「字符串→组件类」的映射
# 用Type包裹Component的原因: Type[Component] 表示 “组件类本身”    正好对应 JS 中 React.ComponentType 的语义 —— 它描述的是 “组件类 / 函数” 本身，而非组件实例。
# 新代码增加的两个参数增加到了NodeProps里
# 需要导入 from reflex.components.component import Component
###
NodeTypes = Dict[str, Type[Component]] # 详见上方NodeType注释 注！NodeTypes≠NodeType， 这里是存放供NodeType调用的Component

OnBeforeDelete: rx.EventHandler[lambda __0: [__0]]  # 【以后再说】这个好像不太一样    # https://reactflow.dev/api-reference/types/on-before-delete

OnConnect = rx.EventHandler[lambda connection: [connection]]  # 接收一个参数  connection  当连接线完成并且用户连接了两个节点时，此事件将随新连接一起触发。 您可以使用该实用程序将连接转换为完整的边。addEdge  包含返回值dict: {'source': '4', 'sourceHandle': None, 'target': '5', 'targetHandle': None}

OnConnectEnd = rx.EventHandler[lambda event, connectionState: [event, connectionState]]    # 接收两个参数 event connectionState 无论是否可以建立有效连接，此回调都会触发。您可以 使用第二个参数在连接时具有不同的行为 不成功。connectionState  注意: 引出连接线后，不论有没有连接上，只要松开线消失都会触发。  包含两个参数(dict, dict): 值={'isTrusted': True}  (很长)值={'isValid': False, 'from': {'x': 124.99982508047702, 'y': 163.9999125402385}, 'fromHandle': {'id': None, 'type': 'source'': '2', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}, 'fromPosition': 'bottom', 'fromNode': {'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 50, 'y': 125}, 'measured': {'width': 150, 'height': 40}, 'internals': {'positionAbsolute':          {'x': 50, 'y': 125}, 'handleBounds': {'source': [{'id': None, 'type': 'source', 'nodeId': '2', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}], 'target': [{'id': None, 'type': 'target', 'nodeId': '2', 'position': 'top', 'x': 71.99982508047702, 'y': -1.999994525565665, 'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '2', 'type': 'default', 'data': {'label': '25'}, 'position': {'x': 50, 'y': 125}}}}, 'to': {'x': 416, 'y': 220}, 'toHandle': {'id': None, 'type': 'source', 'nodeId': '4', 'position': 'bottom', 'x': 424.999825080477, 'y': 188.9999125402385, 'width': 6, 'height': 6}, 'toPosition': 'top', 'toNode': {'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}, 'measured': {'width': 150, 'height': 40}, 'internals': {'positionAbsolute': {'x': 350, 'y': 150}, 'handleBounds': {'source': [{'id': None, 'type': 'source', 'nodeId': '4', 'position': 'bottom', 'x': 71.99982508047702, 'y': 35.99991254023851, 'width': 6, 'height': 6}], 'target': [{'id': None, 'type': 'target', 'nodeId': '4', 'position': 'top', 'x': 71.99982508047702, 'y': -1.999994525565665, 'width': 6, 'height': 6}]}, 'z': 0, 'userNode': {'id': '4', 'type': 'default', 'data': {'label': '5'}, 'position': {'x': 350, 'y': 150}}}}}

OnConnectStart = rx.EventHandler[lambda event, params: [event, params]]  #  接收两个参数 event params        (dict, dict): 值={'isTrusted': True}   值={'nodeId': '4', 'handleId': None, 'handleType': 'source'}

OnDelete = rx.EventHandler[lambda params: [params]]  # 接收一个参数   params	{ nodes: NodeType[]; edges: EdgeType[]; }

OnEdgesChange = rx.EventHandler[lambda changes: [changes]]    # 接收一个参数 changes	EdgeChange<EdgeType>[]

OnEdgesDelete = rx.EventHandler[lambda edges: [edges]]    # 接收一个参数 edges	EdgeType[]

OnError = rx.EventHandler[lambda id, message: [id, message]]  # 接收两个参数    id	string	message	string

OnInit = rx.EventHandler[lambda reactFlowInstance: [reactFlowInstance]]   # 接收一个参数 reactFlowInstance	ReactFlowInstance<NodeType, EdgeType>

OnMove = rx.EventHandler[lambda event, viewport: [event, viewport]]   # 接收两个参数  event	MouseEvent | TouchEvent	    viewport	Viewport

OnNodeDrag = rx.EventHandler[lambda event, node, nodes: [event, node, nodes]]   # 接收三个参数

OnNodesChange = rx.EventHandler[lambda changes: [changes]]  # 接收一个参数    changes	NodeChange<NodeType>[]

OnNodesDelete = rx.EventHandler[lambda nodes: [nodes]]  # 接收一个参数  nodes	NodeType[]

OnReconnect = rx.EventHandler[lambda oldEdge, newConnection: [oldEdge, newConnection]]  # 接收两个参数

OnSelectionChangeFunc = rx.EventHandler[lambda params: [params]]    # 接收一个参数    params	OnSelectionChangeParams<NodeType, EdgeType>

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
    account: Optional[str]
    hideAttribution: bool

class ReactFlowInstance:
    pass
    #getNodes
    #setNodes
    #addNodes
    #getNode
    #getInternalNode
    #getEdges
    #setEdges
    #addEdges
    #getEdge
    #toObject
    #deleteElements
    #updateNode
    #updateNodeData
    #updateEdge
    #updateEdgeData
    #getNodesBounds
    #getHandleConnections
    #getNodeConnections

class Viewport:
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
    zoom: float = 1.0   # 虽然文档没有默认值，但还是1.0规范一下。

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

SelectionDragHandler = rx.EventHandler[lambda event, nodes: [event, nodes]] # # 接收两个参数


SelectionMode = Literal['partial', 'full']

SnapGrid = Union[
    List[float],  # 列表形式：[x, y]
    Tuple[float, float]  # 元组形式：(x, y)
]  # 长度为2的列表 type SnapGrid = [number, number];  SnapGrid 类型定义窗格上捕捉节点的网格大小。它与 snapToGrid 属性结合使用以启用网格捕捉功能。












