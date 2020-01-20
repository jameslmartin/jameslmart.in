FROM python:3.7

RUN pip install pelican[Markdown]
EXPOSE 8000:8000
