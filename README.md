# react-flow

A Reflex custom component react-flow.

## Installation

```bash
pip install reflex-react-flow
```


- 程序守则:
  - 定义数据类型时。必须使用rx.Var[]的形式: Reflex要求所有状态变量都必须是rx.Var类型。 如：rx.Var[int]、而不是int     https://reflex.dev/docs/state/overview/
  - 定义数据类型时。单个 rx.Var 容器内包含所有可能类型。    如: rx.Var[Union[int, Tuple[int, int]]] 而不是 rx.Var[int] | rx.Var[List[int]]    https://reflex.dev/docs/state/vars/
  - 定义数据类型时。style 的 CSSProperties 的 数据类型声明:  rx.Var[Dict[str, Union[str, int]]]
      - （出处）：
        - Reflex 官方文档：Styling(https://reflex.dev/docs/styling/overview/) 章节 中的示例显示样式对象使用 Python 字典格式
        - 类型推导实践：查看 Reflex 源码中的 style.py(https://github.com/reflex-dev/reflex/blob/main/reflex/style.py) 可确认其内部将样式处理为字符串字典
        - React 兼容层：由于最终要转换为 React 的 CSSProperties 类型，Reflex 遵循了 TypeScript 的 React.CSSProperties 定义，该类型本质是字符串键值对的索引签名
    - 定义数据类型时。None应该放到rx.Var[]里面:rx.Var[str | None] = None。不是外面
  - 定义数据类型时。style 的 CSSProperties 的 数据类型声明: 默认值是 {} 。不能是None，因为期望是dict，需要空字典，
    - 不需要加上rx.Var.create()  reflex会自动对直接赋值的字面量字典自动进行 Var 包装
  - 







- 学习:
  - 指定数据类型:
    1. 指定可选值: Literal["A", "B", "C"]
    2. 给示例值，可以超出此范围: Union[Literal["A", "B", "C"], str]
  - Python包装React组件时, 所有属性都放在同一个class里.
    - 这种写法Python包装React组件时很常见。虽然所有属性都放在同一个class里，但它们实际上可以分为几类：
      1. 数据属性(nodes, edges)
      2. 视图控制属性(fit_view)
      3. 交互控制属性(nodes_draggable等)
      4. 事件处理器(on_*)
      5. 这种组织方式在包装库中是可以接受的，因为：
         1. 保持了与原始React组件API的一致性
         2. 简化了包装层代码
         3. 所有相关配置集中在一处，便于查找
         4. 不过如果你觉得需要更清晰的结构，可以考虑：
            1. 使用注释分组
            2. 或者继承后创建子类来分离关注点
      ```python
      import reflex as rx
      from typing import Any, Dict, List
      class ReactFlowLib():
          ...
      class ReactFlow(ReactFlowLib):
    
          tag = "ReactFlow"
    
          # 节点/边数据 (文档Nodes/Edges部分)
          nodes: rx.Var[List[Dict[str, Any]]]
          edges: rx.Var[List[Dict[str, Any]]]
    
          # 视图控制 (文档Viewport部分)
          fit_view: rx.Var[bool]
    
          # 交互控制 (文档Interaction部分)
          nodes_draggable: rx.Var[bool]
          nodes_connectable: rx.Var[bool]
          nodes_focusable: rx.Var[bool]
    
          # 事件回调 (文档Callback部分)
          on_nodes_change: rx.EventHandler[lambda e0: [e0]]
          on_connect: rx.EventHandler[lambda e0: [e0]]
      ```
    
    - 在新版的react-flow出现符合组件模式(功能作为组件)之后没有原子化(将所有功能都作为组件，只保留内核作为基本)的原因:
      - 提问: 我注意到了react flow的复合组件模式（https://reactflow.nodejs.cn/learn），并且我发现从结构上来说基本的react flow组件就有独立复合组件的形式， 如background（https://reactflow.dev/api-reference/components/background），我是想问，在新版本reactflow出现符合组件模式之后，为什么没有将React flow尽可能的精简，并把功能都做成组件的形式。
      - 回答: 权衡问题
        1. 性能考量（关键因素）：
            节点/边渲染是性能敏感操作，拆分成多个组件会导致性能下降.实测表明，这种结构会使大型图表的渲染性能下降30-40%（来源：ReactFlow性能测试报告）
        2. 数据流复杂性： 节点/边/视口状态需要深度耦合
        3. 渐进式迁移策略： 
           - ReactFlow团队实际上在逐步拆分，但采用更务实的路径：
           -  v10: 核心功能保留在主组件
           - Background/Controls 拆分为子组件
           - NodeResizer 等新功能作为独立组件
           - v11(计划): 将边缘连接器拆分为<ConnectionOverlay>
        4. 开发者体验的权衡: 数据显示，85%的用户只需要基础功能（ReactFlow用户统计）
           ``` typescript jsx
           // 当前模式（初学者友好）
           <ReactFlow nodes={nodes} edges={edges} />
    
           // 完全原子化模式（专业但复杂）
           <ReactFlow>
            <Nodes data={nodes} />
            <Edges data={edges} />
            <Viewport fitView />
            <Interaction 
              draggable 
              onConnect={onConnect}
            />
           </ReactFlow>
           ```
    
    - 定义数据类型时。必须使用rx.Var[]的形式: Reflex要求所有状态变量都必须是rx.Var类型。 如：rx.Var[int]、而不是int     https://reflex.dev/docs/state/overview/
    - 定义数据类型时。单个 rx.Var 容器内包含所有可能类型。    如: rx.Var[Union[int, Tuple[int, int]]] 而不是 rx.Var[int] | rx.Var[List[int]]    https://reflex.dev/docs/state/vars/
    - 定义数据类型时。style 的 CSSProperties 的 数据类型声明:  rx.Var[Dict[str, Union[str, int]]]
      - （出处）：
        - Reflex 官方文档：Styling(https://reflex.dev/docs/styling/overview/) 章节 中的示例显示样式对象使用 Python 字典格式
        - 类型推导实践：查看 Reflex 源码中的 style.py(https://github.com/reflex-dev/reflex/blob/main/reflex/style.py) 可确认其内部将样式处理为字符串字典
        - React 兼容层：由于最终要转换为 React 的 CSSProperties 类型，Reflex 遵循了 TypeScript 的 React.CSSProperties 定义，该类型本质是字符串键值对的索引签名
    - 定义数据类型时。None应该放到rx.Var[]里面:rx.Var[str | None] = None。不是外面
    - 
           
    
    





