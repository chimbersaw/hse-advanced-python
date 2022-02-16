import setuptools

setuptools.setup(
    name="ast-visualizer-demo",
    version="2.3.9",
    author="Maxim Sukhodolskii",
    description="AST visualizer demo for hse-advanced-python course HW.",
    install_requires=["networkx==2.6.2", "pydot==1.4.2"],
    python_requires=">=3.8",
    url="https://github.com/maxuh14/hse-advanced-python",
    packages=["ast_visualizer_demo"]
)
