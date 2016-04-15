import json
import os
import tempfile
from uuid import uuid4

from openpyxl import Workbook


def export_to_excel(contributions):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    # Pick up headers first
    q = json.loads(contributions[0].questionnaire_data)
    headers = q.keys()
    headers.sort()

    # Add it to the sheet
    ws.append(['id', 'created'] + headers)

    # Emit all contributions
    for contribution in contributions:
        q = json.loads(contribution.questionnaire_data)
        row = [contribution.id, contribution.created]
        for h in headers:
            row.append(q[h])
        ws.append(row)

    # Return
    filename = '%s.xlsx' % (uuid4(),)
    path = os.path.join(tempfile.gettempdir(), filename)
    wb.save(path)

    with open(path, 'rb') as f:
        data = f.read()

    os.remove(path)
    return data
