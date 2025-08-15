import reflex as rx

config = rx.Config(
    app_name="react_flow_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)