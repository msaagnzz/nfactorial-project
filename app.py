from flask import Flask, render_template, request, redirect, url_for, flash, abort
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'secret_key'

events = [
    {
        'id': 1,
        'title': 'Концерт 50 Cent',
        'description': 'В рамках финального мирового тура артиста, который включает в себя США, Европу, Африку и Австралию, 50 Cent даст единственный концерт в Алматы.',
        'time': datetime(2024, 5, 25, 20, 0),
        'location': 'г. Алматы, Almaty Arena',
        'capacity': 10000,
        'available_tickets': 5000
    },
    {
        'id': 2,
        'title': 'Алматинский марафон',
        'description': 'Самое крупное беговое соревнование в Центральной Азии, городской праздник спорта с основной дистанцией 42 км 195 м.',
        'time': datetime(2024, 9, 29, 9, 0),
        'location': 'Площадь Республики, ул. Сатпаева',
        'capacity': 30000,
        'available_tickets': 10000
    }
]


@app.route('/')
def index():
    return render_template('index.html', events=events)


@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = next((event for event in events if event['id'] == event_id), None)
    if event is None:
        abort(404) 

    if request.method == 'POST':
        ticket_request = int(request.form.get('tickets', 0))
        if event['available_tickets'] == 0:
            flash('К сожалению, билеты на это мероприятие уже закончились.', 'error')
        elif ticket_request > 0 and ticket_request <= event['available_tickets']:
            event['available_tickets'] -= ticket_request
            flash(f"Вы успешно забронировали {ticket_request} билетов на \"{event['title']}\".", 'success')
            return redirect(url_for('event_detail', event_id=event_id))
        elif ticket_request <= 0:
            flash('Ошибка бронирования. Количество билетов должно быть больше нуля.', 'error')
        else:
            flash('Ошибка бронирования. Пожалуйста, проверьте количество доступных мест и повторите попытку.', 'error')

    return render_template('event_detail.html', event=event)

if __name__ == '__main__':
    app.run(debug=True)
