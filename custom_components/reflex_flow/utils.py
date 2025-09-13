# 实用工具
import reflex as rx
from typing import Union, List, Dict
from typing_extensions import TypedDict  # 用于定义 TypeScript 兼容的类型
from flow import Flow
from .types import Connection

# region 下面是实用程序部分
#实用程序无需实例化create

# EdgeParams 类型：支持 Connection 或 Edge（对应文档的 EdgeType | Connection）
EdgeParams = Union[Connection, Flow.Edges]

class addEdge(rx.Component):
    """
    封装 React Flow 的 addEdge 实用程序的桥接组件
    return 添加了新边的数组

    使用示例
    # 实例化桥接组件：传递 Props（输入参数 + 结果回调）
        ReactFlowAddEdge(
            edges=FlowState.edges,  # 从状态中获取现有边列表（Simple Prop）
            new_edge_config=rx.watch(FlowState.new_edge),  # 监听新边配置（Simple Prop）
            on_updated_edges=FlowState.update_edges,  # 结果回调（更新状态，Event Handler）
        )
    """
    # --------------------------
    # 核心 Props 设计（匹配 addEdge() 输入参数）
    # --------------------------
    # 1. Simple Prop：当前边列表（对应 addEdge(edges) 参数）
    edges: rx.Var[List[Flow.Edges]] = rx.Var(
        default_value=[],
        mutable=True,  # 支持响应式更新（当 edges 变化时触发前端重新计算）
        description="当前 React Flow 的所有边列表"
    )

    # 2. Simple Prop：新边配置（对应 addEdge(edgeParams) 参数，支持 Connection/Edge）
    edge_params: rx.Var[EdgeParams] = rx.Var(
        default_value={},
        description="新边配置（支持 Connection 最小配置或完整 Edge 配置）"
    )

    # 3. Event Handler：传递 addEdge() 的返回结果（更新后的边列表）
    on_updated_edges: rx.EventHandler[lambda: [List[Flow.Edges]]] = rx.EventHandler(
        required=True,  # 必须绑定回调，否则无法接收结果
        description="接收 addEdge() 返回的更新后边列表"
    )

    # --------------------------
    # 前端配置（关联 react-flow 依赖和 JS 逻辑）
    # --------------------------
    # 组件对应的前端库：react-flow 的 addEdge 来自 @xyflow/react
    library = "@xyflow/react"
    # 自定义标签名（无实际 DOM 渲染，仅用于前端逻辑执行）
    tag = "ReactFlowAddEdge"

    # 步骤3：编写前端 JS 逻辑（精准调用 addEdge()）
    def _get_component(self) -> str:
        return f"""
            // 导入 react-flow 的 addEdge 工具函数（匹配官方文档的导入方式）
            import {{ addEdge }} from '{self.library}';
            import React from 'react';

            // 前端组件逻辑：接收 Reflex 传递的 Props，执行 addEdge 并回调结果
            const {self.tag} = ({{ edges, edge_params, on_updated_edges }}) => {{
                // 监听 edges 或 edge_params 变化：只要任一参数更新，就重新执行 addEdge
                React.useEffect(() => {{
                    // 1. 校验参数：确保 edge_params 包含 source 和 target（必选字段）
                    if (!edge_params?.source || !edge_params?.target) {{
                        console.warn("addEdge 缺少必选参数：source 或 target");
                        return;
                    }}

                    // 2. 调用 react-flow 官方 addEdge()（参数顺序严格匹配文档）
                    const updatedEdges = addEdge(edge_params, edges);

                    // 3. 通过 Event Handler 将结果传回 Reflex Python 层
                    on_updated_edges(updatedEdges);
                }}, [edges, edge_params, on_updated_edges]);  // 依赖变化触发重新执行

                // 工具类组件：无需渲染 DOM，返回 null
                return null;
            }};

            export default {self.tag};
            """

    # 步骤4：声明前端依赖（确保 Reflex 打包时引入 @xyflow/react）
    def _get_imports(self) -> Dict[str, str]:
        return {
            self.library: "import { addEdge } from '@xyflow/react'"
        }

# endregion
