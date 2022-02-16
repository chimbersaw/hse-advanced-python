FROM python:3.9-slim
COPY main.py main.py
RUN apt-get update
RUN apt-get install texlive graphviz -y
RUN python3 -m pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ast-visualizer-demo==2.3.9
RUN python3 main.py

WORKDIR artifacts
RUN pdflatex sample.tex
RUN rm sample.aux sample.log
# output pdf can be found in artifacts/sample.pdf
