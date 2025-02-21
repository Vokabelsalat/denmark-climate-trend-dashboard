FROM python:3.10.0

COPY requirements.txt ./requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

COPY ProjektKonference.py ./ProjektKonference.py
COPY use_cases.py ./use_cases.py
COPY info_sheet.py ./info_sheet.py
COPY data ./data
COPY assets ./assets

CMD ["python","ProjektKonference.py"]
