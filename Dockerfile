FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

RUN python -m nltk.downloader -d /usr/share/nltk_data punkt wordnet stopwords

ENV NLTK_DATA=/usr/share/nltk_data

COPY . .

EXPOSE 7860

CMD ["gunicorn", "--bind", "0.0.0.0:7860", "app:app"]