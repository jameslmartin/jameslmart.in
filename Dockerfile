FROM python:3.7

RUN pip install pelican[Markdown]
RUN pip install Pillow bs4 git+https://www.github.com/hbldh/hitherdither
EXPOSE 8000:8000
