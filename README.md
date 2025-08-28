# flow
# developing...Look forward to v1.0
# 仍在开发中，尽情期待1.0版本
A Reflex custom component flow.

## Installation

```bash
pip install reflex-flow
```

Yes, I referred to the example of wrapping React Flow in the Reflex documentation, and I hope it is not just an example, but a comprehensive React Flow feature within Reflex
是的，我参考了reflex文档中包装react-flow的示例，我希望它不仅只是一个示例，而是成为一个reflex里一个完善的react-flow功能.

- 使用方法:
  - 

- 程序守则:
  - 无限大: float('inf')  无限小: -float('inf')
  - 数据类型要定义好，不然会没有反应。 比如事件处理器rx.EventHandler[lambda e0: [e0]]，没有返回值的，但声明有返回值，则不会响应，没有返回值就不要定义，如rx.EventHandler
    - 接受返回值也不能用*args和**kwargs代替，没有返回值的话会报错。
    - reflex调用组件的时候可以不用显式地使用lambda传参，只在定义里修改声明是否有传参就可以了，如果有参数，自动就传过来了。 
      - 注意！：如果有返回的参数，但是声明里没要求参数，则参数**会被忽略！**， 所以声明要先声明参数，报错再改为无参数。
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
  - 定义数据类型时。react-flow的数据类型 () => void 在这里定义为 rx.Var[Callable[[], None]] = None      需要 from typing import Callable
  - 定义数据类型时。react-flow的数据类型 (interactiveStatus: boolean) => void  在这里定义为 rx.Var[Callable[[bool], None]] = None     需要 from typing import Callable
  - 定义数据类型时。react-flow的数据类型 TypedDict  就是需要单独定义一个class的类型，需要rx.Var[]包装class，但class里面不要: 
    ```python
    from typing import TypedDict
    import reflex as rx
    
    class XYPosition(TypedDict):
        x: int  # 这里不要包装rx.Var[]
        y: int  # 这里不要包装rx.Var[]
    
    class MyComponent(rx.Component):
        #          这里要包装rx.Var[]        默认值
        position: rx.Var[XYPosition] = {"x": 0, "y": 0} 
    ```
  - 定义数据类型时。react-flow的数据类型 ..props  参考： https://reflex.dev/docs/wrapping-react/props/
  - 定义数据类型时。react-flow的数据类型 NodeType 的可选参数为 "default" | "input" | "output" | "group"    https://reactflow.dev/api-reference/types/node#default-node-types
  - 定义数据类型时。react-flow的数据类型 HandleType 的可选参数为  'source' | 'target'     不写是 'source'   重要！handle竟然没有对应的官网页面？NodeType和EdgeType都有了，但是HandelType确实404？？这应该是react-flow内部的问题，需要问一问官方的情况
  - 定义数据类型时。react-flow的数据类型 EdgeType 的可选参数为 "default" | "straight" | "step" | "smoothstep" | "simplebezier" https://reactflow.dev/api-reference/types/edge#default-edge-types
  - 定义数据类型时。react-flow的数据类型 OnConnect 的数据类型定义为: rx.EventHandler[lambda e0: [e0]]  可选参数是一个事件处理器
  - 定义数据类型时。react-flow的数据类型 PanelPosition 的数据类型定义为: rx.Var[Literal['top-left', 'top-center', 'top-right', 'bottom-left', 'bottom-center', 'bottom-right']]  通常默认值是: 'bottom-right'  https://reactflow.dev/api-reference/types/panel-position
  - 变量连接的eventhandle类函数要不要加括号？ 不加，除非要传入参数  因为: 这里只是引用，加了就是执行了。
  - 定义hooks中, react代码的hook **带参数的不用特别传参**,因为hook可以访问自定义代码中定义的变量。
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
    - 现在按Ctrl+C可以种植reflex的运行，防止僵尸进程。
  - 工作方法: 将react的组件添加注册到reflex里面： 注意！：限定事件处理器类别
    1. 在顶级包里面声明数据类型 rx.EventHandler[lambda e0: [e0]]
    2. 在demo里测试  如果报错 RangeError，或者不执行: Maximum call stack size exceeded 则 var=State.fake_event_handel
    3. 如果不报错，且正常输出：增加声明的数据类型  rx.EventHandler[lambda e0, e1: [e0, e1]]
    4. 4的增加声明，直到报错或者不执行，然后减少。
    5. 看一看几个参数的情况下时不报错且全部声明都执行的方案，那么实际参数量就是这个。
    6. 修改为准确的数量：var=lambda e0: State.fake_event_handel(e0)
  - 说是Hoooks不是集中管理的，而是放到Hooks对应组件的class的def add_hooks下
    
- 报错经历:
  - 前端无法运行，报错如下:  问题:组件tag里的名称与react的名称不对应，reflex找不到react里对应的组件。 解决方法: 将tag名称改为react里对应的名称
    ```text
    [Reflex Frontend Exception]
     Error: Element type is invalid. Received a promise that resolves to: undefined. Lazy element type must resolve to a class or function.
     Error: Element type is invalid. Received a promise that resolves to: undefined. Lazy element type must resolve to a class or function.
        at beginWork (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:5630:13)
        at runWithFiberInDEV (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:1256:66)
        at performUnitOfWork (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:7612:94)
        at workLoopSync (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:7506:37)
        at renderRootSync (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:7489:6)
        at performWorkOnRoot (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:7257:36)
        at performWorkOnRootViaSchedulerTask (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:8180:4)
        at MessagePort.performWorkUntilDeadline (http://localhost:3001/node_modules/.vite/deps/react-dom_client.js?v=70572017:28:38)
    
     ```
  - 原因: 数据类型声明定义错误  解决方案: 数据类型定义，注意返回的数据数量，返回的数据数量不对会报错。 数据类型要定义好，不然会没有反应。 比如事件处理器rx.EventHandler[lambda e0: [e0]]，没有返回值的，但声明有返回值，则不会响应，没有返回值就不要定义，如rx.EventHandler
    ```text
    [Reflex Frontend Exception]
     RangeError: Maximum call stack size exceeded
    RangeError: Maximum call stack size exceeded
        at [Symbol.hasInstance] (<anonymous>)
        at isBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1821:103)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1829:6)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
        at hasBinary (http://localhost:3000/node_modules/.vite/deps/socket__io-client.js?v=23edb850:1831:79)
    ```
  - 【很有可能是正确的】包裹react时，将react组件参数的camel(驼峰命名法)转为reflex使用的snake(蛇形命名法)  简单来说就是: 1. 大写转小写 2. 原来的大写分隔改为下划线_分隔
    ```python
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
    
    
    print(offical_switch_case.to_snake_case('onConnect'))
    
    ```
  - 包裹react时， react组件参数的  数据类型声明的参数比实际多了：  注意！ 有时候已经改过来了，还会报错，只是因为缓存，多刷新/重载几次就好了
    -  报错: RangeError: Maximum call stack size exceeded
  - 

- 未解决的问题:
  - 所有没有默认值的参数，应不应该默认为None？ 还是就是空着？
  - 我不知道为什么事件处理器的类型声明使用rx.EventHandler[lambda e0: [e0]]   只是示例里是这么写的，而且都可以正常运行。
  - 不知道把偶哦react的时候，如何转换react组件的参数名未reflex的参数名？  这个具体的规则不知道，但有些时有效的，比如react的onConnect转为reflex的on_connect
  - 

- 代码示例：
  - 检测某事件处理器触发器的所有返回值   【好像所有返回值都集中在一个里面，不确定】  
    - **两个现象帮助判断：对于(多/少)参数的两种不对应产生的异常现象，可用作函数是否有参数的判断。 *多参数的情况也是如此！***  多参数示例：包含三个返回值 on_node_drag_start
      1. 【声明的参数量比实际多->函数不执行或执行但不执行多声明的参数】
         - 如果没有参数返回，但声明有参数， 则对应的函数不会执行(实际一个参数都没有)。   或者只是执行真正数量的参数(多声明的部分不会体现到函数里)(实际至少有一个参数)
      2. 【声明的参数量比实际少->函数执行但不执行多传入的参数参数】
         - 如果有参数返回，但声明没有参数， 则对应的函数会执行， 只是函数没有参数。
    - 注意！当得知有多少返回值后，应该将数据类型声明改为对应数量的返回值，如 rx.EventHandler[lambda e0: [e0]] 
      1. 触发器数据类型定义:    
         - **少参数会忽略，而多参数会报错。**     从多参数向下尝试，指直到有输出
         0. 无参数的情况: rx.EventHandler
         1. 一个参数的情况： rx.EventHandler[lambda e0: [e0]]
         2. 两个参数的情况（先使用这种情况是否有更多的参数）：rx.EventHandler[lambda e0, e1: [e0, e1]]
    2. 触发器端：
       - 测试做法: on_click=State.fake_event_handel,     不论有多少参数, 会自动补充位置参数
       - 标准做法: on_click=lambda e0, e1: State.fake_event_handel(e0, e1),     显式表示的参数与实际参数一致
       - 通过这样要求多参数的方法检测实际的参数数量
    3. 接收端:
         ``` python 
        # 占位符事件处理器-可接受(0~5)个参数——为事件处理器提供一个虚假的接入点
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
        ```
  - 
